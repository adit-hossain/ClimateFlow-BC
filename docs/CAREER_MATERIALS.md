# ClimateFlow BC Career Materials

Final public links are included below and are ready to copy.

## Resume — two-bullet version

**ClimateFlow BC | Environmental Data Science Project**  
*Python, pandas, scikit-learn, Matplotlib, Streamlit, time-series analysis*

- Built a reproducible hydro-climate analytics pipeline using 366 real 2020 observations from Squamish Airport and Water Survey of Canada station 08GA022; cleaned and joined daily records and engineered lagged, rolling, and seasonal features for 349 modeling observations.
- Evaluated persistence, Linear Regression, and Random Forest with a chronological 80/20 split; Random Forest achieved the lowest MAE (51.564 m³/s), while Linear Regression achieved the lowest RMSE (83.974 m³/s) and highest R² (0.663), with results communicated through an interactive Streamlit dashboard.

## Resume — compact one-bullet version

- Built and published an end-to-end Python/Streamlit hydro-climate analytics project using real 2020 Squamish data, engineering time-series features and chronologically evaluating persistence, Linear Regression, and Random Forest across 349 modeling observations.

## Resume — technical data-science version

**ClimateFlow BC | Time-Series Machine Learning Project**

- Developed a reproducible pandas pipeline to validate, merge, and transform 366 daily ECCC and Water Survey of Canada observations; treated short climate gaps, engineered lagged/rolling hydroclimate predictors, and created a leakage-aware next-day target.
- Trained and evaluated persistence, Linear Regression, and Random Forest on a chronological 80/20 split without shuffling; produced held-out MAE/RMSE/R² comparisons, prediction diagnostics, and Random Forest feature importance, then deployed the analysis through Streamlit.

## LinkedIn Project entry

**Project name**  
ClimateFlow BC — Hydro-Climate Analytics and Streamflow Modeling

**Description**  
Built an end-to-end environmental data science project using real 2020 observations from Squamish Airport and Squamish River near Brackendale (station 08GA022). I cleaned and merged 366 daily observations, engineered lagged and rolling hydroclimate features, and compared a persistence baseline, Linear Regression, and Random Forest using chronological validation. Random Forest produced the lowest MAE (51.564 m³/s), while Linear Regression produced the best RMSE (83.974 m³/s) and R² (0.663). Results are presented in an interactive Streamlit dashboard, with limitations documented clearly.

**Skills**  
Python · pandas · scikit-learn · Matplotlib · Streamlit · Data Cleaning · Exploratory Data Analysis · Time-Series Analysis · Feature Engineering · Machine Learning · Data Visualization · Environmental Data Analysis

**Project URLs**

- GitHub: `https://github.com/adit-hossain/ClimateFlow-BC`
- Live dashboard: `https://j7wndxxdfa8vc8dvc3ufgj.streamlit.app/`

## LinkedIn Featured section

### GitHub repository

**Title:** ClimateFlow BC — Environmental Data Science Project  
**Description:** Reproducible analysis of real 2020 Squamish climate and streamflow data, including cleaning, EDA, time-series feature engineering, chronological model evaluation, documentation, and tests.

### Live Streamlit dashboard

**Title:** ClimateFlow BC — Interactive Hydro-Climate Dashboard  
**Description:** Explore 2020 Squamish climate and river conditions, lagged relationships, held-out model performance, feature importance, methodology, and limitations.

## LinkedIn launch post

I built ClimateFlow BC to bring together the two areas I study at UBC: Environmental Science and Statistics.

The project uses real 2020 daily climate observations from Squamish Airport and streamflow records from Squamish River near Brackendale (Water Survey of Canada station 08GA022). I cleaned and joined 366 daily observations, explored seasonal and extreme-flow patterns, and created lagged and rolling features for next-day streamflow modeling.

I compared a persistence baseline, Linear Regression, and Random Forest using a chronological train/test split rather than randomly shuffling the time series. The models showed a useful tradeoff: Random Forest had the lowest typical absolute error, while Linear Regression had the strongest RMSE and R². Current streamflow dominated Random Forest feature importance, which reflects the strong day-to-day persistence of river discharge—not a causal conclusion.

The most valuable part for me was learning how much work happens around the model: validating public datasets, preventing leakage, choosing an honest baseline, documenting assumptions, and communicating limitations. With only one year of data, this is a portfolio analysis rather than an operational forecasting system, but it gave me a much clearer understanding of an end-to-end environmental data workflow.

GitHub: https://github.com/adit-hossain/ClimateFlow-BC  
Live dashboard: https://j7wndxxdfa8vc8dvc3ufgj.streamlit.app/

#EnvironmentalData #DataScience #Python #Streamlit #TimeSeries #UBC

## Portfolio website copy

### Project title

ClimateFlow BC

### One-line subtitle

Real Squamish climate and river data transformed into an interactive, time-aware streamflow analysis.

### Problem

How do daily temperature and precipitation relate to Squamish River streamflow, and how well can simple models estimate next-day flow?

### Approach

Clean and join official 2020 climate and hydrometric records, explore seasonal patterns, engineer lagged and rolling features, and compare three prediction approaches using a chronological holdout.

### Dataset

366 daily observations from Squamish Airport and Squamish River near Brackendale (`08GA022`), producing 349 complete modeling rows.

### Key findings

- The wettest and highest-flow days did not coincide, supporting the use of lagged features.
- Current streamflow was the strongest predictive Random Forest feature because river discharge is temporally persistent.
- Predictive importance and correlation were treated as associations, not causal evidence.

### Model results

- Random Forest: lowest MAE, 51.564 m³/s
- Linear Regression: lowest RMSE, 83.974 m³/s, and highest R², 0.663
- No model was universally strongest across every metric.

### Technologies

Python · pandas · scikit-learn · Matplotlib · Streamlit · time-series feature engineering

### Limitations

One year of data, a seasonally concentrated holdout, limited extreme events, airport-based climate measurements, and missing watershed variables such as snowpack and soil moisture.

### Calls to action

- **View source and methodology:** `https://github.com/adit-hossain/ClimateFlow-BC`
- **Explore the live dashboard:** `https://j7wndxxdfa8vc8dvc3ufgj.streamlit.app/`
