<template>
    <b-container :class="loadingStyle">
        <b-navbar type="dark" variant="primary" toggleable="md" class="mt-3">
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

        <b-form @submit="onSubmit" class="mt-4">
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

            <div class="mb-4">
                <h5>Credits</h5>
                <p>We will take money out of these accounts.</p>
                <AccountList account-type="credit"
                             :list="transaction.src"
                             :sum="srctotal"
                             :counter-sum="desttotal"
                             :opts.sync="inputOptions"></AccountList>
            </div>

            <div class="mb-4">
                <h5>Debits</h5>
                <p>We will put money into these accounts.</p>
                <AccountList account-type="debit"
                             :list="transaction.dest"
                             :sum="desttotal"
                             :counter-sum="srctotal"
                             :opts.sync="inputOptions"></AccountList>
            </div>

            <hr>
            <h5>Evidence</h5>
            <p>Attach any images that witness this transaction.
                Note that any previously attached images will be overwritten on submission.</p>

            <div class="mb-4">
            <b-form-file class="mb-2" multiple
                         v-model="transaction._evidence"
                         accept="image/jpeg, image/png, image/gif">
                <template slot="file-name" slot-scope="{ names }">
                    <b-badge variant="primary" v-for="name in names" class="mr-2" :key="name">
                        {{ name }}
                    </b-badge>
                </template>
            </b-form-file>
            <b-button @click="transaction._evidence = null">Clear</b-button>
            </div>
            <b-card-group columns>
                <a v-for="(evidence_path, index) in transaction._evidence_paths" :key="evidence_path"
                   :href="'/evidence/get/' + evidence_path"
                   target="_blank">
                    <b-card :img-src="'/evidence/get/' + evidence_path"
                            overlay>
                        <div slot="footer">
                            <small class="text-muted">{{transaction._evidence_names[index]}}</small>
                        </div>
                    </b-card>
                </a>
            </b-card-group>

            <b-card no-body class="mb-4" align="center">
                <b-button type="submit" variant="primary" :disabled="hasErrors" block>Submit</b-button>

                <b-list-group flush>
                    <b-list-group-item v-for="error in errors" :key="error">
                        {{ error }}
                    </b-list-group-item>
                </b-list-group>
            </b-card>
        </b-form>
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
                    // TODO vulnerable to XSS
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
                    dest: [],
                    _evidence_paths: [],    // stores evidence paths from server
                    _evidence_names: [],    // stores evidence names from server, by uploader
                    _evidence: null         // stores local File objects from form
                },
                inputOptions: {
                    percentLock: {          // only one column can use percent at a time
                        name: '',
                        count: 0
                    },
                    diffLock: {             // only one input can use diff at a time
                        name: '',
                        handle: null
                    },
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
            total(arr) {
                return arr.reduce((p, c) => p + c.amount, 0);
            },
        },
        computed: {
            errors() {
                let err = [];
                if (this.srctotal !== this.desttotal)
                    err.push('Debits and credits do not balance!');
                if (this.srctotal <= 0 || this.desttotal <= 0)
                    err.push('Debit and/or credits cannot be non-positive!');
                return err;
            },
            hasErrors() {
                return this.errors.length > 0;
            },
            srctotal() {
                return this.total(this.transaction.src);
            },
            desttotal() {
                return this.total(this.transaction.dest);
            }
        }
    }
</script>