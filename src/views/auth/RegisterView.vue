<template lang="pug">
.login
  h2 Создание TURBO аккаунта
  p.login-subtitle Используйте один логин для лаунчера и форума.
  UiInput.field-20(
    v-model="form.account"
    type="text"
    placeholder="Логин"
    :is-error="isError(v$.form.account)"
    @update:modelValue="setTouchValidator(v$.form.account)"
  )
    template(#icon)
      icon-user
  UiInput.field-20(
    v-model="form.password"
    type="password"
    placeholder="Пароль"
    :is-error="isError(v$.form.password)"
    @update:modelValue="setTouchValidator(v$.form.password)"
  )
    template(#icon)
      icon-lock
  UiInput.field-30(
    v-model="form.passwordRetry"
    type="password"
    placeholder="Повторение пароля"
    :is-error="isError(v$.form.passwordRetry)"
    @update:modelValue="setTouchValidator(v$.form.passwordRetry)"
  )
    template(#icon)
      icon-lock
  UiButtonPrimary.field-30(
    :disabled="v$.form.$invalid"
    :loading="formLoading"
    @click="onAuth"
  ) Создать аккаунт
  UiLink.field-30(:to="{ name: 'forgot' }") Восстановление пароля
</template>

<script>
import UiInput from '@/uikit/inputs/ui-input.vue';
import IconUser from '@/assets/icons/icon-user.vue';
import IconLock from '@/assets/icons/icon-lock.vue';
import UiButtonPrimary from '@/uikit/buttons/ui-button-primary.vue';
import UiLink from '@/uikit/ui-link.vue';
import { required, sameAs } from '@vuelidate/validators';
import validationMixin from '@/mixins/validation-mixin';
import { mapActions } from 'vuex';

export default {
  name: 'RegisterView',
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
      passwordRetry: '',
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
        passwordRetry: {
          required,
          sameAsPassword: sameAs(this.form.password),
        },
      },
    };
  },
  methods: {
    ...mapActions(['register']),
    async onAuth() {
      this.formLoading = true;
      try {
        await this.register({
          username: this.form.account,
          password: this.form.password,
        });
        this.$notify({
          group: 'main',
          type: 'success',
          text: 'Вы успешно зарегистрировались, авторизуйтесь под своим логином',
        });
        this.$router.push({ name: 'login' });
      } catch (error) {
        this.$notify({
          group: 'main',
          type: 'error',
          text: error.message,
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
