# CRM Integration Guide

This document provides architectural guidance for integrating the D2C Churn Inference API with the internal Marketing CRM.

## Architecture & Workflow

### 1. Nightly Data Extraction (ETL)
Every night at 02:00 AM UTC, the Data Warehouse must run a batch job to compute the latest RFM and behavioral features for all active customers over the trailing 180 and 30-day windows. The resulting dataset must match the Pydantic schema defined in the API.

### 2. Batch Inference Call
Rather than querying the API for each of the ~100,000 customers individually, the CRM should use the `/predict_batch` endpoint.
- **Batch Size:** We recommend chunking the requests into blocks of 1,000 to 5,000 customers per HTTP POST request to avoid overwhelming the network payload size.
- **Timeout Configuration:** Set the HTTP client timeout to at least 30 seconds for batch requests.

### 3. CRM Tagging & Action
The API will return an array containing `churn_probability` and `churn_risk_flag`. 
- **Flag Logic:** If `churn_risk_flag == true` (meaning the probability is $\ge 0.40$), the CRM should automatically tag the customer profile with `[AT_RISK_CHURN]`.
- **Campaign Triggers:** 
  - If a customer is tagged `[AT_RISK_CHURN]`, immediately suppress them from generic "New Launch" campaigns (as per EDA findings).
  - Add them to the "Win-Back" email automation flow.
  - If their monetary value is $>$ 1000 INR and they have open support tickets, trigger an alert to the Customer Success Slack channel for manual review.

## Error Handling best practices
- **422 Unprocessable Entity:** If the API returns a 422, it means the ETL job sent a malformed record (e.g., passing a string into a float field). The CRM should log the specific `customer_id` and continue processing the rest of the batch.
- **503 Service Unavailable:** If the model fails to load into the API's memory during startup, the CRM should trigger a PagerDuty alert to the MLOps team rather than silently failing.
