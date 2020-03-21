import Vue from 'vue'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

import App from './App'

if (!process.env.IS_WEB) Vue.use(require('vue-electron'))
Vue.config.productionTip = false

Vue.use(BootstrapVue);
Vue.use(IconsPlugin)

/* eslint-disable no-new */
new Vue({
  components: { App },
  template: '<App/>'
}).$mount('#app')
