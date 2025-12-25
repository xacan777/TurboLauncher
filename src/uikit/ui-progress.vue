<template lang="pug">
.progress(v-tippy=`{
  content: notifyTippy,
  zIndex: 99999999999,
  placement: 'bottom' }`)
  .progress-fill(:style="{ width: progress }")
</template>

<script>
export default {
  name: 'UiProgress',
  props: {
    finalValue: {
      type: Number,
      default: 0,
    },
    currentValue: {
      type: Number,
      default: 0,
    },
    notifyTippy: {
      type: String,
      default: '',
    },
  },
  computed: {
    progress() {
      return `${(this.currentValue / this.finalValue) * 100}%`;
    },
  },
};
</script>

<style lang="scss" scoped>
.progress {
  min-width: 225px;
  height: 10px;
  background: #e7e7e7;
  border-radius: 4px;
  cursor: pointer;

  &-fill {
    display: block;
    height: 100%;
    width: 0%;
    transition: width 0.2s ease;
    // background: #FFC107;
    background-image: linear-gradient(90deg, #ffce3c 0px, #ffc107 40px, #ffd559 80px);
    border-radius: 4px;
    animation: shine-lines 2s infinite linear;
  }
}

@keyframes shine-lines {
  0% {
    background-position: -100px;
  }

  100% {
    background-position: 140px;
  }
}
</style>
