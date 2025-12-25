import { createApp } from 'vue';
import { ipcRenderer } from 'electron';
import { Axios } from 'axios';
import VueAxios from 'vue-axios';
import VueTippy from 'vue-tippy';
import Notifications, { notify } from '@kyvg/vue3-notification';
import Vue3Storage from 'vue3-storage';
import moment from 'moment';
import App from './App.vue';
import router from './router';
import store from './store';
import { storageConfig } from './config/storage.config';
// import DownloadManager from './downloader';

// eslint-disable-next-line import/no-extraneous-dependencies
import 'tippy.js/dist/tippy.css';
// eslint-disable-next-line import/no-extraneous-dependencies
import 'tippy.js/animations/perspective.css';

const appVue = createApp(App);
appVue.config.globalProperties.$ipc = ipcRenderer;

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

const api = new Axios({
  // baseURL: 'https://nulled-world.com/api',
  // baseURL: '',
  // baseURL: 'http://91.149.202.99/hak612bdasd781b2fasf',
  baseURL: 'https://pay.r2legacy.com/hak612bdasd781b2fasf',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const newConf = { ...config };
  const item = {
    secret_key: 'tKUK3E9KSEgZp2qrfGzQ4gxq3Aj5WSDj',
  };

  if (config.method === 'get') {
    newConf.params = {
      ...newConf.params,
      ...item,
    };
  } else {
    newConf.data = JSON.stringify({
      ...newConf.data,
      ...item,
    });
  }

  return newConf;
});
api.interceptors.response.use(
  (response) => {
    const data = JSON.parse(response.data);
    // if (
    //   (typeof data.success !== 'undefined' && !data.success) ||
    //   (typeof data.status !== 'undefined' && !data.status)
    // ) {
    //   const responseError = typeof data.error !== 'undefined' ? data.error : data.message;
    //   console.log(responseError);
    //   notify({
    //     type: 'error',
    //     group: 'main',
    //     text: responseError,
    //   });
    //   return Promise.reject(responseError);
    // }
    if (typeof data.error !== 'undefined') {
      const responseError = typeof data.error !== 'undefined' ? data.error : data.message;
      notify({
        type: 'error',
        group: 'main',
        text: responseError,
      });
      return Promise.reject(responseError);
    }
    console.log('sdlkfsdlkfjsdfjlkds', data);
    return data;
  },
  (error) => Promise.reject(error)
);

moment.locale('ru');
appVue.config.globalProperties.$moment = moment;
appVue.config.globalProperties.$filters = {
  dateFromNow: (date) => moment(date).fromNow(),
};
appVue.use(VueAxios, api);
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
  // appVue.config.globalProperties.$downloadManager = new DownloadManager({
  //   path: store.getters.download.path,
  // });
  appVue.use(store).use(router).mount('#app');
});
