<style scoped>
    @keyframes flickerAnimation {
        0%   { opacity:0.5; }
        50%  { opacity:0.1; }
        100% { opacity:0.5; }
    }

    .lp-loading {
        pointer-events: none;
        animation: flickerAnimation 2s infinite ease-in-out;
    }

    .lp-success {
        opacity: 1.0;
    }

    .lp-error {
        opacity: 0.5;
        pointer-events: none;
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
