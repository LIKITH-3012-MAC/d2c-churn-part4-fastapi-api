# Model Monitoring & Drift Plan

To ensure the Churn Prediction Model remains accurate in production, the MLOps team must implement the following monitoring strategies:

## 1. Data Drift Monitoring (Features)
We will monitor the distribution of incoming API payloads against the training data (`rfm_modeling_snapshot.csv`).
- **Metric:** Population Stability Index (PSI) and Kolmogorov-Smirnov (K-S) test.
- **Alert Threshold:** Trigger a Slack alert to the Data Science team if the PSI of critical features (e.g., `last_visit_days_ago`, `recency_days`, `ticket_count_90d`) exceeds 0.2.
- **Cause:** Changes in the underlying website UX might drastically alter `last_visit_days_ago` distributions.

## 2. Concept Drift Monitoring (Target)
The relationship between the features and the actual churn label may change over time (e.g., due to macroeconomic factors).
- **Metric:** F1-Score and Recall.
- **Process:** At the end of every month, we will join our predictions with the actual 60-day purchasing behavior to calculate real-world Recall.
- **Alert Threshold:** Trigger an automatic model retraining pipeline if monthly Recall drops below 85% (from the baseline of 90.4%).

## 3. API Performance Monitoring
- **Metric:** P99 Latency and Error Rates (422 and 500 status codes).
- **Tooling:** Prometheus and Grafana.
- **Alert:** PagerDuty alert if P99 latency exceeds 500ms on the `/predict_batch` endpoint, as this could cause timeouts in the CRM ETL sync.
