from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import joblib, json, os

from src.features import load_vectorizer
from src.data_utils import simple_clean_text

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

app = FastAPI(title="Cyberbullying Detection System")

# ----------------- ML Model -----------------
clf = joblib.load("models/model.joblib")
vec = load_vectorizer()

# ----------------- Storage Files -----------------
REPORT_FILE = "reported_messages.json"
BLOCK_FILE = "blocked_users.json"
OFFENSE_FILE = "offense_counts.json"


# ----------------- Pydantic Models -----------------
class TextIn(BaseModel):
    username: str
    text: str


# ----------------- Helper Functions -----------------
def _read_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r") as f:
        return json.load(f)


def _write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def save_report(text: str):
    data = _read_json(REPORT_FILE, [])
    data.append({"message": text})
    _write_json(REPORT_FILE, data)


def save_to_blocklist(username: str):
    users = _read_json(BLOCK_FILE, [])
    if username not in users:
        users.append(username)
    _write_json(BLOCK_FILE, users)


def is_blocked(username: str) -> bool:
    users = _read_json(BLOCK_FILE, [])
    return username in users


def get_offense_counts() -> dict:
    return _read_json(OFFENSE_FILE, {})


def add_offense(username: str) -> int:
    """Increase offense count and return updated count."""
    offenses = get_offense_counts()
    current = offenses.get(username, 0) + 1
    offenses[username] = current
    _write_json(OFFENSE_FILE, offenses)
    return current


# ----------------- Core Prediction Endpoint -----------------
@app.post("/predict")
def predict(payload: TextIn):
    username = payload.username
    text = payload.text

    # Check if user is already blocked
    if is_blocked(username):
        return {
            "username": username,
            "status": "🚫 User already blocked",
            "message": "Your actions violated safety rules. You cannot post further comments."
        }

    # Clean & predict
    clean = simple_clean_text(text)
    X = vec.transform([clean])
    pred = int(clf.predict(X)[0])
    prob = float(clf.predict_proba(X)[0][1])

    # If not bullying
    if pred == 0:
        return {
            "username": username,
            "prediction": pred,
            "confidence": prob,
            "response": "✔ Safe message.",
            "action": "Comment posted successfully."
        }

    # If bullying
    save_report(text)  # Save abusive content

    offense_count = add_offense(username)

    # Warning System
    if offense_count < 3:
        return {
            "username": username,
            "prediction": pred,
            "confidence": prob,
            "response": "⚠ Cyberbullying detected.",
            "action": f"❌ Comment hidden. Warning {offense_count}/3. Repeated abuse will lead to blocking."
        }
    else:
        save_to_blocklist(username)  # 3rd strike → block user
        return {
            "username": username,
            "prediction": pred,
            "confidence": prob,
            "response": "⚠ Cyberbullying detected repeatedly.",
            "action": "❌ Comment hidden and 🚫 user blocked (3/3 warnings reached)."
        }


# ----------------- Check Block Status -----------------
@app.get("/is_blocked/{username}")
def check_block(username: str):
    return {"username": username, "blocked": is_blocked(username)}


# ----------------- Dashboard -----------------
@app.get("/dashboard")
def dashboard():
    reports = _read_json(REPORT_FILE, [])
    blocked = _read_json(BLOCK_FILE, [])
    offenses = get_offense_counts()

    return {
        "summary": {
            "total_reported_messages": len(reports),
            "total_blocked_users": len(blocked),
            "total_offense_events": sum(offenses.values())
        },
        "blocked_users": blocked,
        "offense_counts": offenses,
    }


# ----------------- PDF Report Generator -----------------
def generate_pdf_report(pdf_path="cyber_report.pdf"):
    reports = _read_json(REPORT_FILE, [])
    blocked = _read_json(BLOCK_FILE, [])
    offenses = get_offense_counts()

    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    textobject = c.beginText(40, height - 50)

    textobject.textLine("Cyberbullying Detection System - Report")
    textobject.textLine("---------------------------------------")
    textobject.textLine("")
    textobject.textLine(f"Total reported messages: {len(reports)}")
    textobject.textLine(f"Total blocked users: {len(blocked)}")
    textobject.textLine(f"Total offense events: {sum(offenses.values())}")
    textobject.textLine("")

    textobject.textLine("Blocked Users:")
    if blocked:
        for u in blocked:
            textobject.textLine(f" - {u}")
    else:
        textobject.textLine(" (None)")
    textobject.textLine("")

    textobject.textLine("Sample Reported Messages:")
    for r in reports[:10]:
        msg = r.get("message", "")
        if len(msg) > 80:
            msg = msg[:77] + "..."
        textobject.textLine(f" - {msg}")

    c.drawText(textobject)
    c.showPage()
    c.save()


@app.get("/export_report")
def export_report():
    pdf_path = "cyber_report.pdf"
    generate_pdf_report(pdf_path)
    return FileResponse(pdf_path, media_type="application/pdf", filename="cyber_report.pdf")