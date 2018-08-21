export const Transaction = {
    get(id) {
        return new Promise((resolve, reject) => {
            fetch(`/transaction/get/${id}`)
                .then(response => response.json())
                .then(resolve)
                .catch(reject);
        });
    },
    getAll() {
        return new Promise((resolve, reject) => {
            fetch(`/transaction/get/all`)
                .then(response => response.json())
                .then(resolve)
                .catch(reject);
        });
    },
    del(id) {
        return new Promise((resolve, reject) => {
            fetch(`/transaction/delete/${id}`)
                .then(resolve)
                .catch(reject);
        });
    },
    upsert(obj) {
        return new Promise((resolve, reject) => {
            fetch(`/transaction/upsert`, {
                method: 'POST',
                body: JSON.stringify(obj),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
                .then(resolve)
                .catch(reject);
        });

    }
};