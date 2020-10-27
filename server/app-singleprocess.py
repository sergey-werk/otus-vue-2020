#!/usr/bin/env python3

import flask
from flask import request
import queue
import sys
import json
import copy
import itertools
import os.path
import atexit
import textwrap

app = flask.Flask(__name__)

# TODO: add multiprocessing support with multiprocessing.Queue or redis.

INITIAL_STATE_FILE = './initial_state.json'
LAST_STATE_FILE = './last_state.json'
QUEUE_MAXSIZE = 101  # drop connection if queue is not read out
MAX_VALUE_LENGTH = 64  # postpone memory overflow by prankers


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



#### State ####
state = { "version": None, }

try:
    # Read initial state if any
    with open(INITIAL_STATE_FILE) as json_file:
        data = json.load(json_file)
        state = data
        if 'version' not in state:
            state['version'] = None

except FileNotFoundError:
    pass

except json.decoder.JSONDecodeError as err:
    print('ERR: INITIAL_STATE_FILE json decode:', str(err), file=sys.stderr)
    exit(1)

def json_dumps_pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))

@atexit.register
def savestate():
    with open(LAST_STATE_FILE, "w") as outfile:
        outfile.write(json_dumps_pretty(state) + '\n')
        print("State saved in {}".format(LAST_STATE_FILE), file=sys.stderr)


version_counter = itertools.count(state['version'] or 0)



def format_sse(data: object, event:str=None, id:int=None) -> str:
    """ Create message in SSE format:
        id: ..., event: ...,  data: ...
    """
    msg = f'data: {json.dumps(data)}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    if id is not None:
        msg = f'id: {id}\n{msg}'
    return msg



@app.route('/')
def index():
    return 'Nothing interesting here, really.'


@app.route('/state')
def get_state():
    return {"data": state}, 200


@app.route('/update', methods=['GET', 'POST'])
def update():
    global state
    upd = {}
    upd = request.values.to_dict()  # args and form combined, preferring args
    
    json = request.get_json(force=True, silent=True)  
                                # force=True - ignore content type
                                # silent=True - ignore content type
    if json and isinstance(json, dict):
        for k,v in json.items():
            safe_v = textwrap.shorten(str(v), width=MAX_VALUE_LENGTH, placeholder="...")
            upd[k] = safe_v  # overwrite if overlap
    
    # Get next version number:
    upd['version'] = next(version_counter)  
    
    # Atomic state update:
    new_state = copy.deepcopy(state)
    new_state.update(upd)
    state = new_state

    # Publish update for subscribers: 
    msg = format_sse(data=upd, event="update", id=upd['version'])
    pubsub.pub(msg)

    print(upd, file=sys.stderr)
    return {"version": upd['version']}, 200


@app.route('/events', methods=['GET'])
def listen():
    def stream():
        messages = pubsub.sub()  # returns a queue.Queue
        yield 'retry: 2000\n\n'
        yield format_sse(data=state, id=state['version'])  # Send state on connect/reconnect
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg

    # Returns a function https://flask.palletsprojects.com/en/1.1.x/patterns/streaming/
    return flask.Response(stream(), mimetype='text/event-stream',)


@app.after_request
def add_cors_headers(resp):
    resp.headers['Access-Control-Allow-Origin']='*'
    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)