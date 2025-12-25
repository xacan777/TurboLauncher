<!-- eslint-disable vuejs-accessibility/alt-text -->
<!-- eslint-disable vuejs-accessibility/form-control-has-label -->
<template>
  <div class="bg__item" :style="backgroundStyle">
    <form action="https://l2.club/ru/pay" method="get" min="50" target="_blank">
      <section class="donat">
        <div class="container_bonus">
          <div class="donat__content">
            <div class="donate__left">
              <h3 class="donat__title">Купить Золотые Монеты</h3>
              <div class="donat__header">
                <!-- <div class="server">
                              <div class="server__select">
                                  <select required name="prefix" id="server" style="background-color: black;">
                                      <option VALUE="1200">L2.CLUB X1200</option>
                                  </select>
                              </div>
                              <input id="account_name" type="text" class="server__input" name="account"
                                  placeholder="Твой никнейм" value="" maxlength="17" required="required">
                          </div> -->
                <div class="donat__monet">
                  <p>
                    Укажи количество:
                    <span id="#morecoinsmorebonuses"><br />больше Монет — больше подарков</span>
                  </p>
                  <input
                    type="text"
                    class="donat__monet-input"
                    id="input-number"
                    name="sum"
                    required="required"
                    v-model="value"
                    @update:model-value="onUpdateValue"
                  />
                </div>
              </div>
              <div class="range">
                <h3 class="range__title">
                  <img
                    src="@/assets/resources/images/bonusline/ru.png"
                    class="promo-image"
                    style="border-radius: 10px"
                  />
                  <br />
                  Двигай ползунок вправо — получай больше подарков
                </h3>

                <div class="range__block">
                  <div class="rangeSlide" id="rangeSlide" ref="slider"></div>
                </div>
              </div>
              <div class="donat__bottom">
                <div class="payment">
                  <h3 class="payment__title">Осталось только оплатить удобным способом</h3>
                  <p class="payment__subtitle">
                    После оплаты Монеты придут сразу, а подарки – через пару минут
                  </p>
                  <div id="instant-pay-container" style="margin-bottom: 35px; display: none">
                    <div class="instant-pay-container">
                      <div id="instant-pay" class="pay"></div>
                    </div>
                  </div>
                  <div class="payment__item">
                    <img src="/assets/payment-buttons/purple_card_68.png" alt="" />
                    <button type="button" class="payment__item-text eur" @click="createPayment">
                      <p>
                        Оплатить
                        <span class="orange"
                          >₽<b>{{ value }}</b></span
                        >
                        любой картой 💳
                      </p>
                      <span class="payment__text-mini">
                        <p style="font-weight: bold">
                          Все карты, Apple Pay, Google Pay через FreeKassa
                        </p>
                        <p style=""></p>
                      </span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div class="donate__right">
              <div class="present">
                <div data-hidden-on-server="1200"></div>
                <h3 class="present__title">
                  <img src="@/assets/gold/images/image/present.png" class="dont-show-gold" />
                  <div class="present__title-text">
                    Подарки к платежу
                    <span>
                      Бонусы приходят автоматически в течение нескольких минут после оплаты
                    </span>
                  </div>
                </h3>
                <div class="present__content">
                  <div
                    :class="['present__item', { active: min_price === activeMinPrice }]"
                    v-for="{ min_price, items } in items"
                    :key="min_price"
                    v-show="min_price === activeMinPrice || min_price === nextMinPrice"
                  >
                    <h4 class="present__item-title">
                      К платежу от <span>{{ min_price }} Монет:</span>
                    </h4>
                    <div
                      class="present__elem goldcoins300"
                      v-for="(item, itemIndex) in items"
                      :key="itemIndex"
                    >
                      <span class="present__icon">
                        <img :src="item.image" alt="" style="bottom: -6px; right: -1px" />
                      </span>
                      <template v-if="!item.url">
                        {{ item.name }}
                      </template>
                      <a :href="item.url" target="_blank" style="color: white" v-else
                        ><u>{{ item.name }}</u></a
                      >
                    </div>
                  </div>
                </div>
                <div class="present__bottom">больше Монет <span>— больше бонусов</span></div>
                <div class="present__show" onclick="$('.m_hide').slideToggle(500)">
                  Показать больше бонусов
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </form>
  </div>
