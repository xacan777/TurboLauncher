<template lang="pug">
.header
  .header-toolbar
    .header-toolbar-left
      .container
        .item(@click="prevPage")
          IconArrow
      .container
        .item(@click="nextPage")
          IconArrow.next
    .header-toolbar-right
      .container(@click="onHide")
        .item
          IconLowerHide
      //- .container(@click="onFullScreen")
      //-   .item
      //-     IconFrame
      .container(@click="showConfirmCloseApp = true")
        .item
          IconClose
  .header-menu
    router-link.header-menu-item(
      v-for="({icon, value, to}, index) in menuItems"
      v-bind="{ to }"
      :key="index"
      tag="div"
      active-class="active"
      )
      .header-menu-item-icon
        component(:is="icon")
      .header-menu-item-text {{ value }}
  .header-logo
    img(src="@/assets/images/logo.png" srcset="@/assets/images/logo@2x.png 2x")
  .header-user
    //- .header-user-avatar
    //-   img(src="https://r2legacy.com/new-frontend/images/users/001.png")
    .header-user-info
      router-link.header-user-name(
        :to="{ name: 'user-settings-general' }"
        tag="div"
      ) {{ user.mEmail }}
      .header-user-footer
        .header-user-footer-item
          router-link.header-user-footer-item-value.green(
            :to="{ name: 'user-settings-payment' }"
            tag="div"
          )
            .header-user-footer-item-value-text {{ user.mBalance }}
            .header-user-footer-item-value-icon ₽
  .header-submenu
    .header-submenu-left
      router-link.header-submenu-left-item(
        v-for="(menu, index) in getActiveMenu?.subCategories"
        :key="index"
        :to="menu.to" active-class="active" exact-active-class="active")
        | {{ sliceLength(menu.value, 50) }}
    .header-submenu-right
      .header-submenu-right-action
        ActionBar
      .header-submenu-right-settings
        IconFolderSettings(@click="showModalDirectoryInfo")
        IconClose(@click="showConfirmUserLogout = true")
ConfirmCloseApp(
  v-if="showConfirmCloseApp"
  @close="onClose"
  @update:state="showConfirmCloseApp = $event"
)
ConfirmLogoutUser(
  v-if="showConfirmUserLogout"
  @close="onLogoutUser"
  @update:state="showConfirmUserLogout = $event"
)
</template>

<script>
import IconArrow from '@/assets/icons/icon-arrow.vue';
import IconLowerHide from '@/assets/icons/icon-lower-hide.vue';
import IconFrame from '@/assets/icons/icon-frame.vue';
import IconClose from '@/assets/icons/icon-close.vue';
import { BrowserWindow, app } from '@electron/remote';
import IconChat from '@/assets/icons/icon-chat.vue';
import IconStars from '@/assets/icons/icon-stars.vue';
import IconUserSettings from '@/assets/icons/icon-user-settings.vue';
import IconMonet from '@/assets/icons/icon-monet.vue';
import IconFolderSettings from '@/assets/icons/icon-folder-settings.vue';
import { mapGetters } from 'vuex';
import utilsMixin from '@/mixins/utils-mixin';
import ActionBar from './ActionBar.vue';
import ConfirmCloseApp from './ConfirmCloseApp.vue';
import ConfirmLogoutUser from './ConfirmLogoutUser.vue';

export default {
  name: 'main-header',
  mixins: [utilsMixin],
  components: {
    IconArrow,
    IconLowerHide,
    IconFrame,
    IconClose,
    IconChat,
    IconStars,
    IconUserSettings,
    IconMonet,
    IconFolderSettings,
    ActionBar,
    ConfirmCloseApp,
    ConfirmLogoutUser,
  },
  data: () => ({
    showConfirmCloseApp: false,
    showConfirmUserLogout: false,
  }),
  mounted() {
    console.log(this.user);
  },
  computed: {
    ...mapGetters(['user']),
    menuItems() {
      return [
        {
          icon: 'IconStars',
          to: { name: 'main' },
          value: 'Новости',
          subCategories: [
            {
              to: { name: 'home' },
              value: 'Главная',
            },
            {
              to: { name: 'about' },
              value: 'Стартер-паки',
            },
            {
              to: { name: 'dopo' },
              value: 'Дополнительно',
            },
          ],
        },
        {
          icon: 'IconChat',
          to: { name: 'support' },
          value: 'Поддержка',
          subCategories: [
            {
              to: { name: 'support-list' },
              value: 'Все обращения',
            },
            {
              to: { name: 'support-create' },
              value: 'Создать обращение',
            },
            ...this.$store.getters.ticketMulti,
          ],
        },
        {
          icon: 'IconUserSettings',
          to: { name: 'user-settings' },
          value: 'Настройки',
          subCategories: [
            {
              to: { name: 'user-settings-general' },
              value: 'Смена пароля',
            },
            {
              to: { name: 'user-settings-payment' },
              value: 'Пополнить баланс',
            },
            {
              to: { name: 'user-settings-promocode' },
              value: 'Промокоды',
            },
          ],
        },
      ];
    },
    getActiveMenu() {
      const routers = this.$route.matched;
      const items = [];
      routers.forEach((item) => {
        if (item.children?.length > 0) {
          // eslint-disable-next-line no-restricted-syntax
          for (const child of item.children) {
            items.push(child.name);
          }
        }

        items.push(item.name);
      });

      return this.menuItems.find((item) => items.includes(item.to.name));
    },
  },
  methods: {
    onHide() {
      BrowserWindow.getFocusedWindow().minimize();
    },
    onFullScreen() {
      BrowserWindow.getFocusedWindow().setFullScreen(
        !BrowserWindow.getFocusedWindow().isFullScreen()
      );
    },
    onClose() {
      app.quit();
    },
    async onLogoutUser() {
      await this.$store.dispatch('logoutUser');
      this.$appEvent('authFrame', {});
    },
    prevPage() {
      this.$router.go(-1);
    },
    nextPage() {
      this.$router.go(1);
    },
    showModalDirectoryInfo() {
      this.$store.commit('setStateModalDirSettings', true);
      // this.$appEvent('selectFolder', {});
    },
  },
};
</script>

