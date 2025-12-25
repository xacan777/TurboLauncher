<template lang="pug">
.page
  .panel
    .panel-header
      h2.panel-title База данных TURBO
      .tabs
        button.tab(:class="{ active: activeTab === 'leaders' }" @click="setTab('leaders')") Таблица лидеров
        button.tab(:class="{ active: activeTab === 'droplist' }" @click="setTab('droplist')") Дроп-лист
        button.tab(:class="{ active: activeTab === 'enhancement' }" @click="setTab('enhancement')") Усиление предметов

    .body v-if="activeTab === 'leaders'"
      .controls
        button.chip(:class="{ active: leaderboardView === 'levels' }" @click="leaderboardView = 'levels'") По уровням
        button.chip(:class="{ active: leaderboardView === 'power' }" @click="leaderboardView = 'power'") По силе
        input.search(type="text" v-model="leaderSearch" placeholder="Поиск по имени или классу")
      .table-wrapper
        table.data-table
          thead
            tr
              th Имя
              th(v-if="leaderboardView === 'levels'") Уровень
              th(v-else) Сила
              th Класс
          tbody
            tr(v-for="row in filteredLeaders" :key="row.name")
              td {{ row.name }}
              td(v-if="leaderboardView === 'levels'") {{ row.level }}
              td(v-else) {{ row.power }}
              td {{ row.class }}
      .state(v-if="leaderboardLoading") Обновляем таблицу лидеров...
      .state.error(v-else-if="leaderboardError") {{ leaderboardError }}

    .body v-if="activeTab === 'droplist'"
      .controls
        input.search(type="text" v-model="droplistFilters.iname" placeholder="Предмет")
        input.search(type="text" v-model="droplistFilters.mname" placeholder="Монстр")
        input.search(type="text" v-model="droplistFilters.place" placeholder="Локация")
        button.primary(@click="loadDroplist") Найти
      .table-wrapper
        table.data-table
          thead
            tr
              th Предмет
              th Кол-во
              th Монстр
              th Локация
          tbody
            tr(v-for="item in droplist" :key="`${item.item_id}-${item.monster_name}`")
              td {{ item.item_name }}
              td {{ item.count }}
              td {{ item.monster_name }}
              td {{ item.place }}
      .state(v-if="droplistLoading") Загружаем дроп-лист...
      .state.error(v-else-if="droplistError") {{ droplistError }}

    .body v-if="activeTab === 'enhancement'"
      .controls
        input.search(type="text" v-model="enhancementFilters.iname" placeholder="Предмет")
        select.select(v-model="enhancementFilters.type")
          option(value="all") Все типы
          option(value="weapon") Оружие
          option(value="defense") Защита
        button.primary(@click="loadEnhancement") Обновить
      .table-wrapper
        table.data-table
          thead
            tr
              th Предмет
              th Свиток
              th Шанс успеха
          tbody
            tr(v-for="row in enhancement" :key="row.item_id")
              td {{ row.iname }}
              td {{ row.scroll_name || '—' }}
              td {{ (row.rsuccess * 100).toFixed(0) }}%
      .state(v-if="enhancementLoading") Загружаем данные усиления...
      .state.error(v-else-if="enhancementError") {{ enhancementError }}
</template>

<script>
import { api } from '@/services/api';

export default {
  name: 'DatabaseView',
  data: () => ({
    activeTab: 'leaders',
    leaderboardView: 'levels',
    leaderSearch: '',
    leaderboard: {
      levels: [],
      power: [],
    },
    leaderboardLoading: false,
    leaderboardError: '',
    droplist: [],
    droplistFilters: {
      iname: '',
      mname: '',
      place: '',
    },
    droplistLoading: false,
    droplistError: '',
    enhancement: [],
    enhancementFilters: {
      iname: '',
      type: 'all',
    },
    enhancementLoading: false,
    enhancementError: '',
  }),
  computed: {
    filteredLeaders() {
      const dataset = this.leaderboard[this.leaderboardView] || [];
      const query = this.leaderSearch.toLowerCase();
      return dataset.filter(
        (item) =>
          item.name.toLowerCase().includes(query) || (item.class || '').toLowerCase().includes(query)
      );
    },
  },
  mounted() {
    this.loadLeaderboards();
    this.loadDroplist();
    this.loadEnhancement();
  },
  methods: {
    setTab(tab) {
      this.activeTab = tab;
    },
    async loadLeaderboards() {
      this.leaderboardError = '';
      this.leaderboardLoading = true;
      try {
        const [levels, power] = await Promise.all([
          api.leaderboardLevels({ lang: 'Russian' }),
          api.leaderboardPower({ lang: 'Russian' }),
        ]);
        this.leaderboard.levels = levels.data;
        this.leaderboard.power = power.data;
      } catch (error) {
        this.leaderboardError = error.message;
      } finally {
        this.leaderboardLoading = false;
      }
    },
    async loadDroplist() {
      this.droplistError = '';
      this.droplistLoading = true;
      try {
        const response = await api.droplist({
          ...this.droplistFilters,
          lang: 'Russian',
        });
        this.droplist = response.data;
      } catch (error) {
        this.droplistError = error.message;
      } finally {
        this.droplistLoading = false;
      }
    },
    async loadEnhancement() {
      this.enhancementError = '';
      this.enhancementLoading = true;
      try {
        const response = await api.enhancement({
          ...this.enhancementFilters,
          lang: 'Russian',
        });
        this.enhancement = response.data;
      } catch (error) {
        this.enhancementError = error.message;
      } finally {
        this.enhancementLoading = false;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.page {
  padding: 24px;
  color: #e6e8ff;
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
  flex-wrap: wrap;
}

.panel-title {
  margin: 0;
  font-size: 20px;
}

.tabs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.tab {
  border: 1px solid #2c2c48;
  background: transparent;
  color: #cfd5f7;
  padding: 10px 14px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;

  &.active {
    background: linear-gradient(135deg, #6c7bff, #2ec7ff);
    color: #0b0b15;
    border-color: transparent;
  }
}

.body {
  margin-top: 16px;
}

.controls {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 12px;
}

.chip {
  border: 1px solid #2c2c48;
  background: transparent;
  color: #cfd5f7;
  padding: 8px 12px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;

  &.active {
    background: #1c1c2b;
    border-color: #6c7bff;
  }
}

.search,
.select {
  background: #0f0f18;
  border: 1px solid #2c2c48;
  color: #e6e8ff;
  padding: 10px 12px;
  border-radius: 10px;
}

.primary {
  border: none;
  background: linear-gradient(135deg, #6c7bff, #2ec7ff);
  color: #0b0b15;
  padding: 10px 14px;
  border-radius: 10px;
  cursor: pointer;
}

.table-wrapper {
  overflow-x: auto;
  border: 1px solid #1b1b2a;
  border-radius: 12px;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 480px;

  th,
  td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #1b1b2a;
  }

  th {
    color: #9da3c5;
    font-weight: 700;
    background: #0f0f18;
  }
}

.state {
  margin-top: 10px;
  color: #9da3c5;

  &.error {
    color: #fca5a5;
  }
}
</style>