</template>

<script>
import noUiSlider from 'nouislider';
// import 'nouislider/dist/nouislider.css';
import '@/assets/gold/js/noUISlider.min.css';
import '@/assets/gold/css/donate.min.css';

export default {
  name: 'App',
  data: () => ({
    value: 1000,
    sliderInstance: null,
    formLoading: false,
    items: [],
  }),
  mounted() {
    const { slider } = this.$refs; // slider is now the DOM element
    this.sliderInstance = noUiSlider.create(slider, {
      // Use 'slider', not 'slider.value'
      start: this.value,
      connect: 'lower',
      range: {
        min: 0,
        '10%': 300,
        '20%': 500,
        '30%': 900,
        '40%': 1500,
        '55%': 3000,
        '70%': 5000,
        '85%': 10000,
        '98%': 15000,
        max: 99999,
      },
      step: 1,
      pips: {
        mode: 'range',
        stepped: true,
        density: 3,
      },
      format: {
        from(value) {
          return parseInt(value, 10);
        },
        to(value) {
          return parseInt(value, 10);
        },
      },
    });

    this.sliderInstance.on('update', (values) => {
      console.log('test!!', values);
      this.value = parseInt(values[0], 10);
    });

    this.$http.get('getDonateBonus.php').then((data) => {
      console.log(data);
      this.items = data;
    });
  },
  methods: {
    onUpdateValue(val) {
      // eslint-disable-next-line eqeqeq
      this.sliderInstance.set(val == '' ? 0 : parseInt(val, 10));
    },
    createPayment() {
      if (this.formLoading) return;
      this.formLoading = true;

      this.$http
        .get('payment.php', {
          params: {
            user_id: this.$store.getters.user.mUserId.trim(),
            value: this.value,
          },
        })
        .then((data) => {
          console.log('data', data);
          const uri = typeof data.location === 'undefined' ? data[0] : data.location;
          setTimeout(() => {
            const win = window.open(
              uri,
              '_blank',
              `toolbar=1, scrollbars=1, resizable=1, frame=true, nodeIntegration=no, width=${1015}, height=${800}`
            );
            const timer = setInterval(() => {
              if (win.closed) {
                this.$router.push({ name: 'main' });
                clearInterval(timer);
              }
            }, 1000);
          }, 2000);
        })
        .catch((err) => {
          console.log(err);
        })
        .finally(() => {
          this.formLoading = false;
        });
    },
  },
  computed: {
    backgroundStyle() {
      return {
        // eslint-disable-next-line global-require
        background: `url(${require('@/assets/resources/image/new_club_bg.webp')}) top no-repeat !important`,
      };
    },
    activeMinPrice() {
      // Находим первый элемент, соответствующий условию
      const items = this.items.filter((item) => item.min_price <= this.value);

      if (items.length > 0) {
        return items[items.length - 1].min_price;
      }

      return null;
    },
    nextMinPrice() {
      if (!this.activeMinPrice && this.items.length > 0) {
        return this.items[0].min_price;
      }

      const findIndex = this.items.findIndex((item) => item.min_price === this.activeMinPrice);

      console.log(findIndex, findIndex !== this.items.length - 1);

      if (findIndex !== this.items.length - 1) {
        return this.items[findIndex + 1].min_price;
      }

      return null;
    },
  },
};
</script>

