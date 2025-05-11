from fastapi import FastAPI
from counter import live_counter, counter_lock
import threading
import counter
app = FastAPI()

@app.post("/line-1/start")
async def start_counting():
    if counter.is_running:
        return {"message": "Already running."}

    counter.is_running = True
    counter.capture_thread = threading.Thread(target=live_counter)
    counter.capture_thread.start()
    return {"message": "started."}

@app.post("/line-1/push")
async def push_pause_resume():
    if not counter.is_running:
        return {"message": "Not running."}

    counter.is_paused = not counter.is_paused
    state = "paused" if counter.is_paused else "resumed"
    return {"message": f"Counting {state}."}

@app.post("/line-1/stop")
async def stop_counting():
    if not counter.is_running:
        return {"message": "Not running."}

    counter.is_running = False
    counter.capture_thread.join()

    with counter.counter_lock:
        counter.messages.clear()
        counter.detected_ids.clear()
    return {"message": "Counting stopped."}

@app.get("/line-1/status") 
async def get_ids():
    with counter_lock:
        return {"status": list(counter.messages)}
