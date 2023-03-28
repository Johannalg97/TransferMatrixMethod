
# Transfer Matrix Method App

This web application is a tool for the analysis of ellipsometric spectroscopy data. It has the ability to create multilayer system models of isotropic materials using the Transfer Matrix Method, including the possibility to implement Effective Medium Theories and Dispersion Formulas. At the end the user will have the option to upload experimental data to compare with the created models calculating the goodness of fit (GOF), determined by the χ2 value.


## Requirements

- Python 3.8
- PostgreSQL 14.5
- Node v14

## Features

- Calculation of refractive indices manually, through a file (CSV, TXT or YML), through dielectric functions or effective medium theories.
- Add custom amount of layers, inclusions and components for theoretical analysis
- Generation of reflectance, absorbance and transmittance graphs for theoretical data.
- Download of calculated theoretical data of absorbance, reflectance, transmittance and refractive indices
- Comparison of theoretical and experimental data through the calculation of Chi square.
- Visualization of the history of Chi squares calculated for each experimental data file uploaded by the user and graph of these for visual comparison.



## Authors

[@johanna](https://www.github.com/xxxxxx)


## Installation

Create a postgreSQL DB

```bash
  sudo -u postgres psql postgres
```
```bash
  CREATE ROLE dbadmin WITH LOGIN ENCRYPTED PASSWORD 'password' CREATEDB CREATEROLE REPLICATION SUPERUSER;
```
```bash
  CREATE DATABASE demodb WITH OWNER dbadmin ENCODING 'UTF8';
```
```bash
  GRANT ALL PRIVILEGES ON DATABASE demodb TO dbadmin;
```
    
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`DATABASE_URL`

Following the example on the *Installation* section:

`DATABASE_URL=postgres://dbadmin:password@localhost/demodb`




## Run Locally

Clone the project

```bash
  git clone https://link-to-project .
```

Install dependencies

```bash
  pip install -r requirements/local.txt
```

Run migrations
```bash
  python manage.py migrate
```
Start the server

```bash
  python manage.py runserver
```
Bundle the app into static files
```bash
 yarn
 yarn run build
```

## API Reference

#### 1. Calculation of reflectance, transmittance, absorbance and refractive index for each material (substrate, layers and host)

```http
  POST /api/v1/transfer-method/
```

This endpoint uses the *CalculateDataView* view to receive all the information collected for each material and the parameters of the selected methods, as well as the supplied initial parameter values. Based on the information received in this POST-type request, the view is in charge of grouping, ordering the materials, and extracting the data with the different functions named in the Backend section. As a response, this view returns a JSON with the values of reflectance, absorbance, transmittance, range in x (either angle or wavelength depending on the type of response chosen by the user), the fixed parameter, and the refractive indices of each material.

Body parameters:
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `initialAngle` | `float` | Initial angle for angular answer |
| `finalAngle` | `float` | Final angle for angular answer |
| `angle` | `float` | Fixed parameter for spectral answer |
| `steps` | `integer` | **Required**. Number of steps between initial and final parameter |
| `initialWaveLength` | `float` | Initial wavelength for spectral answer |
| `finalWaveLength` | `float` | Initial wavelength for spectral answer |
| `waveLength` | `float` | Fixed parameter for angular answer |
| `polarization` | `string` | **Required**. Polarization P/S |
| `materials` | `array` | **Required**. List with all the materials data (files, parameters, method selected) |



#### 2. Download data from tables and graphs

```http
  POST /api/v1/download-data/
```

This endpoint uses the view *DownloadDataView* to download CSV files with the information coming from the table of refractive indices or the reflectance, transmittance, absorbance graphs.


Body parameters:
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `source` | `string` | **Required**. Table/Graph Indicates where the data comes from |
| `data` | `JSON` | **Required**. Values in Y for the selected type in case of being a graph or list of refractive indices in case of being a table, plus the range in x |
| `answer` | `string` | **Required**. Angular/Spectral answer selected |
| `type` | `string` | If the source is a graphic, the type is indicated (reflectance, transmittance, absorbance) |


#### 3. Comparison of experimental data

```http
  POST /api/v1/calculate-chi/
```

This endpoint uses the *CompareExperimentalDataView* view in order to receive, through a POST request, the information on the theoretical curve and the file uploaded by the user with the experimental data. As a result, this view returns a JSON with the interpolated experimental data vector, the chi-square value, the corresponding x-vector, and the name of the file to generate the front curve with its label.

Body parameters:
| Parameter | Type     | Description                                            |
| :-------- | :------- | :-------------------------------- |
| `answer`      | `string` | **Required**. Angular/Spectral | 
| `calculated_reflectance`      | `array` | **Required**. Vector of floating values with the reflectance calculated with the theoretical data | 
| `initial_param`      | `float` | **Required**. Initial angle or wavelength depending on the type of response (angular or spectral) |
| `final_param`      | `float` | **Required**. Initial angle or wavelength depending on the type of response (angular or spectral) | 
| `steps`      | `integer` | **Required**. Number of steps between the initial and the final parameter | 
| `file`      | `bytes` | **Required**. Experimental data file (CSV or TXT) |





## Support

For support, email johannalg97@gmail.com


## Screenshots
[![HG3LVQj.md.png](https://iili.io/HG3LVQj.md.png)](https://freeimage.host/i/HG3LVQj)
[![HG3QdaS.md.png](https://iili.io/HG3QdaS.md.png)](https://freeimage.host/i/HG3QdaS)
[![HG3LMhb.md.png](https://iili.io/HG3LMhb.md.png)](https://freeimage.host/i/HG3LMhb)
[![HG3LhEQ.md.png](https://iili.io/HG3LhEQ.md.png)](https://freeimage.host/i/HG3LhEQ)

## Tech Stack

**Client:** Vue 2, Bootstrap, Sass

**Server:** Django, PostgreSQL


## Usage
The files supplied as part of the parameters of the different materials in the Materials and initial parameters screen must meet the following characteristics:

- Have CSV, txt, or YML format
- The wavelength columns, n, and k must have the same length
- In CSV files a two-column file is expected, where the first column corresponds to the wavelength (headed by 'wl') and the second column corresponds to n (headed by 'n'). Subsequently, at the end of the wavelength vector, this column of wavelengths is expected to be repeated in the first column, heading the column with the letters 'wl' followed by column k (headed by the letter 'k').
- For plain text files the values of 'wl', 'n', and 'k' are expected to be provided in three columns separated by a space.
- For YML files the data section is expected to contain rows of three columns separated by a space, where each column represents the values of 'wl', 'n', and 'k' respectively.
- The reflectance file uploaded by the user in the experimental data section is expected to be in CSV or plain text format. This file must contain two columns, one of the points in x and another of reflectance values, in that order respectively.
## Demo

URL to the current instance on Linode.
