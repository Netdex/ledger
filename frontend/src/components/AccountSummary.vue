<template>
    <b-card-group columns>
        <b-card v-for="(amt, acc) in accounts"
                v-if="amt !== 0"
                :key="acc"
                :title="acc"
                :sub-title="(amt < 0) ? 'owes the group ledger' : 'is owed by the group ledger'">
            <b-btn :variant="(amt < 0) ? 'danger' : 'success'" 
                   @click="reconcile(acc)" 
                   block>
                <b>{{currency(amt)}}</b>
            </b-btn>
        </b-card>
    </b-card-group>
</template>

<script>
    import Format from '@/mixins/Format'
    import uuidv4 from 'uuid/v4'

    export default {
        props: {
            list: Array
        },
        mixins: [Format],
        created() {

        },
        data() {
            return {}
        },
        methods: {
            reconcile(account) {
                // validate total is negative
                let remain = -this.accounts[account];
                if (remain <= 0)
                    return;
                let src = [];
                // for each account that is not this one, generate an 
                // entry to remove debit until it is balanced
                this.accountsListDescByAmount.some(val => {
                    if (val.account !== account && val.amount > 0) {
                        let amount = Math.min(val.amount, remain);
                        if (amount > 0) {
                            src.push({
                                _id: uuidv4(),
                                account: val.account,
                                amount: amount,
                                rtype: 'exact'
                            });
                            remain -= amount;
                        }
                    }
                    return remain <= 0;
                });
                // generate a transaction with the entries
                let tact = {
                    id: "",
                    date: Format.today(),
                    dest: [{
                        _id: uuidv4(),
                        account: account,
                        amount: -this.accounts[account],
                        rtype: 'exact'
                    }],
                    src: src,
                    reason: `Reconcile ${account}'s account`
                };
                // send transaction to transaction editor
                this.$router.push({path: '/post', query: {tact: JSON.stringify(tact)}});
            }
        },
        computed: {
            accounts() {
                let accs = {};
                
                // add transaction amount to account map
                function mapsum(list, sign) {
                    for (let acc of list) {
                        if (!accs[acc.account])
                            accs[acc.account] = 0;
                        accs[acc.account] += sign * acc.amount;
                    }
                }

                let todayStr = Format.today();
                // add all transactions to account map
                for (let tact of this.list) {
                    if(tact.date <= todayStr) { // str comparison hack
                        mapsum(tact.src, -1);
                        mapsum(tact.dest, 1);
                    }
                }
                return accs;
            },
            accountsListDescByAmount() {
                let acr = [];
                Object.keys(this.accounts).forEach(key => {
                    acr.push({account: key, amount: this.accounts[key]});
                });
                acr.sort((a, b) => {
                    return b.amount - a.amount
                });
                return acr;
            }
        }
    }
</script>
