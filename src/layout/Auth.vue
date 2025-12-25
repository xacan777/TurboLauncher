<template lang="pug">
.auth
  .auth-image
    img(src="@/assets/images/auth-image.png")
  .auth-content
    .auth-content-toolbar
      .hide-button(@click="onHideApp")
        IconLowerHide
      .close-button(@click="onCloseApp")
        IconClose
    .auth-content-logo
      img(srcset="@/assets/images/logo@2x.png 2x" src="@/assets/images/logo.png")
    .auth-content-menu
      .auth-content-menu-line(ref="line")
      router-link.auth-content-menu-item(
        :ref="setItemRef"
        :to="{ name: 'login' }"
        active-class="active") Вход в ЛК
      router-link.auth-content-menu-item(
        :ref="setItemRef"
        :to="{ name: 'register' }"
        active-class="active") Создать аккаунт
    .auth-content-body
      router-view(v-slot="{ Component }")
        transition(name="scale" mode="out-in")
          component(:is="Component")
</template>

<script>
import IconClose from '@/assets/icons/icon-close.vue';
import IconLowerHide from '@/assets/icons/icon-lower-hide.vue';
import gsap from 'gsap';
import { BrowserWindow, app } from '@electron/remote';

export default {
  name: 'AuthLayout',
  data: () => ({
    itemRefs: [],
  }),
  mounted() {
    this.setMenuActiveLine();
  },
  beforeUpdate() {
    this.itemRefs = [];
  },
  updated() {
    console.log(this.itemRefs);
  },
  methods: {
    setItemRef(el) {
      console.log(el);
      if (el) {
        this.itemRefs.push(el);
      }
    },
    setMenuActiveLine(clear = false) {
      const menuItems = this.itemRefs;
      const activeLine = this.$refs.line;
      console.log(Array.from(menuItems));
      const activeItem = menuItems.find((item) => item.to.name === this.$route.name);
      if (!clear || activeItem) {
        // const activeItemIndex = Array.from(menuItems).indexOf(activeItem.$el);
        const activeItemWidth = activeItem.$el.offsetWidth;
        const activeItemOffsetLeft = activeItem.$el.offsetLeft;
        activeLine.style.width = `${activeItemWidth}px`;
        activeLine.style.left = `${activeItemOffsetLeft}px`;
        menuItems.forEach((item) => {
          item.$el.addEventListener('click', () => {
            const itemWidth = item.$el.offsetWidth;
            const itemOffsetLeft = item.$el.offsetLeft;
            this.setAnimation(activeLine, {
              width: `${itemWidth}px`,
              left: `${itemOffsetLeft}px`,
            });
          });
        });
      } else {
        activeLine.style.width = '0px';
        activeLine.style.left = '0px';
      }
    },
    setAnimation(el, { left, width }) {
      gsap.to(el, {
        ease: 'back.out',
        duration: 0.4,
        left,
        width,
      });
    },
    onCloseApp() {
      app.quit();
    },
    onHideApp() {
      BrowserWindow.getFocusedWindow().minimize();
    },
  },
  computed: {
    routerView() {
      return this.$route.name;
    },
  },
  watch: {
    routerView(name) {
      if (!this.itemRefs.map((item) => item.to.name).includes(name)) {
        this.setMenuActiveLine(true);
      } else {
        this.setMenuActiveLine();
      }
    },
  },
  components: { IconClose, IconLowerHide },
};
</script>

<style lang="scss" scoped>
.auth {
  height: 100%;
  background: transparent !important;

  display: flex;

  &-image {
    -webkit-app-region: drag;
    -webkit-user-select: none;
    max-width: 334px;
    width: 100%;
    height: 100%;

    & img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }

  &-content {
    width: 100%;
    height: 100%;
    background: #12121b;
    box-shadow: -4px 0px 10px rgba(0, 0, 0, 0.5);
    position: relative;

    &-toolbar {
      position: absolute;
      display: flex;
      align-items: center;
      top: 15px;
      right: 15px;

      & > * {
        cursor: pointer;
        margin-right: 20px;

        color: #8585a9;
        transition: all 0.2s ease;

        &:hover {
          color: #636399;
        }

        &:last-child {
          margin-right: 0;
        }
      }
    }

    padding: 30px 0;

    &-logo {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-bottom: 50px;
      -webkit-app-region: drag;
      -webkit-user-select: none;
    }

    &-menu {
      position: relative;

      &-line {
        position: absolute;
        left: 0;
        bottom: 0;
        background: #fff;
        width: 0px;
        height: 2px;
      }

      display: flex;
      justify-content: center;
      margin-bottom: 50px;
      height: 31px;
      border-bottom: 1px solid #4e4e72;
      -webkit-tap-highlight-color: rgba(255, 255, 255, 0);

      &-item {
        transition: color 0.2s ease;

        &.active {
          color: #ffffff;
        }

        margin-right: 25px;

        font-style: normal;
        font-weight: 600;
        font-size: 12px;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        text-decoration: none;

        color: #4e4e72;

        &:last-child {
          margin-right: 0;
        }
      }
    }

    &-body {
      max-width: 245px;
      width: 100%;
      margin: 0 auto;
    }
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.1s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.scale-enter-active,
.scale-leave-active {
  transition: all 0.2s ease;
}

.scale-enter-from,
.scale-leave-to {
  opacity: 0;
  transform: scale(0.9);
}
</style>
