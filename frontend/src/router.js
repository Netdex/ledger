import Vue from 'vue'
import Router from 'vue-router'
import Ledger from './views/Ledger.vue'

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            name: 'home',
            component: Ledger
        },
        {
            path: '/post',
            name: 'post',
            component: () => import( './views/Post.vue')
        }
    ]
})
