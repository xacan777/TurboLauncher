<template lang="pug">
div
  .page-title Пополнение баланса
  .page-content.content
    .form
      .form-content
        .form-field
          UiInput(
            type="number"
            v-model="form.sum"
            placeholder="Сумма баланса"
          )
            template(#icon)
              IconLock
        .form-field.methods
          .badge(
            v-for="badge in methods"
            :key="badge.id"
            @click="form.method = badge.id"
            :class="{'active': badge.id === form.method}")
            .badge-text {{ badge.name }}
        UiButtonPrimary(
          @click="createPayment()"
          :disabled="v$.$invalid"
          :loading="formLoading"
        ) Пополнить
      .form-text.text-success(v-if="isSendPayment") Запрос на пополнение создан.
    .info
      .info-payment(v-for="(payment, index) in bonuses" :key="index")
        .info-payment-left
          .info-payment-left-title Купить
          .info-payment-left-text {{ payment.monet }} монет ({{ payment.sum }} рублей)
        .info-payment-right
          UiButtonPrimary(
            size="small"
            @click="createPayment(payment.sum)"
            :disabled="formLoading"
          ) Пополнить

</template>

<script>
import UiInput from '@/uikit/inputs/ui-input.vue';
import UiButtonPrimary from '@/uikit/buttons/ui-button-primary.vue';
import IconLock from '@/assets/icons/icon-lock.vue';
import validationMixin from '@/mixins/validation-mixin';

import { required, numeric } from '@vuelidate/validators';

export default {
  name: 'PaymentSettingsView',
  mixins: [validationMixin],
  components: {
    UiInput,
    UiButtonPrimary,
    IconLock,
  },
  data: () => ({
    isSendPayment: false,
    methods: [
      {
        id: 'ps1',
        name: 'FreeKassa',
      },
      {
        id: 'qiwi',
        name: 'QIWI',
      },
    ],
    bonuses: [
      { monet: 100, sum: 25 },
      { monet: 200, sum: 50 },
      { monet: 300, sum: 100 },
      { monet: 400, sum: 250 },
      { monet: 500, sum: 1000 },
      { monet: 600, sum: 5000 },
    ],
    formLoading: false,
    form: {
      sum: 100,
      method: 'ps1',
    },
  }),
  validations: {
    form: {
      sum: {
        required,
        numeric,
      },
      method: {
        required,
      },
    },
  },
  methods: {
    createPayment(sum = 0) {
      if (this.formLoading || (sum ? !sum : this.v$.$invalid)) return;
      this.formLoading = true;
      this.$http
        .post('generatePaymentUri', {
          mUserId: this.$store.getters.user.mUserId,
          mEmail: this.$store.getters.user.mEmail,
          payment: this.form.method,
          sum: sum || this.form.sum,
        })
        .then((data) => {
          if (data.success) {
            this.form.sum = 100;
            this.$notify({
              type: 'success',
              group: 'main',
              title: 'Заказ создан',
              text: 'Сейчас вы будете перенаправлены на страницу оплаты',
            });
            this.isSendPayment = true;
            const uri = typeof data.uri === 'undefined' ? data[0] : data.uri;
            setTimeout(() => {
              const win = window.open(
                uri,
                '_blank',
                `toolbar=1, scrollbars=1, resizable=1, frame=true, nodeIntegration=no, width=${1015}, height=${800}`
              );
              const timer = setInterval(() => {
                if (win.closed) {
                  this.$router.push({ name: 'main' });
                  clearInterval(timer);
                }
              }, 1000);
            }, 2000);
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
.content {
  display: flex;
  align-items: flex-start;
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

  &-text {
    margin-top: 25px;
    line-height: 25px;
  }
}

.info {
  width: 100%;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;

  &-payment {
    border: 2px solid #606085;
    border-radius: 4px;
    height: 94px;
    padding: 0 10px;
    box-sizing: border-box;

    display: flex;
    align-items: center;
    justify-content: space-between;

    &-left {
      display: flex;
      flex-direction: column;
      justify-content: space-evenly;
      height: 100%;

      &-title {
        font-weight: 700;
        font-size: 14px;
        line-height: 17px;
        color: #8585a9;
      }

      &-text {
        font-weight: 700;
        font-size: 12px;
        color: #ffffff;
        white-space: nowrap;
      }
    }
  }
}

.methods {
  display: flex;
  align-items: center;
}

.badge {
  margin-right: 15px;

  padding: 5px 10px;

  &.active {
    background: #606085;
    cursor: default;
  }

  background: #1877f2;
  border-radius: 4px;
  cursor: pointer;

  &:not(.active):hover {
    background: #2f81ed;
  }

  &:last-child {
    margin-right: 0;
  }
}
</style>
