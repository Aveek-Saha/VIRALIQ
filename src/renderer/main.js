import Vue from 'vue'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faFolder } from '@fortawesome/free-regular-svg-icons'
import { faFolderOpen } from '@fortawesome/free-solid-svg-icons/faFolderOpen'
import { faMusic } from '@fortawesome/free-solid-svg-icons/faMusic'
import { faFileDownload } from '@fortawesome/free-solid-svg-icons/faFileDownload'

import App from './App'

if (!process.env.IS_WEB) Vue.use(require('vue-electron'))
Vue.config.productionTip = false

library.add(faFolder, faFolderOpen, faMusic, faFileDownload)

Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.use(BootstrapVue);
Vue.use(IconsPlugin)

/* eslint-disable no-new */
new Vue({
  components: { App },
  template: '<App/>'
}).$mount('#app')
