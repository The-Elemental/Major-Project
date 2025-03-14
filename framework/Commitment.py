from framework import Event
from framework import Location
from datetime import time

class Commitment:
    def __init__(self, name:str, start_time:time, end_time:time, days:set, location:Location, tags:set):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.days = days
        self.event = Event(name=name, location=location, behaviour_tags=tags)