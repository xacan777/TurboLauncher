<template lang="pug">
div
  .page-title Список обращений
  .page-filters
    UiButtonSecondary(
      :outline="filter !== 'Все'" size="small" @click="filter = 'Все'") Все
    UiButtonSecondary(
      :outline="filter !== 'Открыт'" size="small" @click="filter = 'Открыт'") Открытые
    UiButtonSecondary(
      :outline="filter !== 'В работе'" size="small" @click="filter = 'В работе'") В работе
    UiButtonSecondary(
      :outline="filter !== 'Закрыт'" size="small" @click="filter = 'Закрыт'") Закрытые
  .page-content
    table.ui-table
      thead
        th #
        th Тема
        th Категория
        th Статус
        th.right Действие
      tbody(v-if="!loading")
        tr
          td(colspan="5") Подождите, идет загрузка...
      tbody(v-else-if="filteredTickets.length === 0")
        tr
          td(colspan="5") По вашему запросу ничего не найдено.
      tbody(v-else)
        tr(v-for="ticket of filteredTickets" :key="ticket.id")
          td {{ ticket.id }}
          td {{ sliceLength(ticket.subject) }}
          td {{ ticket.category }}
          td
            span(:class=`{
            'text-success': ticket.status === 'Открыт',
            'text-primary': ticket.status === 'В работе',
            'text-secondary': ticket.status === 'Закрыт',
            }`) {{ ticket.status }}
          td.right
            UiButtonPrimary(size="small" @click="toInfo(ticket.id)") Посмотреть
</template>

<script>
import utilsMixin from '@/mixins/utils-mixin';
import UiButtonPrimary from '@/uikit/buttons/ui-button-primary.vue';
import UiButtonSecondary from '@/uikit/buttons/ui-button-secondary.vue';

export default {
  name: 'SupportListView',
  mixins: [utilsMixin],
  components: {
    UiButtonPrimary,
    UiButtonSecondary,
  },
  data: () => ({
    loading: false,
    tickets: [],
    filter: 'Открыт',
  }),
  created() {
    this.fetchTickets();
  },
  computed: {
    filteredTickets() {
      if (this.filter === 'Все') {
        return this.tickets;
      }
      return this.tickets.filter((ticket) => ticket.status === this.filter);
    },
  },
  methods: {
    fetchTickets() {
      this.loading = false;
      this.$http
        .get('support/getTickets', {
          params: {
            mUserId: this.$store.getters.user.mUserId,
          },
        })
        .then((data) => {
          const { success, tickets } = data;
          if (success) {
            this.tickets = tickets;
          }
        })
        .finally(() => {
          this.loading = true;
        });
    },
    toInfo(id) {
      this.$router.push({ name: 'support-info', params: { id } });
    },
  },
};
</script>

<style lang="scss" scoped>
.page-filters {
  margin-top: 20px;
  display: flex;

  & > * {
    margin-right: 10px;

    &:last-child {
      margin-right: 0;
    }
  }
}
</style>
