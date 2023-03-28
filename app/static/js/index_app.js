/* 
This file is in charge to mount our main vue application App.vue
on a Django template. For this, js looks for the tag id 'app' and inserts
all the generated html on it. We also import the store, where all of the centralized
data is located. Finally, we also add the django context to send data directly from 
Django to the vue components.

Here we also make global all the bootstrap vue components to build 
the front-end with built-in form fields. 
*/


import "bootstrap"
import "../sass/index_app.scss"

import Vue from "vue"
import App from "./App.vue"
import store from "./store/state"
import 'bootstrap-vue/dist/bootstrap-vue.css'
import { BootstrapVue } from "bootstrap-vue"
import { ValidationObserver, ValidationProvider, extend } from 'vee-validate';
import * as rules from "vee-validate/dist/rules"
import './store/utils/validations'
import $ from "jquery"

Vue.use(BootstrapVue);
Vue.component('ValidationProvider', ValidationProvider)
Vue.component('ValidationObserver', ValidationObserver)

if (document.getElementById('app') != null) {
  new Vue({
    store,
    data() {
      return {
        django_context: CONTEXT,
      }
    },
    render: h => h(App),
  }).$mount('#app')
}