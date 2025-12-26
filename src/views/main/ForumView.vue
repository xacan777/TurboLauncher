<template lang="pug">
.page(:class="{ expanded }")
  .panel
    .panel-header
      h2.panel-title Форум TURBO
      .actions
        button.secondary(@click="expanded = !expanded") {{ expanded ? 'Свернуть' : 'Развернуть' }}
        button.primary(@click="loadTopics" :disabled="topicsLoading") Обновить
    .layout
      .topics
        .topics-header
          h3 Темы
          button.chip(@click="showTopicForm = !showTopicForm") Новая тема
        form.topic-form(v-if="showTopicForm" @submit.prevent="createTopic")
          input.input(type="text" v-model="topicForm.title" placeholder="Заголовок (3-120 символов)")
          textarea.input(v-model="topicForm.message" placeholder="Сообщение (1-2000 символов)" rows="3")
          .topic-actions
            button.primary(type="submit" :disabled="topicLoading") Создать
            button.secondary(type="button" @click="resetTopicForm") Отмена
        .topic-list
          .topic-card(
            v-for="topic in topics"
            :key="topic.id"
            :class="{ active: topic.id === selectedTopic?.id }"
            @click="selectTopic(topic)"
          )
            .title {{ topic.title }}
            .meta {{ topic.message_count || 0 }} сообщений · {{ formatDate(topic.updated_at) }}
        .state(v-if="topicsLoading") Загружаем темы...
        .state.error(v-else-if="topicsError") {{ topicsError }}
      .messages
        template(v-if="selectedTopic")
          .messages-header
            h3 {{ selectedTopic.title }}
            p.meta Автор: {{ selectedTopic.author || 'anon' }}
          .message-list
            .message-card(v-for="msg in messages" :key="msg.id")
              .message-author {{ msg.author }}
              .message-text {{ msg.text }}
              .message-date {{ formatDate(msg.created_at) }}
          form.message-form(@submit.prevent="sendMessage")
            textarea.input(v-model="messageText" rows="3" placeholder="Ответить..." required)
            .topic-actions
              button.primary(type="submit" :disabled="messageLoading") Отправить
        template(v-else)
          .empty Выберите тему, чтобы прочитать сообщения.
</template>

<script>
import { api } from '@/services/api';

export default {
  name: 'ForumView',
  data: () => ({
    topics: [],
    topicsLoading: false,
    topicsError: '',
    selectedTopic: null,
    messages: [],
    messageText: '',
    messageLoading: false,
    topicForm: {
      title: '',
      message: '',
    },
    topicLoading: false,
    showTopicForm: false,
    expanded: false,
  }),
  mounted() {
    this.loadTopics();
  },
  methods: {
    formatDate(date) {
      if (!date) return '—';
      return this.$moment(date).fromNow();
    },
    async loadTopics() {
      this.topicsError = '';
      this.topicsLoading = true;
      try {
        const response = await api.forumTopics();
        this.topics = response.topics || [];
        if (this.topics.length && !this.selectedTopic) {
          this.selectTopic(this.topics[0]);
        }
      } catch (error) {
        this.topicsError = error.message;
      } finally {
        this.topicsLoading = false;
      }
    },
    async selectTopic(topic) {
      this.selectedTopic = topic;
      this.messageText = '';
      try {
        const response = await api.forumMessages(topic.id);
        this.messages = response.messages || [];
      } catch (error) {
        this.$notifyError(error.message);
      }
    },
    resetTopicForm() {
      this.topicForm = { title: '', message: '' };
      this.showTopicForm = false;
    },
    async createTopic() {
      this.topicLoading = true;
      try {
        const response = await api.createTopic({
          title: this.topicForm.title,
          message: this.topicForm.message,
          author: this.$store.getters.user?.username || 'anonymous',
        });
        this.resetTopicForm();
        await this.loadTopics();
        if (response.topic) {
          const created = this.topics.find((t) => t.id === response.topic.id) || response.topic;
          this.selectTopic(created);
        }
      } catch (error) {
        this.$notifyError(error.message);
      } finally {
        this.topicLoading = false;
      }
    },
    async sendMessage() {
      if (!this.selectedTopic) return;
      this.messageLoading = true;
      try {
        await api.sendMessage(this.selectedTopic.id, {
          text: this.messageText,
          author: this.$store.getters.user?.username || 'anonymous',
        });
        this.messageText = '';
        await this.selectTopic(this.selectedTopic);
      } catch (error) {
        this.$notifyError(error.message);
      } finally {
        this.messageLoading = false;
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
  gap: 12px;
  flex-wrap: wrap;
}

.panel-title {
  margin: 0;
}

.actions {
  display: flex;
  gap: 8px;
}

.primary,
.secondary,
.chip {
  border-radius: 10px;
  padding: 10px 14px;
  cursor: pointer;
  border: 1px solid #2c2c48;
  background: transparent;
  color: #cfd5f7;
}

.primary {
  background: linear-gradient(135deg, #6c7bff, #2ec7ff);
  color: #0b0b15;
  border: none;
}

.chip {
  background: rgba(255, 255, 255, 0.04);
}

.layout {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 16px;
  margin-top: 16px;
}

.topics,
.messages {
  background: #0f0f18;
  border: 1px solid #1b1b2a;
  border-radius: 12px;
  padding: 12px;
  min-height: 420px;
}

.topics-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.topic-form,
.message-form {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
}

.input {
  background: #0c0c15;
  border: 1px solid #2c2c48;
  color: #e6e8ff;
  padding: 10px 12px;
  border-radius: 10px;
  width: 100%;
}

.topic-actions {
  display: flex;
  gap: 8px;
}

.topic-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.topic-card {
  padding: 10px;
  border-radius: 10px;
  border: 1px solid #1b1b2a;
  background: rgba(255, 255, 255, 0.02);
  cursor: pointer;
  transition: all 0.15s ease;

  &.active {
    border-color: #6c7bff;
    background: rgba(108, 123, 255, 0.08);
  }
}

.title {
  font-weight: 700;
}

.meta {
  color: #9da3c5;
  font-size: 12px;
  margin: 4px 0 0;
}

.message-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
}

.message-card {
  padding: 10px;
  border: 1px solid #1b1b2a;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.02);
}

.message-author {
  font-weight: 700;
}

.message-text {
  margin: 4px 0;
}

.message-date {
  color: #9da3c5;
  font-size: 12px;
}

.state {
  margin-top: 8px;
  color: #9da3c5;

  &.error {
    color: #fca5a5;
  }
}

.empty {
  color: #9da3c5;
}

@media (max-width: 1100px) {
  .layout {
    grid-template-columns: 1fr;
  }
}
</style>
