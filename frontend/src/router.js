import Vue from 'vue'
import Router from 'vue-router'
import Ledger from './views/Ledger.vue'
import Post from './views/Post.vue'

Vue.use(Router)

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
            component: Post
        }
    ]
})
