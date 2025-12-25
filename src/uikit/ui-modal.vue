<template lang="pug">
.ui-modal(@click="onClickAwayCheck")
  .ui-modal-over
  .ui-modal-frame
    .ui-modal-frame-position(v-long-modal ref="modalFrame" :class="{ 'fixed': isFixed }")
      .ui-modal-frame-body(:style="{ 'max-width': `${width + 100}px` }")
        .ui-modal-frame-image(
          v-if="image"
          )
          img(src="@/assets/images/modal-1.png")
        .ui-modal-frame-container(:style="{ 'max-width': image ? `${width - 100}px` : '100%' }")
          .ui-modal-frame-body-close(
            @click="onCloseByClick(), onUpdateStateModal(false)"
            v-if="withClose")
              IconClose
          .ui-modal-frame-body-header(v-if="header") {{ header }}
          template(v-if="form")
            form(@submit.prevent.stop="form")
              .ui-modal-frame-body-content
                slot(name="content")
              .ui-modal-frame-body-footer
                slot(name="footer")
          template(v-else)
            .ui-modal-frame-body-content
              slot(name="content")
            .ui-modal-frame-body-footer
              slot(name="footer")

</template>

<script>
import IconClose from '@/assets/icons/icon-close.vue';
import { mapActions } from 'vuex';

// eslint-disable-next-line no-unused-vars
const onUpdateModalSize = (el) => {
  const frame = el.querySelector('.ui-modal-frame-body');
  const { height } = frame.getBoundingClientRect();
  const wHeight = window.innerHeight;
  if (height >= wHeight) el.classList.add('long');
  else el.classList.remove('long');
};

export default {
  name: 'ui-modal',
  directives: {
    longModal: {
      mounted(el) {
        onUpdateModalSize(el);
        window.onresize = () => {
          onUpdateModalSize(el);
        };
      },
      updated(el) {
        onUpdateModalSize(el);
      },
    },
  },
  props: {
    image: {
      type: String,
      default: '',
    },
    withClose: {
      type: Boolean,
      default: true,
    },
    width: {
      type: Number,
      default: 500,
      required: false,
    },
    header: {
      type: String,
      default: '',
      required: false,
    },
    form: {
      type: Function,
      default: null,
    },
    isFixed: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['update:state', 'close'],
  mounted() {
    document.body.style.overflow = 'hidden';
  },
  unmounted() {
    document.body.style.overflow = 'auto';
  },
  computed: {
    imagePath() {
      return this.image;
    },
  },
  methods: {
    ...mapActions(['addModalIndex', 'removeModalIndex']),
    onCloseByClick() {
      this.$emit('close');
    },
    onUpdateStateModal(state) {
      this.$emit('update:state', state);
    },
    onClickAwayCheck(e) {
      const isSelectedTextDetected = this.getSelectedText() === '';
      if (!isSelectedTextDetected) {
        return;
      }
      const { modalFrame } = this.$refs;
      if (e.target.contains(modalFrame)) {
        this.onCloseByClick();
        this.onUpdateStateModal(false);
      }
    },
    getSelectedText() {
      let text = '';
      if (typeof window.getSelection !== 'undefined') {
        text = window.getSelection().toString();
      } else if (typeof document.selection !== 'undefined' && document.selection.type === 'Text') {
        text = document.selection.createRange().text;
      }
      return text;
    },
  },
  components: { IconClose },
};
</script>

<style lang="scss" scoped>
.ui-modal {
  &-over {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 999999999;
  }

  &-frame {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    overflow-y: auto;
    z-index: 9999999999;

    &-image {
      width: 100%;
      max-width: 200px;
      height: 100%;

      & img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
    }

    &-position {
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;

      &.fixed {
        margin-top: 5vh;
        display: flex;
        align-items: flex-start !important;
        justify-content: center !important;
      }

      &.long {
        position: relative;
        top: 5%;
        height: auto;
      }
    }

    &-container {
      width: 100%;
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      justify-content: center;
      padding: 30px;
      box-sizing: border-box;
    }

    &-body {
      display: flex;
      position: relative;
      width: 100%;
      background: #12121b;
      min-height: 40px;

      &-close {
        position: absolute;
        top: 16px;
        right: 16px;
        cursor: pointer;
      }

      &-content {
        width: 100%;
      }

      &-header {
        font-family: 'Gilroy';
        font-style: normal;
        font-weight: 700;
        font-size: 18px;
        color: #ffffff;
        margin-bottom: 60px;
        line-height: 160%;
        text-align: left;
      }

      &-footer {
        margin-top: 60px;
        width: 100%;
        display: flex;
        justify-content: center;
      }
    }
  }
}
</style>
