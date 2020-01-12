<template>
    <hot-table :settings="hotSettings" ref="table">
        <!--                    <hot-column title="First column header">-->
        <!--                    </hot-column>-->
        <!--                    <hot-column :settings="{ title: 'Second column header' }" read-only="true">-->
        <!--                    </hot-column>-->
    </hot-table>
    <!--    <b-card>-->
    <!--        <div slot="header">-->
    <!--            <b-nav pills>-->
    <!--                <b-nav-item @click="addAccount" active>Add <i class="fas fa-plus"/></b-nav-item>-->
    <!--                <b-nav-item @click="clearAccounts">Clear <i class="fas fa-eraser"/></b-nav-item>-->
    <!--                <div class="ml-auto">-->
    <!--                    <b-btn variant="primary">-->
    <!--                        Total -->
    <!--                        <b-badge variant="success">{{currency(sum)}}</b-badge>-->
    <!--                    </b-btn>-->
    <!--                </div>-->
    <!--            </b-nav>-->

    <!--        </div>-->

    <!--        <b-form-group v-for="acc in list" :key="acc._id" inline>-->
    <!--            <b-row>-->
    <!--                <b-col md="6">-->
    <!--                    <b-form-input type="text"-->
    <!--                                  placeholder="Account name"-->
    <!--                                  v-model="acc.account"-->
    <!--                                  required/>-->
    <!--                </b-col>-->
    <!--                <b-col md="4">-->
    <!--                    <CurrencyInput v-model="acc.amount"-->
    <!--                                   :account-type="accountType"-->
    <!--                                   :opts.sync="opts"-->
    <!--                                   :sum="sum"-->
    <!--                                   :counter-sum="counterSum"-->
    <!--                                   :type.sync="acc.rtype"/>-->
    <!--                </b-col>-->
    <!--                <b-col md="2">-->
    <!--                    <b-button variant="danger" @click="delAccount(acc)" block>-->
    <!--                        <i class="fas fa-trash"/></b-button>-->
    <!--                </b-col>-->
    <!--            </b-row>-->
    <!--        </b-form-group>-->

    <!--    </b-card>-->
</template>

<script>
    import {HotTable} from '@handsontable/vue'
    import Handsontable from 'handsontable'

    var accountWatcher = {
        handler: function () {
            this.$refs.table.hotInstance.render();
        },
        deep: true
    };
    const CREDITOR_COL = 0;
    const DEBTOR_COL = 1;

    export default {
        components: {HotTable},
        props: {
            "debtors": Array,
            "creditors": Array,
        },
        mounted() {
            this.$refs.table.hotInstance.render();
        },
        watch: {
            debtors: accountWatcher,
            creditors: accountWatcher
        },
        data() {
            var that = this;
            return {
                hotSettings: {
                    data: [['0']],
                    rowHeaders: true,
                    minSpareRows: 1,
                    minSpareCols: 1,
                    minCols: 20,
                    maxCols: 20,
                    minRows: 10,
                    maxRows: 20,
                    licenseKey: 'non-commercial-and-evaluation',
                    formulas: true,
                    manualColumnResize: true,
                    afterChange: (changes) => {
                        changes.forEach(([row, col, oldValue, newValue]) => {
                            if (col === CREDITOR_COL) {
                                if(row < this.creditors.length){
                                    this.creditors[row]._sheetValue = newValue;
                                    this.$emit('update:creditors', this.creditors);
                                    console.log(this.creditors[row]);
                                }
                            } else if (col === DEBTOR_COL) {
                                if(row < this.debtors.length){
                                    this.debtors[row]._sheetValue = newValue;
                                    this.$emit('update:debtors', this.debtors);
                                    console.log(this.debtors[row]);
                                }
                            }
                            console.log(row, col, oldValue, newValue);
                        });
                    },
                    colHeaders: function (index) {
                        switch (index) {
                            case 0:
                                return 'A: Creditors';
                            case 1:
                                return 'B: Debtors';
                            default:
                                return String.fromCharCode(65 + index);
                        }
                    },
                    cells: function (row, col) {
                        var cellProperties = {};

                        if (col === CREDITOR_COL) {
                            // cellProperties.readOnly = true;
                            cellProperties.renderer = function (instance, td, row, col, prop, value, cellProperties) {
                                Handsontable.renderers.TextRenderer.apply(this, arguments);

                                if (row >= that.creditors.length)
                                    return;
                                cellProperties;
                                td.style.background = '#CEC';
                                td.innerHTML = `<i style="color:#a9a9a9">${that.creditors[row].account}:</i> ` + td.innerHTML;
                            };
                        } else if (col === DEBTOR_COL) {
                            // cellProperties.readOnly = true;
                            cellProperties.renderer = function (instance, td, row, col, prop, value, cellProperties) {
                                Handsontable.renderers.TextRenderer.apply(this, arguments);
                                if (row >= that.debtors.length)
                                    return;
                                cellProperties;
                                td.style.background = '#ECC';
                                td.innerHTML = `<i style="color:#a9a9a9">${that.debtors[row].account}:</i> ` + td.innerHTML;
                            };

                        }


                        return cellProperties;
                    }
                    // columns: [
                    //     {
                    //         title: 'Debits',
                    //         renderer: function(instance, td, row, col, prop, value) {
                    //             const escaped = Handsontable.helper.stringify(value);
                    //             let img = null;
                    //
                    //             if (escaped.indexOf('http') === 0) {
                    //                 img = document.createElement('IMG');
                    //                 img.src = value;
                    //
                    //                 Handsontable.dom.addEvent(img, 'mousedown', function(event) {
                    //                     event.preventDefault();
                    //                 });
                    //
                    //                 Handsontable.dom.empty(td);
                    //                 td.appendChild(img);
                    //             } else {
                    //                 Handsontable.renderers.TextRenderer.apply(this, arguments);
                    //             }
                    //
                    //             return td;
                    //         }
                    //     },
                    //     {
                    //         title: 'Credits',
                    //         renderer: function(instance, td, row, col, prop, value) {
                    //             const escaped = Handsontable.helper.stringify(value);
                    //             let img = null;
                    //
                    //             if (escaped.indexOf('http') === 0) {
                    //                 img = document.createElement('IMG');
                    //                 img.src = value;
                    //
                    //                 Handsontable.dom.addEvent(img, 'mousedown', function(event) {
                    //                     event.preventDefault();
                    //                 });
                    //
                    //                 Handsontable.dom.empty(td);
                    //                 td.appendChild(img);
                    //             } else {
                    //                 Handsontable.renderers.TextRenderer.apply(this, arguments);
                    //             }
                    //
                    //             return td;
                    //         }
                    //     },
                    //
                    //
                    // ],
                }
            }
        },
        // methods: {
        //     addAccount() {
        //         this.list.push({
        //             _id: uuidv4(),
        //             account: '',
        //             amount: 0,
        //             rtype: 'exact',
        //         });
        //     },
        //     delAccount(account) {
        //         delarrobj(this.list, account);
        //     },
        //     clearAccounts() {
        //         this.list.splice(0, this.list.length);
        //     }
        // },
        // computed: {
        //
        // }
    }
</script>
