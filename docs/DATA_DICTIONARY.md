# Data Dictionary

## Data sources

- Climate: Environment and Climate Change Canada daily observations, Squamish Airport, 2020
- Streamflow: Water Survey of Canada daily discharge, Squamish River near Brackendale, station `08GA022`, 2020

## Core variables

| Variable | Meaning | Unit | Modeling timing |
|---|---|---|---|
| `date` | Date on which predictors are observed | YYYY-MM-DD | Current day |
| `mean_temp_c` | Daily mean air temperature | °C | Current day |
| `precipitation_mm` | Daily total precipitation | mm | Current day |
| `streamflow_cms` | Daily mean river discharge | m³/s | Current day |

## Engineered variables

| Variable | Definition | Unit | Modeling timing |
|---|---|---|---|
| `precip_lag1` | Precipitation one day earlier | mm | Previous day |
| `precip_3day` | Sum of precipitation over current and previous two days | mm | Through current day |
| `precip_7day` | Sum of precipitation over current and previous six days | mm | Through current day |
| `temp_3day_mean` | Mean temperature over current and previous two days | °C | Through current day |
| `temp_7day_mean` | Mean temperature over current and previous six days | °C | Through current day |
| `streamflow_lag1` | Streamflow one day earlier | m³/s | Previous day |
| `streamflow_lag3` | Streamflow three days earlier | m³/s | Three days earlier |
| `streamflow_7day_mean` | Mean streamflow over the seven days before the current day | m³/s | Prior days only |
| `month` | Calendar month number | 1–12 | Current day |
| `day_of_year` | Sequential calendar day | 1–366 | Current day |
| `target_next_day_streamflow` | Streamflow one day after `date` | m³/s | Prediction target only |

## Missing-value treatment

The merged dataset has four missing temperature observations and nine missing precipitation observations. Feature engineering applies linear interpolation only to internal climate gaps of at most three consecutive days. Longer gaps remain missing, and affected modeling rows are dropped. Streamflow is not interpolated.

Linear interpolation is used for this retrospective portfolio analysis. A live forecasting workflow would require a past-only imputation method.
