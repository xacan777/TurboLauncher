<template lang="pug">
component(:is="layoutComponent")
notifications(group="main" position="bottom right")
</template>

<script>
import MainLayout from '@/layout/Main.vue';
import AuthLayout from '@/layout/Auth.vue';
import LoaderLayout from '@/layout/Loader.vue';

export default {
  name: 'App',
  components: { LoaderLayout, AuthLayout, MainLayout },
  computed: {
    layoutComponent() {
      const layout = this.$route.meta.layout || 'main';

      switch (layout) {
        case 'auth':
          return 'AuthLayout';
        case 'loader':
          return 'LoaderLayout';
        default:
          return 'MainLayout';
      }
    },
  },
};
</script>

<style lang="scss">
#app {
  font-family: 'Gilroy', sans-serif;
  width: 100%;
  height: 100vh;
}

body {
  width: 100%;
  height: 100%;
}
</style>
