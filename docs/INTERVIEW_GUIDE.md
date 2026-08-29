# ClimateFlow BC Interview Guide

Use these answers as talking points rather than a memorized script. Keep the explanation conversational and adjust the technical depth to the interviewer.

## Tell me about this project.

ClimateFlow BC is an end-to-end environmental data science project using real daily observations from Squamish Airport and the Squamish River near Brackendale. I cleaned and joined the 2020 climate and streamflow records, explored seasonal and extreme-flow patterns, created lagged and rolling features, and compared a persistence baseline, Linear Regression, and Random Forest for next-day streamflow. I used a chronological holdout because this is time-ordered data and presented the results in a Streamlit dashboard.

## Why did you choose it?

I study Statistics and Environmental Science at UBC, so I wanted a project that genuinely connected both areas. River flow is environmentally meaningful, and it also creates a useful statistics problem involving missing data, seasonality, temporal dependence, feature engineering, and honest model evaluation.

## Why did you use an inner join?

Each modeling row needs climate and streamflow observations for the same date. An inner join keeps only dates present in both cleaned datasets, so it avoids creating rows that have no matching observation from one source. Because the climate file covered all 366 days of 2020 and streamflow was complete for those dates, the merged dataset retained all 366 days.

## Why did you use chronological validation?

A random split would mix later dates into the training data and earlier dates into the test data. That would not represent the real task of learning from the past and predicting a later period. I trained on the first 80% of modeling dates and tested on the final 20% without shuffling.

## What is data leakage?

Data leakage happens when information that would not be available at prediction time enters model training or a feature. It can make test performance look unrealistically strong. In this project, tomorrow's streamflow appears only in the target, lagged variables are created with shifts, the historical seven-day flow mean is shifted before rolling, and the models are fitted only on the earlier training rows.

## Why create lagged features?

Rivers respond over time rather than only to conditions on one date. The wettest day and highest-flow day in 2020 were different, which suggested that same-day precipitation alone was insufficient. Lagged flow, accumulated precipitation, and rolling temperature features represent recent environmental conditions and river memory.

## Why does current streamflow dominate feature importance?

Daily river discharge has strong temporal persistence: tomorrow's flow is usually related to today's flow because watershed storage and river conditions do not reset overnight. Current streamflow therefore contains a large amount of predictive information. That is also why persistence is a meaningful baseline.

## What does MAE mean?

Mean Absolute Error is the average absolute difference between predicted and observed flow. It stays in the original unit, cubic metres per second, and describes the size of a typical error without giving extra weight to very large misses.

## What does RMSE mean?

Root Mean Squared Error also measures prediction error in cubic metres per second, but it squares errors before averaging. Large misses therefore have more influence, which is useful when peak-flow errors are especially important.

## What does R² mean?

R² describes how much of the variation in the held-out observations is explained relative to simply predicting the test-set mean. The Linear Regression R² of 0.663 means it explained about 66% of the held-out variation in this particular 70-day test period. It is not a claim about causal explanation or guaranteed future performance.

## Why did Random Forest win MAE while Linear Regression won RMSE and R²?

Random Forest made the smallest typical absolute error, so it had the lowest MAE at 51.564 m³/s. Linear Regression handled the overall variation and larger errors better, producing the lowest RMSE at 83.974 m³/s and the highest R² at 0.663. The metrics emphasize different error behavior, so I would not call either model universally best.

## How did you handle missing data?

The merged data contained four missing mean-temperature values and nine missing precipitation values, with no missing streamflow. I linearly interpolated only short internal climate gaps of up to three days. Longer gaps remained missing, affected modeling rows were removed, and streamflow was never interpolated. For an operational workflow, I would replace retrospective interpolation with a past-only approach.

## What are the project's biggest limitations?

The project uses only one year, so it cannot represent year-to-year variability. The 70-day holdout covers late autumn and winter rather than every season. Airport observations may not represent the full watershed, and the models omit snowpack, soil moisture, elevation, and possible river regulation. Rare high-flow events are also difficult to learn from a small sample.

## What would you do with another month to improve it?

I would add multiple years of consistent observations, use rolling-origin time-series validation, and compare performance across seasons and high-flow events. I would also investigate watershed-level precipitation, snowpack, soil moisture, and regulation data. Finally, I would add residual diagnostics and test whether simpler seasonal encodings improve generalization.

## Why doesn't feature importance imply causation?

Feature importance describes how useful a variable was for predictions inside one fitted model. It does not isolate an environmental mechanism, rule out confounding variables, or show that changing the feature would change streamflow. Correlated lagged and rolling variables can also divide importance among themselves.

## Short closing summary

The main value of ClimateFlow BC is the complete, reproducible workflow: real public environmental data, transparent data-quality decisions, time-aware feature engineering, chronological evaluation against a strong baseline, and clear communication of both results and limitations.
