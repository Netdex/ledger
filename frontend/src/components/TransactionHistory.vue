<template>
    <b-card>
        
        <b-table :fields="fields"
                 :items="list"
                 :sort-by.sync="sortBy"
                 :sort-desc.sync="sortDesc"
                 :per-page="per_page"
                 :current-page="page"
                 stacked="md"
                 hover>
            <template slot="tact" slot-scope="data">
                <b-row>
                    <b-col md="6">
                        <b-badge variant="primary" class="w-100" v-for="src in data.item.src">{{src.account}}
                            <b-badge variant="danger" class="float-right">-{{currency(src.amount)}}</b-badge>
                        </b-badge>
                    </b-col>
                    <b-col md="6">
                        <b-badge variant="primary" class="w-100" v-for="dest in data.item.dest">{{dest.account}}                            
                            <b-badge variant="success" class="float-right">+{{currency(dest.amount)}}</b-badge>
                        </b-badge>
                    </b-col>
                </b-row>
            </template>
            <template slot="edit" slot-scope="data">
                <b-button :to="{name:'post',query:{id:data.item.id}}" variant="warning" block size="sm">
                    <i class="fas fa-pencil-alt"></i>
                </b-button>
            </template>
        </b-table>
        <b-pagination :total-rows="list.length" :per-page="per_page" v-model="page" align="center"></b-pagination>
    </b-card>
</template>


<script>
    import Format from '@/mixins/Format'

    export default {
        mixins: [Format],
        data() {
            return {
                page: 0,
                per_page: 10,
                sortBy: 'date',
                sortDesc: true,
                fields: [
                    {key: 'date', sortable: true},
                    {key: 'tact', label: 'Transaction'},
                    'reason',
                    {key: 'edit', label: 'Edit'}
                ]
            };
        },
        props: {
            list: Array
        },
        methods: {}
    }
</script>