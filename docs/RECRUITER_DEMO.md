# Recruiter Demo Guide

## 30-second pitch

I built ClimateFlow BC, an end-to-end environmental data science project using real 2020 observations from Squamish Airport and the Squamish River near Brackendale. I cleaned and joined daily climate and hydrometric data, explored seasonal and extreme-flow patterns, engineered lagged time-series features, evaluated three next-day prediction approaches with a chronological holdout, and communicated the results in a Streamlit dashboard.

## Two-minute walkthrough

1. Start with the README research question and real official data sources.
2. Show the EDA finding that the wettest and highest-flow days are different.
3. Explain why that motivates lagged and rolling predictors.
4. Show the chronological train/test boundary in the modeling notebook.
5. Compare all three models against persistence.
6. Show the held-out prediction chart and feature importance.
7. End with the dashboard and limitations.

## Results to remember

- 366 merged daily observations; 349 complete modeling rows
- Train: January 8–October 21; test: October 22–December 30
- Linear Regression: best RMSE (83.974 m³/s) and R² (0.663)
- Random Forest: best MAE (51.564 m³/s)
- Current streamflow is the strongest Random Forest feature

## Resume bullet

Built an end-to-end Python environmental analytics pipeline using real ECCC and Water Survey of Canada data; engineered lagged hydroclimate features, compared persistence, Linear Regression, and Random Forest with chronological validation, and communicated results through a Streamlit dashboard.

## Likely interview questions

**Why use a chronological split?**  
Random splitting would mix later dates into training and make the test less representative of predicting an unseen future period.

**Why include a persistence baseline?**  
River flow is persistent. A learned model should be judged against the simple assumption that tomorrow resembles today.

**Why include current streamflow in the learned models?**  
The forecast is defined at the end of the current day, when today’s flow is known. The baseline uses the same observation, so including it makes the comparison fair.

**Why did different metrics select different models?**  
Random Forest has the lowest average absolute error, while Linear Regression handles the held-out variance and larger errors better. Model choice depends on the cost of typical versus large misses.

**Does feature importance prove causation?**  
No. It measures predictive usefulness inside one fitted model and can be distributed among correlated variables.

**What would you improve?**  
Add multiple years, rolling-origin validation, watershed precipitation, snowpack, soil moisture, elevation, and information about river regulation.

## Credibility guardrails

- Say “predictive association,” not “cause.”
- Describe results as held-out 2020 performance, not expected future accuracy.
- Do not call the project an operational flood forecasting system.
