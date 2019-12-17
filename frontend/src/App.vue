<style>
    .slide-fade-enter-active {
        transition: all .3s ease;
    }

    .slide-fade-leave-active {
        transition: all .3s cubic-bezier(1.0, 0.5, 0.8, 1.0);
    }

    .slide-fade-enter, .slide-fade-leave-to {
        transform: translateX(10px);
        opacity: 0;
    }
</style>
<template>
    <div id="app">
        <b-navbar type="dark" variant="primary" toggleable="md">
            <b-navbar-brand to="/">ledger redux</b-navbar-brand>
            <b-navbar-toggle target="app_nav_collapse"/>
            <b-collapse is-nav id="app_nav_collapse">
                <b-navbar-nav>
                    <b-btn to="/post" variant="success">New transaction <i class="fas fa-pencil-alt"/></b-btn>
                    <b-nav-item to="/">Home</b-nav-item>
                    <b-nav-item v-b-modal="'help-modal'">Help <i class="fas fa-question-circle"/></b-nav-item>
                </b-navbar-nav>
                <b-navbar-nav class="ml-auto">
                    <b-nav-item>this is truly the future of money management</b-nav-item>
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>

        <transition name="slide-fade" mode="out-in">
            <router-view/>
        </transition>

        <HelpModal/>
    </div>
</template>

<script>
    import HelpModal from '@/components/HelpModal'

    export default {
        components: {HelpModal}
    }
</script>