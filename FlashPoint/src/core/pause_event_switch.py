import threading

"""Use this to pause an event mid-way. Call pause_event.wait() to pause, and pause_event.set() to unpause."""
pause_event = threading.Event()
