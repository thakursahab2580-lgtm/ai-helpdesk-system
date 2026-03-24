import pandas as pd

# ------------------------------
# In-memory storage
# ------------------------------

event_log = []


# ------------------------------
# Event Handling
# ------------------------------

def handle_event(event):
    """
    Called by event consumer.
    Stores classified ticket event.
    """
    if event.get("event") == "TICKET_CLASSIFIED":
        event_log.append(event)
        print(f"Logged Event: {event['category']} | {event['priority']} | {event['confidence']}%")


def get_dataframe():
    """
    Convert event log to pandas DataFrame.
    """
    if not event_log:
        return pd.DataFrame()
    return pd.DataFrame(event_log)


# ------------------------------
# Monitoring & Evaluation Tools
# ------------------------------

def high_priority_per_day():
    df = get_dataframe()
    if df.empty:
        print("No events logged yet.")
        return

    df["date"] = pd.to_datetime(df["timestamp"]).dt.date
    high_counts = df[df["priority"] == "High"].groupby("date").size()

    print("\nHigh Priority Tickets Per Day:")
    print(high_counts)


def average_confidence():
    df = get_dataframe()
    if df.empty:
        return 0
    return df["confidence"].mean()


# ------------------------------
# Drift Detection
# ------------------------------

def get_drift_status(threshold=5):
    """
    Simple drift simulation:
    Compare first half vs second half confidence averages.
    Threshold is in percentage points.
    """
    df = get_dataframe()

    if len(df) < 10:
        return {
            "status": "Not enough data",
            "drift": False
        }

    midpoint = len(df) // 2
    first_half = df.iloc[:midpoint]["confidence"].mean()
    second_half = df.iloc[midpoint:]["confidence"].mean()

    drift_detected = abs(first_half - second_half) > threshold

    return {
        "status": "Drift Detected" if drift_detected else "Stable",
        "drift": drift_detected
    }


# ------------------------------
# Dashboard Statistics
# ------------------------------

def get_dashboard_stats():
    df = get_dataframe()

    if df.empty:
        return {}

    total = len(df)
    high_priority = len(df[df["priority"] == "High"])
    manual_review = len(df[df["manual_review"] == True])
    avg_confidence = round(df["confidence"].mean(), 2)

    category_counts = df["category"].value_counts().to_dict()
    drift_info = get_drift_status()

    tickets = df.to_dict(orient="records")

    return {
        "total": total,
        "high_priority": high_priority,
        "manual_review": manual_review,
        "avg_confidence": avg_confidence,
        "category_counts": category_counts,
        "drift_status": drift_info,
        "tickets": tickets
    }


# ------------------------------
# Export Logs
# ------------------------------

def export_logs(path="logs/ticket_log.csv"):
    df = get_dataframe()

    if df.empty:
        print("No events to export.")
        return

    import os
    os.makedirs("logs", exist_ok=True)

    df.to_csv(path, index=False)
    print(f"Logs exported to {path}")
