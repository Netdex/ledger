<template>
    <b-card>
        <div slot="header">
            <b-nav pills>
                <b-nav-item @click="addAccount" active>Add <i class="fas fa-plus"/></b-nav-item>
                <b-nav-item @click="clearAccounts">Clear <i class="fas fa-eraser"/></b-nav-item>
                <div class="ml-auto">
                    <b-btn variant="primary">
                        Total 
                        <b-badge variant="success">{{currency(sum)}}</b-badge>
                    </b-btn>
                </div>
            </b-nav>

        </div>

        <b-form-group v-for="acc in list" :key="acc._id" inline>
            <b-row>
                <b-col md="6">
                    <b-form-input type="text"
                                  placeholder="Account name"
                                  v-model="acc.account"
                                  required/>
                </b-col>
                <b-col md="4">
                    <CurrencyInput v-model="acc.amount"
                                   :account-type="accountType"
                                   :opts.sync="opts"
                                   :sum="sum"
                                   :counter-sum="counterSum"
                                   :type.sync="acc.rtype"/>
                </b-col>
                <b-col md="2">
                    <b-button variant="danger" @click="delAccount(acc)" block>
                        <i class="fas fa-trash"/></b-button>
                </b-col>
            </b-row>
        </b-form-group>

    </b-card>
</template>

<script>
    import Format from '@/mixins/Format'
    import CurrencyInput from '@/components/CurrencyInput'
    import uuidv4 from 'uuid/v4'

    function delarrobj(array, obj) {
        let index = array.indexOf(obj);
        if (index !== -1) {
            array.splice(index, 1);
        }
    }

    export default {
        components: {CurrencyInput},
        mixins: [Format],
        props: {
            "accountType": String,
            "list": Array,
            "counterSum": Number,
            "sum": Number,
            "opts": Object
        },
        data() {
            return {
                money: {
                    decimal: '.',
                    thousands: ',',
                    prefix: '',
                    suffix: '',
                    precision: 2,
                    masked: false
                },
            }
        },
        methods: {
            addAccount() {
                this.list.push({
                    _id: uuidv4(),
                    account: '',
                    amount: 0,
                    rtype: 'exact',
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
            
        }
    }
</script>


<style scoped>

</style>