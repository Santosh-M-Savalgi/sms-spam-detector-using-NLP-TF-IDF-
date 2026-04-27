import streamlit as st
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import ComplementNB
from url_detection.analyzer import analyze_url

# Download NLTK data needed for preprocessing
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

@st.cache_resource(show_spinner="Training model... This only happens once!")
def load_model():
    """
    Loads dataset, processes text, and trains the model.
    Using @st.cache_resource ensures this computationally heavy step 
    is only run once per session, keeping the UI lightning fast.
    """
    df = pd.read_csv('data/combined_dataset.csv', encoding='latin1')
    
    # 1. Cleaning text
    def clean_text(text):
        text = text.lower()
        text = re.sub(r'&\w+;', ' ', text)   
        text = text.replace('_', ' ')        
        text = re.sub(r'\bnbsp\b', ' ', text) 
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)  
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    df['v2'] = df['v2'].apply(clean_text)
    
    # 2. Removing stop words
    stop_words = set(stopwords.words('english'))
    df['v2'] = df['v2'].apply(lambda x: " ".join([word for word in x.split() if word not in stop_words]))
    
    # 3. Lemmatization
    lemmatizer = WordNetLemmatizer()
    df['v2'] = df['v2'].apply(lambda x: " ".join([lemmatizer.lemmatize(word) for word in x.split()]))
    
    # 4. TF-IDF Vectorization
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['v2'])
    
    # 5. Model Training
    df['v1'] = df['v1'].map({'ham': 0, 'spam': 1})
    y = df['v1']
    
    # Train on full data for maximum inference accuracy in production
    model = ComplementNB()
    model.fit(X, y)
    
    return vectorizer, model, stop_words, lemmatizer

def preprocess(text, stop_words, lemmatizer):
    """Applies the exact same cleaning steps to raw user input."""
    # Apply initial cleaning
    text = text.lower()
    text = re.sub(r'&\w+;', ' ', text)   
    text = text.replace('_', ' ')        
    text = re.sub(r'\bnbsp\b', ' ', text) 
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)  
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove stop words
    text = " ".join([word for word in text.split() if word not in stop_words])
    
    # Apply lemmatization
    text = " ".join([lemmatizer.lemmatize(word) for word in text.split()])
    return text

# -----------------
# Streamlit Web UI
# -----------------
st.set_page_config(page_title="SMS Spam Detector", page_icon="📱", layout="centered")

st.title("📱 SMS Spam Detector")
st.markdown("""
Welcome to the SMS Spam Detector! powered by NLP and **Complement Naive Bayes**. 
Simply enter a text message below to predict if it's safe (**Ham**) or malicious (**Spam**).
""")

# Load models (cached)
vectorizer, model, stop_words, lemmatizer = load_model()

# User input
user_input = st.text_area("Enter Message Below:", placeholder="e.g., URGENT: Your bank account has been suspended. Confirm your identity now to avoid permanent closure: http://secure-update-login.net", height=150)

# Make Prediction
if st.button("Detect Spam 🔍", use_container_width=True):
    if user_input.strip() == "":
        st.warning("⚠️ Please enter a message to analyze.")
    else:
        # Preprocess the message
        msg_clean = preprocess(user_input, stop_words, lemmatizer)
        msg_vec = vectorizer.transform([msg_clean])
        
        # Predict
        prediction = model.predict(msg_vec)[0]
        
        # URL extraction
        url_pattern = re.compile(r'https?://[^\s]+')
        urls_found = url_pattern.findall(user_input)
        
        # Display Results
        st.markdown("---")
        if prediction == 1:
            st.error("🚨 **RESULT: SPAM**")
            st.markdown("This message exhibits patterns commonly found in malicious or unsolicited messages.")
        else:
            st.success("✅ **RESULT: HAM (Safe)**")
            st.markdown("This message appears to be safe and legitimate.")
            
        if urls_found:
            st.markdown("### 🌐 URL Risk Analysis")
            for url in urls_found:
                with st.spinner(f"Analyzing {url}..."):
                    analysis = analyze_url(url)
                
                risk = analysis['risk_level']
                if risk == "High":
                    st.error(f"**{url}** - Risk Level: **High** 🚨")
                elif risk == "Medium":
                    st.warning(f"**{url}** - Risk Level: **Medium** ⚠️")
                else:
                    st.success(f"**{url}** - Risk Level: **Low** ✅")
                    
                if analysis['warnings']:
                    st.markdown("**Warnings:**")
                    for w in analysis['warnings']:
                        st.markdown(f"- {w}")
