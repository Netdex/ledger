<template>
    <div id="app">
        <b-navbar type="light" toggleable="md">
            <router-link to="/" class="navbar-brand">ledger</router-link>
            <b-navbar-toggle target="app_nav_collapse"></b-navbar-toggle>
            <b-collapse is-nav id="app_nav_collapse">
                <b-navbar-nav>
                    <b-nav-item to="/">Home</b-nav-item>
                    <b-nav-item to="/post">New transaction <i class="fas fa-pencil-alt"></i></b-nav-item>
                    <b-nav-item v-b-modal="'help-modal'">Help <i class="fas fa-question-circle"></i></b-nav-item>
                </b-navbar-nav>
                <b-navbar-nav class="ml-auto">
                    <b-nav-item>this is truly the future of money management</b-nav-item>
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>

        <router-view/>

        <HelpModal></HelpModal>
    </div>
</template>

<script>
    import HelpModal from '@/components/HelpModal'

    export default {
        components: {HelpModal}
    }
</script>