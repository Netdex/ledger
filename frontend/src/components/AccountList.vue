<template>
    <b-card>
        <div slot="header">
            <b-nav pills>
                <b-nav-item @click="addAccount" active>Add <i class="fas fa-plus"></i></b-nav-item>
                <b-nav-item @click="clearAccounts">Clear <i class="fas fa-eraser"></i></b-nav-item>
            </b-nav>
        </div>

        <b-form-group v-for="tr in list" inline>
            <b-row>
                <b-col md="6">
                    <b-form-input type="text"
                                  placeholder="Account name"
                                  v-model="tr.account"
                                  required></b-form-input>
                </b-col>
                <b-col md="4">
                    <b-input-group prepend="$">
                        <b-form-input type="number"
                                      placeholder="Amount"
                                      v-model.number="tr.amount"
                                      min="0.01" step="0.01"
                                      required></b-form-input>
                    </b-input-group>
                </b-col>
                <b-col md="2">
                    <b-button variant="danger" @click="delAccount(tr)">
                        <i class="fas fa-trash"></i></b-button>
                </b-col>
            </b-row>
        </b-form-group>
        <div slot="footer">
            <b-badge variant="primary">
                Total 
                <b-badge variant="success">{{currency(total)}}</b-badge>
            </b-badge>
        </div>
    </b-card>
</template>

<script>
    import Format from '@/mixins/Format'

    function delarrobj(array, obj) {
        let index = array.indexOf(obj);
        if (index !== -1) {
            array.splice(index, 1);
        }
    }

    export default {
        mixins: [Format],
        props: {"list": Array},
        data() {
            return {}
        },
        methods: {
            addAccount() {
                this.list.push({
                    account: '',
                    amount: 0.01
                });
            },
            delAccount(account) {
                delarrobj(this.list, account);
            },
            clearAccounts() {
                this.list.splice(0, this.list.length);
            }
        },
        computed: {
            total() {
                return this.list.reduce((p, c) => p + c.amount, 0);
            }
        }
    }
</script>


<style scoped>

</style>