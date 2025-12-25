<template lang="pug">
div
  .page-title Создать обращение
  .page-content.wrapper
    .field
      UiInput(placeholder="Тема" v-model="form.subject")
        template(#icon)
          IconMail
    .field-2
      UiSelect(
        placeholder="Выберите категорию"
        v-model="form.category"
        :items="categories")
          template(#icon)
            IconLock
    .field
      UiTextarea(placeholder="Сообщение" v-model="form.message")
        template(#icon)
          IconLock
    .field.footer
      UiButtonPrimary(
        type="submit"
        :disabled="v$.$invalid"
        :loading="formLoading"
        @click="createTicket"
      ) Создать обращение
</template>

<script>
import UiInput from '@/uikit/inputs/ui-input.vue';
import UiSelect from '@/uikit/inputs/ui-select.vue';
import UiTextarea from '@/uikit/inputs/ui-textarea.vue';
import UiButtonPrimary from '@/uikit/buttons/ui-button-primary.vue';

import IconMail from '@/assets/icons/icon-mail.vue';
import IconLock from '@/assets/icons/icon-lock.vue';
import validationMixin from '@/mixins/validation-mixin';

import { required } from '@vuelidate/validators';

export default {
  name: 'SupportActionView',
  mixins: [validationMixin],
  components: {
    UiInput,
    UiSelect,
    UiTextarea,
    UiButtonPrimary,
    IconMail,
    IconLock,
  },
  data: () => ({
    formLoading: false,
    form: {
      subject: '',
      category: '',
      message: '',
    },
    categories: [],
  }),
  validations: {
    form: {
      subject: {
        required,
      },
      category: {
        required,
      },
      message: {
        required,
      },
    },
  },
  mounted() {
    this.fetchCategories();
  },
  methods: {
    fetchCategories() {
      this.$http.get('support/getCategories').then(({ success, categories }) => {
        if (success) {
          this.categories = categories.map((item) => ({
            value: item.id,
            text: item.name,
          }));
        }
      });
    },
    createTicket() {
      if (this.v$.$invalid || this.formLoading) return;
      this.formLoading = true;
      this.$http
        .post('support/createTicket', {
          mUserId: this.$store.getters.user.mUserId,
          ticket: {
            subject: this.form.subject,
            categoryId: parseInt(this.form.category, 10),
            message: this.form.message,
          },
        })
        .then(({ success, ticket }) => {
          if (success) {
            this.$router.push({ name: 'support-info', params: { id: ticket.id } });
            this.$notify({
              type: 'success',
              title: 'Успешно',
              group: 'main',
              text: 'Обращение успешно создано',
            });
          }
        })
        .finally(() => {
          this.formLoading = false;
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.wrapper {
  max-width: 600px;
}

.field {
  margin-bottom: 25px;
}

.field-2 {
  margin-bottom: 40px;
}

.footer {
  max-width: 200px;
}
</style>
