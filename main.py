from inference_service import classify_ticket
from event_bus import start_event_consumer, stop_event_consumer
from monitoring import high_priority_per_day, detect_drift, export_logs
import time


def simulate_requests():
    sample_tickets = [
        "I cannot access Moodle since yesterday.",
        "My fee payment failed during checkout.",
        "I need a deferral for tomorrow's exam.",
        "My timetable has overlapping classes.",
        "Can you tell me about library hours?",
        "The portal is not working during login.",
        "My transaction was deducted but not reflected."
    ]

    for ticket in sample_tickets:
        result = classify_ticket(ticket)
        print("Prediction:", result)
        time.sleep(0.5)


if __name__ == "__main__":
    print("Starting University Support AI System...\n")

    consumer_thread = start_event_consumer()

    simulate_requests()

    time.sleep(2)

    high_priority_per_day()
    detect_drift()
    export_logs()

    stop_event_consumer()

    print("\nSystem shutdown complete.")
