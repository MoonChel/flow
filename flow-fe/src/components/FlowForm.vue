<template>
  <FormulateForm v-model="formValues" @submit="submitForm">
    <template v-if="step">
      <div v-for="field in step.form.fields" :key="field.name">
        <FormulateInput
          :label="field.label"
          :type="field.type"
          :name="field.name"
          :validation="field.validation"
        />
      </div>
    </template>
    <br />

    <FormulateInput type="submit" label="Submit" />

    <br />

    {{ step }}
  </FormulateForm>
</template>

<script>
import api from "@/api";

export default {
  created() {
    api.getActiveStep().then((response) => {
      this.step = response.data;
    });
  },

  data() {
    return {
      step: null,
      formValues: {},
    };
  },

  methods: {
    submitForm() {
      api.submitForm(this.formValues).then((response) => {
        this.step = response.data;
      });
    },
  },
};
</script>

<style>
</style>
