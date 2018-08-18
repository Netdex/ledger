function delarrobj(array, obj) {
    var index = array.indexOf(obj);
    if (index !== -1) {
        array.splice(index, 1);
    }
}

var app = new Vue({
    delimiters: ['${', '}'],
    el: '#post',
    data: {
        transaction: {
            src: [],
            dest: []
        }
    },
    methods: {
        // add account to transaction source column
        addSrcAccount: function (event) {
            this.transaction.src.push({
                account: '',
                amount: 0.01
            });
        },

        // add account to transaction destination column
        addDestAccount: function (event) {
            this.transaction.dest.push({
                account: '',
                amount: 0.01
            });
        },

        // delete account from transaction source column
        delSrcAccount: function (account) {
            delarrobj(this.transaction.src, account);
        },

        // delete account from transaction destination column
        delDestAccount: function (account) {
            delarrobj(this.transaction.dest, account);
        }
    },
    computed: {
        srcTotal: function () {
            return this.transaction.src.reduce(function (prev, cur) {
                return prev + cur.amount;
            }, 0);
        },
        destTotal: function () {
            return this.transaction.dest.reduce(function (prev, cur) {
                return prev + cur.amount;
            }, 0);
        },
        error: function () {
            var st = this.srcTotal;
            var dt = this.destTotal;

            if (st !== dt) {
                return 'Debits and credits do not balance!';
            }
            if (st <= 0 || dt <= 0) {
                return 'Debit and/or credits cannot be non-positive!';
            }
            return '';
        }
    }
});

// we want default accounts
app.addSrcAccount();
app.addDestAccount();