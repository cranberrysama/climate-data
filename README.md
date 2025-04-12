# CMIP6 Data Summary

## 1. Data Source

The NEX-GDDP-CMIP6 dataset is obtained from the [NASA Center for Climate Simulation (NCCS)](https://www.nccs.nasa.gov/services/data-collections/land-based-products/nex-gddp-cmip6). The NEX-GDDP-CMIP6 is comprised of global downscaled climate scenarios derived from 35 General Circulation Model (GCM) runs conducted under the Coupled Model Intercomparison Project Phase 6 (CMIP6) [Eyring et al. 2016] and across the four “Tier 1” greenhouse gas emissions scenarios known as Shared Socioeconomic Pathways (SSPs). Four SSPs represent different levels of greenhouse gas emissions:

- **SSP126**: Low emissions scenario (sustainability)
- **SSP245**: Intermediate emissions scenario
- **SSP370**: High emissions scenario with regional rivalry
- **SSP585**: Very high emissions scenario (fossil-fueled development)

For detailed explanation of the SSP scenarios, visit the [German Climate Computing Center (DKRZ)](https://www.dkrz.de/en/communication/climate-simulations/cmip6-en/the-ssp-scenarios).

You can manually browse or download the original data from the AWS S3 portal:  
📎 [https://nex-gddp-cmip6.s3.us-west-2.amazonaws.com/index.html](https://nex-gddp-cmip6.s3.us-west-2.amazonaws.com/index.html)

To re-download the raw data, use the provided `.bat` script and modify the scenario name and variables as needed.

## 2. Downloaded Parameters

We downloaded daily climate variables from 2015 to 2100, and the spatial resolution of the grid-level raw data is 0.25 degrees x0.25 degrees:

- `tas` (K): Daily Near-Surface Air Temperature  
- `tasmax` / `tasmin` (K): Daily Maximum / Minimum Near-Surface Air Temperature  
- `hurs` (%): Near-Surface Relative Humidity  
- `huss` (kg/kg): Near-Surface Specific Humidity  
- `prec` (kg/m²/s): Precipitation Rate (mean daily)

> ⚠️ Note: Not all GCMs include all variables. Some may lack `tasmax`, `tasmin`, or `prec`.

The grid-level raw data has been deleted.  We are planing to redownloading and store all the raw data, you will find it in McCarl group NAS。

## 3. Data Cleaning Process

### • Spatial Aggregation

We aggregated grid-level data to **county-level** averages using agricultural land area as weights. The final dataset has the format:

