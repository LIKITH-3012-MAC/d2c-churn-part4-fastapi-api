from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import logging
from typing import List

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize App
app = FastAPI(
    title="D2C Customer Churn Inference API",
    description="API to predict 60-day customer churn risk using RFM and behavioral data.",
    version="1.0.0"
)

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / 'model.pkl'
try:
    model = joblib.load(MODEL_PATH)
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    model = None

# Custom optimal threshold defined in Part 3
OPTIMAL_THRESHOLD = 0.40

# Define Pydantic Input Schema
class CustomerFeatures(BaseModel):
    customer_id: str
    city_tier: str
    age_group: str
    acquisition_channel: str
    loyalty_tier: str
    preferred_category: str
    marketing_consent: str
    recency_days: float
    frequency_180d: float
    monetary_180d: float
    return_rate_180d: float
    avg_discount_pct_180d: float
    avg_rating_180d: float
    category_diversity_180d: float
    ticket_count_90d: float
    negative_ticket_rate_90d: float
    avg_resolution_hours_90d: float
    days_since_signup: float
    sessions_30d: float
    product_views_30d: float
    cart_adds_30d: float
    wishlist_adds_30d: float
    abandoned_carts_30d: float
    email_opens_30d: float
    campaign_clicks_30d: float
    last_visit_days_ago: float

class PredictionResponse(BaseModel):
    customer_id: str
    churn_probability: float
    predicted_class: int
    risk_level: str
    risk_explanation: str

class BatchPredictionResponse(BaseModel):
    predictions: List[PredictionResponse]

@app.get("/health")
def health_check():
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "healthy", "model": "RandomForest Classifier"}

@app.post("/predict", response_model=PredictionResponse)
def predict_churn(customer: CustomerFeatures):
    if model is None:
        raise HTTPException(status_code=503, detail="Model is currently unavailable.")
    
    try:
        # Convert input to DataFrame (drop customer_id as it's not a feature)
        input_dict = customer.dict()
        cust_id = input_dict.pop('customer_id')
        df = pd.DataFrame([input_dict])
        
        # Predict Probability
        prob = model.predict_proba(df)[0][1]
        
        # Apply custom threshold
        risk_flag = bool(prob >= OPTIMAL_THRESHOLD)
        level = "high" if risk_flag else "low"
        explanation = "High risk of churn. Priority intervention required." if risk_flag else "Low risk of churn. Monitor routinely."
        
        return PredictionResponse(
            customer_id=cust_id,
            churn_probability=round(prob, 4),
            predicted_class=int(risk_flag),
            risk_level=level,
            risk_explanation=explanation
        )
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/batch_predict", response_model=BatchPredictionResponse)
def predict_churn_batch(customers: List[CustomerFeatures]):
    if model is None:
        raise HTTPException(status_code=503, detail="Model is currently unavailable.")
    
    try:
        df_list = []
        cust_ids = []
        for c in customers:
            d = c.dict()
            cust_ids.append(d.pop('customer_id'))
            df_list.append(d)
        
        df = pd.DataFrame(df_list)
        probs = model.predict_proba(df)[:, 1]
        
        results = []
        for cid, prob in zip(cust_ids, probs):
            flag = bool(prob >= OPTIMAL_THRESHOLD)
            level = "high" if flag else "low"
            exp = "High risk of churn. Priority intervention required." if flag else "Low risk of churn. Monitor routinely."
            results.append(PredictionResponse(
                customer_id=cid,
                churn_probability=round(prob, 4),
                predicted_class=int(flag),
                risk_level=level,
                risk_explanation=exp
            ))
            
        return BatchPredictionResponse(predictions=results)
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
