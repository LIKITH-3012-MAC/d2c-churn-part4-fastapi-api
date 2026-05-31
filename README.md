# Part 4: FastAPI Prediction Service

Serves the churn model via a REST API.

## 1. Repository Structure
```
.
├── data/
│   └── d2c_churn_data_package/
│       ├── customers.csv
│       ├── orders.csv
│       ├── support_tickets.csv
│       ├── rfm_modeling_snapshot.csv
│       └── ...
├── README.md
├── requirements.txt
└── (Notebooks and Scripts)
```

## 2. Dataset Location
The original dataset package is securely bundled inside the repository under `data/d2c_churn_data_package/`. 
All notebooks and scripts use relative paths to automatically load the data from this directory without requiring any modifications.

## 3. Installation Command
Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 4. Run Command
Execute the following to run this part:
```bash
uvicorn app.main:app --reload
```

## 5. Expected Outputs
Upon successful execution, you should expect:
Running API service on http://127.0.0.1:8000. Go to http://127.0.0.1:8000/docs for Swagger UI.
