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
            const formData = new FormData();
            formData.append('data', JSON.stringify(obj, this.filter));
            if (obj._evidence) {
                for (const file of obj._evidence) {
                    formData.append('evidence[]', file);
                }
            }

            fetch(`/transaction/upsert`, {
                method: 'POST',
                // body: ,
                body: formData,
                // headers: {
                //     'Content-Type': 'application/json'
                // }
            }).then(response => {
                if (response.ok)
                    resolve();
                else {
                    response.text().then(reject)
                }
            }).catch(reject);
        });
    },
    filter(key, value) {
        // remove meta props
        if (key.startsWith("_"))
            return undefined;
        return value;
    }
};