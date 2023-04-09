<!-- This is our main frontend file since it cointains all the elements
shown in the second screen, it is, the materials and initial parameters screen.
Here we have all the form inputs and modals shown to get data from user on each material
for each method (manual, file, dielectric function or effective medium theory) -->

<template>
  <!-- General container for all data -->
  <div class="methods-main-container w-100">
    <!-- Initial parameters title on the second screen -->
    <h2 class="text-left">Materials and Initial Parameters</h2>
    <!-- Container for the left middle of the screen where the initial parameters are located -->
    <div class="d-flex justify-content-center align-items-center middle-container">
      <div class="initial-params-container">
        <div class="initial-params">
          <!-- List of form groups for every initial parameters. Every group has a label with the name
          of the parameter and the actual input that can be a float number, dropdown or radio button. Each input
          saves the value given by the user in the variable related to the v-model field. You can find
          this variable in the data() section at the end of the file -->
          
          <!-- From group for the units -->
          <b-form-group 
          label="Units" 
          label-for="units"
          label-align-sm="right"
          class="d-flex align-items-center mr-3">
            <b-form-radio-group
              v-model="units"
              :options="unitsOptions"
              class="d-flex align-items-center"
              value-field="item"
              text-field="name"
              id="units"
            ></b-form-radio-group>
          </b-form-group>

          <!-- From group for the initial angle, type float with steps of 0.1 in the spinner. It is shown just
          if the answer selected by the user is angular. Value saved in the initialAngle variable -->
          <b-form-group
            label="Initital angle"
            label-for="initial-angle"
            label-align-sm="right"
            class="d-flex align-items-center mr-3 grade"
            v-if="type === 'angular'"
          >
            <b-form-input id="initial-angle" v-model="initialAngle" type="number" step="0.1" min="0">°</b-form-input>
            <span class="grade-symbol">°</span>
          </b-form-group>

          <!-- From group for the final angle, type float with steps of 0.1 in the spinner. It is shown just
          if the answer selected by the user is angular. Value saved in the finalAngle variable -->
          <b-form-group
            label="Final angle"
            label-for="final-angle"
            label-align-sm="right"
            class="d-flex align-items-center mr-3 grade"
            v-if="type === 'angular'"
          >
            <b-form-input id="final-angle" v-model="finalAngle" type="number" step="0.1" min="0"></b-form-input>
            <span class="grade-symbol">°</span>
          </b-form-group>

          <!-- From group for the angle, type float with steps of 0.1 in the spinner. It is shown just
          if the answer selected by the user is espectral. Value saved in the angle variable-->
          <b-form-group
            label="Angle"
            label-for="angle"
            label-align-sm="right"
            class="d-flex align-items-center mr-3 grade"
            v-if="type === 'espectral'"
          >
            <b-form-input id="angle" v-model="angle" type="number" step="0.1" min="0"></b-form-input>
            <span class="grade-symbol">°</span>
          </b-form-group>

          <!-- From group for the steps, type integer. It is shown for both types of answer. 
            Value saved in the steps variable-->
          <b-form-group
            label="Steps"
            label-for="steps"
            label-align-sm="right"
            class="d-flex align-items-center mr-3"
          >
            <b-form-input id="teps" v-model="steps" type="number" min="0"></b-form-input>
          </b-form-group>

          <!-- From group for the Initial Wave Length, type float with steps of 0.1 in the spinner. It is shown just
          if the answer selected by the user is espectral. Value saved in the initialWaveLength variable-->
          <b-form-group
            label="Initial Wavelength"
            label-for="initialWaveLength"
            label-align-sm="right"
            class="d-flex align-items-center mr-3 grade"
            v-if="type === 'espectral'"
          >
            <b-form-input id="initialWaveLength" v-model="initialWaveLength" type="number" step="0.1" min="0"></b-form-input>
            <span class="unit-symbol">{{ currentUnit }}</span>
          </b-form-group>

          <!-- From group for the Final Wave Length, type float with steps of 0.1 in the spinner. It is shown just
          if the answer selected by the user is espectral. Value saved in the finalWaveLength variable-->
          <b-form-group
            label="Final Wavelength"
            label-for="finalWaveLength"
            label-align-sm="right"
            class="d-flex align-items-center mr-3 grade"
            v-if="type === 'espectral'"
          >
            <b-form-input id="finalWaveLength" v-model="finalWaveLength" type="number" step="0.1" min="0"></b-form-input>
            <span class="unit-symbol">{{ currentUnit }}</span>
          </b-form-group>

          <!-- From group for the Wave Length, type float with steps of 0.1 in the spinner. It is shown just
          if the answer selected by the user is angular. Value saved in the waveLength variable-->
          <b-form-group
            label="Wavelength"
            label-for="waveLength"
            label-align-sm="right"
            class="d-flex align-items-center mr-3 grade"
            v-if="type === 'angular'"
          >
            <b-form-input id="waveLength" v-model="waveLength" type="number" step="0.1" min="0"></b-form-input>
            <span class="unit-symbol">{{ currentUnit }}</span>
          </b-form-group>

          <!-- From group for the Wave Length, type radio button (in this case the value will be a string: p or s). 
            It is shown for both types of answer. Value saved in the polarization variable. The options rendered come from
            the variable polarizationOptions on the data() at the end of the file-->          
          <b-form-group 
          label="Polarization" 
          label-for="polarization"
          label-align-sm="right"
            class="d-flex align-items-center mr-3">
            <b-form-radio-group
              v-model="polarization"
              :options="polarizationOptions"
              class="d-flex align-items-center"
              value-field="item"
              text-field="name"
              id="polarization"
            ></b-form-radio-group>
          </b-form-group>
        </div>
        <!-- Container for substrate and host options -->
        <div class="d-flex justify-content-center align-items-center method-options">
          <!-- From group for substrate. It contains the label and the dropdown with the method options.
          This case is repeated for all materials. The method options comes from methodOptions and
          each option is dinamically created as an html object using de v-for directive. -->
          <b-form-group 
            label="Substrate" 
            label-for="substrate"
            label-align-sm="right"
            class="d-flex align-items-center mr-3">
            <!-- The event openMethodModal is triggered everytime the option selected on this dropdown changes.
            We send the name of the material to know which material is being edited by the user, in this case
            the substrate -->
            <b-form-select v-model="substrate" id="substrate" @input="openMethodModal($event, 'substrate')">
              <b-form-select-option 
                :value="option.value"
                v-for="(option, index) in methodOptions"
                :key="index" 
              >
                {{ option.text }}
              </b-form-select-option>
            </b-form-select>
          </b-form-group>

          <b-form-group 
            label="Host" 
            label-for="host"
            label-align-sm="right"
            class="d-flex align-items-center mr-3">
            <!-- Show the same method options as the substrate and open the corresponding modal when the method
            selected changes. Indicates that the host material is being edited at this moment -->
            <b-form-select v-model="host" :options="methodOptions" id="host" @input="openMethodModal($event, 'host')"></b-form-select>
          </b-form-group>
        </div>
      </div>
      <!-- Right side container for the layers -->
      <div class="layers-container">
        <div class="layers-side">
          <div class="d-flex justify-content-between align-items-center title mb-4">
            <!-- Titles inside the container to indicate layers and thicknesses -->
            <h5 class="mt-2">Layers</h5>
            <h5 class="mt-2 ml-4">Thicknesses</h5>
            <!-- Button to add a new layer. the variant only indicates that we want a green button.
            Every time the button is clicked the method addLayer is executed from the methods()
            section at the end of this file -->
            <b-button variant="success" @click="addLayer">+</b-button>
          </div>
          <!-- Substrate box to indicate position of elements -->
          <div class="font-weight-bold alert alert-secondary w-100 d-flex justify-content-center align-items-center" role="alert">
            Substrate
          </div>
          <!-- Create the html elements for each layer dinamically. The layers variable exits at the data() section. Layers variable
          is an array of objects (objects are like python dictionaries). So each layer data is stored as an object. We 
          iterate over every object in the list so we can create the visualization of the different layers with their labels, inputs
          and buttons -->
          <div v-for="(layer, index) in layers" :key="index" class="w-100 d-flex align-items-start layer-input">
            <div class="d-flex justify-content-center align-items-center layer-group">
              <!-- Form group to store the method or option selected for the 'n' current layer in the list of layers.
              Everytime the method selected changes on the dropdown we call the openMethodModal method from the methods() section
              below. We indicate that the `layer-${index+1}` is being edited at this moment. +1 is necessary since the indexation starts at 0
              and we want to show layers starting from 1. The method is stored at the 'model' key within the layer object.-->
              <b-form-group 
                :label="`Layer ${index+1}`" 
                :label-for="`layer-${index+1}`"
                label-align-sm="right"
                class="d-flex align-items-center mr-3 mb-0"
              >
                <b-form-select v-model="layer.model" :id="`layer-${index+1}`"  @input="openMethodModal($event, `layer-${index+1}`)">
                  <b-form-select-option 
                    :value="option.value"
                    v-for="(option, index) in methodOptions"
                    :key="index" 
                  >
                    {{ option.text }}
                  </b-form-select-option>
                </b-form-select>
              </b-form-group>
            </div>
            <!-- Input for the thickness of the current 'n' layer. This value is stored at the key
            thickness of the current layer. This is a floatfield with steps of 0.1 in the spinner. -->
            <div>
              <div class="thickness-input d-flex justify-content-center align-items-center">
                <b-form-group 
                  :label="`Thickness ${index+1}`" 
                  :label-for="`thickness-${index+1}`"
                  label-align-sm="right"
                  class="d-flex align-items-center mr-3 mb-0 grade"
                >
                  <b-form-input :id="`thickness-${index+1}`" v-model="layer.thickness" type="number" step="0.1" min="0"></b-form-input>
                  <span class="unit-symbol">{{ currentUnit }}</span>
                </b-form-group>
              </div>
              <span class="text-danger font-weight-bold error-message" v-show="(!layer.thickness || layer.thickness <= 0) && sentButtonPressed">
                Thickness for layer {{ index + 1 }} is a mandatory field
              </span>
            </div>
            <!-- Button to remove the current layer. Everytime the button is clicked the removeLayer is executed
            from the methods() section. We pass the index in the list for this current layer so wen can know which object
            should be deleted from the layers list. Danger indicates that we want a red button -->
            <b-button variant="danger" @click="removeLayer(index)">-</b-button>
          </div>
        </div>
      </div>
    </div>
    <!-- Button to create a POST request with the data collected from all the materials -->
    <div class="d-flex justify-content-center align-items-center">
      <b-button variant="info" class="align-self-end mt-4" @click="validateData">Calculate</b-button>
    </div>

    <!-- From here the section for modals starts. Modals are the windows opened when certain action occurs.
    This elements are not being showed all the time, just when the method selected on
    any of the materials changes. Each modal has its own name according to the method selected. -->

    <!-- Modal Upload -->
    <b-modal id="modal-upload" title="Upload file" centered no-close-on-esc no-close-on-backdrop>
      <template #modal-header>
        <h5>Upload file</h5>
      </template>
      <!-- Method to just upload a file for the material. It only allows csv and txt files. The value is
      stores on the file key in data(). Once the button ok is clicked we upload the file and add the
      material to the list of materials. Cancel button closes the modal -->
      <b-form-group label="File" label-cols-sm="2">
        <b-form-file id="file-default" accept=".csv, .txt, .yml" v-model="file"></b-form-file>
      </b-form-group>
      <template #modal-footer="{ ok }">
        <b-button size="sm" variant="success" @click="uploadFile(ok, 'modal-upload')">
          OK
        </b-button>
        <b-button size="sm" variant="danger" @click="cancel('modal-upload')">
          Cancel
        </b-button>
      </template>
    </b-modal>

    <!-- Modal Dielectric -->
    <b-modal id="modal-dielectric" title="Dispersion Formulas" centered no-close-on-esc no-close-on-backdrop>
      <template #modal-header>
        <h5>Dispersion Formulas</h5>
      </template>
      <!-- Modal for dielectric method. It has a dropdown to select a model and show different options according to it.
      The model selected is stored on the dielectricModel in data() -->
      <b-form-select v-model="dielectricModel" id="dielectric-model">
        <b-form-select-option 
          :value="option.value"
          v-for="(option, index) in dielectricMethods"
          :key="index" 
        >
          {{ option.text }}
        </b-form-select-option>
      </b-form-select>

      <!-- Lorenz -->
      <!-- Container with fields and data for lorenz method -->
      <div class="method-container" v-show="dielectricModel === 'lorenz'">
        <p class="w-100 font-weight-bold text-left my-2">For dielectrics materials</p>
        <!-- Formula picture -->
        <img :src="lorenz_img" alt="lorenz-model" class="lorenz">
        <div>
          <!-- Each of the following form groups contains the label according to the parameter
          required by the method and the input field for numbers of type float with a step of 0.1 
          in the spinner. Each of the values is stores inside of the object 'lorenz' in the data() section
          -->
          <b-form-group
            label="Ne"
            label-for="ne"
            label-align-sm="right"
            class="d-flex align-items-center mr-3 grade"
          >
            <b-form-input id="ne" v-model="lorenz.ne" class="ml-3" type="number" step="0.1" min="0"></b-form-input>
            <span class="unit-symbol">eV</span>
          </b-form-group>

          <b-form-group
            label="ωo"
            label-for="wo"
            label-align-sm="right"
            class="d-flex align-items-center mr-3 grade"
          >
            <b-form-input id="wo" v-model="lorenz.wo" class="ml-3" type="number" step="0.1" min="0"></b-form-input>
            <span class="unit-symbol">eV</span>
          </b-form-group>

          <b-form-group
            label="ω"
            label-for="w"
            label-align-sm="right"
            class="d-flex align-items-center mr-3 grade"
          >
            <b-form-input disabled id="w" v-model="lorenz.w" class="ml-3"></b-form-input>
            <span class="unit-symbol">eV</span>
          </b-form-group>

          <b-form-group
            label="Γ"
            label-for="r"
            label-align-sm="right"
            class="d-flex align-items-center mr-3 grade"
          >
            <b-form-input id="r" v-model="lorenz.r" class="ml-3" type="number" step="0.1" min="0"></b-form-input>
            <span class="unit-symbol">eV</span>
          </b-form-group>
        </div>
      </div>

      <!-- Drude -->
      <!-- Container for data when the user selects Drude model -->
      <div class="method-container" v-show="dielectricModel === 'drude'">
        <p class="w-100 font-weight-bold text-left my-2">For metals</p>
        <img :src="drude_img" alt="lorenz-model" class="drude">
        <div>
          <!-- Each of the following form groups contains the label according to the parameter
          required by the method and the input field for numbers of type float with a step of 0.1 
          in the spinner. Each of the values is stores inside of the object 'Drude' in the data() section
          -->
          <b-form-group
            label="ωp"
            label-for="drude-ne"
            label-align-sm="right"
            class="d-flex align-items-center mr-3 grade"
          >
            <b-form-input id="drude-ne" v-model="drude.ne" class="ml-3" type="number" step="0.1" min="0"></b-form-input>
            <span class="unit-symbol">eV</span>
          </b-form-group>

          <b-form-group
            label="ε∞"
            label-for="drude-e"
            label-align-sm="right"
            class="d-flex align-items-center mr-3 grade"
          >
            <b-form-input id="drude-e" v-model="drude.e" class="ml-3" type="number" step="0.1" min="0"></b-form-input>
            <span class="unit-symbol">  </span>
          </b-form-group>

          <b-form-group
            label="ω"
            label-for="drude-w"
            label-align-sm="right"
            class="d-flex align-items-center mr-3 grade"
          >
            <b-form-input disabled id="drude-w" v-model="drude.w" class="ml-3"></b-form-input>
            <span class="unit-symbol">eV</span>
          </b-form-group>

          <b-form-group
            label="Γ"
            label-for="drude-r"
            label-align-sm="right"
            class="d-flex align-items-center mr-3 grade"
          >
            <b-form-input id="drude-r" v-model="drude.r" class="ml-3" type="number" step="0.1" min="0"></b-form-input>
            <span class="unit-symbol">eV</span>
          </b-form-group>
        </div>
      </div>

      <!-- Sellmeier -->
      <!-- Container for Sellmeier fields -->
      <div class="method-container" v-show="dielectricModel === 'sellmeier'">
        <p class="w-100 font-weight-bold text-left my-2">For transparents materials</p>
        <img :src="sellmeier_img" alt="lorenz-model" class="sellmeier">
        <div>
          <!-- Each of the following form groups contains the label according to the parameter
          required by the method and the input field for numbers of type float with a step of 0.1 
          in the spinner. Each of the values is stores inside of the object 'sellmeier' in the data() section
          -->
          <b-form-group
            label="A"
            label-for="sellmeier-a"
            label-align-sm="right"
            class="d-flex align-items-center mr-3 grade"
          >
            <b-form-input id="sellmeier-a" v-model="sellmeier.a" class="ml-3" type="number" step="0.1" min="0"></b-form-input>
            <span class="unit-symbol">  </span>
          </b-form-group>

          <b-form-group
            label="B"
            label-for="sellmeier-b"
            label-align-sm="right"
            class="d-flex align-items-center mr-3 grade"
          >
            <b-form-input id="sellmeier-b" v-model="sellmeier.b" class="ml-3" type="number" step="0.1" min="0"></b-form-input>
            <span class="unit-symbol">  </span>
          </b-form-group>

          <b-form-group
            label="λ"
            label-for="sellmeier-lambda"
            label-align-sm="right"
            class="d-flex align-items-center mr-3 grade"
          >
            <!-- This field is disabled since we are taking it's value from the initial parameter field filled
            by the user -->
            <b-form-input id="sellmeier-lambda" v-model="waveLength" class="ml-3" disabled></b-form-input>
            <span class="unit-symbol">{{ currentUnit }}</span>
          </b-form-group>

          <b-form-group
            label="λo"
            label-for="sellmeier-lambdao"
            label-align-sm="right"
            class="d-flex align-items-center mr-3 grade"
          >
            <b-form-input id="sellmeier-lambdao" v-model="sellmeier.lambdaO" class="ml-3" type="number" step="0.1" min="0"></b-form-input>
            <span class="unit-symbol">{{ currentUnit }}</span>
          </b-form-group>
        </div>
      </div>

       <!-- Couchy -->
       <!-- Container for couchy fields -->
       <div class="method-container" v-show="dielectricModel === 'cauchy'">
        <p class="w-100 font-weight-bold text-left my-2">For transparent materials</p>
        <img :src="cauchy_img" alt="lorenz-model">
        <div>
          <!-- Each of the following form groups contains the label according to the parameter
          required by the method and the input field for numbers of type float with a step of 0.1 
          in the spinner. Each of the values is stores inside of the object 'couchy' in the data() section
          -->
          <b-form-group
            label="A"
            label-for="cauchy-a"
            label-align-sm="right"
            class="d-flex align-items-center mr-3 grade"
          >
            <b-form-input id="cauchy-a" v-model="cauchy.a" class="ml-3" type="number" step="0.1" min="0"></b-form-input>
            <span class="unit-symbol">  </span>
          </b-form-group>

          <b-form-group
            label="B"
            label-for="cauchy-b"
            label-align-sm="right"
            class="d-flex align-items-center mr-3 grade"
          >
            <b-form-input id="cauchy-b" v-model="cauchy.b" class="ml-3" type="number" step="0.1" min="0"></b-form-input>
            <span class="unit-symbol">  </span>
          </b-form-group>

          <b-form-group
            label="C"
            label-for="cauchy-c"
            label-align-sm="right"
            class="d-flex align-items-center mr-3 grade"
          >
            <b-form-input id="cauchy-c" v-model="cauchy.c" class="ml-3" type="number" step="0.1" min="0"></b-form-input>
            <span class="unit-symbol">  </span>
          </b-form-group>

          <b-form-group
            label="λ"
            label-for="cauchy-lambda"
            label-align-sm="right"
            class="d-flex align-items-center mr-3 grade"
          >
            <b-form-input id="cauchy-lambda" v-model="waveLength" class="ml-3" disabled></b-form-input>
            <span class="unit-symbol">{{ currentUnit }}</span>
          </b-form-group>
        </div>
      </div>
      <!-- Footer of the modal with two buttons, one to set the dielectric method for this material, 
      and another one to just close the modal -->
      <template #modal-footer="{ ok }">
        <b-button size="sm" variant="success"  @click="setDielectricMethod(ok, 'modal-dielectric')">
          OK
        </b-button>
        <b-button size="sm" variant="danger" @click="cancel('modal-dielectric')">
          Cancel
        </b-button>
      </template>
    </b-modal>

    <!-- Modal Manually -->
    <b-modal id="modal-manually" title="Manually" centered no-close-on-esc no-close-on-backdrop>
      <template #modal-header>
        <h5>Manually</h5>
      </template>
      <!-- Modal to set manual values for n and k. It just has this two input fields
      and two buttons, the same buttons used in the other modals so we can set
      the current method for the material or close the modal -->
      <b-form-group
        label="n"
        label-for="manual-n"
        label-align-sm="right"
        class="d-flex align-items-center mr-3"
      >
        <b-form-input id="manual-n" v-model="manual.n" class="ml-3" type="number" step="0.1" min="0"></b-form-input>
      </b-form-group>

      <b-form-group
        label="k"
        label-for="manual-k"
        label-align-sm="right"
        class="d-flex align-items-center mr-3"
      >
        <b-form-input id="manual-k" v-model="manual.k" class="ml-3" type="number" step="0.1" min="0"></b-form-input>
      </b-form-group>
      <template #modal-footer="{ ok }">
        <b-button size="sm" variant="success"  @click="setManualMethod(ok, 'modal-manually')">
          OK
        </b-button>
        <b-button size="sm" variant="danger" @click="cancel('modal-manually')">
          Cancel
        </b-button>
      </template>
    </b-modal>

    <!-- Modal Effective Medium Theories -->
    <!-- Modal for effective medium theories -->
    <b-modal id="modal-efective" title="Effective Medium Theories" centered size="lg" no-close-on-esc no-close-on-backdrop>
      <template #modal-header>
        <h5>Effective Medium Theories</h5>
      </template>
      <b-form-select v-model="effectiveMediumModel" id="effective-model">
        <!-- Dropdown to show the different effective medium theories and show the fields according to it -->
        <b-form-select-option 
          :value="option.value"
          v-for="(option, index) in effectiveMethods"
          :key="index" 
        >
          {{ option.text }}
        </b-form-select-option>
      </b-form-select>

      <!-- Maxwell -->
      <!-- Container shown if the theory selected is Maxwell -->
      <div class="method-container" v-show="effectiveMediumModel === 'maxwell'">
        <p class="w-100 font-weight-bold text-left my-2">Maxwell Garnett Formula</p>
        <img :src="maxwell_img" alt="lorenz-model">
        <div class="w-100">
          <div class="w-100">
            <!-- Form groups to show the label and input field for this theory -->
            <b-form-group
              label="εm"
              label-for="maxwell-em"
              label-align-sm="right"
              class="d-flex align-items-center mr-3"
            >
              <!-- Dropwdown to show the manual and file options -->
              <b-form-select v-model="maxwell.em" id="maxwell-em" class="ml-3">
                <b-form-select-option 
                  :value="option.value"
                  v-for="(option, index) in epsilonOptions"
                  :key="index" 
                >
                  {{ option.text }}
                </b-form-select-option>
              </b-form-select>
            </b-form-group>

            <!-- Fields shown in case the user chooses the manual option -->
            <div v-if="maxwell.em === 'manually'" class="d-flex align-items-center">
              <b-form-group 
                label="" 
                label-for="maxwell-em-manual"
                label-align-sm="right"
                class="d-flex align-items-center mr-3 ml-2"
              >
                <b-form-radio-group
                  v-model="maxwell.emManual"
                  :options="maxwellManualOptions"
                  class="d-flex align-items-center"
                  value-field="item"
                  text-field="name"
                  id="maxwell-em-manual"
                ></b-form-radio-group>
              </b-form-group>

              <div v-if="maxwell.emManual === 'e'" class="d-flex align-items-center">
                <b-form-group
                  label="ε1"
                  label-for="manual-e1m"
                  label-align-sm="right"
                  class="d-flex align-items-center mr-3"
                >
                  <b-form-input id="manual-e1m" v-model="maxwell.e1m" class="ml-3 mr-3" type="number" step="0.1" min="0"></b-form-input>
                </b-form-group>
                <b-form-group
                  label="ε2"
                  label-for="manual-e2m"
                  label-align-sm="right"
                  class="d-flex align-items-center mr-3 ml-3"
                >
                  <b-form-input id="manual-e2m" v-model="maxwell.e2m" class="ml-3" type="number" step="0.1" min="0"></b-form-input>
                </b-form-group>
              </div>
              <div v-if="maxwell.emManual === 'nk'" class="d-flex align-items-center">
                <b-form-group
                  label="n"
                  label-for="manual-nm"
                  label-align-sm="right"
                  class="d-flex align-items-center mr-3"
                >
                  <b-form-input id="manual-nm" v-model="maxwell.nm" class="ml-3 mr-3" type="number" step="0.1" min="0"></b-form-input>
                </b-form-group>
                <b-form-group
                  label="k"
                  label-for="manual-km"
                  label-align-sm="right"
                  class="d-flex align-items-center mr-3 ml-3"
                >
                  <b-form-input id="manual-km" v-model="maxwell.km" class="ml-3" type="number" step="0.1" min="0"></b-form-input>
                </b-form-group>
              </div>
            </div>

            <!-- Input field to upload file in case the user chooses the file option -->
            <div v-if="maxwell.em === 'file'">
              <b-form-group label="File" label-cols-sm="2" class="ml-2">
                <b-form-file id="file-maxwell-em" accept=".csv, .txt, .yml" v-model="maxwell.file" class="maxwell-file"></b-form-file>
              </b-form-group>
            </div>
            
            <!-- Inlusions section -->
            <div class="w-100">
              <div class="d-flex justify-content-between align-items-center title mb-4">
                <h5 class="my-4">Inclusions</h5>
                <div class="d-flex justify-content-between align-items-center">
                  <h5 class="my-4 mr-4 pr-3">Volume Fraction</h5>
                  <!-- Button to add an inclusion in the list, the variant only assings a green style to the button -->
                  <b-button variant="success" @click="addInclusion">+</b-button>
                </div>
              </div>
              <!-- We create all the components for the inclusion dinamically. It means that for every object in the list of inclusions
              this html will have a copy of the div below, including all the field inputs. -->
              <div v-for="(inclusion, index) in inclusions" :key="index" class="w-100 d-flex justify-content-between align-items-center inclusions-container">
                <div>
                  <!-- Group to select file or manual method for the inclusion -->
                  <b-form-group 
                    :label="`ε${index+1}`" 
                    :label-for="`inclusion-maxwell-${index+1}`"
                    label-align-sm="right"
                    class="d-flex align-items-center mr-3 mb-0"
                  >
                    <b-form-select class="ml-4" v-model="inclusion.method" :id="`inclusion-maxwell-${index+1}`">
                      <b-form-select-option 
                        :value="option.value"
                        v-for="(option, index) in epsilonOptions"
                        :key="index" 
                      >
                        {{ option.text }}
                      </b-form-select-option>
                    </b-form-select>
                  </b-form-group>

                  <!-- Options shown in case the user chooses the manual option for the current inclusion -->
                  <div v-if="inclusion.method === 'manually'" class="ml-3 mt-3">
                    <b-form-group 
                      label="" 
                      :label-for="`inclusion-maxwell-${index+1}`"
                      label-align-sm="right"
                      class="d-flex align-items-center mr-3 ml-2"
                    >
                      <b-form-radio-group
                        v-model="inclusion.manual"
                        :options="maxwellManualOptions"
                        class="d-flex align-items-center"
                        value-field="item"
                        text-field="name"
                        :id="`inclusion-maxwell-${index+1}`"
                      ></b-form-radio-group>
                    </b-form-group>

                    <div v-if="inclusion.manual === 'e'" class="d-flex align-items-center">
                      <b-form-group
                        label="ε1"
                        :label-for="`manual-e1m-${index+1}`"
                        label-align-sm="right"
                        class="d-flex align-items-center mr-3"
                      >
                        <b-form-input :id="`manual-e1m-${index+1}`" v-model="inclusion.e1m" class="ml-3 mr-3" type="number" step="0.1" min="0"></b-form-input>
                      </b-form-group>
                      <b-form-group
                        label="ε2"
                        :label-for="`manual-e2m-${index+1}`"
                        label-align-sm="right"
                        class="d-flex align-items-center mr-3 ml-3"
                      >
                        <b-form-input :id="`manual-e2m-${index+1}`" v-model="inclusion.e2m" class="ml-3" type="number" step="0.1" min="0"></b-form-input>
                      </b-form-group>
                    </div>
                    <div v-if="inclusion.manual === 'nk'" class="d-flex align-items-center">
                      <b-form-group
                        label="n"
                        :label-for="`manual-nm-${index+1}`"
                        label-align-sm="right"
                        class="d-flex align-items-center mr-3"
                      >
                        <b-form-input :id="`manual-nm-${index+1}`" v-model="inclusion.nm" class="ml-3 mr-3" type="number" step="0.1" min="0"></b-form-input>
                      </b-form-group>
                      <b-form-group
                        label="k"
                        :label-for="`manual-km-${index+1}`"
                        label-align-sm="right"
                        class="d-flex align-items-center mr-3 ml-3"
                      >
                        <b-form-input :id="`manual-km-${index+1}`" v-model="inclusion.km" class="ml-3" type="number" step="0.1" min="0"></b-form-input>
                      </b-form-group>
                    </div>
                  </div>

                  <!-- Options shown in case the user chooses the file option for the current inclusion -->
                  <div v-if="inclusion.method === 'file'" class="mt-3">
                    <b-form-group label="File" label-cols-sm="2" class="ml-3">
                      <b-form-file :id="`inclusion-file-${index+1}`" accept=".csv, .txt, .yml" v-model="inclusion.file" class="maxwell-file"></b-form-file>
                    </b-form-group>
                  </div>

                </div>
                
                <!-- Container for the volume of the current inclusion -->
                <div class="d-flex flex-column align-items-end justify-content-end">
                  <!-- Button to delete the current inclusion. There is a condition of index > 0 so we make sure that the user can
                  not delete the first inclusion since this method requires at least one inclusion -->
                  <b-button variant="danger" @click="removeInclusion(index)" v-if="index > 0" class="mb-3">-</b-button>
                  <b-form-group 
                    :label="`f${index+1}`" 
                    :label-for="`maxwell-f-${index+1}`"
                    label-align-sm="right"
                    class="d-flex align-items-center mr-3 mb-0"
                  >
                    <b-form-input class="ml-4" :id="`maxwell-f-${index+1}`" v-model="inclusion.volume" type="number" step="0.1" min="0" max="1"></b-form-input>
                  </b-form-group>
                  <span class="text-danger font-weight-bold error-message mt-2" v-show="(!inclusion.volume || inclusion.volume <= 0) && okButtonPressed">
                    Fraction volume is a mandatory field
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Lorentz -->
      <!-- Container to show fields for Lorentz theory -->
      <div class="method-container" v-show="effectiveMediumModel === 'lorentz'">
        <p class="w-100 font-weight-bold text-left my-2">The Lorentz-Lorenz Relation</p>
        <img :src="lorentz_img" alt="lorenz-model" class="lorentz">
        <div class="d-flex justify-content-between align-items-end w-100">
          <div>
            <div class="w-100">
              <!-- Form groups to show the label and input field for this theory. Each field shown in the browser is contained
              by one form group. The label option is the current text shown to the user. All of the values given by the user
              on this method are stored in the lorentz object at the data() section -->

              <!-- Em input -->
              <b-form-group
                label="εm"
                label-for="lorentz-em"
                label-align-sm="right"
                class="d-flex align-items-center mr-3"
              >
                <b-form-select v-model="lorentz.em" id="lorentz-em" class="ml-3">
                  <b-form-select-option 
                    :value="option.value"
                    v-for="(option, index) in epsilonOptions"
                    :key="index" 
                  >
                    {{ option.text }}
                  </b-form-select-option>
                </b-form-select>
              </b-form-group>

              <!-- Fields in case the user chooses manual method for Em -->
              <div v-if="lorentz.em === 'manually'" class="d-flex align-items-center">
                <b-form-group 
                  label="" 
                  label-for="lorentz-em-manual"
                  label-align-sm="right"
                  class="d-flex align-items-center mr-3 ml-2"
                >
                  <b-form-radio-group
                    v-model="lorentz.emManual"
                    :options="maxwellManualOptions"
                    class="d-flex align-items-center"
                    value-field="item"
                    text-field="name"
                    id="lorentz-em-manual"
                  ></b-form-radio-group>
                </b-form-group>

                <div v-if="lorentz.emManual === 'e'" class="d-flex align-items-center">
                  <b-form-group
                    label="ε1"
                    label-for="lorentz-manual-e1m"
                    label-align-sm="right"
                    class="d-flex align-items-center mr-3"
                  >
                    <b-form-input id="lorentz-manual-e1m" v-model="lorentz.e1m" class="ml-3 mr-3" type="number" step="0.1" min="0"></b-form-input>
                  </b-form-group>
                  <b-form-group
                    label="ε2"
                    label-for="lorentz-manual-e2m"
                    label-align-sm="right"
                    class="d-flex align-items-center mr-3 ml-3"
                  >
                    <b-form-input id="lorentz-manual-e2m" v-model="lorentz.e2m" class="ml-3" type="number" step="0.1" min="0"></b-form-input>
                  </b-form-group>
                </div>
                <div v-if="lorentz.emManual === 'nk'" class="d-flex align-items-center">
                  <b-form-group
                    label="n"
                    label-for="lorentz-nm"
                    label-align-sm="right"
                    class="d-flex align-items-center mr-3"
                  >
                    <b-form-input id="lorentz-nm" v-model="lorentz.nm" class="ml-3 mr-3" type="number" step="0.1" min="0"></b-form-input>
                  </b-form-group>
                  <b-form-group
                    label="k"
                    label-for="lorentz-km"
                    label-align-sm="right"
                    class="d-flex align-items-center mr-3 ml-3"
                  >
                    <b-form-input id="lorentz-km" v-model="lorentz.km" class="ml-3" type="number" step="0.1" min="0"></b-form-input>
                  </b-form-group>
                </div>
              </div>

              <!-- Fields in case the user chooses file method for Em -->
              <div v-if="lorentz.em === 'file'">
                <b-form-group label="File" label-cols-sm="2" class="ml-2">
                  <b-form-file id="file-lorentz-em" accept=".csv, .txt, .yml" v-model="lorentz.file" class="maxwell-file"></b-form-file>
                </b-form-group>
              </div>
            </div>

            <!-- Fields in case the user chooses manual method for Ei -->
            <div class="w-100 mt-3">
              <b-form-group
                label="εi"
                label-for="lorentz-ei"
                label-align-sm="right"
                class="d-flex align-items-center mr-4"
              >
                <b-form-select v-model="lorentz.ei" id="lorentz-ei" class="ml-3">
                  <b-form-select-option 
                    :value="option.value"
                    v-for="(option, index) in epsilonOptions"
                    :key="index" 
                  >
                    {{ option.text }}
                  </b-form-select-option>
                </b-form-select>
              </b-form-group>
              <div v-if="lorentz.ei === 'manually'" class="d-flex align-items-center">
                <b-form-group 
                  label="" 
                  label-for="lorentz-ei-manual"
                  label-align-sm="right"
                  class="d-flex align-items-center mr-3 ml-2"
                >
                  <b-form-radio-group
                    v-model="lorentz.eiManual"
                    :options="maxwellManualOptions"
                    class="d-flex align-items-center"
                    value-field="item"
                    text-field="name"
                    id="lorentz-ei-manual"
                  ></b-form-radio-group>
                </b-form-group>

                <div v-if="lorentz.eiManual === 'e'" class="d-flex align-items-center">
                  <b-form-group
                    label="ε1"
                    label-for="lorentz-manual-e1i"
                    label-align-sm="right"
                    class="d-flex align-items-center mr-3"
                  >
                    <b-form-input id="lorentz-manual-e1i" v-model="lorentz.e1i" class="ml-3 mr-3" type="number" step="0.1" min="0"></b-form-input>
                  </b-form-group>
                  <b-form-group
                    label="ε2"
                    label-for="lorentz-manual-e2i"
                    label-align-sm="right"
                    class="d-flex align-items-center mr-3 ml-3"
                  >
                    <b-form-input id="lorentz-manual-e2i" v-model="lorentz.e2i" class="ml-3" type="number" step="0.1" min="0"></b-form-input>
                  </b-form-group>
                </div>
                <div v-if="lorentz.eiManual === 'nk'" class="d-flex align-items-center">
                  <b-form-group
                    label="n"
                    label-for="lorentz-ni"
                    label-align-sm="right"
                    class="d-flex align-items-center mr-3"
                  >
                    <b-form-input id="lorentz-ni" v-model="lorentz.ni" class="ml-3 mr-3" type="number" step="0.1" min="0"></b-form-input>
                  </b-form-group>
                  <b-form-group
                    label="k"
                    label-for="lorentz-ki"
                    label-align-sm="right"
                    class="d-flex align-items-center mr-3 ml-3"
                  >
                    <b-form-input id="lorentz-ki" v-model="lorentz.ki" class="ml-3" type="number" step="0.1" min="0"></b-form-input>
                  </b-form-group>
                </div>
              </div>
              <!-- Fields in case the user chooses file method for Ei -->
              <div v-if="lorentz.ei === 'file'">
                <b-form-group label="File" label-cols-sm="2" class="ml-2">
                  <b-form-file id="file-lorentz-ei" accept=".csv, .txt, .yml" v-model="lorentz.filei" class="maxwell-file"></b-form-file>
                </b-form-group>
              </div>
            </div>
          </div>
          <div class="d-flex flex-column align-items-end justify-content-end">
            <!-- Volume fraction input -->
            <b-form-group
                label="f"
                label-for="lorentz-f"
                label-align-sm="right"
                class="d-flex align-items-center mr-3"
              >
              <b-form-input id="lorentz-f" v-model="lorentz.volume" class="ml-3" type="number" step="0.1" min="0" max="1"></b-form-input>
              </b-form-group>
            <span class="text-danger font-weight-bold error-message" v-show="(!lorentz.volume || lorentz.volume <= 0) && okButtonPressed">
              Fraction volume is a mandatory field
            </span>
          </div>
        </div>
      </div>

      <!-- Bruggeman -->
      <!-- Container for bruggeman theory fields -->
      <div class="method-container" v-show="effectiveMediumModel === 'bruggeman'">
        <p class="w-100 font-weight-bold text-left my-2">Bruggeman Relation</p>
        <img :src="brugreman_img" alt="lorenz-model">
        
        <!-- Components section -->
        <div class="w-100">
          <div class="d-flex justify-content-between align-items-center title mb-4">
            <h5 class="my-4">Components</h5>
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="my-4 mr-4 pr-3">Volume Fractions</h5>
              <!-- Button to add a new component in the front. the variant only assings a green color to the button -->
              <b-button variant="success" @click="addComponent">+</b-button>
            </div>
          </div>
          <!-- Create all the html elements dinamically for every object inside of the components list. For each component we will
          replicate the div below -->
          <div v-for="(component, index) in components" :key="index" class="w-100 d-flex justify-content-between align-items-center inclusions-container">
            <div>
              <!-- Form group to choose method for the current method -->
              <b-form-group 
                :label="`ε${index+1}`" 
                :label-for="`component-${index+1}`"
                label-align-sm="right"
                class="d-flex align-items-center mr-3 mb-0"
              >
                <b-form-select class="ml-4" v-model="component.method" :id="`component-${index+1}`">
                  <b-form-select-option 
                    :value="option.value"
                    v-for="(option, index) in epsilonOptions"
                    :key="index" 
                  >
                    {{ option.text }}
                  </b-form-select-option>
                </b-form-select>
              </b-form-group>

              <!-- Fields shown when the user chooses the manual option -->
              <div v-if="component.method === 'manually'" class="ml-3 mt-3">
                <b-form-group 
                  label="" 
                  :label-for="`component-${index+1}`"
                  label-align-sm="right"
                  class="d-flex align-items-center mr-3 ml-2"
                >
                  <b-form-radio-group
                    v-model="component.manual"
                    :options="maxwellManualOptions"
                    class="d-flex align-items-center"
                    value-field="item"
                    text-field="name"
                    :id="`component-${index+1}`"
                  ></b-form-radio-group>
                </b-form-group>

                <div v-if="component.manual === 'e'" class="d-flex align-items-center">
                  <b-form-group
                    label="ε1"
                    :label-for="`component-e1i-${index+1}`"
                    label-align-sm="right"
                    class="d-flex align-items-center mr-3"
                  >
                    <b-form-input :id="`component-e1i-${index+1}`" v-model="component.e1i" class="ml-3 mr-3" type="number" step="0.1" min="0"></b-form-input>
                  </b-form-group>
                  <b-form-group
                    label="ε2"
                    :label-for="`component-e2i-${index+1}`"
                    label-align-sm="right"
                    class="d-flex align-items-center mr-3 ml-3"
                  >
                    <b-form-input :id="`component-e2i-${index+1}`" v-model="component.e2i" class="ml-3" type="number" step="0.1" min="0"></b-form-input>
                  </b-form-group>
                </div>
                <div v-if="component.manual === 'nk'" class="d-flex align-items-center">
                  <b-form-group
                    label="n"
                    :label-for="`component-ni-${index+1}`"
                    label-align-sm="right"
                    class="d-flex align-items-center mr-3"
                  >
                    <b-form-input :id="`component-ni-${index+1}`" v-model="component.ni" class="ml-3 mr-3" type="number" step="0.1" min="0"></b-form-input>
                  </b-form-group>
                  <b-form-group
                    label="k"
                    :label-for="`component-ki-${index+1}`"
                    label-align-sm="right"
                    class="d-flex align-items-center mr-3 ml-3"
                  >
                    <b-form-input :id="`component-ki-${index+1}`" v-model="component.ki" class="ml-3" type="number" step="0.1" min="0"></b-form-input>
                  </b-form-group>
                </div>
              </div>

              <!-- Fields shown when the user chooses the file option -->
              <div v-if="component.method === 'file'" class="mt-3">
                <b-form-group label="File" label-cols-sm="2" class="ml-3">
                  <b-form-file :id="`component-file-${index+1}`" accept=".csv, .txt, .yml" v-model="component.file" class="maxwell-file"></b-form-file>
                </b-form-group>
              </div>

            </div>

            <!-- Container for the volume of the current component -->
            <div class="d-flex flex-column align-items-end justify-content-end">
              <!-- Button to remove the current component. To have at least one component is mandatory, so that's why
              we just show this button from the index 1 (second component) -->
              <b-button variant="danger" @click="removeComponent(index)" v-if="index > 0" class="mb-3">-</b-button>
              <!-- Volume field for the current component -->
              <b-form-group 
                :label="`f${index+1}`" 
                :label-for="`component-f-${index+1}`"
                label-align-sm="right"
                class="d-flex align-items-center mr-3 mb-0"
              >
                <b-form-input class="ml-4" :id="`component-f-${index+1}`" v-model="component.volume" type="number" step="0.1" min="0" max="1"></b-form-input>
              </b-form-group>
              <span class="text-danger font-weight-bold error-message mt-2" v-show="(!component.volume || component.volume <= 0) && okButtonPressed">
                Fraction volume is a mandatory field
              </span>
            </div>
          </div>
        </div>
         
      </div>
      <!-- Footer to set the effective medium theory or close the modal -->
      <template #modal-footer="{ ok }">
        <b-button size="sm" variant="success"  @click="validateEffectiveMethod(ok, 'modal-efective')">
          OK
        </b-button>
        <b-button size="sm" variant="danger" @click="cancel('modal-efective')">
          Cancel
        </b-button>
      </template>
    </b-modal>

  </div>
  </template>

  
  
