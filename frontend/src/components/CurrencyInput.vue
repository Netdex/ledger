<template>
    <div>
        <b-input-group :prepend="prepend">
            <input type="number"
                   step="0.01"
                   min="0.01"
                   @change="changed($event.target.value)"
                   :value="format"
                   ref="input"
                   class="form-control"
                   :disabled="type === 'diff'"/>
            <b-form-radio-group buttons
                                button-variant="outline-primary"
                                v-model="typeModel">
                <b-form-radio value="exact">$</b-form-radio>
                <b-form-radio value="percent" :disabled="!hasPercentLock">%</b-form-radio>
                <b-form-radio value="diff" :disabled="!hasDiffLock">B</b-form-radio>
            </b-form-radio-group>
        </b-input-group>

    </div>
</template>
<script>
    import Format from '@/mixins/Format'

    export default {
        props: {
            value: Number,
            opts: Object,
            accountType: String,
            counterSum: Number,
            sum: Number,
            type: String
        },
        mixins: [Format],
        created() {
            this.inputValue = (this.value / 100).toFixed(2);
            this.acquireLock(this.type);
        },
        destroyed() {
            this.destroyLock(this.type);
        },
        data() {
            return {
                prepend: '',
                inputValue: '0.00',
                isSumWatcherDepend: false
            }
        },
        watch: {
            sum: function () {
                if (this.isSumWatcherDepend) {
                    this.isSumWatcherDepend = false;
                    return;
                }
                this.changed(this.format);
            },
            counterSum: function () {
                this.changed(this.format);
            },
            type: function (newMode, oldMode) {
                this.destroyLock(oldMode);
                this.acquireLock(newMode);

                this.changed(this.inputValue);
            }
        },
        methods: {
            destroyLock(oldMode) {
                switch (oldMode) {
                    case 'exact':
                        break;
                    case 'percent':
                        this.opts.percentLock.count--;
                        if (this.opts.percentLock.count === 0)
                            this.opts.percentLock.name = '';
                        this.inputValue = (this.value / 100).toFixed(2);
                        break;
                    case 'diff':
                        this.opts.diffLock.name = '';
                        this.opts.diffLock.handle = null;
                        break;
                }
            },
            acquireLock(newMode) {
                switch (newMode) {
                    case 'exact':
                        this.prepend = '$';
                        break;
                    case 'percent':
                        this.opts.percentLock.name = this.accountType;
                        this.opts.percentLock.count++;
                        if (this.counterSum === 0)
                            this.inputValue = '0.00';
                        else
                            this.inputValue = (this.value / this.counterSum * 100).toFixed(2);
                        break;
                    case 'diff':
                        this.prepend = '$';
                        this.opts.diffLock.name = this.accountType;
                        this.opts.diffLock.handle = this;
                        break;
                }
            },
            changed(val) {
                // calculate the real monetary value in cents
                let inputVal = parseFloat(+val.replace(/[^\d.]/g, ''));

                let newValue = 0;
                switch (this.type) {
                    case 'exact':
                        newValue = inputVal * 100;
                        break;
                    case 'percent':
                        newValue = Math.round(this.counterSum * inputVal / 100);
                        this.prepend = this.currency(newValue);
                        break;
                    case 'diff':
                        this.isSumWatcherDepend = true;
                        newValue = Math.max(this.counterSum - this.sum + inputVal * 100, 0);
                        break;
                }
                this.$emit('input', newValue);
                this.inputValue = val;
            }
        },
        computed: {
            format() {
                // display formatted monetary value
                let fmtValue = '';
                switch (this.type) {
                    case 'exact':
                        fmtValue = (parseFloat(this.value) / 100).toFixed(2);
                        break;
                    case 'percent':
                        fmtValue = this.inputValue;
                        break;
                    case 'diff':
                        fmtValue = (parseFloat(this.value) / 100).toFixed(2);
                        break;
                }
                return fmtValue;
            },
            hasPercentLock() {
                return (this.opts.percentLock.name === this.accountType || this.opts.percentLock.name === '') &&
                    (this.opts.diffLock.name === this.accountType || this.opts.diffLock.name === '');
            },
            hasDiffLock() {
                return (this.opts.diffLock.handle === this || this.opts.diffLock.handle === null) &&
                    this.hasPercentLock;
            },
            typeModel: {
                get () { return this.type },
                set (value) { this.$emit('update:type', value) },
            },
        }
    }
</script>