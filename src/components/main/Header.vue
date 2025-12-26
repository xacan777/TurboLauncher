<template lang="pug">
header.header
  .header-left
    router-link.brand(:to="{ name: 'home' }")
      .brand-mark TURBO
      .brand-subtitle Launcher
    .nav
      router-link.nav-item(:to="{ name: 'home' }" active-class="active") Главная
      router-link.nav-item(:to="{ name: 'database' }" active-class="active") База данных
      router-link.nav-item(:to="{ name: 'forum' }" active-class="active") Форум
  .header-right
    .status(v-if="statusText")
      span.status-dot(:class="{ online: statusOnline, offline: !statusOnline }")
      span.status-text {{ statusText }}
    template(v-if="isAuthorized")
      .user
        .user-name {{ user?.username || 'Игрок' }}
        button.pill(@click="onLogout") Выйти
    template(v-else)
      router-link.pill(:to="{ name: 'login' }") Войти
      router-link.secondary.pill(:to="{ name: 'register' }") Регистрация
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import { api } from '@/services/api';

export default {
  name: 'MainHeader',
  data: () => ({
    statusText: '',
    statusOnline: false,
  }),
  computed: {
    ...mapGetters(['isAuthorized', 'user']),
  },
  mounted() {
    this.fetchStatus();
  },
  methods: {
    ...mapActions(['logoutUser']),
    async fetchStatus() {
      try {
        const { online, players } = await api.serverStatus();
        this.statusOnline = online;
        this.statusText = online ? `Сервер онлайн · ${players} игроков` : 'Сервер оффлайн';
      } catch (error) {
        this.statusText = 'Статус недоступен';
        this.statusOnline = false;
      }
    },
    async onLogout() {
      await this.logoutUser();
      this.$router.push({ name: 'login' });
    },
  },
};
</script>

<style lang="scss" scoped>
.header {
  position: sticky;
  top: 0;
  z-index: 20;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  background: rgba(10, 10, 18, 0.92);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid #2c2c48;
}

.header-left {
  display: flex;
  align-items: center;
}

.brand {
  display: flex;
  flex-direction: column;
  text-decoration: none;
  color: #fff;
  margin-right: 32px;
  user-select: none;
}

.brand-mark {
  font-size: 18px;
  font-weight: 800;
  letter-spacing: 0.1em;
}

.brand-subtitle {
  font-size: 12px;
  color: #9da3c5;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.nav {
  display: flex;
  gap: 14px;
}

.nav-item {
  color: #aab0d6;
  text-decoration: none;
  font-weight: 600;
  padding: 8px 12px;
  border-radius: 10px;
  transition: all 0.2s ease;

  &.active,
  &:hover {
    background: linear-gradient(135deg, #6c7bff, #2ec7ff);
    color: #0b0b15;
  }
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.status {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.04);
  color: #cfd5f7;
  font-size: 12px;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  &.online {
    background: #4ade80;
    box-shadow: 0 0 0 4px rgba(74, 222, 128, 0.15);
  }
  &.offline {
    background: #f87171;
    box-shadow: 0 0 0 4px rgba(248, 113, 113, 0.15);
  }
}

.status-text {
  white-space: nowrap;
}

.pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 16px;
  border-radius: 12px;
  border: 1px solid transparent;
  background: linear-gradient(135deg, #6c7bff, #2ec7ff);
  color: #0b0b15;
  font-weight: 700;
  text-decoration: none;
  cursor: pointer;
  transition: transform 0.1s ease, box-shadow 0.2s ease;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 12px 30px rgba(45, 151, 255, 0.25);
  }

  &.secondary {
    background: transparent;
    color: #cfd5f7;
    border-color: #2c2c48;
    &:hover {
      border-color: #6c7bff;
      color: #fff;
    }
  }
}

.user {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #e5e7ff;
}

.user-name {
  font-weight: 700;
}
</style>
