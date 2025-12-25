import { createApp } from 'vue';
import { ipcRenderer } from 'electron';
import VueTippy from 'vue-tippy';
import Notifications, { notify } from '@kyvg/vue3-notification';
import Vue3Storage from 'vue3-storage';
import moment from 'moment';
import App from './App.vue';
import router from './router';
import store from './store';
import { storageConfig } from './config/storage.config';
import apiClient from './services/api';
// eslint-disable-next-line import/no-extraneous-dependencies
import 'tippy.js/dist/tippy.css';
// eslint-disable-next-line import/no-extraneous-dependencies
import 'tippy.js/animations/perspective.css';

const appVue = createApp(App);
appVue.config.globalProperties.$ipc = ipcRenderer;
appVue.config.globalProperties.$api = apiClient;
appVue.config.globalProperties.$notifyError = (message) =>
  notify({
    type: 'error',
    group: 'main',
    text: message,
  });

const appEvent = (command, data, callback = null) => {
  ipcRenderer.send('app-event', {
    command,
    data,
    callback,
  });
};

appVue.config.globalProperties.$appEvent = appEvent;
appVue.use(Vue3Storage, {
  namespace: storageConfig.namespaced,
});
appVue.use(Notifications);

moment.locale('ru');
appVue.config.globalProperties.$moment = moment;
appVue.config.globalProperties.$filters = {
  dateFromNow: (date) => moment(date).fromNow(),
};
appVue.use(VueTippy, {
  directive: 'tippy', // => v-tippy
  component: 'tippy', // => <tippy/>
  componentSingleton: 'tippy-singleton', // => <tippy-singleton/>,
  defaultProps: {
    animation: 'perspective',
    placement: 'bottom',
    allowHTML: true,
  }, // => Global default options * see all props
});

store.$app = appVue;

store.dispatch('initApp').then(() => {
  appVue.use(store).use(router).mount('#app');
});
