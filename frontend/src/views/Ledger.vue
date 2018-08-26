<template>
    <b-container :class="loadingStyle">
        <AccountSummary :list="transactions" class="my-4"></AccountSummary>
        <TransactionHistory :list="transactions" class="my-4"></TransactionHistory>
    </b-container>
</template>

<script>
    import AccountSummary from "@/components/AccountSummary"
    import TransactionHistory from '@/components/TransactionHistory'
    import LoadProgress from "@/mixins/LoadProgress";
    import {Transaction} from "@/util/Transaction"
    
    export default {
        name: 'home',
        components: {
            AccountSummary,
            TransactionHistory
        },
        mixins: [LoadProgress],
        data() {
            return {
                transactions: [],
                accounts: []
            }
        },
        created() {
            this.fetchData();
        },
        methods: {
            fetchData() {
                this.setState('loading');
                Transaction.getAll()
                    .then(response => {
                        this.transactions = response;
                        this.state = 'success';
                    })
                    .catch(() => {
                        this.state = 'error'
                    });
            }
        }
    }
</script>
