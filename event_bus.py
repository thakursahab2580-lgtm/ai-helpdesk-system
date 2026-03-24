import queue
import threading
import time

from monitoring import handle_event


# Global event queue
event_queue = queue.Queue()

# Control flag for clean shutdown
running = True


def publish_event(event):
    """
    Producer: Called by inference_service.
    """
    event_queue.put(event)


def event_consumer():
    """
    Background consumer thread.
    Continuously listens for new events.
    """
    print("Event consumer started...")

    while running:
        try:
            event = event_queue.get(timeout=1)
            handle_event(event)
            event_queue.task_done()
        except queue.Empty:
            continue

    print("Event consumer stopped.")


def start_event_consumer():
    """
    Start consumer in background thread.
    """
    thread = threading.Thread(target=event_consumer, daemon=True)
    thread.start()
    return thread


def stop_event_consumer():
    """
    Graceful shutdown.
    """
    global running
    running = False
    time.sleep(1)
