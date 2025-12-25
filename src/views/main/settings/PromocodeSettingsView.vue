<template lang="pug">
div
  .page-title Промокоды
  .page-content.content
    .form
      .form-content
        .form-field
          UiInput(
            v-model="form.promocode"
            label="Промокод"
            placeholder="XXXX-XXXX-XXXX-XXXX"
          )
            template(#icon)
              IconLock
        UiButtonPrimary(
          @click="addPromocode"
          :disabled="!form.promocode.length"
          :loading="formLoading"
        ) Использовать
    .info
      .info-title Как получить промокод?
      .info-description Получить промокоды можно несколько способами:
      ol.info-list
        li Выигрывать в игре на событиях от администрации
        li Получить бонус при пополнении счета на определенную сумму.
        li Купить некоторые промокоды можно в магазине.
</template>

<script>
import UiInput from '@/uikit/inputs/ui-input.vue';
import UiButtonPrimary from '@/uikit/buttons/ui-button-primary.vue';
import IconLock from '@/assets/icons/icon-lock.vue';

export default {
  name: 'PromocodeSettingsView',
  components: {
    UiInput,
    UiButtonPrimary,
    IconLock,
  },
  data: () => ({
    formLoading: false,
    form: {
      promocode: '',
    },
  }),
  methods: {
    addPromocode() {
      if (this.formLoading || this.form.promocode.length === 0) return;
      this.formLoading = true;
      this.$http
        .get('promocodeActions.php', {
          params: {
            action: 'activation',
            user_id: this.$store.getters.user.mUserId,
            code: this.form.promocode,
          },
        })
        .then(() => {
          this.form.promocode = '';
          this.$notify({
            type: 'success',
            group: 'main',
            title: 'Промокод активирован',
            text: 'Промокод успешно активирован',
          });
          this.$store.dispatch('fetchBalanceUser');
        })
        .catch(() => {
          this.formLoading = false;
        })
        .finally(() => {
          setTimeout(() => {
            this.formLoading = false;
          }, 1000);
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.content {
  display: flex;
}

.form {
  margin-right: 40px;
  background: rgba(28, 28, 45, 0.9);
  border-radius: 4px;
  padding: 40px;
  box-sizing: border-box;

  &-field {
    margin-bottom: 40px;
  }

  &-content {
    width: 100%;
    min-width: 200px;
    max-width: 200px;
  }
}

.info {
  &-title {
    font-family: 'Gilroy';
    font-style: normal;
    font-weight: 600;
    font-size: 16px;
    line-height: 20px;
    color: #ffffff;
    margin-bottom: 20px;
  }

  &-description {
    font-family: 'Gilroy';
    font-style: normal;
    font-weight: 400;
    font-size: 14px;
    line-height: 160%;
    color: #ffffff;
    margin-bottom: 27px;
  }

  &-list {
    margin: 0;
    padding: 0;
    list-style-position: inside;

    & li {
      font-family: 'Gilroy';
      font-style: normal;
      font-weight: 400;
      font-size: 14px;
      line-height: 160%;
      margin-bottom: 10px;
    }
  }
}
</style>
