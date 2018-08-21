<template>
    <b-card-group columns>
        <b-card v-for="(amt, acc) in accounts"
                v-if="amt !== 0"
                :title="acc"
                :sub-title="(amt < 0) ? 'owes the group ledger' : 'is owed by the group ledger'">
            <b-btn :variant="(amt < 0) ? 'danger' : 'success'" @click="reconcile(acc)" block>
                <b>{{currency(amt)}}</b>
            </b-btn>
        </b-card>
    </b-card-group>
</template>

<script>
    import Format from '@/mixins/Format'

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
                let remain = -this.accounts[account];
                if (remain <= 0)
                    return;
                let src = [];
                this.accountsListDescByAmount.some(val => {
                    if (val.account !== account && val.amount > 0) {
                        let amount = Math.round(Math.min(val.amount, remain) * 100) / 100;
                        if (amount > 0) {
                            src.push({account: val.account, amount: amount});
                            remain -= amount;
                        }
                    }
                    return remain <= 0;
                });
                let tact = {
                    id: "",
                    date: Format.today(),
                    dest: [{account: account, amount: Math.round(-this.accounts[account] * 100) / 100}],
                    src: src,
                    reason: `Reconcile ${account}'s account`
                };
                this.$router.push({path: '/post', query: {tact: JSON.stringify(tact)}});
            }
        },
        computed: {
            accounts() {
                let accs = {};
                for (let tact of this.list) {
                    for (let acc of tact.src) {
                        if (!accs[acc.account])
                            accs[acc.account] = 0;
                        accs[acc.account] -= acc.amount;
                    }
                    for (let acc of tact.dest) {
                        if (!accs[acc.account])
                            accs[acc.account] = 0;
                        accs[acc.account] += acc.amount;
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
