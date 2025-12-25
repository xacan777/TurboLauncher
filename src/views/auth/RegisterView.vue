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
  UiInput.field-20(
    v-model="form.email"
    type="email"
    placeholder="Почта"
    :is-error="isError(v$.form.email)"
    @update:modelValue="setTouchValidator(v$.form.email)"
  )
    template(#icon)
      icon-mail
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
import { email, required, sameAs } from '@vuelidate/validators';
import validationMixin from '@/mixins/validation-mixin';
import IconMail from '@/assets/icons/icon-mail.vue';

export default {
  name: 'RegisterView',
  mixins: [validationMixin],
  components: {
    IconMail,
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
      email: '',
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
        email: {
          required,
          email,
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
    onAuth() {
      this.formLoading = true;
      this.$http
        .get('createAccount.php', {
          params: {
            login: this.form.account,
            mail: this.form.email,
            password: this.form.password,
          },
        })
        .then(() => {
          this.$notify({
            group: 'main',
            type: 'success',
            text: 'Вы успешно зарегистрировались, авторизуйтесь под своим логином',
          });
          this.$router.push({ name: 'login' });
        })
        .finally(() => {
          this.formLoading = false;
        });
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
