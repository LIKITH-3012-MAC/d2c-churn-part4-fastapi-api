# ChurnLens AI — D2C Customer Churn FastAPI Prediction Service

This repository hosts **Part 4** of the D2C Churn prediction series: a production-ready FastAPI inference service bundled with a premium interactive 3D visual analytics dashboard. 

The service loads a trained machine learning model to predict the 60-day customer churn risk using RFM metrics (Recency, Frequency, Monetary) and real-time customer behavioral features.

---

## 🚀 Key Features

* **Real-time Inference API**: RESTful endpoints powered by FastAPI for single-customer predictions (`/predict`) and bulk predictions (`/batch_predict`).
* **In-Memory ML Model**: Loaded on startup from `model.pkl` (RandomForest Classifier) with preprocessing pipeline steps (imputation, scaling, one-hot encoding).
* **ChurnLens AI Dashboard**: A premium, responsive glassmorphic console served directly at the root URL (`/`) featuring 3D double shadows and support for both Light and Dark modes.
* **Interactive Persona Presets**: Quick-load predefined customer profiles (VIP Promoter, Bargain Hunter, Slipping Champion, and New Inactive) to inspect model results.
* **Live Threshold Simulator**: Dynamically adjust the decision threshold (default: `0.40`) to inspect how it shifts low/high risk categories, revenue at risk, and intervention requirements in real-time.
* **CSV Batch Upload Drop-zone**: Drag-and-drop or select customer list CSVs to perform batch predictions, calculate aggregate metrics, and download the outcomes.
* **CRM Intervention Engine**: Programmatically generates automated recommendations (e.g. email win-back routing, Slack alert escalation for high-value clients with unresolved support tickets, marketing suppression tags).

---

## 📂 Repository Structure

```
.
├── app/
│   ├── static/
│   │   └── index.html      # Premium visual dashboard console
│   ├── __init__.py
│   ├── main.py             # FastAPI main application & endpoint definitions
│   └── ui.py               # UI serving route logic
├── data/
│   └── d2c_churn_data_package/
│       ├── customers.csv
│       ├── orders.csv
│       ├── support_tickets.csv
│       └── ...
├── tests/
│   └── test_api.py         # Integration & unit tests for endpoints
├── Dockerfile              # Docker container definition
├── model.pkl               # Serialized RandomForest classifier pipeline
├── requirements.txt        # Package dependencies
├── ui_app.py               # Main python entrypoint wrapper (standard)
└── ui-app.py               # Entrypoint wrapper (alias)
```

---

## 🔧 Installation & Setup

Ensure you have Python 3.9+ installed, then run the following:

```bash
# 1. Create a virtual environment
python -m venv venv

# 2. Activate the virtual environment
# On macOS / Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 3. Install required packages
pip install -r requirements.txt
```

---

## 🏃 Running the Application

There are three ways to launch the prediction service:

### Option A: Standard Python Script (Recommended)
Run the execution wrapper directly from the root of the repository. This is PEP 8 compliant, handles module resolutions automatically, and configures automatic code-reload:
```bash
python ui_app.py
```

### Option B: Python Alias Script
Alternatively, you can run using the hyphenated alias script name matching your terminal preferences:
```bash
python ui-app.py
```

### Option C: Uvicorn Directly
You can run the ASGI server directly using Uvicorn:
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Once running, the application will print:
```
Starting ChurnLens AI unified server...
Dashboard will be available at http://127.0.0.1:8000
```
Open your web browser and navigate to **`http://127.0.0.1:8000`** to access the graphical console, or **`http://127.0.0.1:8000/docs`** to test endpoints directly inside the interactive Swagger UI.

---

## 📋 API Endpoint Documentation

### 1. Health Status check
* **Route**: `/health` (`GET`)
* **Returns**: Verification that the API is running and the machine learning model is loaded in memory.
* **Response**:
  ```json
  {
    "status": "healthy",
    "model": "RandomForest Classifier"
  }
  ```

### 2. Single Customer Prediction
* **Route**: `/predict` (`POST`)
* **Payload**: Complete JSON customer details (demographics, transaction stats, tickets, clickstream sessions).
* **Response**:
  ```json
  {
    "customer_id": "CUST_TEST",
    "churn_probability": 0.0861,
    "predicted_class": 0,
    "risk_level": "low",
    "risk_explanation": "Low risk of churn. Monitor routinely."
  }
  ```

### 3. Bulk Batch Prediction
* **Route**: `/batch_predict` (`POST`)
* **Payload**: A JSON array of customer objects.
* **Response**: A list of predictions detailing risk metrics for each customer.

---

## 🧪 Testing

We use `pytest` with `httpx` to verify endpoint routing, schema requirements, and edge-cases. To run tests, use:

```bash
PYTHONPATH=. pytest
```
