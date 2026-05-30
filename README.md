# Part 4: Churn Inference API & Documentation

## Project Overview
This repository contains Part 4 of the D2C Customer Churn Intelligence & Retention API Capstone. The objective is to deploy the Champion Machine Learning model trained in Part 3 as a REST API that the marketing CRM can query to identify at-risk customers.

## File Structure
- `app.py`: FastAPI application containing the `/health`, `/predict`, and `/batch_predict` endpoints.
- `model.pkl`: The serialized `scikit-learn` Random Forest Champion model imported from Part 3.
- `api_spec.md`: Detailed documentation on the API endpoints, request schemas, response formats, and cURL examples.
- `integration_guide.md`: Architectural guidance for the CRM team on how to query the batch endpoint nightly and trigger downstream retention workflows.
- `requirements.txt`: Python dependencies required to run the API.

## Setup & Execution
1. This project part is meant to be a standalone repository.
2. Ensure Python 3.9+ is installed.
3. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the FastAPI server using Uvicorn:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```
5. Access the interactive Swagger API documentation in your browser at:
   `http://localhost:8000/docs`

## Features
- **Pydantic Validation:** Strict type enforcement on all 25 input features.
- **Custom Threshold:** The model returns a dynamic boolean `churn_risk_flag` calculated against the heavily-researched threshold of `0.40` (optimized for Recall).
- **Batch Processing:** Highly optimized `/batch_predict` endpoint to avoid thousands of individual API calls during nightly CRM syncs.

## Sample Request & Response

**Endpoint:** `/predict`

**Request:**
```json
{
  "customer_id": "CUST00001",
  "city_tier": "Tier 1",
  "age_group": "25-34",
  "acquisition_channel": "Organic",
  "loyalty_tier": "Gold",
  "preferred_category": "Skin Care",
  "marketing_consent": "Yes",
  "recency_days": 12.5,
  "frequency_180d": 4.0,
  "monetary_180d": 2500.0,
  "return_rate_180d": 0.0,
  "avg_discount_pct_180d": 0.15,
  "avg_rating_180d": 4.5,
  "category_diversity_180d": 2.0,
  "ticket_count_90d": 0.0,
  "negative_ticket_rate_90d": 0.0,
  "avg_resolution_hours_90d": 0.0,
  "days_since_signup": 365.0,
  "sessions_30d": 5.0,
  "product_views_30d": 12.0,
  "cart_adds_30d": 2.0,
  "wishlist_adds_30d": 1.0,
  "abandoned_carts_30d": 0.0,
  "email_opens_30d": 4.0,
  "campaign_clicks_30d": 1.0,
  "last_visit_days_ago": 3.0
}
```

**Response:**
```json
{
  "customer_id": "CUST00001",
  "churn_probability": 0.2314,
  "predicted_class": 0,
  "risk_level": "low",
  "risk_explanation": "Low risk of churn. Monitor routinely."
}
```

## Docker Support
This API includes a Dockerfile for exact reproducibility. To build and run:
```bash
docker build -t churn-api .
docker run -p 8000:8000 churn-api
```
