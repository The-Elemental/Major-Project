from framework.Event import Event
from framework.Commitment import Commitment
from datetime import datetime, timedelta
from collections import deque


class Schedule:
    def __init__(self):
        self.queue = deque([None] * 2016)
        self.index_offset = 0
        self.commitments = []

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
        new_event_time = current_time + timedelta(days=7, minutes=5)
        for x in self.commitments:
            if x.days.contains(new_event_time.weekday()):
                if new_event_time.time() > x.start_time.time() and new_event_time.time() < x.end_time.time():
                    self.queue.append(x.event)
                else:
                    self.queue.append(None)
            else:
                self.queue.append(None)
        
        return self.queue.popleft()
        
    def add_commitment(self, name, start_time, end_time, days, location, tag):
        self.commitments.append(Commitment(name, start_time, end_time, days, location, tag))
    
    def __repr__(self):
        return "\n".join([f"Current Event: {self.queue[0].name}"])