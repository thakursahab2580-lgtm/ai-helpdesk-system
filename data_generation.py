import random
import pandas as pd
from datetime import datetime, timedelta

random.seed(42)

CATEGORIES = ["IT", "Fees", "Timetable", "Exams", "General"]

# Phrase components for semi-random generation
PHRASES = {
    "IT": {
        "subjects": ["I", "My account", "The system", "Moodle", "The portal"],
        "actions": [
            "cannot access", "is not working", "keeps showing an error",
            "won't let me log in", "is crashing"
        ],
        "contexts": [
            "since yesterday", "during login", "after password reset",
            "this morning", "when I try to sign in"
        ]
    },
    "Fees": {
        "subjects": ["My payment", "The tuition fee", "The transaction", "My fee payment"],
        "actions": [
            "failed", "did not go through", "was deducted but not reflected",
            "is showing an error", "was declined"
        ],
        "contexts": [
            "yesterday", "during checkout", "while paying online",
            "after submission", "this afternoon"
        ]
    },
    "Timetable": {
        "subjects": ["I", "My timetable", "The schedule"],
        "actions": [
            "cannot see", "is missing", "is incorrect",
            "has overlapping classes", "is not updated"
        ],
        "contexts": [
            "for this semester", "on the portal", "after enrollment",
            "since registration", "this week"
        ]
    },
    "Exams": {
        "subjects": ["I", "My exam", "The exam schedule"],
        "actions": [
            "need a deferral", "has a clash", "is not showing",
            "needs clarification", "was missed due to illness"
        ],
        "contexts": [
            "for tomorrow", "this semester", "due to medical reasons",
            "because of emergency", "during finals week"
        ]
    },
    "General": {
        "subjects": ["I", "I would like to", "Can you help me to"],
        "actions": [
            "get information about campus facilities",
            "update my profile details",
            "know about student clubs",
            "change my contact information",
            "ask about library hours"
        ],
        "contexts": [
            "", "", "", "", ""
        ]
    }
}


def generate_ticket(category):
    parts = PHRASES[category]
    subject = random.choice(parts["subjects"])
    action = random.choice(parts["actions"])
    context = random.choice(parts["contexts"])

    if context:
        text = f"{subject} {action} {context}."
    else:
        text = f"{subject} {action}."

    return text


def generate_timestamp():
    now = datetime.now()
    random_days = random.randint(0, 30)
    random_seconds = random.randint(0, 86400)
    return now - timedelta(days=random_days, seconds=random_seconds)


def create_dataset(n_samples=400):
    data = []

    per_category = n_samples // len(CATEGORIES)

    for category in CATEGORIES:
        for _ in range(per_category):
            text = generate_ticket(category)
            timestamp = generate_timestamp()
            data.append({
                "text": text,
                "category": category,
                "timestamp": timestamp
            })

    random.shuffle(data)

    df = pd.DataFrame(data)
    df.to_csv("dataset.csv", index=False)
    print(f"Dataset generated with {len(df)} samples.")


if __name__ == "__main__":
    create_dataset(400)
