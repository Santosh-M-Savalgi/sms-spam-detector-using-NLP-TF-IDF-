# 📩 SMS Spam Detection using NLP (TF-IDF + Naive Bayes)

## 🚀 Overview

This project builds a machine learning model to classify SMS messages as **Spam or Ham (Not Spam)** using Natural Language Processing (NLP) techniques.

It uses **TF-IDF vectorization** and a **Complement Naive Bayes classifier**, which provides excellent performance and recall even on extremely imbalanced text classification tasks!

---

## 🧠 Project Pipeline

1. **Data Cleaning**
   * Lowercasing
   * Removing special characters
2. **Text Preprocessing**
   * Stopword removal (NLTK)
   * Lemmatization
3. **Feature Extraction**
   * TF-IDF Vectorization
4. **Model Training**
   * Complement Naive Bayes (improving upon MultinomialNB for imbalanced data)
5. **Evaluation**
   * Accuracy, Precision, Recall, F1-score

---

## 📂 Dataset

* SMS Spam dataset (spam/ham classification)
* **Note:** Ensure dataset is placed inside the `tfdf spam/data/` folder.

---

## ⚙️ Installation

```bash
pip install -r requirements.txt
```
*(First run may download NLTK resources automatically in the background).*

---

## ▶️ How to Run

You have multiple ways to interact with this project!

### Option 1: Jupyter Notebook (Analysis & Training)
```bash
jupyter notebook "tfdf spam/tfidfforsmsspam.ipynb"
```

### Option 2: Streamlit Web App
A lightweight, fast, beautiful web app in pure Python.
```bash
cd "tfdf spam"
streamlit run app.py
```

### Option 3: Full-Stack React + FastAPI App
A premium, glassmorphic React frontend communicating with a REST API backend.

**Terminal 1 (Backend):**
```bash
cd "tfdf spam"
fastapi run api.py --port 8000
```
**Terminal 2 (Frontend):**
```bash
cd "tfdf spam/frontend"
npm install
npm run dev
```

---

## 📊 Model Performance

* **Accuracy:** ~97%
* **Precision:** High
* **Recall:** Enhanced significantly compared to baseline through the use of `ComplementNB` and balanced `stratify=y` test splits!

---

## 🔮 Future Improvements

* Try advanced deep models (Transformers, BERT)
* Add database for capturing flagged SMS instances over time

---

## 🌍 Real-World Applications

* SMS spam filtering
* Email classification
* Fraud and phishing detection

---

## 👨‍💻 Author

Santosh M Savalgi
