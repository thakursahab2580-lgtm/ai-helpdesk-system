from flask import Flask, render_template, request
from inference_service import classify_ticket
from event_bus import start_event_consumer
from monitoring import get_dashboard_stats
import os

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        user_text = request.form.get("ticket_text")
        if user_text:
            result = classify_ticket(user_text)

    return render_template("index.html", result=result)


@app.route("/admin")
def admin_dashboard():
    stats = get_dashboard_stats()
    return render_template("admin.html", stats=stats)


if __name__ == "__main__":
    # Prevent duplicate consumer in debug mode
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        start_event_consumer()

    app.run(debug=True)
