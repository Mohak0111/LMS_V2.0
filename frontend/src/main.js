import '@babel/polyfill';
import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'
import store from './store';
import index from './components/index.vue'
import libr_login from './components/libr_login.vue'
import libr_dash from './components/libr_dash.vue' 
import requests from './components/requests.vue' 
import section_create from './components/section_create.vue' 
import section_edit from './components/section_edit.vue' 
import section_delete from './components/section_delete.vue' 
import book_create from './components/book_create.vue' 
import book_delete from './components/book_delete.vue' 
import book_edit from './components/book_edit.vue' 
import libr_summary from './components/libr_summary.vue' 
import logout from './components/logout.vue' 
import user_login from './components/user_login.vue' 
import user_dash from './components/user_dash.vue' 
import user_requests from './components/user_requests.vue' 
import user_books from './components/user_books.vue' 
import user_return from './components/user_return.vue' 
import user_feedback from './components/user_feedback.vue' 
import user_view from './components/user_view.vue' 
import user_search from './components/user_search.vue' 
import user_register from './components/user_register.vue' 
import user_request from './components/user_request.vue' 



Vue.use(VueRouter)

const routes=[
  {
    path: "/",
    component: index,
  },
  {
    path:"/libr_login",
    component: libr_login
  },
  {
    path:"/libr_dash",
    component: libr_dash
  },
  {
    path:"/requests",
    component: requests
  },
  {
    path:"/section_create",
    component: section_create
  },
  {
    path:"/section_edit",
    component: section_edit
  },
  {
    path:"/section_delete",
    component: section_delete
  },
  {
    path:"/book_create",
    component: book_create
  },
  {
    path:"/book_delete",
    component: book_delete
  },
  {
    path:"/book_edit",
    component: book_edit
  },
  {
    path:"/admin_summary",
    component: libr_summary
  },
  {
    path:"/logout",
    component: logout
  },
  {
    path:"/user_login",
    component: user_login
  },
  {
    path:"/user_dash",
    component: user_dash
  },
  {
    path:"/user_requests",
    component: user_requests
  },
  {
    path:"/user_books",
    component: user_books
  },
  {
    path:"/user_return",
    name:"user_return",
    component: user_return
  },
  {
    path:"/user_feedback",
    name:"user_feedback",
    component: user_feedback
  },
  {
    path:"/user_view",
    name:"user_view",
    component: user_view
  },
  {
    path:"/user_search",
    name:"user_search",
    component: user_search
  },
  {
    path:"/user_register",
    name:"user_register",
    component: user_register
  },
  {
    path:"/user_request",
    name:"user_request",
    component: user_request
  },
]

const router=new VueRouter({
  routes,
  mode: 'history'
});

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
