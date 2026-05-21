from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "model": "RandomForest Classifier"}

def test_predict_single_customer():
    payload = {
      "customer_id": "CUST_TEST",
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
    
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "churn_probability" in data
    assert "predicted_class" in data
    assert "risk_level" in data
    assert "risk_explanation" in data
    assert data["customer_id"] == "CUST_TEST"

def test_batch_predict():
    payload = [{
      "customer_id": "CUST_1",
      "city_tier": "Tier 1", "age_group": "25-34", "acquisition_channel": "Organic",
      "loyalty_tier": "Gold", "preferred_category": "Skin Care", "marketing_consent": "Yes",
      "recency_days": 12.5, "frequency_180d": 4.0, "monetary_180d": 2500.0,
      "return_rate_180d": 0.0, "avg_discount_pct_180d": 0.15, "avg_rating_180d": 4.5,
      "category_diversity_180d": 2.0, "ticket_count_90d": 0.0, "negative_ticket_rate_90d": 0.0,
      "avg_resolution_hours_90d": 0.0, "days_since_signup": 365.0, "sessions_30d": 5.0,
      "product_views_30d": 12.0, "cart_adds_30d": 2.0, "wishlist_adds_30d": 1.0,
      "abandoned_carts_30d": 0.0, "email_opens_30d": 4.0, "campaign_clicks_30d": 1.0,
      "last_visit_days_ago": 3.0
    }]
    response = client.post("/batch_predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predictions" in data
    assert len(data["predictions"]) == 1
    assert "risk_explanation" in data["predictions"][0]

def test_predict_missing_fields():
    payload = {
      "customer_id": "CUST_TEST",
      "city_tier": "Tier 1"
      # Missing all other fields
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422 # Unprocessable Entity
