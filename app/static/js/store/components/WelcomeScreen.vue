<!-- This is the first screen seen by the user once the application is loaded.
Here the user selects the answer type (angular, spectral) before continue
to the materials and initial parameters screen. We call the action setCurrentPage
to change the value of the current page on the sate of vuex once the user
click the go button and the bottom of the screen. -->
<template>
  <div class="main-container container">
    <div class="d-flex justify-content-start align-items-center w-100">
      <img class="m-0 mb-2 p-0" :src="group_logo" alt="semillero">
    </div>
    <div class="welcome-header w-100 d-flex justify-content-center align-items-center">
      <h3 class="w-100 mt-3 mb-0 text-center">Computational Tool for Ellipsometric Spectroscopy</h3>
    </div>
    <!-- Container for the introduction to the method -->
    <div class="introduction">
      <div>
        <div class="text-justify intro-text">
          This web application is a tool for the analysis of ellipsometric
          spectroscopy data. It has the ability to create multilayer system models of isotropic
          materials using the Transfer Matrix Method, including the possibility to implement
          Effective Medium Theories and  Dispersion Formulas. At the end the user will have
          the option to upload experimental data to compare with the created models calculating
          the goodness of fit (GOF), determined by the χ2 value.</br> </br> 

          <p>To know more about the optical theory or the code of this application 
          <a href="https://www.lifeder.com/chi-cuadrada/">click here</a> . </p>

        </div>
      </div>
      <div>
        <img :src="method_intro" alt="transfer_matrix_method" class="intro-img">
      </div>
    </div>
    <!-- Dropdown to select the answer -->
    <div class="d-flex w-50 justify-content-center align-items-center mt-5">
      <b-form-select v-model="type" :options="options" id="input-type"></b-form-select>
      <!-- Button to continue to the next page -->
      <b-button variant="info" class="ml-3" @click="goToMethods">Go</b-button>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions, mapMutations } from "vuex"
export default {
  data() {
    return {
      group_logo: this.$root.$data.django_context.group_logo,
      method_intro: this.$root.$data.django_context.method_intro,
      // Key to store the answer
      type: null,
      // Type of answers allowed
      options: [
        { value: null, text: 'Select Answer' },
        { value: 'angular', text: 'Angular' },
        { value: 'espectral', text: 'Spectral' },
      ],
    }
  },
  computed: {
    ...mapState({
    }),
  },
  methods: {
    ...mapMutations({
      setCurrentPage: "transfer/setCurrentPage", // action to change the current page to the second one
      setType: "transfer/setType", // action to store the answer selected by the user
    }),
    // When the 'Go' button is clicked we will store the answer and change screen
    goToMethods() {
      this.setType(this.type)
      if (this.type) {
        this.setCurrentPage('second')
      }
    }
  },
  mounted() {
  },
}
</script>