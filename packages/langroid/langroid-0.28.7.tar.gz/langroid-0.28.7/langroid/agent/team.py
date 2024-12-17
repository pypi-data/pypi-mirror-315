from abc import ABC, abstractmethod

class TeamComponent(ABC):
    @abstractmethod
    def run(self, msg):
        pass

class Team(TeamComponent):
    def __init__(self):
        self.components = []
        self.input_port = []
        self.followers = []
        self.scheduler = None

    def follow(self, team):
        team.followers.append(self)

    def add_component(self, component):
        self.components.append(component)

    def notify_followers(self, result):
        for follower in self.followers:
            follower.input_port.append(result)

    def run(self, msg):
        if self.scheduler:
            return self.scheduler.run(self.components, msg)
        # Default sequential execution
        result = ""
        for component in self.components:
            result += component.run(msg)
        self.notify_followers(result)
        return result

class Agent(TeamComponent):
    def __init__(self, name):
        self.name = name

    def run(self, msg):
        result = f"Agent {self.name} processed: {msg}"
        return result