<template>
    <div class="container">
        <div class="card my-4">
            <div class="card-body">
                <form id="post" action="" method="post">
                    <h3>New transaction</h3>
                    <hr>
                    <div class="form-group">
                        <label for="reason">Reason</label>
                        <input type="text" class="form-control" name="reason" id="reason" placeholder="Transaction reason" required>
                    </div>
                    <div class="form-group">
                        <label for="date">Date</label>
                        <input type="date" class="form-control" name="date" id="date" required>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <h4>Credits</h4>
                            <AccountList :list="transaction.src"></AccountList>
                        </div>
                        <div class="col-md-6">
                            <h4>Debits</h4>
                            <AccountList :list="transaction.dest"></AccountList>
                        </div>
                    </div>
                    <hr>
                    
                    <p><span class="badge badge-danger" v-if="error">Invalid transaction: {{ error }}</span></p>
                    <button type="submit" class="btn btn-primary btn-block" :disabled="error !== ''">Submit</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
    import AccountList from '@/components/AccountList.vue'
    
    
    
    function total(list) {
        return list.reduce(function (prev, cur) {
            return prev + cur.amount;
        }, 0);
    }

    export default {
        components: {AccountList},
        data() {
            return {
                transaction: {
                    src: [],
                    dest: []
                }
            }
        },
        methods: {},
        computed: {
            error: function () {
                let st = total(this.transaction.src);
                let dt = total(this.transaction.dest);

                if (st !== dt) {
                    return 'Debits and credits do not balance!';
                }
                if (st <= 0 || dt <= 0) {
                    return 'Debit and/or credits cannot be non-positive!';
                }
                return '';
            }
        }
    }
</script>