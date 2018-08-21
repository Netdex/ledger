<template>
    <b-container :class="loadingStyle">
        <b-card>
            <b-navbar type="light" toggleable="md">
                <b-navbar-brand>{{transaction.id ? 'Edit transaction' : 'New transaction'}}</b-navbar-brand>
                <b-navbar-toggle target="post_nav_collapse"></b-navbar-toggle>
                <b-collapse is-nav id="post_nav_collapse">
                    <b-navbar-nav>
                    </b-navbar-nav>
                </b-collapse>
                <b-navbar-nav class="ml-auto">
                    <b-button id="deletePopover"
                              variant="danger"
                              v-if="transaction.id !== ''">
                        Delete <i class="fas fa-trash"></i>
                        <b-popover target="deletePopover"
                                   placement="right"
                                   title="Confirm"
                                   triggers="click blur">
                            <b-btn variant="danger" size="sm" @click="deleteTransaction" block>Delete this transaction
                            </b-btn>
                        </b-popover>
                    </b-button>
                </b-navbar-nav>
            </b-navbar>

            <b-form @submit="onSubmit">
                <h3></h3>
                <hr>
                <b-form-group label="Reason"
                              label-for="reason"
                              description="The reason this transaction was made.">
                    <b-form-input id="reason"
                                  type="text"
                                  placeholder="Transaction reason"
                                  v-model="transaction.reason"
                                  required></b-form-input>
                </b-form-group>
                <b-form-group label="Date"
                              label-for="date"
                              description="The date this transaction occurred.">
                    <b-form-input id="date"
                                  type="date"
                                  v-model="transaction.date"
                                  required></b-form-input>
                </b-form-group>

                <b-row>
                    <b-col>
                        <h4>Credits</h4>
                        <AccountList :list="transaction.src"></AccountList>
                    </b-col>
                    <b-col>
                        <h4>Debits</h4>
                        <AccountList :list="transaction.dest"></AccountList>
                    </b-col>
                </b-row>
                <hr>

                <b-card no-body align="center">
                    <b-button type="submit" variant="primary" :disabled="hasErrors" block>Submit</b-button>

                    <b-list-group flush>
                        <b-list-group-item v-for="error in errors">
                            {{ error }}
                        </b-list-group-item>
                    </b-list-group>
                </b-card>
            </b-form>
        </b-card>
    </b-container>
</template>

<script>
    import AccountList from '@/components/AccountList.vue';
    import LoadProgress from "@/mixins/LoadProgress";
    import {Transaction} from "@/util/Transaction";
    import Format from "@/mixins/Format";

    function centTotal(list) {
        return list.reduce((p, c) => p + c.amount * 100, 0);
    }

    export default {
        components: {AccountList},
        mixins: [LoadProgress],
        created() {
            if (this.$route.query.id) {
                this.fetchData(this.$route.query.id);
            } else if (this.$route.query.tact) {
                try {
                    this.transaction = Object.assign(this.transaction, JSON.parse(this.$route.query.tact));
                } catch (e) {
                    alert(`error: ${e}`);
                }
            }
        },
        data() {
            return {
                transaction: {
                    id: "",
                    reason: "",
                    date: Format.today(),
                    src: [],
                    dest: []
                }
            }
        },
        methods: {
            fetchData(id) {
                this.setState('loading');
                Transaction.get(id)
                    .then(response => {
                        this.transaction = response;
                        this.setState('success');
                    })
                    .catch(() => {
                        this.setState('error');
                    });
            },
            onSubmit() {
                this.setState('loading');
                Transaction.upsert(this.transaction)
                    .then(() => {
                        this.$router.push('/');
                        this.setState('success');
                    })
                    .catch(e => {
                        alert(`error: ${e}`);
                        this.setState('error');
                    });
            },
            deleteTransaction() {
                this.setState('loading');
                Transaction.del(this.transaction.id)
                    .then(() => {
                        this.setState('success');
                        this.$router.push('/');
                    })
                    .catch(e => {
                        alert(`error: ${e}`);
                        this.setState('error');
                    });
            }
        },
        computed: {
            errors() {
                let st = centTotal(this.transaction.src);
                let dt = centTotal(this.transaction.dest);

                let err = [];
                if (st !== dt) {
                    err.push('Debits and credits do not balance!');
                }
                if (st <= 0 || dt <= 0) {
                    err.push('Debit and/or credits cannot be non-positive!');
                }
                return err;
            },
            hasErrors() {
                return this.errors.length > 0;
            }
        }
    }
</script>