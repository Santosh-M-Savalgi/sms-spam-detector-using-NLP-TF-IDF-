#  SMS Spam & Fraud URL Detection System

## Overview

This is a  machine learning-based system designed to classify SMS messages as **Spam** or **Ham (Not Spam)** using Natural Language Processing (NLP). 

Going beyond standard text classification, this system features a powerful **Fraud URL Detection Module** that extracts and analyzes URLs within messages to identify potentially malicious or phishing links.

The system combines:
- **NLP-based spam classification** (Complement Naive Bayes)
- **URL-based fraud detection** using multi-layer analysis (Machine Learning, Network Analysis, IP Geolocation)

---

## Key Features

### 1.  SMS Spam Detection (NLP)
- Advanced text preprocessing and cleaning
- TF-IDF vectorization
- Complement Naive Bayes classifier (optimized for imbalanced datasets)

### 2. Fraud URL Detection
- Automatic URL extraction using regex
- **Multi-layer analysis pipeline:**
  - **Machine Learning Classification:** Random Forest model trained on malicious URL patterns.
  - **Network Analysis:** DNS resolution, redirection tracking, and SSL certificate checks.
  - **IP Analysis:** IP resolution and geolocation tracking.
- Provides actionable risk levels: **Low, Medium, High** with detailed warning indicators.

---

## Project Architecture

### URL Detection Module Structure
```text
url_detection/
├── feature_extraction.py   # Extracts URL-based features
├── ml_model.py             # Random Forest classifier
├── network_analysis.py     # DNS, redirects, SSL checks
├── ip_analysis.py          # IP resolution and geolocation
└── analyzer.py             # Combines all checks and outputs risk score
```

### Full-Stack Integration
- **Backend:** FastAPI application providing a high-performance REST endpoint (`/api/predict`).
- **Frontend:** Modern, responsive React application displaying spam classification, URL risk cards, and confidence scores.

---

##  Getting Started

### Prerequisites
- Python 3.8+
- Node.js & npm (for the React frontend)

### 1. Clone & Setup
Ensure you have the required dataset `combined_dataset.csv` inside `tfdf spam/data/`.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

##  How to Run

NeuralGuard offers three ways to run and interact with the system:

### Option 1: Jupyter Notebook (For Data Scientists)
Run the complete training and evaluation pipeline interactively.
```bash
jupyter notebook "tfdf spam/tfidfforsmsspam.ipynb"
```

### Option 2: Streamlit Application (Quick UI)
Launch a lightweight, Python-only web interface.
```bash
cd "tfdf spam"
streamlit run app.py
```

### Option 3: Full-Stack Application (Production-Ready)
Run the FastAPI backend and React frontend.

**Terminal 1: Start the Backend**
```bash
cd "tfdf spam"
fastapi run api.py --port 8000
```

**Terminal 2: Start the Frontend**
```bash
cd "tfdf spam/frontend"
npm install
npm run dev
```
*Access the web interface at `http://localhost:5173`.*

---

## Model Performance

- **Accuracy:** ~97%
- **Precision:** High precision to minimize false positives (important for Ham messages).
- **Recall:** Significantly improved using the Complement Naive Bayes algorithm.
- **Robustness:** Effectively handles imbalanced datasets.

---

##  Technology Stack

- **Machine Learning & NLP:** `scikit-learn`, `nltk`, `pandas`, `numpy`
- **Backend API:** `FastAPI`, `uvicorn`, `pydantic`
- **Web Interfaces:** `Streamlit`, `React` (Vite)
- **Networking:** `requests`

---

##  Future Improvements

- Integration with external threat intelligence APIs (e.g., VirusTotal, AbuseIPDB).
- Implementation of deep learning models (BERT, Transformers) for complex context understanding.
- Persistent storage (database) for flagging and reviewing messages.
- Browser extension for real-time, on-the-fly URL detection.

---

##  Author
**Santosh M Savalgi**
