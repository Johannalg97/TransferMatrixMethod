<!-- This file represents the graph screen, where reflectance, 
transmittance, and abrosbance are shown. It is the third page -->
<template>
  <div class="main-container container">
    <!-- Titles for the third screen where grpahics are being showed -->
    <div class="w-100 calculations-title d-flex justify-content-between align-items-center">
      <h2 class="m-0 p-0">Calculations</h2> 
    </div>
    <!-- Vue component to render grpahic as a line chart 
    all the parameters inside are called from 'props' and
    'data' following the documentation provided by the
    dependency https://vue-chartjs.org/guide/#creating-your-first-chart-->
    <div class="d-flex-justify-content-center align-items-start row w-100">
      <div class="my-4 col-8">
        <div class="espectral-table-title align-self-start">
          Graphic
        </div>
        <LineChartGenerator
          :chart-options="chartOptions"
          :chart-data="chartData"
          :chart-id="chartId"
          :dataset-id-key="datasetIdKey"
          :plugins="plugins"
          :css-classes="cssClasses"
          :styles="styles"
          :width="width"
          :height="height"
        />
        <!-- Container for the dropdown and 'download button' -->
        <div class="d-flex justify-content-center align-items-center mt-3">
          <!-- Group of input option in the broswer, the groups contain a label for the input
          and the input that can be for text, files, dropdown... In this case is a dropdown,
          which is called a select in raw HTML and b-form-select on Bootstrap VUE -->
          <b-form-group 
            label="" 
            label-for="graph-download"
            label-align-sm="right"
            class="d-flex align-items-center mr-3 mb-0"
          >
            <!-- The option selected by the user is going to be stored at the download
            key on the data() below-->
            <b-form-select class="ml-4" v-model="download" id="graph-download">
              <!-- Render each option inside of downloadOptions in data(), the value for 
              each option corresponds to the value key, and the text shown to the user 
              corresponds to the text key. On the backend we will receive the value option, 
              while the text option is just for visualization at front end -->
              <b-form-select-option 
                :value="option.value"
                v-for="(option, index) in downloadOptions"
                :key="index" 
              >
                {{ option.text }}
              </b-form-select-option>
            </b-form-select>
          </b-form-group>
          <!-- Button to download the graphic data, once it is clicked the method downloadData
          is called and executed from the methods() section below. Class and variant only
          gives built-in bootstrap styles to the button -->
          <b-button class="ml-3" variant="success" @click="downloadGraphData">Download</b-button>
        </div>
      </div>
      <div class="d-flex flex-column align-items-center justify-content-between col-4 mt-4 w-100">
        <div class="d-flex justify-content-center align-items-center flex-column w-100 mb-2">
          <div class="espectral-table-title align-self-start mb-4">
            Refractive Indexes
          </div>
          <b-table 
            v-if="type === 'angular'"
            caption-top
            responsive
            hover 
            :items="items" 
            :fields="fields"
            head-variant="light"
            sticky-header="500px"
          ></b-table>
          <div v-else class="spectral-table-container">
            <table class="table table-fit" >
              <thead class="thead-light">
                <tr>
                  <th scope="col">
                    Wave Length
                  </th>
                  <th scope="col" v-for="(material, index) in Object.keys(result.refractive_indexes_by_material)" :key="index">
                    {{material.charAt(0).toUpperCase() + material.slice(1)}}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="index in Array.from({length: result.x_range.length}, (v, i) => i)" :key="index">
                  <td >
                    {{result.x_range[index]}}
                  </td>
                  <td v-for="(material, indexM) in Object.keys(result.refractive_indexes_by_material)" :key="indexM">
                    {{result.refractive_indexes_by_material[material].replaceAll('[', '').replaceAll(']', '').split(',')[index]}}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <b-button class="mt-0" variant="success" @click="downloadTableData">Download Table</b-button>
        </div>
        <div class="d-flex justify-content-center align-items-center flex-column w-100">
          <div class="espectral-table-title align-self-start mb-4 mt-2">
            Experimental Data
          </div>
          <p class="m-0 p-0 my-1 experimental-data-text">To upload experimental data and compare it with the reflectance data obtained, please click the button below.</p>
          <b-button variant="info" class="mt-3" @click="goToExperimentalData">Upload experimental data</b-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// Import vuex to have access to the central storage of information. This storage can be visible
// from the different .vue files in the project, so it allows us to share data between components
import { mapState, mapActions, mapMutations } from "vuex"
// Import components from the dependency installed to create graphs
import { Line as LineChartGenerator } from 'vue-chartjs/legacy'

