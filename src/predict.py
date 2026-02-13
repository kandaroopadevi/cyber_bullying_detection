import joblib
from src.features import load_vectorizer
from src.data_utils import simple_clean_text


def predict_text(text):
    clf = joblib.load("models/model.joblib")
    vec = load_vectorizer()
    clean = simple_clean_text(text)
    X = vec.transform([clean])
    pred = clf.predict(X)[0]
    prob = clf.predict_proba(X)[0][1]
    return pred, prob

if _name_ == "_main_":
    print(predict_text("You are a stupid idiot."))