<style lang="scss" scoped>
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 999999999;
  height: 168px;
  background: linear-gradient(180deg, rgba(18, 18, 27, 0.95) 0%, rgba(18, 18, 27, 0.9) 100%);
  display: flex;
  flex-direction: column;
  justify-content: space-between;

  &-toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: 0 !important;
    padding: 10px;
    -webkit-app-region: drag;

    &-right,
    &-left {
      display: flex;
      align-items: center;
      -webkit-app-region: no-drag;
    }
  }

  &-menu {
    display: flex;
    align-items: center;
    justify-content: center;

    &-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      text-decoration: none;
      margin-right: 30px;

      transition: all 0.3s ease;

      &.active {
        cursor: default;
      }

      &.active &-icon,
      &.active &-text {
        color: #fff;
      }

      &:not(.active):hover &-icon,
      &:not(.active):hover &-text {
        color: #fff;
      }

      &:last-child {
        margin-right: 0;
      }

      &-icon {
        margin-bottom: 5px;
        color: #8585a9;
        transition: all 0.3s ease;
      }

      &-text {
        font-style: normal;
        font-weight: 600;
        font-size: 14px;
        color: #8585a9;
        transition: all 0.3s ease;
      }
    }
  }

  &-logo {
    position: absolute;
    top: 34px;
    left: 15px;

    & > img {
      width: 100%;
      height: 100%;
      object-fit: contain;
    }
  }

  &-user {
    position: absolute;
    top: 75px;
    right: 20px;
    display: flex;
    text-decoration: none;

    &-avatar {
      min-width: 25px;
      max-width: 25px;
      height: 25px;
      margin-right: 10px;
      border: 2px solid #8585a9;
      border-radius: 50%;
      padding: 2px;

      & > img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
    }

    &-info {
      display: flex;
      flex-direction: row;
      align-items: center;
    }

    &-name {
      text-decoration: none;
      color: #fff;
      font-style: normal;
      font-weight: 600;
      font-size: 14px;
      margin-right: 10px;
      transition: all 0.3s ease;
      cursor: pointer;
      opacity: 0.5;
      &:hover {
        opacity: 1;
      }
    }

    &-footer {
      display: flex;
      align-items: center;

      &-item {
        margin-right: 15px;

        display: flex;
        align-items: center;

        &-label {
          margin-right: 5px;
          font-style: normal;
          font-weight: 600;
          font-size: 14px;
          color: #5c5c69;
        }

        &-value {
          display: flex;
          align-items: center;
          cursor: pointer;
          text-decoration: none;
          transition: all 0.3s ease;
          opacity: 0.5;
          &:hover {
            opacity: 1;
          }

          &.green {
            color: #fff;
          }

          &.blue {
            color: #00d1ff;
          }

          &-text {
            margin-right: 5px;
            margin-top: 1px;
            font-style: normal;
            font-weight: 600;
            font-size: 14px;
          }

          &-icon {
            width: 17px;
            height: 17px;
            border-radius: 50%;
            border: 1.5px solid #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 11px;
            font-weight: 400;
            padding-top: 3px;
          }
        }

        &:last-child {
          margin-right: 0;
        }
      }
    }
  }

  &-submenu {
    height: 45px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-top: 1px solid #4e4e72;
    padding: 0 20px;
    box-sizing: border-box;

    &-left {
      display: flex;
      align-items: center;

      &-item {
        margin-right: 20px;
        font-family: 'Gilroy';
        font-style: normal;
        font-weight: 700;
        font-size: 12px;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        cursor: pointer;
        color: #8585a9;
        transition: all 0.2s ease;
        text-decoration: none;

        &.active {
          color: #fff !important;
          cursor: default;
        }

        &:hover {
          color: #fff;
        }

        &:last-child {
          margin-right: 0;
        }
      }
    }

    &-right {
      display: flex;
      align-items: center;
      height: 100%;

      & > * {
        margin-right: 20px;
        height: 100%;

        display: flex;
        align-items: center;

        &:last-child {
          margin-right: 0;
        }
      }

      &-settings {
        color: #8585a9;

        transition: all 0.2s ease;
        margin-top: 4px;

        & > * {
          margin-right: 10px;
          cursor: pointer;

          &:hover {
            color: #696992;
          }

          &:last-child {
            margin-right: 0;
          }
        }
      }
    }
  }
}

.next {
  transform: rotate(180deg);
}

.container {
  width: 45px;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;

  &:not(.disabled):hover .item {
    color: #8989a8;
  }
}

.item {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: flex-end;
  justify-content: center;

  color: #606085;
  transition: color 0.2s ease;
}
</style>
