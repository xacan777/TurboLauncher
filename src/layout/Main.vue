<template lang="pug">
Header
.content(:class="{ 'web': !isWeb }")
  router-view(v-slot="{ Component }")
    transition(name="fade" mode="out-in")
      component(:is="Component")
DirSettings
</template>

<script>
import DirSettings from '@/components/main/DirSettings.vue';
import Header from '@/components/main/Header.vue';
import utilsMixin from '@/mixins/utils-mixin';
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'MainLayout',
  components: { Header, DirSettings },
  mixins: [utilsMixin],
  data: () => ({
    intervalBalance: null,
  }),
  computed: {
    ...mapGetters(['userBase', 'user', 'isAfterAuthorized']),
    isWeb() {
      return typeof this.$route.meta?.isWeb === 'undefined' ? false : this.$route.meta.isWeb;
    },
  },
  mounted() {
    this.$store.dispatch('fetchBalanceUser');
    this.intervalBalance = setInterval(() => {
      this.$store.dispatch('fetchBalanceUser');
    }, 5000);

    if (this.isAfterAuthorized) {
      this.setIsClientReady(true);
    } else if (this.userBase.login && !this.isAfterAuthorized) {
      setTimeout(() => {
        this.onReauthForGenerationToken();
      }, 3000);
    }
  },
  methods: {
    ...mapActions(['logoutUser', 'setIsClientReady', 'setClientParams']),
  },
  unmounted() {
    clearInterval(this.intervalBalance);
  },
};
</script>

<style scoped>
.content {
  height: 100%;
}

.web {
  padding-top: 230px;
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
