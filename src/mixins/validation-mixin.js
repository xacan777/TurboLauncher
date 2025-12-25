import useVuelidate from '@vuelidate/core';

export default {
  data: () => ({
    v$: useVuelidate(),
  }),
  methods: {
    isError(obj) {
      return obj.$dirty && obj.$invalid;
    },
    setTouchValidator(obj, state = true) {
      if (state) obj.$touch();
    },
    clearValidator() {
      this.v$.$reset();
    },
  },
};
