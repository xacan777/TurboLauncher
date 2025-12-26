import { storage } from '@/config/storage.config';
import { createStore } from 'vuex';
import { api } from '@/services/api';

export default createStore({
  state: {
    isAuthorized: storage.getStorageSync('isAuthorized') || false,
    user: storage.getStorageSync('user') || {},
    token: storage.getStorageSync('token') || null,
    isAfterAuthorized: false,
    userBase: {
      login: null,
      password: null,
    },
    clientParams: {
      param1: null,
      param2: null,
    },
    isClientReady: false,
    ticketMulti: [],
    modalDirSettingsState: false,
    download: {
      path: null,
      state: 'default',
      downloaded: false,
      verified: false,
    },
  },
  getters: {
    isAuthorized: (state) => state.isAuthorized,
    token: (state) => state.token,
    isAfterAuthorized: (state) => state.isAfterAuthorized,
    user: (state) => state.user,
    ticketMulti: (state) => state.ticketMulti,
    isShowDirSettings: (state) => state.modalDirSettingsState,
    download: (state) => state.download,
    userBase: (state) => state.userBase,
    clientParams: (state) => state.clientParams,
    isClientReady: (state) => state.isClientReady,
  },
  mutations: {
    setIsAfterAuthorized(state, payload) {
      state.isAfterAuthorized = payload;
    },
    setIsClientReady(state, payload) {
      console.log('CLIENT READFY!');
      state.isClientReady = payload;
    },
    setUserBase(state, payload) {
      state.userBase = payload;
    },
    setClientParams(state, payload) {
      state.clientParams = payload;
    },
    setAuthorized(state, payload) {
      state.isAuthorized = payload;
    },
    setUser(state, payload) {
      state.user = payload;
    },
    setToken(state, payload) {
      state.token = payload;
    },
    setUserBalance(state, payload) {
      state.user.mBalance = payload;
    },
    setTicketMulti(state, payload) {
      state.ticketMulti = payload;
    },
    setStateModalDirSettings(state, payload) {
      state.modalDirSettingsState = payload;
    },
    setDownloadPath(state, payload) {
      state.download.path = payload;
    },
    setDownloadState(state, payload) {
      state.download.state = payload;
    },
    setDownloadClient(state, payload) {
      state.download.downloaded = payload;
    },
    setDownloadVerified(state, payload) {
      if (!payload) {
        state.download.state = 'default';
      }
      state.download.verified = payload;
    },
  },
  actions: {
    initApp({ commit }) {
      return new Promise((resolve) => {
        commit('setDownloadPath', storage.getStorageSync('downloadPath') || null);
        commit('setDownloadClient', storage.getStorageSync('downloaded') || false);

        const storageUserBase = storage.getStorageSync('userBase');
        const storageClientParams = storage.getStorageSync('clientParams');

        if (storageUserBase) {
          commit('setUserBase', storage.getStorageSync('userBase'));
        }

        if (storageClientParams) {
          commit('setClientParams', storage.getStorageSync('clientParams'));
        }

        const storageToken = storage.getStorageSync('token');
        if (storageToken) {
          commit('setToken', storageToken);
          commit('setAuthorized', true);
        }

        resolve();
      });
    },
    async login({ commit }, payload) {
      const response = await api.login(payload);
      commit('setToken', response.token);
      storage.setStorageSync('token', response.token);
      commit('setAuthorized', true);
      commit('setUser', response.user);
    },
    async register(_, payload) {
      return api.register(payload);
    },
    setIsAfterAuthorized({ commit }, payload) {
      commit('setIsAfterAuthorized', payload);
    },
    setIsClientReady({ commit }, payload) {
      commit('setIsClientReady', payload);
    },
    setUserBase({ commit }, payload) {
      commit('setUserBase', payload);
      storage.setStorageSync('userBase', payload);
    },
    setClientParams({ commit }, payload) {
      commit('setClientParams', payload);
      storage.setStorageSync('clientParams', payload);
    },
    setDownloadPath({ commit }, payload) {
      commit('setDownloadPath', payload);
      storage.setStorageSync('downloadPath', payload);
    },
    setDownloadClient({ commit }, payload) {
      commit('setDownloadClient', payload);
      storage.setStorageSync('downloaded', payload);
    },
    setAuthorized({ commit }, payload) {
      storage.setStorageSync('isAuthorized', payload);
      commit('setAuthorized', payload);
    },
    setUser({ commit }, payload) {
      storage.setStorageSync('user', payload);
      commit('setUser', payload);
    },
    setTicketMulti({ commit }, payload) {
      commit('setTicketMulti', payload);
    },
    logoutUser({ commit }) {
      return new Promise((resolve) => {
        commit('setAuthorized', false);
        commit('setUser', {});
        commit('setToken', null);
        if (storage.hasKey('isAuthorized')) {
          storage.removeStorage({ key: 'isAuthorized' }).then(async () => {
            if (storage.hasKey('user')) await storage.removeStorage({ key: 'user' });
            if (storage.hasKey('clientParams'))
              await storage.removeStorage({ key: 'clientParams' });
            if (storage.hasKey('userBase')) await storage.removeStorage({ key: 'userBase' });
            if (storage.hasKey('token')) await storage.removeStorage({ key: 'token' });
          });
        }
        resolve();
      });
    },
  },
  modules: {},
});
