#!/usr/bin/env python3

import threading
import flask
from flask import g, json, request, Blueprint, abort
from flask_cors import CORS
import flask_login
import queue
import sys
import copy
import itertools
import os.path
import atexit
import textwrap
import random 
import string
import colorsys
import uuid
import time
import bleach

app = flask.Flask(__name__)
api_state = Blueprint('state', 'state', url_prefix='/api/state/')

# cors = CORS(app)
# cors = CORS(api_state)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# TODO: add multiprocessing support with redis.
#  https://stackoverflow.com/questions/12232304/how-to-implement-server-push-in-flask-framework


INITIAL_STATE_FILE = './initial_state.json'
LAST_STATE_FILE = './last_state.json'
QUEUE_MAXSIZE = 100  # drop connection if queue is not read out
MAX_VALUE_LENGTH = 1000  # postpone memory overflow by prankers


@app.route('/')
def index():
    return 'Nothing interesting here, really.'

@app.after_request
def add_cors_headers(resp):
    resp.headers['Access-Control-Allow-Origin']='*'
    return resp

@api_state.after_request
def add_cors_headers(resp):
    resp.headers.add('Access-Control-Allow-Origin', '*')
    resp.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    resp.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return resp

#### State ####

def version_inc(f):
    def wrapper(self, *args):       
        ret = f(self, *args)
        *ret, = ret,
        new_version = next(self._version_counter)
        self.version = new_version
        return *ret, new_version
    return wrapper

class State():
    def __init__(self, kind):
        try:  # Read initial state
            with open(INITIAL_STATE_FILE) as json_file:
                data = json.load(json_file)
        except FileNotFoundError: pass
        except json.decoder.JSONDecodeError as err:
            raise Exception('INITIAL_STATE_FILE json decode:', str(err))
        
        if kind in data:
            for k,v in data[kind].items():
                setattr(self, k, v)
        
        if not hasattr(self, 'items'): # fixme: check items is a list
            self.items = [] 

        if not hasattr(self, 'version'): # fixme version is an int
            self.version = 0

        self._version_counter = itertools.count(self.version + 1)

        if self.items:  # not empty
            max_item_id = max( (int(item['id']) if 'id' in item else 0 for item in self.items))
        else:
            max_item_id = 0

        self._item_id_counter = itertools.count(max_item_id+1)

    def get_item(self, id):
        for item in self.items:
            if 'id' in item and str(item['id']) == str(id):
                return item
        
    @version_inc
    def del_item(self, id):
        item = self.get_item(id)
        if not item:
            raise KeyError("Not found by id.")
        self.items.remove(item)

    @version_inc
    def add_item(self, obj):
        next_id = next(self._item_id_counter)
        obj['id'] = next_id
        self.items.append(obj)
        return next_id

    @version_inc
    def update_item(self, id, obj):
        item = self.get_item(id)
        if not item:
            raise KeyError("Not found by id.")
        if 'id' in obj:
            raise ValueError("Can't update `id`.")
        item.update(obj)
        return obj

    def dump(self):
        return {
            "version": self.version,
            "items": self.items,
        }

class StateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, State):
            return obj.dump()
        else:
            return json.JSONEncoder.default(self, obj)

app.json_encoder = StateEncoder

books = State('books')  # Global
users = State('users')

state = { 'books': books, 'users': users}

def json_dumps(*args, **kvargs):
    return json.dumps(*args, **kvargs, cls=StateEncoder)

def json_dumps_pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '), cls=StateEncoder)


@atexit.register  # When process shutting down
def savestate():
    with open(LAST_STATE_FILE, "w") as outfile:
        outfile.write(json_dumps_pretty(state) + '\n')
        print("State saved in {}".format(LAST_STATE_FILE), file=sys.stderr)


@app.route('/state')
def get_state():
    global state
    return {"state": state}, 200


#### SSE ####

class PubSub:
    """ A class for pubublisher-subscibers pattern. """
    def __init__(self):
        self.subscribers = []

    def sub(self):
        q = queue.Queue(maxsize=QUEUE_MAXSIZE)
        self.subscribers.append(q)
        return q

    def pub(self, msg: str):
        # reversed because we deleting items:
        for i in reversed(range(len(self.subscribers))): 
            try:
                self.subscribers[i].put_nowait(msg)
            except queue.Full:
                del self.subscribers[i]

pubsub = PubSub()
current_milli_time = lambda: int(round(time.time() * 1000))

def format_sse(data: object, event:str=None, id:int=None) -> str:
    """ Create message in SSE format:
        id: ..., event: ...,  data: ...
    """
    msg = f'data: {json_dumps(data)}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    if id is not None:
        msg = f'id: {id}\n{msg}'
    return msg


@app.route('/events', methods=['GET'])
def listen():
    def stream():
        messages = pubsub.sub()  # returns a queue.Queue
        yield 'retry: 2000\n\n'
        # Send state on connect/reconnect
        yield format_sse(id=current_milli_time(), event='init', data=state)
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg

    # Returns a function https://flask.palletsprojects.com/en/1.1.x/patterns/streaming/
    return flask.Response(stream(), mimetype='text/event-stream',)


#### API ####
# pub messages: 
# id: <ts>
# event: change
# data: { module: 'books', 
#         version: <version>,
#         uid: <uid>,
#         action: 'set' | 'delete' | 'update' | 'add'
#         payload: <payload> }
#
# =Action= = Payload =
# Set      { items: [ <item>, ...] }
# Update   { <id>: {<key>: <value>, ...} }
# Delete   [ <id>, ...]
# Add      <item>


