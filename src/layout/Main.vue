<template lang="pug">
Header
.content(:class="{ 'web': !isWeb }")
  router-view(v-slot="{ Component }")
    transition(name="fade" mode="out-in")
      component(:is="Component")
</template>

<script>
import Header from '@/components/main/Header.vue';
import utilsMixin from '@/mixins/utils-mixin';

export default {
  name: 'MainLayout',
  components: { Header },
  mixins: [utilsMixin],
  computed: {
    isWeb() {
      return typeof this.$route.meta?.isWeb === 'undefined' ? false : this.$route.meta.isWeb;
    },
  },
};
</script>

<style scoped>
.content {
  height: 100%;
  padding-top: 16px;
}

.web {
  padding-top: 24px;
  box-sizing: border-box;
  max-width: 920px;
  width: 100%;
  margin: 0 auto;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
