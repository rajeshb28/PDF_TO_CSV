import Vue from 'vue'
import Router from 'vue-router'
import { interopDefault } from './utils'
import scrollBehavior from './router.scrollBehavior.js'

const _5ea0731f = () => interopDefault(import('..\\pages\\NewWorkspace.vue' /* webpackChunkName: "pages/NewWorkspace" */))
const _9330df2c = () => interopDefault(import('..\\pages\\SavedWorkspace\\index.vue' /* webpackChunkName: "pages/SavedWorkspace/index" */))
const _bf018b72 = () => interopDefault(import('..\\pages\\workspace\\index.vue' /* webpackChunkName: "pages/workspace/index" */))
const _6092a552 = () => interopDefault(import('..\\pages\\SavedWorkspace\\_id.vue' /* webpackChunkName: "pages/SavedWorkspace/_id" */))
const _4b367a98 = () => interopDefault(import('..\\pages\\index.vue' /* webpackChunkName: "pages/index" */))

// TODO: remove in Nuxt 3
const emptyFn = () => {}
const originalPush = Router.prototype.push
Router.prototype.push = function push (location, onComplete = emptyFn, onAbort) {
  return originalPush.call(this, location, onComplete, onAbort)
}

Vue.use(Router)

export const routerOptions = {
  mode: 'history',
  base: decodeURI('/'),
  linkActiveClass: 'nuxt-link-active',
  linkExactActiveClass: 'nuxt-link-exact-active',
  scrollBehavior,

  routes: [{
    path: "/NewWorkspace",
    component: _5ea0731f,
    name: "NewWorkspace"
  }, {
    path: "/SavedWorkspace",
    component: _9330df2c,
    name: "SavedWorkspace"
  }, {
    path: "/workspace",
    component: _bf018b72,
    name: "workspace"
  }, {
    path: "/SavedWorkspace/:id",
    component: _6092a552,
    name: "SavedWorkspace-id"
  }, {
    path: "/",
    component: _4b367a98,
    name: "index"
  }],

  fallback: false
}

export function createRouter () {
  return new Router(routerOptions)
}
