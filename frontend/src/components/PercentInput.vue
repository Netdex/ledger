<template>
    <b-input-group :prepend="currency(actual)">
        <input type="number"
               step="0.01"
               min="0"
               max="100"
               class="form-control"
        v-model="inputValue"/>
    </b-input-group>
</template>
<script>
    import Format from '@/mixins/Format'

    export default {
        mixins: [Format],
        props: { value: Number, counterSum: Number},
        data() {
            return {
                inputValue:this.value/this.counterSum*100
            };
        },
        created() {
        },
        watch:{
        },
        methods: {
            
        },
        computed: {
            actual(){
                let n = Math.floor(this.inputValue * this.counterSum / 100);
                this.$emit('input', n);
                return n;
            }
        }
    };
</script>