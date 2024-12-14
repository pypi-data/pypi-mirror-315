from abc import ABC, abstractmethod
import pyspiel

class GoBot(ABC):
    def __init__(self, name):
        self.name = name
        self.match_data = {}

    def on_start(self, player_data):
        """Called at the start of each match"""
        self.match_data.clear()
        self.match_data['player'] = player_data['player']
        self.setup()

    def on_update(self, game_state: pyspiel.State):
        """Called after each move is made"""
        self.update(game_state)

    def get_action(self, game_state: pyspiel.State) -> int:
        """Main method to get the bot's next move"""
        return self.get_move(game_state)

    def setup(self):
        """Override to add custom match start logic"""
        pass

    def update(self, game_state: pyspiel.State, last_move: int):
        """Override to add custom move tracking logic"""
        pass

    @abstractmethod
    def get_move(self, game_state: pyspiel.State) -> int:
        """Select a move given the current game state"""
        pass

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)