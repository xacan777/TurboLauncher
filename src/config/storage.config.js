import { useStorage } from 'vue3-storage';

const config = {
  namespaced: 'launcher_',
};

export const storageConfig = config;
export const storage = useStorage(storageConfig.namespaced);
