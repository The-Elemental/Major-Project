from .Location import Location
from .BehaviourNode import BehaviourNode
class Event:
    """Event object for schedule"""
    def __init__(self, name:str, location:Location, behaviour_tags:set=None, behaviour_node:BehaviourNode=None):
        self.name = name
        self.location = location
        self.behaviour_tag = behaviour_tags
        self.behaviour_node = behaviour_node