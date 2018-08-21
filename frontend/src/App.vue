<template>
    <div id="app">
        <b-navbar type="light" toggleable="md">
            <router-link to="/" class="navbar-brand">ledger</router-link>
            <b-navbar-toggle target="app_nav_collapse"></b-navbar-toggle>
            <b-collapse is-nav id="app_nav_collapse">
                <b-navbar-nav>
                <router-link to="/post" class="nav-link"><i class="fas fa-pencil-alt"></i> New transaction</router-link>
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
        <router-view/>
    </div>
</template>

