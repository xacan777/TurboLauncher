<template lang="pug">
.login
  h2 TURBO аккаунт
  p.login-subtitle Войдите, чтобы получить доступ к базе данных и форуму.
  UiInput.field-20(
    v-model="form.account"
    type="text"
    placeholder="Логин"
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
  methods: {
    ...mapActions([
      'login',
      'setUserBase',
    ]),
    async onAuth() {
      if (this.formLoading) return;
      this.formLoading = true;
      try {
        await this.login({
          username: this.form.account,
          password: this.form.password,
        });
        this.setUserBase({
          login: this.form.account,
          password: this.form.password,
        });
        this.$router.push({ name: 'home' });
        this.$appEvent('mainFrame');
      } catch (error) {
        this.$notify({
          title: 'Ошибка авторизации',
          group: 'main',
          text: error.message,
          type: 'error',
        });
      } finally {
        this.formLoading = false;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.login {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;

  .login-subtitle {
    color: #9da3c5;
    margin-bottom: 18px;
  }

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
