import joblib
from fastapi import FastAPI
import os
import librosa
import numpy as np
from sklearn.linear_model import LogisticRegression
from pydantic import BaseModel
from utils import extract_features, download_audio_from_youtube

app = FastAPI()

# Load the logistic regression model
logistic_regression_model = joblib.load('logistic_regression_model.pkl')

# Load the StandardScaler
sc = joblib.load('standard_scaler.pkl')

def predict_genre(url):
    audio_path = 'data/audio.wav'
    download_audio_from_youtube(url)
    # Extract features from the audio file
    features = extract_features(audio_path)
    
    # Prepare the feature vector for prediction
    feature_vector = [features[feat] for feat in features if feat not in ["filename", "label"]]
    feature_vector = np.array(feature_vector).reshape(1, -1)
    
    # Normalize the feature vector using StandardScaler
    feature_vector_normalized = sc.transform(feature_vector)
    
    # Predict the genre using the provided model
    prediction = logistic_regression_model.predict(feature_vector_normalized)
    
    # Map numerical label to genre name
    genre_mapping = {
        0: 'Nhạc Bolero',
        1: 'Nhạc hiphop',
        2: 'Nhạc thiếu nhi',
        3: 'Nhạc R&B',
        4: 'Nhạc đỏ',
        5: 'Nhạc rock'
    }
    
    predicted_genre = genre_mapping[prediction[0]]
    
    return predicted_genre

class Request(BaseModel):
    url: str

@app.post('/predict')
def predict(request: Request):
    result = predict_genre(request.url)
    return {"genre": result}



