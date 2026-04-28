import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import ComplementNB
from fastapi import FastAPI
from url_detection.analyzer import analyze_url
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager

# Download NLTK data safely
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

# Global variables to store trained models in memory
vectorizer = None
model = None
stop_words = None
lemmatizer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load and train model exactly ONCE on application startup
    global vectorizer, model, stop_words, lemmatizer
    
    df = pd.read_csv('data/combined_dataset.csv', encoding='latin1')
    
    def clean_text(text):
        text = text.lower()
        text = re.sub(r'&\w+;', ' ', text)   
        text = text.replace('_', ' ')        
        text = re.sub(r'\bnbsp\b', ' ', text) 
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)  
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    df['v2'] = df['v2'].apply(clean_text)
    
    stop_words = set(stopwords.words('english'))
    df['v2'] = df['v2'].apply(lambda x: " ".join([word for word in x.split() if word not in stop_words]))
    
    lemmatizer = WordNetLemmatizer()
    df['v2'] = df['v2'].apply(lambda x: " ".join([lemmatizer.lemmatize(word) for word in x.split()]))
    
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['v2'])
    
    df['v1'] = df['v1'].map({'ham': 0, 'spam': 1})
    y = df['v1']
    
    model = ComplementNB()
    model.fit(X, y)
    
    yield
    # Cleanup logic can go here if needed

# Initialize FastAPI App
app = FastAPI(lifespan=lifespan)

# Setup CORS to allow React Frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Replace with 'http://localhost:5173' for strict dev security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    message: str

def preprocess(text, stop_words, lemmatizer):
    text = text.lower()
    text = re.sub(r'&\w+;', ' ', text)   
    text = text.replace('_', ' ')        
    text = re.sub(r'\bnbsp\b', ' ', text) 
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)  
    text = re.sub(r'\s+', ' ', text).strip()
    
    text = " ".join([word for word in text.split() if word not in stop_words])
    text = " ".join([lemmatizer.lemmatize(word) for word in text.split()])
    return text

@app.post("/api/predict")
async def predict_spam(request: MessageRequest):
    global vectorizer, model, stop_words, lemmatizer
    
    # URL extraction and Analysis
    url_pattern = re.compile(r'https?://[^\s]+')
    urls_found = url_pattern.findall(request.message)
    
    # Check if input is ONLY URLs
    message_without_urls = url_pattern.sub('', request.message).strip()
    is_only_url = len(message_without_urls) == 0 and len(urls_found) > 0
    
    response = {}
    
    if is_only_url:
        response["prediction"] = "url_only"
    else:
        msg_clean = preprocess(request.message, stop_words, lemmatizer)
        msg_vec = vectorizer.transform([msg_clean])
        prediction = model.predict(msg_vec)[0]
        result = "spam" if prediction == 1 else "ham"
        response["prediction"] = result
    
    url_analysis_results = []
    for url in urls_found:
        url_analysis_results.append(analyze_url(url))
    
    if url_analysis_results:
        response["url_analysis"] = url_analysis_results
    
    return response
