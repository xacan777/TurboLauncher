<template lang="pug">
.login
  UiInput.field-20(
    v-model="form.account"
    type="text"
    placeholder="Аккаунт"
    :is-error="isError(v$.form.account)"
    @update:modelValue="setTouchValidator(v$.form.account)"
  )
    template(#icon)
      icon-user
  UiInput.field-30(
    v-model="form.password"
    type="password"
    placeholder="Пароль"
    :is-error="isError(v$.form.password)"
    @update:modelValue="setTouchValidator(v$.form.password)"
  )
    template(#icon)
      icon-lock
  UiButtonPrimary.field-30(
    :disabled="v$.form.$invalid"
    :loading="formLoading"
    @click="onAuth"
  ) Войти
  UiLink.field-30(:to="{ name: 'forgot' }") Восстановление пароля
</template>

<script>
import UiInput from '@/uikit/inputs/ui-input.vue';
import IconUser from '@/assets/icons/icon-user.vue';
import IconLock from '@/assets/icons/icon-lock.vue';
import UiButtonPrimary from '@/uikit/buttons/ui-button-primary.vue';
import UiLink from '@/uikit/ui-link.vue';
import { required } from '@vuelidate/validators';
import validationMixin from '@/mixins/validation-mixin';
import { mapActions } from 'vuex';
import { ipcRenderer } from 'electron';

export default {
  name: 'LoginView',
  mixins: [validationMixin],
  components: {
    UiLink,
    UiButtonPrimary,
    IconLock,
    IconUser,
    UiInput,
  },
  data: () => ({
    formLoading: false,
    form: {
      account: '',
      password: '',
    },
  }),
  validations() {
    return {
      form: {
        account: {
          required,
        },
        password: {
          required,
        },
      },
    };
  },
  mounted() {
    // eslint-disable-next-line no-unused-vars
    ipcRenderer.on('auth-response', (event, { success, data }) => {
      if (success) {
        this.$http
          .get('getUserInfo.php', {
            params: {
              do_user_info: '',
              email: this.form.account,
            },
          })
          .then((dataResponse) => {
            this.setIsClientReady(true);
            this.setIsAfterAuthorized(true);
            this.setAuthorized(true);
            this.setUser(dataResponse);
            this.setUserBase({
              login: this.form.account,
              password: this.form.password,
            });
            this.setClientParams({
              param1: `${dataResponse.mUserId.trim()}|${data.param1}`,
              param2: data.param2,
            });

            this.$appEvent('mainFrame');
          });
      } else {
        this.$notify({
          title: 'Ошибка авторизации',
          group: 'main',
          text: data,
          type: 'error',
        });
      }

      this.formLoading = false;
    });
  },
  methods: {
    ...mapActions([
      'setAuthorized',
      'setUser',
      'setUserBase',
      'setIsClientReady',
      'setClientParams',
      'setIsAfterAuthorized',
    ]),
    onAuth() {
      if (this.formLoading) return;

      this.formLoading = true;
      ipcRenderer.send('auth', {
        login: this.form.account,
        password: this.form.password,
      });

      // this.$http
      //   .post('auth', {
      //     mUserId: this.form.account,
      //     password: this.form.password,
      //   })
      //   .then(({ user }) => {
      //     this.setAuthorized(true);
      //     this.setUser(user);
      //     this.$appEvent('mainFrame');
      //   })
      //   .catch((error) => {
      //     console.log(error);
      //   })
      //   .finally(() => {
      //     this.formLoading = false;
      //   });
    },
  },
};
</script>

<style lang="scss" scoped>
.login {
  display: flex;
  flex-direction: column;
  align-items: center;

  .field {
    &-20 {
      margin-bottom: 20px;
    }

    &-30 {
      margin-bottom: 30px;
    }
  }
}
</style>
