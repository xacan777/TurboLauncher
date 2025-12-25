<template lang="pug">
.login
  UiInput.field-20(
    v-model="form.email"
    type="email"
    placeholder="Почта"
    :is-error="isError(v$.form.email)"
    @update:modelValue="setTouchValidator(v$.form.email)"
  )
    template(#icon)
      icon-mail
  UiButtonPrimary(
    :disabled="v$.form.$invalid"
    :loading="formLoading"
    @click="onAuth"
  ) Восстановить пароль
</template>

<script>
import UiInput from '@/uikit/inputs/ui-input.vue';
import IconUser from '@/assets/icons/icon-user.vue';
import IconLock from '@/assets/icons/icon-lock.vue';
import UiButtonPrimary from '@/uikit/buttons/ui-button-primary.vue';
import UiLink from '@/uikit/ui-link.vue';
import { email, required } from '@vuelidate/validators';
import validationMixin from '@/mixins/validation-mixin';
import IconMail from '@/assets/icons/icon-mail.vue';

export default {
  name: 'ForgotView',
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
      email: '',
    },
  }),
  validations() {
    return {
      form: {
        email: {
          required,
          email,
        },
      },
    };
  },
  methods: {
    onAuth() {},
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
