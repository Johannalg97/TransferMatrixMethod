/* 
This is the main file to centralize information from VUEX, 
here we create a store from the different modules folder. In this case
we just have a module file called transfer.js where all the global data
is located as well as the actions and mutations to change this global data.
*/

import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from "vuex-persistedstate";
import transfer from './modules/transfer';

Vue.use(Vuex)

const debug = true;

// We make available all the values on the state of the file transfer.js
// as well as the actions and mutations to use them from differente .vue files
export default new Vuex.Store({
  modules: {
    transfer,
  },
  strict: debug,
  plugins: [
    createPersistedState({
      paths: [],
    }),
],
})