<style scoped>
@import '@/assets/gold/js/noUISlider.min.css';
@import '@/assets/gold/css/rus.css';
@import '@/assets/gold/css/main.css';
@import '@/assets/gold/css/nav.css';
@import '@/assets/gold/css/font.css';
@import '@/assets/gold/css/inner.css';
@import '@/assets/css/register.css';
@import '@/assets/css/download.css';
@import '@/assets/main/css/font.min.css';
@import '@/assets/main/css/header.css';
@import '@/assets/gold/css/donate.min.css';
@import '@/assets/gold/fonts/stylesheet.css';

body {
  background-size: contain;
}

button {
  text-align: left;
  padding: 0;
  border: none;
  font: inherit;
  color: inherit;
  background-color: transparent;
  /* отображаем курсор в виде руки при наведении; некоторые
  считают, что необходимо оставлять стрелочный вид для кнопок */
  cursor: pointer;
}

.announcekit-widget-floating-badge {
  display: none !important;
}

.present__item.active .present__elem {
  animation: iconBonus 1s ease forwards;
}

.present__item.active.opacity .present__elem {
  animation: none;
}

@keyframes iconBonus {
  0% {
    transform: scale(1);
  }

  50% {
    transform: scale(1.15);
  }

  100% {
    transform: scale(1);
  }
}

.range #rangeSlide .noUi-value-horizontal[data-value='99999'] {
  display: none;
}

@media (max-width: 768px) {
  .present__item.active .present__elem {
    display: inline-block;
  }

  .present__bottom {
    display: none;
  }

  .range {
    display: none;
  }

  .dont-show-gold {
    display: none;
  }

  .donat__monet-input {
    margin-top: 15px;
  }
}

.btn {
  background-color: transparent;
  border: 1px solid transparent;
  border-radius: 4px;
  color: #666;
  display: inline-block;
  font-family: Nunito, sans-serif;
  font-size: 0.8125rem;
  font-weight: 700;
  line-height: 1.25rem;
  padding: 0.4375rem 1.125rem;
  text-align: center;
  transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out,
    border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  vertical-align: middle;
}

.btn-primary {
  background-color: rgba(231, 32, 36, 0.8);
  border-color: rgba(231, 32, 36, 0.8);
  color: #fff;
}

.btn-sm {
  border-radius: 3px;
  font-size: 0.75rem;
  line-height: 1.25rem;
  padding: 0.25rem 0.75rem;
}

.btn {
  align-items: center;
  display: inline-flex;
  letter-spacing: 0.02em;
  position: relative;
}

.btn:not(:disabled):not(.disabled) {
  cursor: pointer;
}

a.btn {
  text-decoration: none;
}

.btn > .enter-icon {
  width: 16px;
  height: 16px;
  object-fit: contain;
  margin-right: 5px;
}

.btn:hover {
  background-color: rgba(231, 32, 36, 0.6);
}

.payment__item {
  width: 100%;
}

.instant-pay-container {
  background-color: white;
  border: 0;
  cursor: pointer;
  max-height: 64px;
  min-height: 32px;
  position: relative;
  height: 100%;
  border-radius: 4px;
  left: 0;
  top: 0;
  padding: 10px 0;
  width: 100%;
  z-index: 1;
  transition: background-color 200ms ease-in-out;

  display: flex;
  justify-content: center;
  align-items: center;
}

.instant-pay-container:hover {
  background-color: #f8f8f8;
}

.instant-pay-container .pay {
  background-origin: content-box;
  background-position: 50%;
  background-repeat: no-repeat;
  background-size: contain;

  width: 150px;
  height: 24px;
  object-fit: contain;
}

.instant-pay-container .pay.apple-pay {
  /* background-image: url('/assets/images/apple-pay.svg'); */
}

.payment__list .payment__item-text > p {
  font-size: 15px;
}

.payment__list .payment__item-text > span {
  font-size: 11px;
}

.donat__monet:before {
  content: 'Монет';
}

.server__input {
  padding-left: 20px;
}
</style>
