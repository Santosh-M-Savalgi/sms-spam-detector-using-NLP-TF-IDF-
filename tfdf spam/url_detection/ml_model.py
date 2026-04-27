import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from url_detection.feature_extraction import extract_features

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'url_fraud_model.pkl')

def train_dummy_model():
    """Trains a simple Random Forest model on synthetic data and saves it."""
    # Synthetic data for basic URL fraud detection
    # Features: [url_length, num_dots, has_special_chars, num_suspicious_keywords]
    # Label: 0 = Benign, 1 = Fraud

    data = [
        # Safe URLs
        ("http://google.com", 0),
        ("https://github.com/Santosh-M-Savalgi", 0),
        ("http://wikipedia.org", 0),
        ("https://youtube.com/watch?v=123", 0),
        ("http://example.com", 0),
        ("https://stackoverflow.com/questions", 0),
        ("https://reactjs.org/docs/getting-started", 0),
        
        # Fraud/Phishing URLs
        ("http://secure-update-login.net", 1),
        ("https://paypal-verify-account-xyz.com", 1),
        ("http://free-prize-claim.org/bonus", 1),
        ("http://bank-of-america-secure.com", 1),
        ("http://login-signin.net?user=1", 1),
        ("http://192.168.1.1/update", 1),
        ("http://verify-your-apple-id.com", 1)
    ]
    
    X = []
    y = []
    
    for url, label in data:
        X.append(extract_features(url))
        y.append(label)
        
    df = pd.DataFrame(X, columns=['url_length', 'num_dots', 'has_special_chars', 'num_suspicious_keywords'])
    
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(df, y)
    
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

def load_model():
    if not os.path.exists(MODEL_PATH):
        train_dummy_model()
    return joblib.load(MODEL_PATH)

def predict_url(url):
    """
    Predicts if a URL is fraudulent using the trained model.
    Returns prediction ('fraud' or 'safe') and confidence.
    """
    model = load_model()
    features = extract_features(url)
    
    # model.predict_proba returns [[prob_0, prob_1]]
    probabilities = model.predict_proba([features])[0]
    fraud_prob = probabilities[1]
    
    if fraud_prob >= 0.5:
        return "fraud", round(fraud_prob, 2)
    else:
        return "safe", round(1 - fraud_prob, 2)

if __name__ == "__main__":
    train_dummy_model()
