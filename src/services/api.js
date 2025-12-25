import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL || 'http://localhost:5000/api',
  timeout: 8000,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const message =
      error?.response?.data?.error ||
      error?.message ||
      'Не удалось выполнить запрос. Проверьте соединение.';
    return Promise.reject(new Error(message));
  }
);

export const api = {
  health() {
    return apiClient.get('/health');
  },
  login(payload) {
    return apiClient.post('/auth/login', payload);
  },
  register(payload) {
    return apiClient.post('/auth/register', payload);
  },
  serverStatus() {
    return apiClient.get('/server/status');
  },
  news() {
    return apiClient.get('/news');
  },
  leaderboardLevels(params) {
    return apiClient.get('/leaderboard/levels', { params });
  },
  leaderboardPower(params) {
    return apiClient.get('/leaderboard/power', { params });
  },
  droplist(params) {
    return apiClient.get('/droplist', { params });
  },
  enhancement(params) {
    return apiClient.get('/enhancement', { params });
  },
  forumTopics() {
    return apiClient.get('/forum/topics');
  },
  createTopic(payload) {
    return apiClient.post('/forum/topics', payload);
  },
  forumMessages(topicId) {
    return apiClient.get(`/forum/topics/${topicId}/messages`);
  },
  sendMessage(topicId, payload) {
    return apiClient.post(`/forum/topics/${topicId}/messages`, payload);
  },
};

export default apiClient;
