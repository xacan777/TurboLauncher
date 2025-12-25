<template lang="pug">
div(style="width: 100%; height: 100%")
  .loader(v-if="isShowLoader", ref="loader")
    .loader-icon
      IconSpinner
  webview.webview(
    ref="loadPage",
    cacheEnabled="false",
    src="http://starter.saidageg.beget.tech/",
    httpreferrer="http://starter.saidageg.beget.tech/",
    style="display: inline-flex; width: 100%; height: 100%",
    nodeintegration,
    disablewebsecurity
  )
</template>

<script>
import IconSpinner from '@/assets/icons/icon-spinner.vue';
import gsap from 'gsap';

export default {
  name: 'AboutView',
  data: () => ({
    isLoaded: false,
    isShowLoader: false,
  }),
  mounted() {
    const timeOut = setTimeout(() => {
      this.isShowLoader = true;
    }, 200);
    const onCallLoaded = () => {
      this.isLoaded = true;
      this.onAnimationShowWebViewOnLoad();
    };
    console.log(this.$refs.loadPage);
    this.$refs.loadPage.addEventListener('did-finish-load', () => {
      if (this.isShowLoader) {
        this.onAnimationHideLoader(() => {
          onCallLoaded();
        });
      } else {
        onCallLoaded();
      }

      clearTimeout(timeOut);
      this.isShowLoader = false;
    });
  },
  methods: {
    onAnimationHideLoader(onComplete = null) {
      const tl = gsap.timeline();
      tl.to(this.$refs.loader, {
        duration: 0.5,
        opacity: 0,
      });

      tl.eventCallback('onComplete', () => {
        if (onComplete) onComplete();
      });
    },
    onAnimationShowWebViewOnLoad(onComplete = null) {
      const tl = gsap.timeline();
      tl.to(this.$refs.loadPage, {
        duration: 0.5,
        opacity: 1,
        ease: 'power2.inOut',
      });
      // callback
      tl.eventCallback('onComplete', () => {
        if (onComplete) onComplete();
      });
    },
  },
  components: { IconSpinner },
};
</script>

<style lang="scss" scoped>
.loader {
  display: flex;
  align-items: center;
  justify-content: center;

  margin-top: 200px;
  &-icon {
    width: 65px;
    height: 65px;
    animation: spin 1s linear infinite;

    & svg {
      width: 100%;
      height: 100%;
      color: #8585a9;
    }
  }
}

.webview {
  opacity: 0;
}
</style>
