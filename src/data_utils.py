import json, re, pandas as pd

def load_json_dataset(path: str) -> pd.DataFrame:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    for item in data:
        text = item.get("content") or item.get("text") or ""
        label = None
        if item.get("annotation") and "label" in item["annotation"]:
            try:
                label = int(item["annotation"]["label"][0])
            except:
                label = None
        rows.append({"text": text, "label": label})

    df = pd.DataFrame(rows).dropna(subset=["text"])
    return df

def simple_clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+|www.\S+", " ", text)
    text = re.sub(r"@\w+", " ", text)
    text = re.sub(r"[^a-z0-9\s']", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text