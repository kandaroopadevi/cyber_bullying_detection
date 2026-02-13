from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import dump, load
import os

VECT_PATH = "models/vectorizer.joblib"

def build_vectorizer(max_features=10000, ngram_range=(1,2)):
    return TfidfVectorizer(
        max_features=max_features,
        ngram_range=ngram_range,
        stop_words="english",
        lowercase=True
    )

def save_vectorizer(vec):
    os.makedirs("models", exist_ok=True)
    dump(vec, VECT_PATH)

def load_vectorizer():
    return load(VECT_PATH)