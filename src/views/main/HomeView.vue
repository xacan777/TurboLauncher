<template lang="pug">
.page
  .hero
    .hero-content
      .eyebrow TURBO LAUNCHER
      h1.title Современный лаунчер для твоего мира
      p.subtitle Новости, база данных, форум и быстрый старт — в одном окне.
      .actions
        button.primary(@click="onPlay") Играть / Запустить
        router-link.secondary(:to="{ name: 'database' }") Открыть базу данных
    .hero-stats
      .stat-card(v-for="stat in stats" :key="stat.label")
        .stat-value {{ stat.value }}
        .stat-label {{ stat.label }}
  .grid
    .panel
      .panel-header
        .panel-title Новости
        button.link(@click="loadNews") Обновить
      template(v-if="news.length")
        .news-card(v-for="item in news" :key="item.title")
          .news-title {{ item.title }}
          .news-body {{ item.body }}
          .news-date {{ $filters.dateFromNow(item.date) }}
      .empty(v-else) Пока нет новостей, но TURBO уже готов к запуску.
    .panel
      .panel-header
        .panel-title Статус серверов
        button.link(@click="fetchStatus" :disabled="statusLoading")
          span(v-if="statusLoading") Обновление...
          span(v-else) Проверить
      .status-block(:class="{ online: status.online }")
        .status-dot
        .status-text {{ status.online ? 'Онлайн' : 'Оффлайн' }}
      p.status-caption(v-if="status.players !== null")
        | Игроков: {{ status.players }}
      p.status-caption(v-if="statusChecked && !status.online")
        | Мы автоматически подсветим статус, когда сервер поднимется.
    .panel
      .panel-header
        .panel-title Быстрые действия
      ul.quick-actions
        li(@click="goTo('database')") База данных (лидеры, дроп, усиления)
        li(@click="goTo('forum')") Форум и обратная связь
        li(@click="goTo('home')") Настройки лаунчера
</template>

<script>
import { api } from '@/services/api';

export default {
  name: 'HomeView',
  data: () => ({
    news: [],
    stats: [
      { label: 'Готовность клиента', value: '100%' },
      { label: 'TURBO API', value: 'LIVE' },
      { label: 'Форум', value: 'Обновлен' },
    ],
    status: {
      online: false,
      players: null,
    },
    statusLoading: false,
    statusChecked: false,
  }),
  mounted() {
    this.loadNews();
    this.fetchStatus();
  },
  methods: {
    async loadNews() {
      try {
        const response = await api.news();
        this.news = response.items || [];
      } catch (error) {
        this.$notifyError(error.message);
      }
    },
    async fetchStatus() {
      this.statusLoading = true;
      try {
        const response = await api.serverStatus();
        this.status = response;
        this.statusChecked = true;
      } catch (error) {
        this.$notifyError(error.message);
      } finally {
        this.statusLoading = false;
      }
    },
    goTo(name) {
      this.$router.push({ name });
    },
    onPlay() {
      this.$notify({
        group: 'main',
        type: 'success',
        text: 'Загрузка клиента TURBO...',
      });
      this.$appEvent('startDownloadClient');
    },
  },
};
</script>

<style lang="scss" scoped>
.page {
  padding: 24px;
  color: #e6e8ff;
}

.hero {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  align-items: stretch;
  margin-bottom: 24px;
}

.hero-content {
  background: radial-gradient(circle at 10% 20%, rgba(110, 125, 255, 0.25), transparent 35%),
    radial-gradient(circle at 80% 0%, rgba(46, 199, 255, 0.2), transparent 30%),
    #11111a;
  border: 1px solid #2c2c48;
  padding: 28px;
  border-radius: 18px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.45);
}

.eyebrow {
  font-weight: 800;
  letter-spacing: 0.2em;
  color: #7ce0ff;
  margin-bottom: 12px;
  font-size: 12px;
}

.title {
  margin: 0 0 12px;
  font-size: 32px;
  line-height: 1.2;
}

.subtitle {
  color: #b8b9d9;
  margin-bottom: 16px;
  max-width: 520px;
}

.actions {
  display: flex;
  gap: 12px;
}

.primary,
.secondary {
  border: none;
  cursor: pointer;
  font-weight: 700;
  padding: 12px 16px;
  border-radius: 12px;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.1s ease, box-shadow 0.2s ease;
}

.primary {
  background: linear-gradient(135deg, #6c7bff, #2ec7ff);
  color: #0b0b15;
  box-shadow: 0 12px 30px rgba(45, 151, 255, 0.3);

  &:hover {
    transform: translateY(-1px);
  }
}

.secondary {
  background: transparent;
  color: #e6e8ff;
  border: 1px solid #2c2c48;

  &:hover {
    border-color: #6c7bff;
  }
}

.hero-stats {
  background: #0c0c15;
  border: 1px solid #2c2c48;
  border-radius: 18px;
  padding: 16px;
  display: grid;
  gap: 12px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(124, 224, 255, 0.15);
  border-radius: 12px;
  padding: 12px;
}

.stat-value {
  font-size: 20px;
  font-weight: 800;
}

.stat-label {
  color: #9da3c5;
  font-size: 12px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.panel {
  background: #0c0c15;
  border: 1px solid #2c2c48;
  border-radius: 16px;
  padding: 16px;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.panel-title {
  font-weight: 700;
  font-size: 16px;
}

.link {
  border: none;
  background: transparent;
  color: #7ce0ff;
  cursor: pointer;
}

.news-card {
  padding: 12px;
  border: 1px solid #202036;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.02);
  margin-bottom: 10px;
}

.news-title {
  font-weight: 700;
}

.news-body {
  color: #cfd1e8;
  margin: 6px 0;
}

.news-date {
  font-size: 12px;
  color: #8f94bd;
}

.status-block {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid #2c2c48;
  background: rgba(255, 255, 255, 0.02);

  &.online {
    border-color: rgba(74, 222, 128, 0.4);
  }
}

.status-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #f87171;
}

.status-block.online .status-dot {
  background: #4ade80;
}

.status-text {
  font-weight: 700;
}

.status-caption {
  color: #9da3c5;
  margin-top: 8px;
}

.quick-actions {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;

  & > li {
    padding: 12px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid #1b1b2a;
    cursor: pointer;
    transition: all 0.15s ease;

    &:hover {
      border-color: #6c7bff;
      color: #fff;
    }
  }
}

.empty {
  color: #9da3c5;
}

@media (max-width: 960px) {
  .hero {
    grid-template-columns: 1fr;
  }
}
</style>
