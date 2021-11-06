import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

require('spectre.css/dist/spectre.css')
require('spectre.css/dist/spectre-exp.css')
require('spectre.css/dist/spectre-icons.css')

import Toasted from 'vue-toasted';

Vue.use(Toasted, {
  duration: 3000
})

import VueFormulate from '@braid/vue-formulate'

Vue.use(VueFormulate)

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
