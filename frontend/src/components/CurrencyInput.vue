<template>
    <div>
        <b-input-group :prepend="prepend">
            <input type="text"
                   step="0.01"
                   min="0.01"
                   @change="changed($event.target.value, true)"
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
    import * as math from 'mathjs'

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
        },
        mounted() {
            this.acquireLock(this.type);
        },
        destroyed() {
            this.destroyLock(this.type);
        },
        data() {
            return {
                prepend: '',
                inputValue: '',
                isWatchSumDependant: false
            }
        },
        watch: {
            sum: function () {
                // if the component is currently watch dependant, ignore the call
                if (this.isWatchSumDependant) {
                    this.isWatchSumDependant = false;
                    return;
                }
                this.changed(this.format);
            },
            counterSum: function () {
                this.changed(this.format);
            },
            type: function (newMode, oldMode) {
                // move to new lock
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
                        // properly destroy old lock by decrementing 
                        // ref counter and removing named entry to account list
                        this.opts.percentLock.count--;
                        if (this.opts.percentLock.count === 0)
                            this.opts.percentLock.name = '';
                        // set input value to currency amount
                        this.inputValue = (this.value / 100).toFixed(2);
                        break;
                    case 'diff':
                        // properly destroy old lock by resetting handle 
                        // and removing name to account list
                        this.opts.diffLock.name = '';
                        this.opts.diffLock.handle = null;
                        break;
                }
            },
            acquireLock(newMode) {
                switch (newMode) {
                    case 'exact':
                        this.prepend = '$';
                        this.inputValue = (this.value / 100).toFixed(2);
                        break;
                    case 'percent':
                        // properly acquire new lock by setting named entry 
                        // and incrementing ref count
                        this.opts.percentLock.name = this.accountType;
                        this.opts.percentLock.count++;

                        // set input value to currency amount
                        if (this.counterSum !== 0) {
                            let val = this.value / this.counterSum * 100;
                            this.inputValue = val.toFixed(2);
                            this.prepend = this.currency(this.value);
                        }
                        else
                            this.inputValue = '0.00';
                        break;
                    case 'diff':
                        this.prepend = '$';
                        // properly acquire new lock by setting handle to 
                        // this component and settting named entry
                        this.opts.diffLock.name = this.accountType;
                        this.opts.diffLock.handle = this;
                        this.inputValue = (this.value / 100).toFixed(2);
                        break;
                }
            },
            changed(val, setWatchFlag) {
                // calculate the real monetary value in cents

                let newValue = 0;
                switch (this.type) {
                    case 'exact': {
                        let inputVal;
                        if (val.startsWith('=')) {
                            try {
                                newValue = Math.trunc(math.eval(val.substring(1)) * 100);
                                val = (newValue / 100).toFixed(2);
                            }catch(error){
                                alert("Invalid mathematical expression");
                                newValue = 0;
                                val = '0.00';
                            }
                        } else {
                            inputVal = parseFloat(+val.replace(/[^\d.]/g, ''));
                            newValue = Math.trunc(inputVal * 100);
                        }

                        break;
                    }
                    case 'percent': {
                        let inputVal = parseFloat(+val.replace(/[^\d.]/g, ''));
                        newValue = Math.trunc(this.counterSum * inputVal / 100);
                        this.prepend = this.currency(newValue);
                        break;
                    }
                    case 'diff': {
                        let inputVal = parseFloat(+val.replace(/[^\d.]/g, ''));
                        // only set watch flag if the change was due to user
                        if (setWatchFlag === true)
                            this.isWatchSumDependant = true;
                        newValue = Math.max(Math.trunc(this.counterSum - this.sum + inputVal * 100), 0);
                        break;
                    }
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
                get() {
                    return this.type
                },
                set(value) {
                    this.$emit('update:type', value)
                },
            },
        }
    }
</script>