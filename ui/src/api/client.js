const delay = 700; // emulate network latency
export default {
  fetchItems(url) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        fetch(url)
          .then(r => r.json())
          .then(jsonObj => {
            resolve(jsonObj);
          })
          .catch(error => {
            // eslint-disable-next-line no-console
            console.log(error);
            reject(new Error('Fetch error.'));
          });
      }, delay);
    });
  },

  addItem(url, data) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        // eslint-disable-next-line no-console
        console.log('Items update: ', data);

        // simulate random failure.
        if (Math.random() > 0.5) {
          resolve({});
        } else {
          reject(new Error('Rangom failure'));
        }

        // TODO: post/put, not implemented yet.
      }, delay);
    });
  },

  updateItem(url, _id, data) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        // eslint-disable-next-line no-console
        console.log('updateItem: ', _id, data);
        fetch(`${url}/${_id}/update`, {
          method: 'POST',
          body: JSON.stringify(data),
        })
          .then(r => r.json())
          .then(jsonObj => {
            resolve(jsonObj);
          })
          .catch(error => {
            reject(new Error(`Fetch error. ${error}`));
          });
      }, delay);
    });
  },

  deleteItem(url, _id) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        // eslint-disable-next-line no-console
        console.log('deleteItems: ', _id);
        fetch(`${url}/${_id}`, {
          method: 'DELETE',
        })
          .then(r => r.json())
          .then(jsonObj => {
            resolve(jsonObj);
          })
          .catch(error => {
            reject(new Error(`Fetch error. ${error}`));
          });
      }, delay);
    });
  },
};
