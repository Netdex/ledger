<template>
    <div id="app">
        <b-navbar type="light" toggleable="md">
            <router-link to="/" class="navbar-brand">ledger</router-link>
            <b-navbar-toggle target="app_nav_collapse"></b-navbar-toggle>
            <b-collapse is-nav id="app_nav_collapse">
                <b-navbar-nav>
                    <b-nav-item to="/">Home</b-nav-item>
                    <b-nav-item to="/post">New transaction <i class="fas fa-pencil-alt"></i></b-nav-item>
                </b-navbar-nav>
                <b-navbar-nav class="ml-auto">
                    <b-nav-item>I fucking hate Vue.js</b-nav-item>
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
        
        <router-view/>
        
        <footer class="page-footer">
            <b-container>
            <b-row>
            <b-col md="6" class="mx-auto text-center">
                <h6><small>Made with hate from Waterloo</small></h6>
            </b-col>
            </b-row>
            </b-container>
        </footer>
    </div>
</template>

