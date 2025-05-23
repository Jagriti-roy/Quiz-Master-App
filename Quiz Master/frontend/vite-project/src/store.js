import { defineStore } from 'pinia';

export const useMainStore = defineStore('main', {
  state: () => ({
    counter: 0,
    user: null, 
    maintoken: localStorage.getItem('maintoken') ? Number(localStorage.getItem('maintoken')) : 0,
    token: localStorage.getItem('token') ? Number(localStorage.getItem('token')) : 0
  }),
  actions: {
    setMainToken(value) {
      this.maintoken = value;
      localStorage.setItem('maintoken', value);
    }
  }
});
