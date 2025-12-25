import { ipcRenderer } from 'electron';
import { mapActions, mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['userBase', 'user']),
  },
  methods: {
    ...mapActions(['logoutUser', 'setClientParams', 'logoutUser', 'setIsClientReady']),
    sliceLength(value, length = 20) {
      return value.length > length ? `${value.slice(0, length)}...` : value;
    },
    onReauthForGenerationToken() {
      return new Promise((resolve, reject) => {
        console.log('ON START AUTH MECH!');
        this.setIsClientReady(false);
        console.log(this.userBase);
        ipcRenderer.send('auth', {
          login: this.userBase.login,
          password: this.userBase.password,
        });

        // eslint-disable-next-line no-unused-vars
        ipcRenderer.on('auth-response', (event, { success, data }) => {
          if (success) {
            console.log('success', success);
            console.log('data', data);
            this.setIsClientReady(true);
            this.setClientParams({
              param1: `${this.user.mUserId.trim()}|${data.param1}`,
              param2: data.param2,
            });
            resolve(true);
          } else {
            this.logoutUser();
            this.$notify({
              title: 'Сессия истекла',
              group: 'main',
              text: 'Вам необходимо повторно авторизоваться...',
              type: 'error',
            });
            this.$appEvent('authFrame', {});
            reject();
          }
        });
      });
    },
  },
};
