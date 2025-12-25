<template lang="pug">
.ui-input
  .ui-input-icon(@click="setFocus(true)" :class="{'error': isError}")
    slot(name="icon")
  .ui-input-action(
    v-if="type === 'password'"
    @click="showAction = !showAction")
    template(v-if="!showAction")
      icon-eye
    template(v-else)
      icon-eye-slash
  .ui-input-field(:class="{ 'active': isFocus, 'error': isError }")
    textarea(
      ref="input"
      :type="typeInput"
      v-bind="{ placeholder }"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      @focus="isFocus = true"
      @blur="isFocus = false"
    )
</template>

<script>
import IconEye from '@/assets/icons/icon-eye.vue';
import IconEyeSlash from '@/assets/icons/icon-eye-slash.vue';

export default {
  name: 'ui-textarea',
  components: { IconEyeSlash, IconEye },
  props: {
    type: {
      type: String,
      default: 'text',
    },
    placeholder: {
      type: String,
      default: '',
    },
    modelValue: {
      type: String,
      default: '',
    },
    isError: {
      type: Boolean,
      default: false,
    },
  },
  data: () => ({
    isFocus: false,
    showAction: false,
  }),
  methods: {
    setFocus(state) {
      if (state) {
        this.$refs.input.focus();
      } else {
        this.$refs.input.blur();
      }
    },
  },
  computed: {
    typeInput() {
      if (this.type === 'password') {
        return this.showAction ? 'text' : 'password';
      }

      return this.type;
    },
  },
};
</script>

<style lang="scss" scoped>
.ui-input {
  position: relative;
  width: 100%;
  user-select: none;

  &-icon {
    position: absolute;
    top: 7px;
    left: 0;
    transform: translateY(-50%);
    color: #4e4e72;
    cursor: text;

    &.error {
      color: #ff0000 !important;
    }
  }

  &-action {
    position: absolute;
    top: 50%;
    right: 0;
    transform: translateY(-50%);
    color: #4e4e72;
    cursor: pointer;
  }

  &-field {
    width: 100%;

    textarea {
      background: transparent;
      width: 100%;
      height: 89px;
      padding: 0 26px;
      border: 0;
      border-bottom: 1px solid #4e4e72;
      outline: none;
      transition: all 0.2s ease;
      resize: none;

      font-style: normal;
      font-weight: 600;
      font-size: 12px;
      color: #ffffff;

      &::placeholder {
        color: #4e4e72;
        opacity: 1;
        transition: all 0.3s ease;
      }

      &:focus {
        color: #fff;
      }

      &:focus::placeholder {
        opacity: 0;
        transform: scaleX(0);
      }
    }

    &.error textarea::placeholder {
      color: #ff0000;
    }

    &.error::before {
      transform: scaleX(1);
      background: #ff0000;
    }

    &.active::before {
      transform: scaleX(1);
    }

    &::before {
      content: ' ';
      display: block;
      position: absolute;
      left: 0;
      right: 0;
      bottom: 5px;
      width: 100%;
      height: 1px;
      background: #8888b3;
      transform: scaleX(0);
      transition: all 0.3s ease;
      z-index: 99;
    }
  }
}
</style>
