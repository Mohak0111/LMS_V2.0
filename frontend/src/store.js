// store.js

import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    jwtToken: null, // Initialize JWT token as null
  },
  mutations: {
    setJwtToken(state, token) {
      state.jwtToken = token; // Mutate the JWT token state
    },
    clearJwtToken(state) {
      state.jwtToken = null; // Clear JWT token when needed
    },
  },
  actions: {
    setToken({ commit }, token) {
      commit('setJwtToken', token);
    },
    clearToken({ commit }) {
      commit('clearJwtToken');
    },
  },
  getters: {
    getToken: (state) => state.jwtToken,
    isLoggedIn: (state) => {
      return state.jwtToken !== null && state.jwtToken !== undefined;
    },
    getUserRole: (state) => {
      if (state.jwtToken) {
        const decodedToken = JSON.parse(atob(state.jwtToken.split('.')[1]));
        return decodedToken.user_type || null; // Return the user_type claim or null
      }
      return null; // Return null if there's no token
    }
  },
});

export default store;