@api_state.url_value_preprocessor
def pull_kind(endpoint, values):
    global state
    kind =  values.pop('kind', None)
    if kind not in state:
        abort(flask.Response('Kind not found', 404))
    else:
        g.state = state[kind]


@api_state.route('/<kind>/<item_id>', methods=['GET'])
def get_item(item_id):
    item = g.state.get_item(item_id)
    if item:
        return {'data': {'item': item}}, 200
    return "Item not found", 404

def on_change_notify(version, uid, action, payload, module='books'):
    msg = format_sse(data = {
        'module': module,
        'version': version,
        'uid': uid,
        'action': action,
        'payload': payload,
        },
        event = 'change',
        id = current_milli_time(),
    )
    pubsub.pub(msg) 

@api_state.route('/<kind>/<item_id>/delete', methods=['GET', 'POST'])
@api_state.route('/<kind>/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        ret, new_version = g.state.del_item(item_id)
    except KeyError as e:
        return {'status': 'error', 'msg' : str(e)}, 404
    
    on_change_notify( version=new_version,
                        uid='<user_Id>',
                        action='delete',
                        payload=[item_id])

    return {'status': 'ok', 'version': new_version }, 200


def request_attrs(request):
    req =  request.values.to_dict()  # args and form combined, preferring args
    json = request.get_json(force=True, silent=True)  
                                # force=True - ignore content type
                                # silent=True - ignore content type
    if json and isinstance(json, dict):
        for k,v in json.items():
            req[k] = v
    
    # prevent huge values
    for k,v in req.items():
        safe_v = textwrap.shorten(str(v), width=MAX_VALUE_LENGTH, placeholder="...")
        safe_v = bleach.clean(safe_v)
        req[k] = safe_v  # overwrite if overlap
    
    return req


@api_state.route('/<kind>/add', methods=['GET', 'POST', 'PUT'])
def add_item():
    req = request_attrs(request)
    if not req:
        return {'status': 'error', 'msg' : 'Request is empty'}, 400 
    try:
        _id, new_version = g.state.add_item(req)  
    except Exception as e:
        return {'status': 'error', 'msg' : str(e)}, 400

    on_change_notify( version=new_version,
                        uid='<user_Id>',
                        action='add',
                        payload=g.state.get_item(_id))

    return {'status': 'ok', 'version': new_version }, 200


@api_state.route('/<kind>/<item_id>/update', methods=['GET', 'POST', 'PUT'])
def update_item(item_id):
    req = request_attrs(request)

    if not req:
        return {'status': 'error', 'msg' : 'Request is empty'}, 400 

    try:
        upd, new_version = g.state.update_item(item_id, req)
    except KeyError as e:
        return {'status': 'error', 'msg' : str(e)}, 404
    except Exception as e:
        return {'status': 'error', 'msg' : str(e)}, 400

    on_change_notify( version=new_version,
                        uid='<user_Id>',
                        action='update',
                        payload={item_id: upd},
                        )

    return {'status': 'ok', 'version': new_version }, 200


#### Users ####
# GET /login?name=xxxx => uid, token
# GET /logout (token)

users = {}

def token_generator(size=10, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def color_generator():
    """ Generate bright colours. """
    h,s,l = random.random(), 0.5 + random.random()/2.0, 0.4 + random.random()/5.0
    r,g,b = [int(256*i) for i in colorsys.hls_to_rgb(h,l,s)]
    return '#%02X%02X%02X' % (r,g,b)
    #return "%06x" % (random.randint(0, 0xFFFFFF))


def username(val):
    name = (str(val).strip())[:MAX_VALUE_LENGTH]  # trim string if too long
    name = ' '.join(name.split()[:2])  # first two words
    if '@' not in name:
        name = string.capwords(name)  # capitalize each word
    return name


app.secret_key = token_generator()  # Change this!


class User(flask_login.UserMixin):
    def __init__(self, uid):
        self.uid = uid
        self.color = color_generator()

    def dump(self):
        return vars(self)

    def get_id(self):
        return str(self.uid)

    def is_active(self):  # account is activated
        return True

    def is_authenticated(self):  # provided valid credentials
        return True


@app.route('/logged-in-users')
def get_users():
    dump = [v.dump() for v in users.values()]
    return {'data': dump}, 200


@login_manager.user_loader
def user_loader(uid):
    if uid not in users:
        return
    return users[uid]


@login_manager.unauthorized_handler
def unauthorized_callback():
    return flask.Response('Login Required', 401)


@app.route('/login', methods=['GET', 'POST'])
def login():
    req_name = flask.request.values['name']
    name = username(req_name)

    # Check username is taken
    user = next( (user for user in users.values() if user.name == name), None)
    if user: 
        return flask.Response('This name was already taken. Choose another one.', 401 )

    uid = uuid.uuid4().hex
    user = User(uid)
    user.name = name
    flask_login.login_user(user)
    users[uid] = user  # save

    msg = format_sse(data=user.dump(), event="users", id=upd['version'])
    pubsub.pub(msg)

    print(upd, file=sys.stderr)

    return flask.Response('Logged in', 200)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    flask_login.logout_user()
    return 'Logged out'


#### PING ####
class Pinger(threading.Thread):
    def __init__(self, delay=1.2345):
        super(self.__class__, self).__init__()
        self.delay = int(delay)
        self.setDaemon(True)

    def run(self):
        while True:
            ts = current_milli_time()
            msg = format_sse(id=current_milli_time(), event='ping', data={})
            pubsub.pub(msg)
            time.sleep(self.delay)


if __name__ == "__main__":
    app.register_blueprint(api_state)
    p = Pinger()
    p.start()
    app.run(host='0.0.0.0', port=5000)
