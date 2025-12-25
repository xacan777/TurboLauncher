<template lang="pug">
div(v-if="ticket")
  //- pre {{ ticket }}
  .ticket-header
    .ticket-header-title {{ sliceLength(ticket.subject, 80) }}
    .ticket-header-status(
      :class=`{
      'text-success': ticket.status === 'Открыт',
      'text-primary': ticket.status === 'В работе',
      'text-secondary': ticket.status === 'Закрыт',
      }`) {{ ticket.status }}
  .ticket-area
    .ticket-content(
      :class="ticket.status === 'Закрыт' ? 'closed' : ''"
      ref="content")
      .ticket-message(
        v-for="message of ticket.messages"
        :class="{ 'user': message.is_user }"
        :key="message.id")
        .ticket-message-body {{ message.message }}
        .ticket-message-date {{ $filters.dateFromNow(message.created_at) }}
  .ticket-footer(v-if="ticket.status !== 'Закрыт'")
    UiTextarea(
      placeholder="Сообщение"
      v-model="form.message"
    )
      template(#icon)
        IconLock
    UiButtonPrimary(
      :loading="formLoading"
      :disabled="!isValidSender"
      @click="onSendMessage") Отправить
  .ticket-footer(v-else)
    .ticket-footer-text.text-secondary Обращение закрыто
</template>

<script>
import UiTextarea from '@/uikit/inputs/ui-textarea.vue';
import UiButtonPrimary from '@/uikit/buttons/ui-button-primary.vue';
import IconLock from '@/assets/icons/icon-lock.vue';
import utilsMixin from '@/mixins/utils-mixin';

export default {
  name: 'SupportInfoView',
  mixins: [utilsMixin],
  components: {
    UiTextarea,
    UiButtonPrimary,
    IconLock,
  },
  data: () => ({
    ticket: null,
    formLoading: false,
    form: {
      message: '',
    },
    poolingInterval: null,
  }),
  mounted() {
    this.poolingInterval = setInterval(() => {
      this.fetchTicketById(false);
    }, 5000);
    this.fetchTicketById();
  },
  unmounted() {
    clearInterval(this.poolingInterval);
  },
  beforeUnmount() {
    this.$store.dispatch('setTicketMulti', []);
  },
  computed: {
    isValidSender() {
      return !this.formLoading && this.form.message.length > 0;
    },
  },
  methods: {
    scrollToBottom() {
      this.$nextTick(() => {
        this.$refs.content.scrollTop = this.$refs.content.scrollHeight;
      });
    },
    fetchTicketById(withScroll = true) {
      this.$http
        .get('support/getTicketById', {
          params: {
            ticketId: this.$route.params.id,
          },
        })
        .then((data) => {
          this.item = data;
          const { success, ticket } = data;
          if (success) {
            const messagesLendth = this.ticket?.messages.length;
            this.ticket = ticket;

            if (withScroll) {
              this.$store.dispatch('setTicketMulti', [
                {
                  to: { name: 'support-info', params: { id: this.$route.params.id } },
                  value: ticket.subject,
                },
              ]);
            }

            if (withScroll) {
              this.scrollToBottom();
            } else if (messagesLendth < this.ticket.messages.length) {
              this.scrollToBottom();
            }
          }
        });
    },
    onSendMessage() {
      if (!this.isValidSender) return;
      this.formLoading = true;
      this.$http
        .post('support/sendMessage', {
          mUserId: this.$store.getters.user.mUserId,
          ticket: {
            id: this.$route.params.id,
            message: this.form.message,
            is_admin: false,
          },
        })
        .then((data) => {
          const { status } = data;
          if (status) {
            this.form.message = '';
            this.$notify({
              type: 'success',
              group: 'main',
              title: 'Успешно',
              text: 'Сообщение отправлено',
            });
            this.fetchTicketById();
          }
        })
        .finally(() => {
          this.formLoading = false;
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.ticket {
  &-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;

    &-title {
      font-family: 'Gilroy';
      font-style: normal;
      font-weight: 700;
      font-size: 18px;
    }

    &-status {
      font-family: 'Gilroy';
      font-style: normal;
      font-weight: 400;
      font-size: 14px;
    }
  }

  &-area {
    background: rgba(28, 28, 45, 0.9);
    border-radius: 4px;
    padding: 0 0 0 30px;
    box-sizing: border-box;
    margin-bottom: 18px;
  }

  &-content {
    display: flex;
    flex-direction: column;
    overflow: auto;
    padding: 30px 30px 30px 0;

    &::-webkit-scrollbar {
      width: 2px;
    }

    &::-webkit-scrollbar-track {
      background: rgba(255, 255, 255, 0.1);
    }

    &::-webkit-scrollbar-thumb {
      background: rgba(255, 255, 255, 0.2);
    }

    &::-webkit-scrollbar-thumb:hover {
      background: rgba(255, 255, 255, 0.3);
    }

    &.closed {
      height: calc(100vh - 330px);
    }

    height: calc(100vh - 450px);
  }

  &-message {
    max-width: 40%;
    margin-bottom: 23px;

    &:last-child {
      margin-bottom: 0;
    }

    &.user {
      align-self: flex-end;
    }

    &.user &-body {
      background: #1877f2;
    }

    &.user &-date {
      align-self: flex-end;
    }

    display: flex;
    flex-direction: column;

    &-body {
      background: #9747ff;
      border-radius: 10px;
      padding: 10px;
      box-sizing: border-box;
      margin-bottom: 15px;
      font-family: 'Gilroy';
      font-style: normal;
      font-weight: 500;
      font-size: 14px;
      line-height: 160%;
    }

    &-date {
      font-family: 'Gilroy';
      font-style: normal;
      font-weight: 500;
      font-size: 14px;
      color: #8b8bbf;
    }
  }

  &-footer {
    padding-top: 10px;

    & button {
      margin-top: 10px;
      max-width: 250px;
    }
  }
}
</style>
