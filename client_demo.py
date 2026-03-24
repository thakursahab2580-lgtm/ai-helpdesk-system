import json
import time
import urllib.request
import urllib.parse

BASE = "http://127.0.0.1:8000"


def submit_ticket(student_id, category, description, priority="LOW"):

    payload = {
        "student_id": student_id,
        "category": category,
        "description": description,
        "priority": priority
    }

    req = urllib.request.Request(
        BASE + "/submit",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())


def get_status(ticket_id):

    url = BASE + "/status?" + urllib.parse.urlencode({
        "ticket_id": ticket_id
    })

    with urllib.request.urlopen(url) as r:
        return json.loads(r.read().decode())


if __name__ == "__main__":

    r = submit_ticket(
        "S12345",
        "Login",
        "Cannot access student portal",
        "HIGH"
    )

    ticket_id = r["ticket_id"]

    print("Submitted:", r)

    while True:

        s = get_status(ticket_id)

        print("Status:", s)

        if s["status"] == "RESOLVED":
            break

        time.sleep(0.5)