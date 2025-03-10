from framework.Event import Event

class Commitment:
    def __init__(self, name, start_time, end_time, days, location, tag):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.days = days
        self.event = Event(name, location, tag)