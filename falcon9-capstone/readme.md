# SpaceX Falcon 9 First Stage Landing Prediction (IBM Applied Data Science Capstone)

Prediction of Falcon 9 first-stage landing success using SpaceX launch data.  
Project created as part of the **IBM Data Science Professional Certificate – Applied Data Science Capstone**.

## Project summary
The goal is to build a classification model that predicts whether the first stage of a Falcon 9 launch will successfully land (target: `Class`).

This repository includes:
- data collection (SpaceX API + web scraping),
- data wrangling & EDA (including SQL),
- interactive visual analytics (Folium maps + Dash dashboard),
- predictive modeling (LogReg, SVM, Decision Tree, KNN + GridSearchCV).

## Key results (high level)
- Best model: **SVM** (tie on test accuracy resolved by higher CV score).
- Evaluation: accuracy + confusion matrix (see notebooks).

## Data sources
- SpaceX public API (launches/rockets/launchpads/payloads/cores)
- Wikipedia launch tables (scraped)
- IBM Skills Network provided CSV datasets (capstone labs)