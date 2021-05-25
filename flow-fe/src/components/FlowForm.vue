<template>
  <div>
    <div class="columns">
      <div class="column col-4">
        <template v-if="process">
          <h4>{{ process.label }}</h4>
          <div v-for="step in process.steps" :key="step.name" class="accordion">
            <input type="radio" :id="step.name" name="accordion-radio" hidden />
            <label class="accordion-header" :for="step.name">
              {{ step.label }}
            </label>

            <div class="accordion-body">
              <ul v-if="step.form_value" class="menu menu-nav">
                <li class="divider" data-content="FORM"></li>
                <li
                  v-for="(value, key) in step.form_value.values"
                  :key="key"
                  class="menu-item"
                >
                  <a href="#"> {{ key }}: {{ value }} </a>
                </li>
                <li class="divider" data-content="ACTION"></li>
                <li class="menu-item">action: {{ step.form_value.action }}</li>
              </ul>
              <ul v-else>
                <li class="menu-item">Here will be form data</li>
              </ul>
            </div>
          </div>
        </template>
      </div>

      <div v-if="step" class="column col-6">
        <h3>{{ step.label }}</h3>

        <template v-if="step.form">
          <FormulateForm v-model="formValues">
            <div v-for="field in step.form.fields" :key="field.name">
              <FormulateInput
                :label="field.label"
                :type="field.type"
                :name="field.name"
                :validation="field.validation"
              />
            </div>

            <br />

            <div class="actions">
              <FormulateInput
                type="button"
                :label="action.label"
                @click="submitForm(action.name)"
                v-for="action in step.form.actions"
                :key="action.name"
              />
            </div>
          </FormulateForm>
        </template>

        <template v-if="step.actions.length > 0">
          <p>Flow will apply next actions in the background:</p>
          <ul>
            <li v-for="action in step.actions" :key="action.name">
              {{ action.label }}
            </li>
          </ul>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/api";

export default {
  created() {
    api.getProcess().then((response) => {
      this.process = response.data;
    });

    this.getActiveStep();
  },

  data() {
    return {
      step: null,
      process: null,
      formValues: {},
    };
  },

  methods: {
    getActiveStep() {
      api.getActiveStep().then((response) => {
        this.step = response.data;

        if (response.data.form_value) {
          this.formValues = response.data.form_value;
        }
      });
    },
    submitForm(action) {
      const form = {
        values: this.formValues,
        action: action,
      };

      api.submitForm(form).then(() => {
        this.$toasted.success("Success");

        api.getProcess().then((response) => {
          this.process = response.data;
        });

        this.getActiveStep();
      });
    },
  },
};
</script>

<style>
.actions {
  display: flex;
  margin-bottom: 1em;
}
.actions .formulate-input {
  margin-right: 1em;
  margin-bottom: 0;
}
</style>
