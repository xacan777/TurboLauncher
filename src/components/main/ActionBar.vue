<template lang="pug">
.bar(v-if="isClientReady")
    div(v-if="download.state === 'default'")
      template(v-if="isClientDownloaded")
        UiButtonPrimary(
          :loading="isStartLoading"
          size="small"
          @click="onStartVerifiedClient"
          ) Запустить клиент
      template(v-else)
        UiButtonPrimary(
        :loading="isStartLoading"
        size="small"
        @click="onStartDownloadClient"
        ) Скачать клиент
    .info(v-else-if="download.state === 'verify'")
      .bar-about
        .bar-about-value Проверка
      .bar-percent
        .bar-percent-value {{ percentVeirfy }}
      .bar-progress
        UiProgress(
          :finalValue="states.verify.finalValue"
          :currentValue="states.verify.currentValue"
          :notifyTippy="states.verify.notifyTippy"
        )
    .info(v-else-if="download.state === 'download'")
      .bar-about
        .bar-about-value Загрузка
      .bar-download
        .bar-download-file {{ states.download.fileName }}
        .bar-download-size
          | {{ formatBytes(states.download.currentValue) }}
          |  из
          |  {{ formatBytes(states.download.finalValue) }}
      .bar-percent
        .bar-percent-value {{ precentDownload }}
      .bar-progress
        .bar-progress-icon(@click="onClickPause")
          IconPlay.pause(v-if="isPause")
          IconPause(v-else)
        UiProgress(
          :finalValue="states.download.finalValue"
          :currentValue="states.download.currentValue"
          :notifyTippy="states.download.notifyTippy"
        )
    div(v-else-if="isClientOnReadyStart")
      UiButtonPrimary(
        size="small"
        :disabled="isStartGaming"
        @click="onStartClient"
        ) Запустить клиент
.bar(v-else)
  UiButtonPrimary(
    size="small"
    disabled
    ) Авторизация...
</template>

<script>
import UiButtonPrimary from '@/uikit/buttons/ui-button-primary.vue';
import UiProgress from '@/uikit/ui-progress.vue';
import { mapActions, mapGetters, mapMutations } from 'vuex';
import { ipcRenderer } from 'electron';
import IconPlay from '@/assets/icons/icon-play.vue';
import IconPause from '@/assets/icons/icon-pause.vue';
import utilsMixin from '@/mixins/utils-mixin';

