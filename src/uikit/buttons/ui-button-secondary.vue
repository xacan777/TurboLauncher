<template lang="pug">
UiButtonPrimary.ui-button-secondary(
  :class="{ 'outline': outline }"
  v-bind="$attrs"
  v-on="$listeners")
  slot
</template>

<script>
import UiButtonPrimary from '@/uikit/buttons/ui-button-primary.vue';

export default {
  name: 'ui-button-secondary',
  props: {
    outline: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    UiButtonPrimary,
  },
};
</script>

<style lang="scss" scoped>
.ui-button-secondary {
  background-color: #9146ff;
  border: 1px solid #9146ff;
  color: #fff;

  &.outline {
    background-color: transparent;
    border: 1px solid #be95fa;
    color: #be95fa;

    &:hover {
      background-color: #9146ff;
      color: #fff;
    }
  }

  &:hover {
    background-color: #7a3bff !important;
  }
}
</style>
