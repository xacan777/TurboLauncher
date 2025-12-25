<template lang="pug">
UiModal(
  :width="200"
  :with-close="false"
)
  template(#content)
    p Вы уверенны, что хотите выйти из аккаунта?
  template(#footer)
    .footer
      UiButtonSecondary(
        @click="$emit('close')"
        size="small"
        type="button"
      ) Да, выйти
      UiButtonPrimary(
        @click="setState(false)"
        size="small"
        type="button"
      ) Отмена
</template>

<script>
import UiButtonPrimary from '@/uikit/buttons/ui-button-primary.vue';
import UiButtonSecondary from '@/uikit/buttons/ui-button-secondary.vue';
import UiModal from '@/uikit/ui-modal.vue';

export default {
  name: 'ConfirmLogoutUser',
  data: () => ({
    isShow: false,
  }),
  $emits: ['close', 'update:state'],
  methods: {
    setState(state) {
      this.$emit('update:state', state);
    },
  },
  components: { UiModal, UiButtonPrimary, UiButtonSecondary },
};
</script>

<style lang="scss" scoped>
p {
  font-size: 14px;
  line-height: 1.5;
  text-align: center;
}

.footer {
  width: 100%;
  display: flex;

  & > * {
    margin-right: 10px;

    &:last-child {
      margin-right: 0;
    }
  }
}
</style>
