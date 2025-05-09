import time
import threading

# Shared variables expected by main.py
counter_lock = threading.Lock()
messages = []
detected_ids = set()

is_running = False
is_paused = False
capture_thread = None

def live_counter():
    global is_running, is_paused
    while is_running:
        if is_paused:
            time.sleep(1)
            continue
        with counter_lock:
            messages.append("+1")
        time.sleep(2)