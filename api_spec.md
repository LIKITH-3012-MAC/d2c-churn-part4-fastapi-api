# D2C Churn Inference API Specification

This document details the HTTP endpoints available in the Churn Inference API.

## Base URL
`http://localhost:8000`

---

## 1. Health Check
**Endpoint:** `/health`
**Method:** `GET`
**Description:** Verifies that the API is running and the machine learning model is loaded into memory.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "model": "RandomForest Classifier"
}
```

---

## 2. Single Customer Prediction
**Endpoint:** `/predict`
**Method:** `POST`
**Description:** Predicts the 60-day churn probability for a single customer.

**Request Body:** (Content-Type: `application/json`)
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

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"customer_id": "CUST00001", "city_tier": "Tier 1", "age_group": "25-34", "acquisition_channel": "Organic", "loyalty_tier": "Gold", "preferred_category": "Skin Care", "marketing_consent": "Yes", "recency_days": 12.5, "frequency_180d": 4.0, "monetary_180d": 2500.0, "return_rate_180d": 0.0, "avg_discount_pct_180d": 0.15, "avg_rating_180d": 4.5, "category_diversity_180d": 2.0, "ticket_count_90d": 0.0, "negative_ticket_rate_90d": 0.0, "avg_resolution_hours_90d": 0.0, "days_since_signup": 365.0, "sessions_30d": 5.0, "product_views_30d": 12.0, "cart_adds_30d": 2.0, "wishlist_adds_30d": 1.0, "abandoned_carts_30d": 0.0, "email_opens_30d": 4.0, "campaign_clicks_30d": 1.0, "last_visit_days_ago": 3.0}'
```

**Response (200 OK):**
```json
{
  "customer_id": "CUST00001",
  "churn_probability": 0.2314,
  "churn_risk_flag": false,
  "threshold_used": 0.40
}
```

---

## 3. Batch Prediction
**Endpoint:** `/batch_predict`
**Method:** `POST`
**Description:** Predicts churn for multiple customers in a single request. Highly optimized for CRM nightly syncs.

**Request Body:** (Array of JSON objects)
```json
[
  { "customer_id": "CUST00001", ... },
  { "customer_id": "CUST00002", ... }
]
```

**Response (200 OK):**
```json
{
  "predictions": [
    {
      "customer_id": "CUST00001",
      "churn_probability": 0.2314,
      "churn_risk_flag": false,
      "threshold_used": 0.4
    },
    {
      "customer_id": "CUST00002",
      "churn_probability": 0.6120,
      "churn_risk_flag": true,
      "threshold_used": 0.4
    }
  ]
}
```
