<!-- This file is in charge to show a loading pop up to tell the
  user that the server is busy processing its request. This component is 
 shared across all the vue components. -->
<template>
  <b-modal 
    id="loading-popup"
    class="loading-popup" 
    centered 
    hide-footer 
    hide-header
    no-close-on-esc
    no-close-on-backdrop
  >
    <div class="d-flex flex-column justify-content-center align-items-center">
      <b-spinner
        variant="secondary"
        type="grow"
      ></b-spinner>
      <p class="text-center font-weight-bold m-0 p-0 mt-3">Calculating...</p>
    </div>
  </b-modal>
</template>
<script>
import { mapState } from 'vuex'

export default {
  computed: mapState({
    isLoadingResult: (state) => state.transfer.isLoadingResult,
    isLoadingComparisonResult: (state) => state.transfer.isLoadingComparisonResult,
  }),
  watch: {
    isLoadingResult: {
      handler(isLoading) {
        let action = "hide"
        if (isLoading){
          action = "show"
        }
        this.$root.$emit(`bv::${action}::modal`, "loading-popup")
      },
    },
    isLoadingComparisonResult: {
      handler(isLoading) {
        let action = "hide"
        if (isLoading){
          action = "show"
        }
        this.$root.$emit(`bv::${action}::modal`, "loading-popup")
      },
    },
  }
}
</script>
<style lang="scss">
#loading-popup {
  .modal-content {
    padding: 0.4rem;
    border-radius: 20px;
    border: none;
  }
}
</style>