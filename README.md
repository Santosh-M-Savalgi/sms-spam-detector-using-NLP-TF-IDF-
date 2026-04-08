# 📩 SMS Spam Detection using NLP (TF-IDF + Naive Bayes)

## 🚀 Overview

This project builds a machine learning model to classify SMS messages as **Spam or Ham (Not Spam)** using Natural Language Processing (NLP) techniques.

It uses **TF-IDF vectorization** and a **Multinomial Naive Bayes classifier**, a strong baseline for text classification tasks.

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

   * Multinomial Naive Bayes
5. **Evaluation**

   * Accuracy, Precision, Recall, F1-score

---

## 📂 Dataset

* SMS Spam dataset (spam/ham classification)

---

## ⚙️ Installation

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Project

```bash
jupyter notebook notebook/tfidf_sms_spam.ipynb
```

---

## 📊 Model Performance

* **Accuracy:** ~97%
* **Precision:** High
* **Recall:** Needs improvement (due to class imbalance)

---

## 🧪 Sample Prediction

```python
msg = ["Congratulations! You've won a free ticket"]
print(model.predict(vectorizer.transform(msg)))
```

---

## ⚠️ Notes

* Ensure dataset is placed inside the `data/` folder
* First run may download NLTK resources

---

## 🔮 Future Improvements

* Improve recall using SMOTE or class balancing
* Try advanced models (Logistic Regression, SVM)
* Deploy as a web app using Streamlit

---

## 🌍 Real-World Applications

* SMS spam filtering
* Email classification
* Fraud and phishing detection

---

## 👨‍💻 Author

Santosh Savalgi