<script>
import { mapState, mapActions, mapMutations } from "vuex"
export default {
  // Initialization of all the parameters and values inside of the forms,
  // we also include here the options on each dropdown shown.
  data() {
    return {
      cauchy_img: this.$root.$data.django_context.cauchy,
      drude_img: this.$root.$data.django_context.drude,
      lorenz_img: this.$root.$data.django_context.lorenz,
      sellmeier_img: this.$root.$data.django_context.sellmeier,
      maxwell_img: this.$root.$data.django_context.maxwell,
      brugreman_img: this.$root.$data.django_context.brugreman,
      lorentz_img: this.$root.$data.django_context.lorentz,
      sentButtonPressed: false,
      okButtonPressed: false,
      initialAngle: 0,
      finalAngle: 90,
      angle: 0,
      steps: 50,
      initialWaveLength: 0.1,
      finalWaveLength: 0.2,
      waveLength: 0.1,
      polarization: 'p',
      units: 'nm',
      substrate: null, 
      host: null,
      file: null,
      polarizationOptions: [
        { item: 'p', name: 'P' },
        { item: 's', name: 'S' },
      ],
      unitsOptions: [
        { item: 'nm', name: 'nm' },
        { item: 'um', name: 'μm' },
        { item: 'a', name: 'Å' },
      ],
      dielectricMethods: [
        { value: null, text: 'Select a model...' },
        { value: 'lorenz', text: 'Lorenz' },
        { value: 'drude', text: 'Drude' },
        { value: 'sellmeier', text: 'Sellmeier' },
        { value: 'cauchy', text: 'Cauchy' },
      ],
      manual: {
        n: null,
        k: null,
      },
      entityPointer: null,
      dielectricModel: null,
      lorenz: {
        ne: null,
        wo: null,
        w: null,
        r: null,
      },
      drude: {
        ne: null,
        e: null,
        w: null,
        r: null,
      },
      sellmeier: {
        a: null,
        b: null,
        lambdaO: null,
      },
      cauchy: {
        a: null,
        b: null,
        c: null,
      },
      layers: [],
      effectiveMediumModel: null,
      effectiveMethods: [
        { value: null, text: 'Select a model...' },
        { value: 'maxwell', text: 'Maxwell Garnett Formula' },
        { value: 'lorentz', text: 'The Lorentz-Lorenz Relation' },
        { value: 'bruggeman', text: 'Bruggeman Relation' },
      ],
      maxwell: {
        em: null,
        file: null,
        emManual: null,
        e1m: null,
        e2m: null,
        nm: null,
        km: null,
      },
      maxwellManualOptions: [
        { item: 'e', name: 'Dielectric Function' },
        { item: 'nk', name: 'Refractive Index' },
      ],
      inclusions: [
        {
          method: null,
          file: null,
          manual: null,
          e1m: null,
          e2m: null,
          nm: null,
          km: null,
          volume: null,
        }
      ],
      lorentz: {
        em: null,
        file: null,
        emManual: null,
        e1m: null,
        e2m: null,
        nm: null,
        km: null,

        ei: null,
        filei: null,
        eiManual: null,
        e1i: null,
        e2i: null,
        ni: null,
        ki: null,

        volume: null,
      },
      components: [
        {
          method: null,
          file: null,
          manual: null,
          e1i: null,
          e2i: null,
          ni: null,
          ki: null,
          volume: null,
        }
      ],
      // Object send to backend with the information of all the materials 
      // (host, substrate and layers)
      materials: {},
    }
  },
  computed: {
    ...mapState({
      // Get the answer selected by the user on the first screen (angular, espectral)
      type: state => state.transfer.type,
    }),
    omega(){
      let result = null
      const h = 4.135667696E-15  //eV⋅Hz−1
      let c = 1
      let a = 1
      if (this.type === 'angular'){
        const wl = parseFloat(this.waveLength)
        const units = this.units || 'nm'
        if (wl !== null && wl !== undefined && units !== null && units !== undefined){
          if (units === "um"){   
            c = 2.99792458E14
            a = h * c
            result = a / wl
          }
          if (units === "a"){
            c = 2.99792458E18 
            a = h * c
            result = a / wl
          }
          if (units === "nm"){
            c = 2.99792458E17
            a = h * c
            result = a / wl
          }
          result = result.toFixed(4);
        }     
      } else {
        const wlo = parseFloat(this.initialWaveLength)
        const wlf = parseFloat(this.finalWaveLength)
        const units = this.units || 'nm'
        let currentW = wlo 
        const increase = (wlf - wlo) / parseFloat(this.steps)
        let range_list = []
        while (range_list.length < this.steps){
          currentW += increase
          range_list.push(currentW)
        }
        result = []
        let r = 1
        range_list.forEach(wl => {
          if (units === "um"){   
            c = 2.99792458E14
            a = h * c
            r = a / wl
          }
          if (units === "a"){
            c = 2.99792458E18 
            a = h * c
            r = a / wl
          }
          if (units === "nm"){
            c = 2.99792458E17
            a = h * c
            r = a / wl
          }
          result.push(r.toFixed(4))
        });  
        result = String(result)   
      }
      return result
    },  
    methodOptions() {
      // The methods on the dropdopwn of host, substrate and layers is dinamically returned since
      // it depends on the answer selected by the user in the first screen. We hide the manual option 
      // for espectral answer
      let methods = [
        { value: null, text: 'Select a method...' },
        { value: 'upload', text: 'Upload file' },
        { value: 'efective', text: 'Efective Medium Theories' },
        { value: 'dielectric', text: 'Dispersion Formulas' }
      ]
      if (this.type === 'angular') {
        methods.push({ value: 'manually', text: 'Manually' })
      }
      return methods
    }, 
    epsilonOptions() {
      let options = [
        { value: null, text: 'Select a model...' },
        { value: 'file', text: 'File' },
      ]
      if (this.type === 'angular') {
        options.push({ value: 'manually', text: 'Manually' })
      }
      return options
    },
    currentUnit() {
      let unit = ''
      if (this.units) {
        this.unitsOptions.forEach(element => {
          if (element.item === this.units) {
            unit = element.name
          }
        });
      } 
      return unit
    },  
  },
  methods: {
    ...mapActions({
      // Method to send data to backend through the enpoint created
      sendData: "transfer/sendData",
    }),
    ...mapMutations({
      setInitialParams: "transfer/setInitialParams",
    }),
    // Function to open the modal and set the current entity. It means
    // that we will know which modal is opened and from what material was opened
    // (host, substrate, layer) in order to save the data under the corresponding
    // key in the materials object above in the data() section
    openMethodModal(method, entity) {
      this.$bvModal.show(`modal-${method}`)
      this.entityPointer = entity
    },
    // Function to add a new layer. This is to add an empty object
    // to the list of layers. The v-for directive in the HTML will be in charge
    // of creating dinamically all the elements needed.
    addLayer() {
      this.updateWLayers() 
      this.layers.push({
        model: null,
        thickness: 0,
      })
    },
    // Function to add a new inclusion. This is to add an empty object
    // to the list of inclusions. The v-for directive in the HTML will be in charge
    // of creating dinamically all the elements needed.
    addInclusion() {
      this.inclusions.push({
        method: null,
        file: null,
        manual: null,
        e1m: null,
        e2m: null,
        nm: null,
        km: null,
        volume: null,
      })
    },
    // Function to add a new component. This is to add an empty object
    // to the list of components. The v-for directive in the HTML will be in charge
    // of creating dinamically all the elements needed.
    addComponent() {
      this.components.push({
        method: null,
        file: null,
        manual: null,
        e1i: null,
        e2i: null,
        ni: null,
        ki: null,
        volume: null,
      })
    },
    // Method to remove a layer using it's position inside the array
    removeLayer(index) {
      this.layers.splice(index, 1);
    },
    // Method to remove an inclusion using it's position inside the array
    removeInclusion(index) {
      this.inclusions.splice(index, 1);
    },
    // Method to remove a component using it's position inside the array
    removeComponent(index) {
      this.components.splice(index, 1);
    },
    // method to rename the files uploaded in order to know 
    // which was the material related to this file in the backend
    renameFile(originalFile, newName) {
      return new File([originalFile], newName, {
          type: originalFile.type,
          lastModified: originalFile.lastModified,
      });
    },
    validateData() {
      this.sentButtonPressed = true;
      const emptyThicknesses = (element) => !element.thickness || element.thickness <= 0;
      const existEmptyThicknesses = this.layers.some(emptyThicknesses)
      if (!existEmptyThicknesses) {
        this.calculate();
      }
    },
    // Method to be executed once the user clicks on the calculate button.
    // Here we group all the data collected in one single variable to be sent
    // to the backend
    calculate() {
      // The variable that will contain all the data is called
      // formData and it is a FormData type so we can send also files
      // using this format.
      const formData = new FormData()

      this.setInitialParams({
        initial_param: this.type === 'angular' ? this.initialAngle : this.initialWaveLength,
        final_param: this.type === 'angular' ? this.finalAngle : this.finalWaveLength,
        steps: this.steps,
      })

      formData.append("initialAngle", this.initialAngle)
      formData.append("finalAngle", this.finalAngle)
      formData.append("angle", this.angle)
      formData.append("steps", this.steps)
      formData.append("initialWaveLength", this.initialWaveLength)
      formData.append("finalWaveLength", this.finalWaveLength)
      formData.append("waveLength", this.waveLength)
      formData.append("polarization", this.polarization)
      formData.append("substrate", this.substrate)
      formData.append("host", this.host)
      formData.append("units", this.units)
      
      // Iterate over all the materials to get the corresponding data
      Object.keys(this.materials).forEach(key => {
        // Different logic for maxwell and its inclusions
        if (this.materials[key].option.includes('maxwell')) {
          // Maxwell with file in the main E
          if (this.materials[key].option.includes('file')) {
            formData.append("materials", this.materials[key].value)
          } 
          // Add manual data
          let material = {}
          material[key] = {}
          Object.keys(this.materials[key]).forEach(subkey => {
            // Omit inclusions data
            if (!subkey.includes('inclusion')) {
              material[key][subkey] = this.materials[key][subkey]
            } else {
              // Add inclusion data
              // Here the key means the material and subkey means the specific inclusion
              // differentiated by index
              if (this.materials[key][subkey].option == 'file') {
                const volume = this.materials[key][subkey].volume
                material[key][subkey] = {volume: volume}
                formData.append("materials", this.materials[key][subkey].value)
              } else {
                material[key][subkey] = this.materials[key][subkey]
              }
            }
          })
          formData.append("materials", JSON.stringify(material))
          
        } else if (this.materials[key].option.includes('bruggeman')) {
          let material = {}
          material[key] = {}
          Object.keys(this.materials[key]).forEach(subkey => {
            // Add component data
            // Here the key means the material and subkey means the specific component
            // differentiated by index
            if (this.materials[key][subkey].option == 'file') {
              const volume = this.materials[key][subkey].volume
              material[key][subkey] = {volume: volume}
              formData.append("materials", this.materials[key][subkey].value)
            } else {
              material[key][subkey] = this.materials[key][subkey]
            }
          })
          formData.append("materials", JSON.stringify(material))
          
          // If the option selected was just to upload a file we add it to the form data
        } else if (this.materials[key].option === 'file' || this.materials[key].option.includes('file')) {  
          formData.append("materials", this.materials[key].value)
        }
        else if (this.materials[key].option === 'lorentz') {
          // For Lorentz add two files, one for Em and another one for Ei
          // Also add manual parameters en each case
          if ('em' in this.materials[key]) {
            formData.append("materials", this.materials[key].em.value)
          } 
          // Constant values
          if ('e-em' in this.materials[key] || 'nk-em' in this.materials[key] ||
            'e-ei' in this.materials[key] || 'nk-ei' in this.materials[key]) {
            let material = {}
            material[key] = this.materials[key]
            formData.append("materials", JSON.stringify(material))
          }
          if ('ei' in this.materials[key]) {
            formData.append("materials", this.materials[key].ei.value)
            let material = {}
            material[key] = {volume: this.materials[key].ei.volume}
            formData.append("materials", JSON.stringify(material))
          }
        } else {
          // Send data for all of the other methods as a JSON
          let material = {}
          material[key] = this.materials[key]
          formData.append("materials", JSON.stringify(material))
        }
        // Add information about thickness on the layer
        if (key.includes('layer')) {
          const index = key.split('-')[1] - 1 
          let material = {}
          material[key] = {
            thickness: this.layers[index].thickness
          }
          formData.append("materials", JSON.stringify(material))
        } 
      });
      // Send data to the backend by calling a vue action.
      this.sendData(formData);
    }, 
    uploadFile(method, modal) {
      // Get entity (subtract, host, layers) to update
      // its option and file uploaded
      let currentEntity = this.entityPointer
      let data = {
        option: 'file',
        value: this.renameFile(this.file, currentEntity),
      }
      method(); // Close modal
      this.materials[currentEntity] = data // Add data for the current material to the materials list
      this.disableEntity() // Disable the dropdown for this material
      this.cleanModal(modal) // Clean all fields on the modal once it is closed
    }, 
    setDielectricMethod(method, modal) {
      // get current material (substract, host or layer)
      let currentEntity = this.entityPointer
      const option = this.dielectricModel
      let data = {
        option: option,
      }
      // Identify dielectric method and get parameters depending on the
      // option selected by the user
      if (option === 'lorenz') {
        data = {
          ...data,
          ne: this.lorenz.ne,
          wo: this.lorenz.wo,
          w: this.omega,
          r: this.lorenz.r,
        }
      }

      if (option === 'drude') {
        data = {
          ...data,
          ne: this.drude.ne,
          e: this.drude.e,
          w: this.omega,
          r: this.drude.r,
        }
      }

      if (option === 'sellmeier') {
        data = {
          ...data,
          a: this.sellmeier.a,
          b: this.sellmeier.b,
          lambda: this.waveLength,
          lambdaO: this.sellmeier.lambdaO,
        }
      }

      if (option === 'cauchy') {
        data = {
          ...data,
          a: this.cauchy.a,
          b: this.cauchy.b,
          c: this.cauchy.c,
          lambda: this.waveLength,
        }
      }
      // Add thickness value in case the current material is a layer
      if (currentEntity.includes('layer')) {
        const index = parseInt(currentEntity.split('-')[1]) - 1;
        data = {
          ...data,
          thickness: this.layers[index].thickness,
        }
      }
      method(); // Close modal
      this.materials[currentEntity] = data // Add data for the current material to the materials list
      this.disableEntity() // Disable the dropdown for this material
      this.cleanModal(modal) // Clean all fields on the modal once it is closed
    },
    setManualMethod(method, modal) {
      // Add manual n and k data
      let currentEntity = this.entityPointer
      let data = {
        option: 'manual',
        k: this.manual.k,
        n: this.manual.n,
      }
      method(); // Close modal
      this.materials[currentEntity] = data // Add data for the current material to the materials list
      this.disableEntity() // Disable the dropdown for this material
      this.cleanModal(modal) // Clean all fields on the modal once it is closed
    },
    validateEffectiveMethod(method, modal) {
      const option = this.effectiveMediumModel
      this.okButtonPressed = true
      
      if (option === 'maxwell') {
        const emptyVolumes = (element) => !element.volume || element.volume <= 0;
        const existEmptyVolumes = this.inclusions.some(emptyVolumes)
        if (!existEmptyVolumes) {
          this. setEffectiveMethod(method, modal);
        }
      }

      if (option === 'lorentz') {
        if (this.lorentz.volume || this.lorentz.volume > 0) {
          this. setEffectiveMethod(method, modal);
        }
      }
      
      if (option === 'bruggeman') {
        const emptyVolumes = (element) => !element.volume || element.volume <= 0;
        const existEmptyVolumes = this.components.some(emptyVolumes)
        if (!existEmptyVolumes) {
          this. setEffectiveMethod(method, modal);
        }
      }
    },  
    setEffectiveMethod(method, modal) {
      // Get current material (substract, host or layer)
      let currentEntity = this.entityPointer
      const option = this.effectiveMediumModel
      let data = {
        option: option,
      }
      // Identify dielectric method and get parameters
      if (option === 'maxwell') {
        // Send parameters for manual Maxwell
        if (this.maxwell.em === 'manually') {
          data[this.maxwell.emManual] = {
            e1m: this.maxwell.e1m,
            e2m: this.maxwell.e2m,
            nm: this.maxwell.nm,
            km: this.maxwell.km,
          }
        }
        // Send file for Maxwell with filename 'entity-maxwell'
        if (this.maxwell.em === 'file') {
          const newFileName = `${currentEntity}-${option}`
          data = {
            option: `${option}-file`,
            value: this.renameFile(this.maxwell.file, newFileName),
          }
        }

        //  Add inclusions
        this.inclusions.forEach((inclusion, index) => {
          if (inclusion.method === "manually") {
            data[`${currentEntity}-inclusion-${index + 1}`] = {
              option: inclusion.manual,
              e1m: inclusion.e1m,
              e2m: inclusion.e2m,
              km: inclusion.km,
              nm: inclusion.nm,
              volume: inclusion.volume,
            }
          }
          if (inclusion.method === "file") {
            const newFileName = `${currentEntity}-inclusion-${index + 1}`
            data[`${currentEntity}-inclusion-${index + 1}`] = {
              option: 'file',
              value: this.renameFile(inclusion.file, newFileName),
              volume: inclusion.volume,
            }
          }
        });
      }

      if (option === 'lorentz') {
        // Send parameters for manual Lorentz
        if (this.lorentz.em === 'manually') {
          data[`${this.lorentz.emManual}-em`] = {
            e1m: this.lorentz.e1m,
            e2m: this.lorentz.e2m,
            nm: this.lorentz.nm,
            km: this.lorentz.km,
          }
        }
        if (this.lorentz.ei === 'manually') {
          data[`${this.lorentz.eiManual}-ei`] = {
            e1i: this.lorentz.e1i,
            e2i: this.lorentz.e2i,
            ni: this.lorentz.ni,
            ki: this.lorentz.ki,
            volume: this.lorentz.volume,
          }
        }
        // Send file for Lorentz with filename 'entity-lorentz'
        if (this.lorentz.em === 'file') {
          const newFileName = `${currentEntity}-em-${option}`
          data['em'] = {
            option: `${option}-file`,
            value: this.renameFile(this.lorentz.file, newFileName),
          }
        }

        if (this.lorentz.ei === 'file') {
          const newFileName = `${currentEntity}-ei-${option}`
          data['ei'] = {
            option: `${option}-file`,
            value: this.renameFile(this.lorentz.filei, newFileName),
            volume: this.lorentz.volume,
          }
        }
      }

      if (option === 'bruggeman') {
        //  Add components
        this.components.forEach((component, index) => {
          if (component.method === "manually") {
            data[`${currentEntity}-component-${index + 1}`] = {
              option: component.manual,
              e1i: component.e1i,
              e2i: component.e2i,
              ni: component.ni,
              ki: component.ki,
              volume: component.volume,
            }
          }
          if (component.method === "file") {
            const newFileName = `${currentEntity}-component-${index + 1}`
            data[`${currentEntity}-component-${index + 1}`] = {
              option: 'file',
              value: this.renameFile(component.file, newFileName),
              volume: component.volume,
            }
          }
        });
      }

      method(); // Close modal
      this.materials[currentEntity] = data // Add data for the current material to the materials list
      this.disableEntity() // Disable the dropdown for this material
      this.cleanModal(modal) // Clean all fields on the modal once it is closed
      this.okButtonPressed = false
    },
    disableEntity() {
      // Set html disabled property to true on the dropdown for the current entity selected
      const currentEntity = this.entityPointer;
      $( `#${currentEntity}` ).prop( "disabled", true );
    },
    cleanModal(modal) {
      // Set again the initial values to each modal according to the id
      // od the moda received on this method
      if (modal === 'modal-upload') {
        this.file = null
      }

      if (modal === 'modal-dielectric') {
        this.dielectricModel = null
        this.lorenz = {
          ne: null,
          wo: null,
          w: this.omega,
          r: null,
        }
        this.drude = {
          ne: null,
          e: null,
          w: this.omega,
          r: null,
        }
        this.sellmeier = {
          a: null,
          b: null,
          lambdaO: null,
        }
        this.cauchy = {
          a: null,
          b: null,
          c: null,
        }
      }

      if (modal === 'modal-manually') {
        this.manual = {
          n: null,
          k: null,
        }
      }

      if (modal === 'modal-efective') {
        this.effectiveMediumModel = null

        this.maxwell = {
          em: null,
          file: null,
          emManual: null,
          e1m: null,
          e2m: null,
          nm: null,
          km: null,
        }

        this.inclusions = [
          {
            method: null,
            file: null,
            manual: null,
            e1m: null,
            e2m: null,
            nm: null,
            km: null,
            volume: null,
          }
        ]

        this.lorentz = {
          em: null,
          file: null,
          emManual: null,
          e1m: null,
          e2m: null,
          nm: null,
          km: null,

          ei: null,
          filei: null,
          eiManual: null,
          e1i: null,
          e2i: null,
          ni: null,
          ki: null,
        }
      }

      this.components = [
        {
          method: null,
          file: null,
          manual: null,
          e1i: null,
          e2i: null,
          ni: null,
          ki: null,
          volume: null,
        }
      ]
    },
    updateWLayers() {
      Object.keys(this.materials).forEach(key => {
        if (key.includes('layer')){
          if ('w' in this.materials[key]){
            this.materials[key].w = this.omega || 'nm'
          }
        }
      });
    },
    cancel(modalId) {
      this.$bvModal.hide(modalId)
      if (this.entityPointer.includes('layer')) {
        const index = parseInt(this.entityPointer.split('-')[1]) - 1
        this.layers[index].model = null
      } else {
        if (this.entityPointer === 'substrate') {
          this.substrate = null
        }
        if (this.entityPointer === 'host') {
          this.host = null
        }
      }
    },
    calculateLambda() {
      let initial = parseFloat(this.initialWaveLength)
      const final = parseFloat(this.finalWaveLength)
      const steps = parseFloat(this.steps)
      const increase = (final - initial) / steps
      let lambda = []
      while (lambda.length < steps) {
        initial += increase
        lambda.push(isNaN(initial)? 0 : initial.toFixed(4))
      }
      this.waveLength = String(lambda) 
    },
  },
  watch: {
    omega: {
      handler(newValue) {
        this.lorenz.w = this.omega
        this.drude.w = this.omega
        this.updateWLayers() 
      }
    },
    initialWaveLength: {
      handler(newValue) {
        if (this.type === 'espectral' && this.initialWaveLength && this.finalWaveLength && this.steps) {
          this.calculateLambda()
        }
      }
    },
    finalWaveLength: {
      handler(newValue) {
        if (this.type === 'espectral' && this.initialWaveLength && this.finalWaveLength && this.steps) {
          this.calculateLambda()
        }
      }
    },
  },
  mounted() {
    this.lorenz.w = this.omega || 'nm'
    this.drude.w = this.omega || 'nm'
    this.updateWLayers() 
    if (this.type === 'espectral') {
      this.calculateLambda()
    }
  },
}
</script>