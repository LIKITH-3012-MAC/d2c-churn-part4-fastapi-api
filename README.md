# Part 4: Churn Inference API & Documentation

## Project Overview
This repository contains Part 4 of the D2C Customer Churn Intelligence & Retention API Capstone. The objective is to deploy the Champion Machine Learning model trained in Part 3 as a REST API that the marketing CRM can query to identify at-risk customers.

## File Structure
- `app.py`: FastAPI application containing the `/health`, `/predict`, and `/predict_batch` endpoints.
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
- **Batch Processing:** Highly optimized `/predict_batch` endpoint to avoid thousands of individual API calls during nightly CRM syncs.