export default {
  name: 'ActionBar',
  mixins: [utilsMixin],
  components: {
    UiButtonPrimary,
    UiProgress,
    IconPlay,
    IconPause,
  },
  data: () => ({
    isStartLoading: false,
    isStartGaming: false,
    isPause: false,
    states: {
      verify: {
        finalValue: 0,
        currentValue: 0,
        notifyTippy: 'Проверка файлов',
      },
      download: {
        finalValue: 0,
        currentValue: 0,
        notifyTippy: 'Загрузка файлов',
        fileName: '',
      },
    },
  }),
  mounted() {
    // this.setDownloadState('verify');
    ipcRenderer.on('download-progress', (event, { type, data }) => {
      if (type === 'verify') {
        this.setDownloadState('verify');
        this.clearDownloadState();
        const { total, current, fileName, isEnd } = data;
        if (isEnd) {
          this.states.verify.notifyTippy = 'Проверка файлов завершена';
          this.$notify({
            title: 'Проверка файлов завершена',
            group: 'main',
            text: current
              ? `${current} файлов не прошли проверку, начинаем загрузку`
              : 'Клиент готов к запуску',
            type: 'success',
          });
          this.setDownloadVerified(true);
        } else {
          this.states.verify.finalValue = total;
          this.states.verify.currentValue = current;
          this.states.verify.notifyTippy = `${fileName} (${current}/${total})`;
        }
      } else if (type === 'download') {
        this.setDownloadState('download');
        const { current, fileName, isEnd, totalSize } = data;
        console.log(data);
        if (isEnd) {
          this.$notify({
            title: 'Загрузка файлов завершена',
            group: 'main',
            text: 'Клиент готов к запуску',
            type: 'success',
          });
          this.states.download.fileName = fileName;
          this.states.download.notifyTippy = 'Загрузка файлов завершена';
        } else {
          this.states.download.fileName = fileName;
          this.states.download.finalValue = totalSize;
          this.states.download.currentValue = current;
          this.states.download.notifyTippy = `${fileName} (${this.formatBytes(
            current
          )}/${this.formatBytes(totalSize)})`;
        }
      } else if (type === 'chunk') {
        const { fileName, currentSize, fullSize, totalSize } = data;
        this.states.download.currentValue = totalSize;
        this.states.download.notifyTippy = `${fileName} [${this.formatBytes(
          currentSize
        )}/${this.formatBytes(fullSize)}]`;
      } else if (type === 'error') {
        this.clearDownloadState();
        this.setDownloadState('default');
        const { code, message } = data;
        this.$notify({
          title: 'В процессе загрузки произошла ошибка',
          group: 'main',
          text: `${code}: ${message}`,
          type: 'error',
        });
      } else {
        this.setDownloadClient(true);
        this.clearDownloadState();
        this.setDownloadState('play');
      }
    });
  },
  computed: {
    ...mapGetters(['download', 'isClientReady']),
    isClientDownloaded() {
      return this.download.downloaded;
    },
    isClientVerify() {
      return this.download.verified;
    },
    isClientOnReadyStart() {
      return this.isClientDownloaded && this.isClientVerify && this.download.state === 'play';
    },
    precentDownload() {
      // finalValue - 100%
      // currentValue - x%
      const { currentValue, finalValue } = this.states.download;
      return this.toFixedPercent((currentValue * 100) / finalValue);
      // return this.toFixedPercent(
      //   (this.states.download.currentValue / this.states.download.finalValue) * 100,
      // );
    },
    percentVeirfy() {
      return this.toFixedPercent(
        (this.states.verify.currentValue / this.states.verify.finalValue) * 100
      );
    },
  },
  methods: {
    ...mapMutations(['setDownloadState', 'setDownloadVerified']),
    ...mapActions(['setDownloadClient']),
    formatBytes(bytes, decimals = 2) {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const dm = decimals < 0 ? 0 : decimals;
      const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return `${parseFloat((bytes / k ** i).toFixed(dm))} ${sizes[i]}`;
    },
    clearDownloadState() {
      setTimeout(() => {
        this.isStartLoading = false;
      }, 1000);
    },
    toFixedPercent(percent) {
      return `${Math.round(percent.toFixed(2))}%`;
    },
    checkPathSelected() {
      if (!this.$store.getters.download.path) {
        this.$store.commit('setStateModalDirSettings', true);
        return false;
      }
      return true;
    },
    onStartDownloadClient() {
      if (!this.checkPathSelected()) return;
      if (this.isStartLoading) return;
      this.isStartLoading = true;
      ipcRenderer.send('download-path', this.$store.getters.download.path);
    },
    onStartVerifiedClient() {
      if (!this.checkPathSelected()) return;
      if (this.isStartLoading) return;
      this.isStartLoading = true;
      ipcRenderer.send('download-path', this.$store.getters.download.path);
    },
    onClickPause() {
      this.isPause = !this.isPause;
      ipcRenderer.send('download-pause');
    },
    onStartClient() {
      console.log('startClient');
      if (!this.checkPathSelected()) return;
      if (this.isStartGaming) return;
      this.isStartGaming = true;

      this.onReauthForGenerationToken()
        .then(() => {
          ipcRenderer.send('start-gaming', {
            param1: this.$store.getters.clientParams.param1,
            param2: this.$store.getters.clientParams.param2,
          });

          setTimeout(() => {
            this.isStartGaming = false;
          }, 5000);
        })
        .catch(() => {
          this.isStartGaming = false;
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.info {
  display: flex;
  align-items: center;
  height: 100%;

  &-percent {
    margin-right: 15px;
  }
}

.bar {
  height: 100%;
  display: flex;
  align-items: center;

  &-progress {
    height: 100%;
    background: linear-gradient(180deg, rgba(118, 118, 118, 0) 0%, rgba(93, 93, 93, 0.38) 100%);
    border-bottom: 2px solid #a1a1a1;
    padding: 0 16px;

    font-family: 'Gilroy';
    font-style: normal;
    font-weight: 700;
    font-size: 14px;

    display: flex;
    flex-direction: row;
    color: #ffffff;
    align-items: center;
    justify-content: center;

    &-icon {
      color: #ffd559;
      margin-top: 5px;
      margin-right: 15px;
      transform: scale(1.3);
      cursor: pointer;
      transition: all 0.2s ease;

      .pause {
        color: #ff5e5e;

        &:hover {
          color: #ff4444;
        }
      }

      &:hover {
        color: #ffa459;
      }
    }
  }

  &-percent {
    width: 70px;
    max-width: 70px;
    height: 100%;
    background: linear-gradient(180deg, rgba(78, 78, 114, 0) 0%, rgba(96, 96, 133, 0.38) 100%);
    border-bottom: 2px solid #6868ad;
    padding: 0 16px;

    font-family: 'Gilroy';
    font-style: normal;
    font-weight: 700;
    font-size: 14px;

    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;

    &-value {
      margin-top: 5px;
    }
  }

  &-about {
    height: 100%;
    background: linear-gradient(180deg, rgba(0, 209, 255, 0) 0%, rgba(0, 209, 255, 0.4) 100%);
    border-bottom: 2px solid #6aadbc;
    padding: 0 16px;

    font-family: 'Gilroy';
    font-style: normal;
    font-weight: 700;
    font-size: 12px;

    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;

    &-value {
      margin-top: 5px;
    }
  }

  &-download {
    width: 120px;
    max-width: 120px;
    height: 100%;
    background: linear-gradient(180deg, rgba(78, 114, 99, 0) 0%, rgba(79, 210, 116, 0.38) 100%);
    border-bottom: 2px solid #459660;
    padding: 0 16px;

    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;

    &-file {
      font-family: 'Gilroy';
      font-style: normal;
      font-weight: 700;
      font-size: 11px;
      margin-bottom: 5px;
      margin-top: 3px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      max-width: 100px;
    }

    &-size {
      font-family: 'Gilroy';
      font-style: normal;
      font-weight: 600;
      font-size: 10px;
      text-align: center;
      white-space: nowrap;
      color: rgba(255, 255, 255, 0.8);
    }
  }
}
</style>
