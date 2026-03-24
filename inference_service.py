import joblib
import os
from datetime import datetime

from event_bus import publish_event
import uuid
ticket_id = "UNI-" + str(uuid.uuid4())[:8].upper()


MODEL_DIR = "models"

# Load model + vectorizer once (efficient design)
classifier = joblib.load(os.path.join(MODEL_DIR, "classifier.pkl"))
vectorizer = joblib.load(os.path.join(MODEL_DIR, "vectorizer.pkl"))


def assign_priority(text):
    text_lower = text.lower()

    high_keywords = ["exam", "deferral", "payment", "failed", "deadline", "urgent"]

    medium_keywords = [
        "cannot", "error", "login", "issue", "not working",
        "password", "forgot", "reset"
    ]

    if any(word in text_lower for word in high_keywords):
        return "High"
    elif any(word in text_lower for word in medium_keywords):
        return "Medium"
    else:
        return "Low"


def classify_ticket(text):
    import uuid

    timestamp = datetime.now().isoformat()
    ticket_id = "UNI-" + str(uuid.uuid4())[:8].upper()

    # Vectorize
    text_vectorized = vectorizer.transform([text])

    # Predict category
    predicted_category = classifier.predict(text_vectorized)[0]

    # Confidence score
    probabilities = classifier.predict_proba(text_vectorized)[0]
    confidence = float(max(probabilities))
    confidence_percent = round(confidence * 100, 2)

    priority = assign_priority(text)

    # Thresholds
    UNCERTAINTY_THRESHOLD = 0.40
    MANUAL_REVIEW_THRESHOLD = 0.55

    manual_review = False
    final_category = predicted_category

    # Very low confidence → Uncertain
    if confidence < UNCERTAINTY_THRESHOLD:
        final_category = "Uncertain"
        manual_review = True

    # Moderate confidence → manual review
    elif confidence < MANUAL_REVIEW_THRESHOLD:
        manual_review = True

    # Always define result BEFORE publishing
    result = {
        "event": "TICKET_CLASSIFIED",
        "ticket_id": ticket_id,
        "text": text,
        "category": final_category,
        "priority": priority,
        "confidence": confidence_percent,
        "manual_review": manual_review,
        "timestamp": timestamp
    }

    # Now publish safely
    publish_event(result)

    return result