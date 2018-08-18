<template>
    <div class="card my-2">
        <div class="card-header">
            <ul class="nav nav-pills card-header-pills">
                <li class="nav-item">
                    <a class="nav-link active" @click="addAccount" href="#">Add</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link " @click="clearAccounts" href="#">Clear</a>
                </li>
            </ul>
        </div>
        <div class="card-body">
            <div v-for="tr in list">
                <div class="form-group form-inline">
                    <div class="row">
                        <div class="col-md-6 my-1">
                            <div class="input-group ">
                                <input type="text" class="form-control" placeholder="Account name"
                                       v-model="tr.account" required>
                            </div>
                        </div>
                        <div class="col-md-4 my-1">
                            <div class="input-group ">
                                <div class="input-group-prepend">
                                    <div class="input-group-text">$</div>
                                </div>
                                <input type="number" class="form-control" placeholder="Amount"
                                       v-model.number="tr.amount" min="0.01" step="0.01" required>
                            </div>
                        </div>
                        <div class="col-md-2 my-1">
                            <button type="button" class="btn btn-danger btn-block" @click="delAccount(tr)">
                                <i class="fas fa-trash"></i></button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="card-footer text-muted">
            <span class="badge badge-success">Total: ${{Number.parseFloat(total).toFixed(2)}}</span>
        </div>
    </div>
</template>

<script>
    function delarrobj(array, obj) {
        let index = array.indexOf(obj);
        if (index !== -1) {
            array.splice(index, 1);
        }
    }

    export default {
        props: {"list": Array},
        data() {
            return {}
        },
        methods: {
            addAccount: function () {
                this.list.push({
                    account: '',
                    amount: 0.01
                });
            },
            delAccount: function (account) {
                delarrobj(this.list, account);
            },
            clearAccounts: function () {
                this.list.splice(0, this.list.length);
            }
        },
        computed: {
            total: function () {
                return this.list.reduce(function (prev, cur) {
                    return prev + cur.amount;
                }, 0);
            }
        }
    }
</script>


<style scoped>
    
</style>