# 📩 SMS Spam Detection using TF-IDF + Naive Bayes

## 🚀 Overview

This project implements an SMS spam classifier using Natural Language Processing (NLP) techniques and a Naive Bayes model.

## 🧠 Pipeline

1. Text Cleaning (regex, lowercase)
2. Stopword Removal (NLTK)
3. Lemmatization
4. TF-IDF Vectorization
5. Multinomial Naive Bayes Classification

## 📂 Dataset

* Combined SMS dataset (spam/ham classification)

## 📊 Visualizations

* Spam vs Ham distribution (Pie Chart)
* WordCloud for spam messages

## ⚙️ Installation

```bash
pip install -r requirements.txt
```

## ▶️ Run the Project

```bash
jupyter notebook notebook/tfidf_sms_spam.ipynb
```

## 📈 Results

* Accuracy: ~97%
* Precision: High
* Recall: Needs improvement (class imbalance)

## ⚠️ Notes

* Make sure dataset is inside `data/` folder
* First run may download NLTK resources

## 🔮 Improvements

* Improve recall using SMOTE or class balancing
* Try Logistic Regression / SVM
* Save model using pickle for deployment

## 👨‍💻 Author

Santosh