// Import components for graphs according to the dependency documentation
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  CategoryScale,
  PointElement
} from 'chart.js'

// Register components for graphs to make them available in this script
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  CategoryScale,
  PointElement
)

export default {
  components: {
    // Make the linechartgenerator component available to called on the html section above
    LineChartGenerator
  },
  // Props that GraphScreen as component can receive to
  // customize the graph. Each one has a default value to the keys
  // are not required to be passed to the component when it is called
  // from other vue files, as in this case (from the App.vue file)
  props: {
    chartId: {
      type: String,
      default: 'line-chart'
    },
    datasetIdKey: {
      type: String,
      default: 'label'
    },
    width: {
      type: Number,
      default: 1000
    },
    height: {
      type: Number,
      default: 500
    },
    cssClasses: {
      default: '',
      type: String
    },
    styles: {
      type: Object,
      default: () => {}
    },
    plugins: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      // Option selected on dropdown by user
      download: null,
      // Options for the dropdown to download data
      downloadOptions: [
        { value: null, text: 'Select an option...' },
        { value: 'reflectance', text: 'Reflectance' },
        { value: 'transmittance', text: 'Transmittance' },
        { value: 'absorptance', text: 'Absorptance' },
      ],
      // Chart initial data
      chartData: {
        labels: [
        ],
        datasets: [
        ]
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        tooltips: {
            callbacks: {
              label: function (tooltipItem, data) {
                return Number(tooltipItem.yLabel).toFixed(4);
              }
            }
          },
        },
      fields: [
        {
          key: 'material',
          sortable: true,
          isRowHeader: true,
        },
        {
          key: 'value',
          sortable: true,
          label: 'Refractive Index',
        },
      ],
    }
  },
  computed: {
    ...mapState({
      result: state => state.transfer.result,
      type: state => state.transfer.type,
    }),
    items() {
      let items = []
      if (this.result && this.result.refractive_indexes_by_material) {
        if (this.type === 'angular') {
          Object.keys(this.result.refractive_indexes_by_material).forEach(material => {
            items.push(
              { 
                isActive: true, 
                material: material.charAt(0).toUpperCase() + material.slice(1),
                value:  this.result.refractive_indexes_by_material[material]
              }
            )
          });
        } 
      }
      return items
    }
  },
  methods: {
    ...mapActions({
      downloadData: "transfer/downloadData",
    }),
    ...mapMutations({
      setCurrentPage: "transfer/setCurrentPage", // action to change the current page to the fourth one
    }),
    downloadGraphData() {
      if (this.download) {
        let graphData = {
          x: this.result.x_range,
          y: this.result[this.download],
          answer: this.type,
        }
        const data = {
          source: 'graph',
          data: graphData,
          type: this.download,
        } 
        this.downloadData(data)
      }
    },
    downloadTableData() {
      const data = {
        source: 'table',
        data: {
          ...this.result.refractive_indexes_by_material,
          x: this.type === 'angular' ? this.result.x_table : this.result.x_range,
          answer: this.type,
        },
      } 
      this.downloadData(data)
    },
    formatChartData() {
      // Format data as 
      // labels for the x values and one javascript object
      // for each curve including the name of the curve, styles
      // for the lines and current values on 'y' axis.
      let data = {}
      data.labels = this.result.x_range;
      data.datasets = []
      data.datasets.push({
        label: 'Reflectance',
        backgroundColor: '#f87979',
        data: this.result.reflectance,
        borderColor: '#f87979',
        fill: false
      })
      data.datasets.push({
        label: 'Absortance',
        backgroundColor: '#A4C098',
        data: this.result.absortance,
        borderColor: '#A4C098',
        fill: false
      })
      data.datasets.push({
        label: 'Transmittance',
        backgroundColor: '#2ACAEA',
        data: this.result.transmittance,
        borderColor: '#2ACAEA',
        fill: false
      })
      return data
    },
    goToExperimentalData() {
      this.setCurrentPage('fourth')
    },
  },
  // If the values for the graph changes the graph will be updated in real time
  watch: {
    result: {
      deep: true,
      handler(newValue) {
        if (this.result) {
          this.chartData = this.formatChartData()
        }
      }
    },
  },
  // Once this screen is redered we get values to plot the chart
  mounted() {
    if (this.result) {
      this.chartData = this.formatChartData()
    }
  },
}
</script>