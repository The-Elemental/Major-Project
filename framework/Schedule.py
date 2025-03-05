from framework.Event import Event
from datetime import datetime, timedelta
from collections import deque

class Schedule:
    def __init__(self):
        self.queue = deque()
        for x in range(0, 1440):
            self.queue.append(Event("Home", "Home"))
        self.current_time = datetime(1970, 1, 1, 0, 0, 0)

    def add_event(self, start_time, end_time, event):
        """Add a new event to the schedule with start and end times."""
        time_offset = self.current_time - datetime(1970, 1, 1, 0, 0, 0)
        start_index = (start_time.to_seconds() - time_offset.to_seconds()) / 300
        end_index = (end_time.to_seconds() - time_offset.to_seconds()) / 300
        for i in range(start_index, end_index + 1):
            self.queue[i] = event

    def check_schedule(self):
        """Check if any event is active during the current time."""
        return self.queue[0]

    def next(self):
        self.current_time = self.current_time + timedelta(minutes=5)
        self.queue.popleft()
        self.queue.append(Event("Home", "Home"))

    def __repr__(self):
        return "\n".join([f"Current Event: {self.queue[0].name}"])