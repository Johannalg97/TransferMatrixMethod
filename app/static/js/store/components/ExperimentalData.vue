<!-- This file represents the screen for experimental date, it is the fourth page -->
<template>
    <div class="main-container container">
      <div class="w-100 calculations-title d-flex justify-content-between align-items-center">
        <h2 class="m-0 p-0">Analysis of experimental data</h2> 
      </div>
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
        </div>
        <div class="d-flex flex-column align-items-center justify-content-between col-4 mt-4 w-100">
          <div class="d-flex justify-content-center align-items-center flex-column w-100 mb-2">
            <div class="espectral-table-title align-self-start mb-2">
              Upload Data
            </div>
            <img class="m-0 w-100 my-3 chi" :src="chi_img" alt="chiquad">
            <div class="w-100 my-2">
              <b-alert show variant="warning"><span class="font-weight-bold">χ²: </span> {{ comparisonResult ? comparisonResult.chi : '0.0' }}</b-alert>
            </div>
            <b-form-file class="mb-3" id="file-default" accept=".csv, .txt" :disabled="file !== null && file !== undefined" v-model="file" @input="plotData"></b-form-file>
            <b-table 
              caption-top
              responsive
              hover 
              :items="items" 
              :fields="fields"
              head-variant="light"
              sticky-header="500px"
            ></b-table>
            <b-button class="mt-0" variant="success">Optimize</b-button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
<script>
import { mapState, mapActions, mapMutations } from "vuex"
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
    LineChartGenerator
  },
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
      chi_img: this.$root.$data.django_context.chi,
      file: null,
      chartData: {
        labels: [
        ],
        datasets: [
        ],
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
          key: 'filename',
          sortable: true,
          isRowHeader: true,
        },
        {
          key: 'value',
          sortable: true,
          label: 'Chi Square',
        },
      ],
      items: [],
    }
  },
  computed: {
    ...mapState({
      result: state => state.transfer.result,
      comparisonResult: state => state.transfer.comparisonResult,
      type: state => state.transfer.type,
    }),
  },
  methods: {
    ...mapActions({
      calculateChi: "transfer/calculateChi",
    }),
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
      return data
    },
    getRandomColor() {
      let letters = '0123456789ABCDEF';
      let color = '#';
      for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    },
    plotData() {
      const formData = new FormData()
      formData.append("file", this.file)
      formData.append("answer", this.type)
      formData.append("calculated_reflectance", this.result.reflectance)
      this.calculateChi(formData)
    },
    addExperimentalData() {
      const color = this.getRandomColor()
      this.chartData.datasets.push({
        label: this.comparisonResult.filename,
        backgroundColor: color,
        data: this.comparisonResult.experimental_reflectance,
        borderColor: color,
        fill: false
      })
      this.items.push(
        { 
          isActive: true, 
          filename: this.comparisonResult.filename,
          value:  this.comparisonResult.chi,
        }
      )
    },
  },
  watch: {
    result: {
      deep: true,
      handler(newValue) {
        if (this.result) {
          this.chartData = this.formatChartData()
        }
      }
    },
    comparisonResult: {
      deep: true,
      handler(newValue) {
        if (this.comparisonResult) {
          this.addExperimentalData()
        }
      }
    },
  },
  mounted() {
    if (this.result) {
      this.chartData = this.formatChartData()
    }
  },
}
</script>