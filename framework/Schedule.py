from framework.Event import Event
from datetime import datetime, timedelta
from collections import deque

class Schedule:
    def __init__(self):
        self.queue = deque([None] * 2016)
        self.index_offset = 0

    def add_event(self, start_time, end_time, event):
        """Add a new event to the schedule with start and end times."""
        start_index = (start_time.timestamp() // 300) - self.index_offset
        end_index = (end_time.timestamp() // 300) - self.index_offset
        for i in range(start_index, end_index + 1):
            self.queue[i] = event

    def check_schedule(self):
        """Check next event."""
        return self.queue[0]

    def next(self, current_time):
        self.index_offset += 1
        
        # Create Scheduling Logic:
        
        return self.queue.popleft()
        

    def __repr__(self):
        return "\n".join([f"Current Event: {self.queue[0].name}"])