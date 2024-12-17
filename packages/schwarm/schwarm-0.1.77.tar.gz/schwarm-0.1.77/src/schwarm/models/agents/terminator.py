"""Terminator agent for ending a agent process"""


from schwarm.models.agent import Agent



class TerminatorAgent(Agent):
    """An agent which does nothing. Ends the agent system flow when active"""

    def __init__(self):
        super().__init__(name="Terminator")
