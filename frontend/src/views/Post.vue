<template>
    <b-container :class="loadingStyle">
        <b-card>
            <b-navbar type="light" toggleable="md">
                <b-navbar-brand>{{transaction.id ? 'Edit transaction' : 'New transaction'}}</b-navbar-brand>
                <b-navbar-toggle target="post_nav_collapse"></b-navbar-toggle>
                <b-collapse is-nav id="post_nav_collapse">
                    <b-navbar-nav class="ml-auto">
                        <b-button id="deletePopover"
                                  variant="danger"
                                  v-if="transaction.id !== ''"
                                  class="m-1">
                            Delete <i class="fas fa-trash"></i>
                            <b-popover target="deletePopover"
                                       placement="right"
                                       title="Confirm"
                                       triggers="click blur">
                                <b-btn variant="danger" size="sm" @click="deleteTransaction" block>
                                    Delete this transaction
                                </b-btn>
                            </b-popover>
                        </b-button>
                        <b-button variant="info"
                                  v-if="transaction.id !== ''"
                                  class="m-1"
                                  @click="duplicate">
                            Duplicate <i class="fas fa-copy"></i>
                        </b-button>
                    </b-navbar-nav>
                </b-collapse>
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

                <hr>

                <b-card title="Credits"
                        sub-title="We will take money out of these accounts."
                        class="mb-4">
                    <AccountList account-type="credit"
                                 :list="transaction.src"
                                 :sum.sync="totals.src"
                                 :counter-sum="totals.dest"
                                 :opts.sync="inputOptions"></AccountList>
                </b-card>
                <b-card title="Debits"
                        sub-title="We will put money into these accounts.">
                    <AccountList account-type="debit"
                                 :list="transaction.dest"
                                 :sum.sync="totals.dest"
                                 :counter-sum="totals.src"
                                 :opts.sync="inputOptions"></AccountList>
                </b-card>

                <hr>

                <b-card no-body align="center">
                    <b-button type="submit" variant="primary" :disabled="hasErrors" block>Submit</b-button>

                    <b-list-group flush>
                        <b-list-group-item v-for="error in errors" :key="error">
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
                },
                totals: {
                    src: 0,
                    dest: 0
                },
                inputOptions: {
                    percentLock: {          // only one column can use percent at a time
                        name: '',
                        count: 0
                    },        
                    diffLock: {
                        name: '',
                        handle: null
                    },           // only one input can use diff at a time
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
            onSubmit(evt) {
                evt.preventDefault();
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
            },
            duplicate() {
                // this is a pretty funny way to duplicate a transaction but hey it works
                this.transaction.id = "";
            },
        },
        computed: {
            errors() {
                let err = [];
                if (this.totals.src !== this.totals.dest)
                    err.push('Debits and credits do not balance!');
                if (this.totals.src <= 0 || this.totals.dest <= 0)
                    err.push('Debit and/or credits cannot be non-positive!');
                return err;
            },
            hasErrors() {
                return this.errors.length > 0;
            }
        }
    }
</script>