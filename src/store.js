// store.js
// import Vue from 'vue';
import Vuex from 'vuex';

// Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    data: null, // initial state
  },
  mutations: {
    setData(state, payload) {
      state.data = payload;
    },
  },
});