<template lang="pug">
div
  .page-title Сменить пароль
  .page-content.wrapper
    .form-input
      UiInput(
        v-model="form.oldPassword"
        type="password"
        placeholder="Старый пароль"
        :is-error="isError(v$.form.oldPassword)"
        @update:modelValue="setTouchValidator(v$.form.oldPassword)"
      )
        template(#icon)
          IconLock
    .form-input
      UiInput(
        v-model="form.newPassword"
        type="password"
        placeholder="Новый пароль"
        :is-error="isError(v$.form.newPassword)"
        @update:modelValue="setTouchValidator(v$.form.newPassword)"
      )
        template(#icon)
          IconLock
    .form-input
      UiInput(
        v-model="form.newPasswordRepeat"
        type="password"
        placeholder="Повторение пароля"
        :is-error="isError(v$.form.newPasswordRepeat)"
        @update:modelValue="setTouchValidator(v$.form.newPasswordRepeat)"
      )
        template(#icon)
          IconLock
    .form-input.footer
      UiButtonPrimary(
        :loading="formLoading"
        :disabled="v$.$invalid"
        @click="onChangePassword"
      ) Изменить пароль

</template>

<script>
import UiInput from '@/uikit/inputs/ui-input.vue';
import IconLock from '@/assets/icons/icon-lock.vue';
import UiButtonPrimary from '@/uikit/buttons/ui-button-primary.vue';
import validationMixin from '@/mixins/validation-mixin';
import { required, sameAs } from '@vuelidate/validators';

export default {
  name: 'GeneralSettingsView',
  mixins: [validationMixin],
  components: {
    UiInput,
    IconLock,
    UiButtonPrimary,
  },
  data: () => ({
    formLoading: false,
    form: {
      oldPassword: '',
      newPassword: '',
      newPasswordRepeat: '',
    },
  }),
  validations() {
    return {
      form: {
        oldPassword: {
          required,
        },
        newPassword: {
          required,
        },
        newPasswordRepeat: {
          sameAs: sameAs(this.form.newPassword),
        },
      },
    };
  },
  methods: {
    async onChangePassword() {
      if (this.formLoading || this.v$.$invalid) return;
      this.formLoading = true;

      // eslint-disable-next-line consistent-return
      await Promise((r) => setTimeout(r, 1000));
      this.$notify({
        type: 'success',
        group: 'main',
        title: 'Пароль успешно изменен',
      });
      this.form.oldPassword = '';
      this.form.newPassword = '';
      this.form.newPasswordRepeat = '';
      this.formLoading = false;
    },
  },
};
</script>

<style lang="scss" scoped>
.wrapper {
  width: 100%;
  max-width: 600px;
}

.form-input {
  margin-bottom: 20px;

  &:last-child {
    margin-bottom: 0;
  }
}

.footer {
  max-width: 160px;
}
</style>
