<template>
    <b-card>
        <b-container fluid>
            <b-row class="mb-2">
                <b-col md="6" class="my-1">
                    <b-form-group horizontal label="Filter" class="mb-0">
                        <b-input-group>
                            <b-form-input v-model="filter" placeholder="Type to search"></b-form-input>
                            <b-input-group-append>
                                <b-btn :disabled="!filter" @click="filter = ''">Clear</b-btn>
                            </b-input-group-append>
                        </b-input-group>
                    </b-form-group>
                </b-col>
            </b-row>
            <b-row>
                <b-table :fields="fields"
                         :items="list"
                         :sort-by.sync="sortBy"
                         :sort-desc.sync="sortDesc"
                         :per-page="per_page"
                         :current-page="page"
                         :filter="filter"
                         @filtered="onFiltered"
                         @row-clicked="onRowClicked"
                         stacked="md"
                         hover show-empty>
                    <template slot="table-caption">
                        Click on a transaction to modify/view details.
                    </template>
                    <template slot="date" slot-scope="data">
                        <span class="text-nowrap">{{data.item.date}}</span>
                    </template>
                    <template slot="tact" slot-scope="data">
                        <b-row>
                            <b-col md="6">
                                <b-badge v-for="src in data.item.src"
                                         :key="src.id"
                                         variant="primary" class="w-100">{{src.account}}
                                    <b-badge variant="danger" class="float-right">-{{currency(src.amount)}}</b-badge>
                                </b-badge>
                            </b-col>
                            <b-col md="6">
                                <b-badge v-for="dest in data.item.dest"
                                         :key="dest.id"
                                         variant="primary" class="w-100">{{dest.account}}                            
                                    <b-badge variant="success" class="float-right">+{{currency(dest.amount)}}</b-badge>
                                </b-badge>
                            </b-col>
                        </b-row>
                    </template>
                </b-table>
            </b-row>
        </b-container>
        <b-pagination :total-rows="rows" :per-page="per_page" v-model="page" align="center"></b-pagination>


    </b-card>
</template>


<script>
    import Format from '@/mixins/Format'

    export default {
        mixins: [Format],
        props: {
            list: Array
        },
        data() {
            return {
                page: 1,
                per_page: 10,
                sortBy: 'date',
                sortDesc: true,
                fields: [
                    {key: 'date', sortable: true},
                    {key: 'tact', label: 'Transaction'},
                    'reason',
                ],
                filter: null
            };
        },
        methods: {
            onFiltered(items) {
                this.rows = items.length;
                this.page = 1;
            },
            onRowClicked(item){
                this.$router.push({name:'post',query:{id:item.id}});
            }
        },
        computed: {
            rows(){
                return this.list.length
            }
        }
    }
</script>