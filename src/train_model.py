import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression

from src.data_utils import load_json_dataset, simple_clean_text
from src.features import build_vectorizer, save_vectorizer

MODEL_PATH = "models/model.joblib"


def train(dataset_path="data/dataset.json"):
    df = load_json_dataset(dataset_path)
    df = df[df["label"].notnull()]
    df["label"] = df["label"].astype(int)
    df["clean"] = df["text"].apply(simple_clean_text)

    X_train, X_test, y_train, y_test = train_test_split(
        df["clean"],
        df["label"],
        test_size=0.2,
        random_state=42,
        stratify=df["label"],
    )

    vec = build_vectorizer()
    X_train_vec = vec.fit_transform(X_train)
    X_test_vec = vec.transform(X_test)

    clf = LogisticRegression(max_iter=1000, class_weight="balanced")
    clf.fit(X_train_vec, y_train)

    # ✅ SAVE MODEL & VECTORIZER
    os.makedirs("models", exist_ok=True)
    print("Saving model to:", MODEL_PATH)

    joblib.dump(clf, MODEL_PATH)
    joblib.dump(vec, "models/vectorizer.joblib")
    save_vectorizer(vec)

    print("Model Saved ✅")
    print(classification_report(y_test, clf.predict(X_test_vec)))


if __name__ == "__main__":
    train()
