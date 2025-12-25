<template lang="pug">
button.ui-button-default(
  :class="[classes, size, { 'loader': loading }]"
  :disabled="disabled")
  .default(ref="simple")
    slot
  .loader(ref="loader")
    .loader-icon
      IconSpinner

</template>

<script>
import IconSpinner from '@/assets/icons/icon-spinner.vue';
import gsap from 'gsap';

export default {
  name: 'ui-button-primary',
  components: { IconSpinner },
  props: {
    loading: {
      type: Boolean,
      default: false,
    },
    text: {
      type: String,
      default: 'Button',
    },
    classes: {
      type: String,
      default: '',
    },
    size: {
      type: String,
      default: '',
    },
  },
  watch: {
    loading(state) {
      this.setAnimation(state);
    },
  },
  computed: {
    disabled() {
      const { disabled } = this.$attrs;
      if (this.loading) {
        return true;
      }
      return disabled;
    },
  },
  methods: {
    setAnimation(state) {
      const { simple, loader } = this.$refs;
      gsap.killTweensOf([simple, loader]);
      const tl = gsap.timeline({ paused: true });
      if (state) {
        tl.to(simple, {
          ease: 'power1.out',
          duration: 0.4,
          opacity: 0,
          display: 'none',
          marginRight: 50,
        }).to(loader, {
          ease: 'power1.out',
          duration: 0.4,
          opacity: 1,
          display: 'flex',
          marginRight: 0,
        });
      } else {
        tl.to(loader, {
          ease: 'power1.out',
          duration: 0.4,
          opacity: 0,
          display: 'none',
          marginRight: 50,
        }).to(simple, {
          ease: 'power1.out',
          duration: 0.4,
          opacity: 1,
          display: 'flex',
          marginRight: 0,
        });
      }
      tl.play();
    },
  },
};
</script>

<style lang="scss" scoped>
.ui-button-default {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 20px;
  height: 42px;
  color: #fff;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #ff7002;
  border-radius: 4px;

  font-style: normal;
  font-weight: 700;
  font-size: 14px;

  &.small {
    height: 28px;
    font-size: 12px;
    padding: 0 10px;
  }

  &.loader {
    cursor: wait;
  }

  &:not(.loader):not(:disabled):hover {
    background-color: #f4822c;
  }

  &:active {
    background-color: #e16f20;
  }

  &:disabled {
    background: #292935;
    color: #5c5c69;
    cursor: not-allowed;
  }

  .loader {
    display: none;
    margin-right: 50px;

    &-icon {
      width: 15px;
      height: 15px;
      display: flex;
      align-items: center;
      justify-content: center;
      animation-name: spin;
      animation-duration: 2000ms;
      animation-iteration-count: infinite;
      animation-timing-function: linear;
      color: #fff;
    }
  }
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  70% {
    transform: rotate(200deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style>
