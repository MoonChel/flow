<template>
  <FormulateForm>
    <div v-for="field in form.fields" :key="field.name">
      <FormulateInput
        :label="field.label"
        :type="field.type"
        :validation="field.validation"
      />
    </div>

    <br />
    <FormulateInput type="submit" :label="form.submit.label" />
  </FormulateForm>
</template>

<script>
// recruitment form processing
export default {
  data() {
    return {
      form: {
        submit: {
          label: "Submit",
        },
        fields: [
          {
            label: "First name",
            name: "first_name",
            type: "text",
            validation: ["required"],
          },
          {
            label: "Last name",
            name: "last_name",
            type: "text",
            validation: ["required"],
          },
          {
            label: "Email",
            name: "email",
            type: "email",
            validation: ["required"],
          },
        ],
      },
    };
  },
};
</script>

<style>
</style>
