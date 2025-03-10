class Event:
    """Event object for schedule"""
    def __init__(self, name, location, behaviour_tag=None, behaviour_node=None):
        self.name = name
        self.location = location
        self.behaviour_tag = behaviour_tag
        self.behaviour_node = behaviour_node