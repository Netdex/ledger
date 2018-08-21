<style scoped>
    .lp-loading {
        opacity: 0.5;
    }

    .lp-success {
        opacity: 1.0;
    }

    .lp-error {
        opacity: 0;
    }
</style>
<script>
    export default {
        data() {
            return {
                state: 'success'
            };
        },
        methods: {
            setState(state) {
                this.state = state;
            },
        },
        computed: {
            loadingStyle() {
                return [`lp-${this.state}`];
            }
        }
    }
</script>
