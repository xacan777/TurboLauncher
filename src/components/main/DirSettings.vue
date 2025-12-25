<template lang="pug">
UiModal(
  v-if="isShowDirSettings"
  header="Настройка загрузки игрового клиента"
  image="@/assets/images/modal-1.png"
  :width="400"
  @close="setStateModalDirSettings(false)"
  @update:state="setStateModalDirSettings"
)
  template(#content)
    .install
      .install-info
        .install-info-title Путь к клиенту
        .install-info-path(
          ref="path"
          v-tippy=`{
            content: pathInstall,
            placement: 'bottom',
            zIndex: 999999999999999,
            onShow: () => isOverflowText }`
          ) {{ formatPath }}
      .install-icon(@click="onOpenPath")
        IconFolderSettings
  template(#footer)
    UiButtonPrimary(
      @click="onSavePath()"
      :disabled="v$.$invalid"
      text="Закрыть"
    ) Сохранить
</template>

<script>
import IconFolderSettings from '@/assets/icons/icon-folder-settings.vue';
import UiButtonPrimary from '@/uikit/buttons/ui-button-primary.vue';
import UiModal from '@/uikit/ui-modal.vue';
import { mapActions, mapGetters, mapMutations } from 'vuex';
import { ipcRenderer } from 'electron';
import validationMixin from '@/mixins/validation-mixin';
import { required } from '@vuelidate/validators';

export default {
  name: 'ModalDirSettings',
  mixins: [validationMixin],
  components: { UiModal, UiButtonPrimary, IconFolderSettings },
  data: () => ({
    pathInstall: null,
  }),
  mounted() {
    if (this.download) {
      this.pathInstall = this.download.path;
    }

    ipcRenderer.on('selectFolder', (event, path) => {
      if (path.length > 0) {
        this.pathInstall = path.length ? path[0] : null;
      }
    });
  },
  validations: {
    pathInstall: {
      required,
    },
  },
  computed: {
    ...mapGetters(['isShowDirSettings', 'download']),
    isOverflowText() {
      return this.pathInstall?.length > 25;
    },
    downloadPath() {
      return this.download.path;
    },
    formatPath() {
      return this.pathInstall ? this.pathInstall.replaceAll('\\\\', '\\') : 'Не выбран';
    },
  },
  watch: {
    downloadPath() {
      this.pathInstall = this.downloadPath;
    },
  },
  methods: {
    ...mapMutations(['setStateModalDirSettings', 'setDownloadVerified']),
    ...mapActions(['setDownloadPath']),
    existClientPath(path) {
      const pathSplit = path.split('\\');
      const pathName = pathSplit[pathSplit.length - 1];
      return pathName === 'client' ? path : `${path}\\R2Club`;
    },
    onOpenPath() {
      if (this.download.state === 'download' || this.download.state === 'verify') {
        this.$notify({
          title: 'Ошибка',
          group: 'main',
          text: 'Нельзя изменить путь к клиенту во время загрузки или проверки',
          type: 'error',
          zIndex: 999999999999999,
        });
        return;
      }
      this.$appEvent('selectFolder', {});
    },
    onSavePath() {
      if (this.v$.$invalid) return;
      this.setDownloadPath(this.pathInstall ? this.pathInstall : this.downloadPath);
      this.setDownloadVerified(false);
      this.setStateModalDirSettings(false);
    },
  },
};
</script>

<style lang="scss" scoped>
.install {
  width: 100%;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;

  &-info {
    max-width: 80%;

    &-title {
      margin-bottom: 10px;
      font-family: 'Gilroy';
      font-style: normal;
      font-weight: 600;
      font-size: 14px;
      color: #ffffff;
    }

    &-path {
      font-family: 'Gilroy';
      font-style: normal;
      font-weight: 600;
      font-size: 14px;
      color: #4e4e72;

      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
  }

  &-icon {
    color: #4e4e72;
    cursor: pointer;
    transition: all 0.2s ease;

    &:hover {
      color: #6d6d95;
    }
  }
}
</style>
