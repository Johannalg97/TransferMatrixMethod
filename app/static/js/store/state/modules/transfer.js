/* This file allows to centralize information on vuex. Here
we save data as the currentPage, to know where the user is located at any
moment on the application. The type or answer selected by the user
at the first screen, the result from the calculations on the second screen
(refractive indices, transmittance, reflectance and absorbance), the chi squared
calculated on third on the experimental data screen, the initial paramerers selected
and some loading variables to know when the server is busy calculating a response
for us.

The state is the actual data, actions are the functions in charge to 
execute the requests to the server and to call the mutations to 
update data on the sate.

*/


import Api from '../../utils/api'

// initial state
const state = ({
  currentPage: "first", // We start at the first page
  type: null, // Answer selected by the user
  isLoadingResult: false, // Variable to know if the backend is currently calculating the graphs data
  result: null, // Variable to store the graphs data as a result of the POST
  isLoadingComparisonResult: false,
  comparisonResult: null,
  initialParams: null,
})

// getters
const getters = {}

// actions
const actions = {
  // Action to send data to backend
  sendData({ commit, state }, data) {
    // Endpoint to receive data
    let url = `/api/v1/transfer-method/`
    // We indicate that the backend starts to calculate data
    commit('toggleLoadingResult', true)

    // Add the answer of the user
    data.append("answer", state.type)

    // Do the post to the server to the url indicated using the
    // data collected (payload)
    return Api.post(url, data).then((response) => {
      // Once we have a response and a confirmation from the 
      //server we store the results and change the status of the 
      // 'loadingResult' since now we have a result
      commit('setResult', response.data)
      commit('toggleLoadingResult', false)
      commit('setCurrentPage', 'third')
      return response.data
    }).catch(error => {
      // If an error occurs print it on the browser console
      commit('toggleLoadingResult', false)
      console.log(error);
    })
  },
  downloadData({ commit, state }, data) {
    // Endpoint to ask for files
    let url = `/api/v1/download-data/`
    return Api.post(url, data).then((response) => {
      const outputFilename = response.headers["content-disposition"].split('filename=')[1]

        // If you want to download file automatically using link attribute.
        const url = URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', outputFilename);
        document.body.appendChild(link);
        link.click();
      return response.data
    }).catch(error => {
      console.log(error);
    })
  },
  calculateChi({ commit, state }, data) {
    // Endpoint to ask for files
    let url = `/api/v1/calculate-chi/`
    commit('toggleLoadingComparisonResult', true)
    data.append("steps", state.initialParams.steps)
    data.append("initial_param", state.initialParams.initial_param)
    data.append("final_param", state.initialParams.final_param)

    return Api.post(url, data).then((response) => {
      commit('setComparisonResult', response.data)
      commit('toggleLoadingComparisonResult', false)
      return response.data
    }).catch(error => {
      commit('toggleLoadingComparisonResult', false)
      console.log(error);
    })
  },
}

// mutations
const mutations = {
  // Mutation to change page (initial, method selection or graphs screen)
  setCurrentPage (state, value) {
    state.currentPage = value
  },
  // Mutation to set the answer selected by the user
  setType (state, value) {
    state.type = value
  },
  // Mutation to save the results with the graphs data
  setResult (state, value) {
    state.result = value
  },
  // Mutation to change the status of the isLoadingResult key 
  // so we will know when the server is calculating results
  toggleLoadingResult(state, value) {
    state.isLoadingResult = value
  },
  // Mutation to know when we are waiting for a response
  // from the server to calculate chi quad and read the
  // experimental data uploaded by the user
  toggleLoadingComparisonResult(state, value) {
    state.isLoadingComparisonResult = value
  },
  setComparisonResult (state, value) {
    state.comparisonResult = value
  },
  setInitialParams(state, value) {
    state.initialParams = value
  }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
