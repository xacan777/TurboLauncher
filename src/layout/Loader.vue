<template lang="pug">
.loader
  .loader__content
    .loader__icon
      IconSpinner
    .loader__text Идет загрузка...
    .loader__logo
      img(src="@/assets/images/logo.png" srcset="@/assets/images/logo@2x.png 2x")
</template>

<script>
import IconSpinner from '@/assets/icons/icon-spinner.vue';
import { mapGetters } from 'vuex';

export default {
  name: 'LoaderLayout',
  components: { IconSpinner },
  computed: {
    ...mapGetters(['isAuthorized']),
  },
  mounted() {
    if (this.isAuthorized) {
      this.$appEvent('mainFrame', {});
    } else {
      this.$appEvent('authFrame', {});
    }
  },
};
</script>

<style lang="scss" scoped>
.loader {
  height: 100%;
}

.loader__content {
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
  -webkit-app-region: drag;
  height: 100%;

  background: rgba(18, 18, 27, 1);
}

.loader__icon {
  width: 65px;
  height: 65px;
  animation: spin 1s linear infinite;

  & svg {
    width: 100%;
    height: 100%;
    color: #fff;
  }
}
</style>
