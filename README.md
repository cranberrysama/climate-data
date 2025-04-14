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

See Readme_download_rawdata about how to download grid-level rawdata.

You can find the list of all projected GCMs and scenarios in the file 'scenarios_table.xlsx'

## 2. Downloaded Parameters

We downloaded daily climate variables from 2015 to 2100, and the spatial resolution of the grid-level raw data is 0.25 degrees x0.25 degrees:

- `tas` (K): Daily Near-Surface Air Temperature  
- `tasmax` / `tasmin` (K): Daily Maximum / Minimum Near-Surface Air Temperature  
- `hurs` (%): Near-Surface Relative Humidity  
- `huss` (kg/kg): Near-Surface Specific Humidity  
- `prec` (kg/m²/s): Precipitation Rate (mean daily)

> ⚠️ Note: Not all GCMs include all variables. Some may lack `tasmax`, `tasmin`, or `prec`.

The grid-level raw data has been deleted.  We are planing to redownloading and store all the raw data, you will find it in McCarl group NAS `10.118.30.41/CMIP6`。

## 3. Data Cleaning Process

### • Spatial Aggregation

We aggregated grid-level CMIP6 data to **county-level** averages using agricultural land area as weights. The processed data is stored in our NAS (`10.118.30.41`) in NetCDF format, with one file per 5-year period.

> If you wish to perform spatial aggregation for other regions (e.g., countries, custom zones), refer the script `weights_example.py`.  
> This script computes the share of each CMIP6 grid cell that overlaps with your target regions, based on a provided shapefile.  
>  **Make sure** the shapefile and CMIP6 grid resolution are aligned and properly buffered to capture all overlapping areas.

### • Additional Variables

We derived the following variables from daily data:

- 55 Degree Day bins (–12°C to 42°C)
- 45 Freezing Degree Day bins (–20°C to 25°C)
- 59 Temperature bins (–12°C to 46°C)
- 2 Precipitation intensity  (90th and 95th percentiles)

> ⚠️ Rare cases of `tasmax < tasmin` in GCM data may cause minor bin errors, but are negligible.


### • Crop-Specific Growing Season Aggregation

We created yearly **growing season summaries** based on crop and state-specific growing dates 

> 🌱 Growing season information is available in ` Modified_GrowingSeason_bystate2.csv`.
> Note: In the growing season aggregation, precipitation rate was converted from **kg/m²/s** to **kg/m²/day**.
> We also computed average growing season data for two future periods: **2045–2055** and **2085–2095**.  
> These datasets are available at:  
> `NAS\Climate data\CMIP6\US\growing_season_data\2050`  
> `NAS\Climate data\CMIP6\US\growing_season_data\2090`


### • Monthly / Quarterly / Yearly Aggregation for Livestock


This upcoming dataset (in progress) will include:

- **Temperature-Humidity Index** (`THI_max`, `THI_min`)
- **THI Bins**
- **Relative Humidity** (`RH_max`, `RH_min`)
- **RH Bins**

The data is prepared for **state-level livestock analysis**, covering major categories such as **cattle, hogs, layers, and broilers ...**.

> Climate variables are aggregated at the state level using county-level livestock populations as weights.



---

## Contact

If you need access to this dataset or need help adapting the preprocessing code, feel free to contact mengqiaoliu@tamu.edu.

