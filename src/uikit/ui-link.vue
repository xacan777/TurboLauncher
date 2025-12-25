<template lang="pug">
.ui-link
  a(:href="href" :target="target" v-if="href")
    slot
  router-link(:to="to" tag="a" v-else)
    slot
</template>

<script>
export default {
  name: 'ui-link',
  props: {
    href: {
      type: String,
      default: '',
    },
    target: {
      type: String,
      default: '_self',
    },
    to: {
      type: Object,
      default: null,
    },
  },
};
</script>

<style lang="scss" scoped>
.ui-link {
  font-style: normal;
  font-weight: 600;
  font-size: 12px;

  a {
    transition: all 0.2s ease;
    color: #ffffff;
    text-decoration: none;
    &:hover {
      color: #ececec;
    }
  }
}
</style>
