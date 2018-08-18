<template>
    <div id="app">
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <router-link to="/" class="navbar-brand">ledger</router-link>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <router-link to="/post" class="nav-link"><i class="fas fa-pencil-alt"></i> New transaction</router-link>
                    </li>
                </ul>
            </div>
        </nav>
        <router-view/>
    </div>
</template>

