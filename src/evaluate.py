import joblib
from sklearn.metrics import classification_report, confusion_matrix
from src.data_utils import load_json_dataset, simple_clean_text
from src.features import load_vectorizer

def evaluate(data_path="data/dataset.json"):
    df = load_json_dataset(data_path)
    df = df[df["label"].notnull()]
    df["label"] = df["label"].astype(int)
    df["clean"] = df["text"].apply(simple_clean_text)

    clf = joblib.load("models/model.joblib")
    vec = load_vectorizer()

    X = vec.transform(df["clean"])
    preds = clf.predict(X)

    print(classification_report(df["label"], preds))
    print(confusion_matrix(df["label"], preds))

if _name_ == "_main_":
    evaluate()