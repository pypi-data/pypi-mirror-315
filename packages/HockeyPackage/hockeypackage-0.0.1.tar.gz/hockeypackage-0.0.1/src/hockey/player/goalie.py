from .player import Player
import pkg_resources

class Goalie(Player):
    """Creating a class to represent a goalie and retrieve their basic and advanced stats. This is a child class from Player"""
    def __init__(self, year):
        """Initialzing the goalie class for a given year"""
        super().__init__(year)
        self.filename = f"goalies{self.year}.csv"

    def load_data(self):
        """Loading the correct csv for the goalie and year"""
        super().load_data(self.filename)

    def basic_stats(self, player_name):
        """Displays basic stats for the goalie such as team, wins, games played, save percentage"""
        player_data = self._get_player_data(player_name)
        if player_data is not None:
            print(f"\nGoalie Basic Stats for {player_name.capitalize()} (Year: {self.year})")
            print(f"Name: {player_data['name'].capitalize()}")
            print(f"Team: {player_data['Team']}")
            print(f"Wins: {player_data['W']}")
            print(f"Games Played: {player_data['GP']}")
            print(f"Save Percentage (SV%): {player_data['SV%']}")
        else:
            print(f"Goalie {player_name.capitalize()} not found.")

    def advanced_stats(self, player_name):
        """Displays advanced stats for the goalie such as goals against average, save percentage, shutouts, total saves"""
        player_data = self._get_player_data(player_name)
        if player_data is not None:
            print(f"\nGoalie Advanced Stats for {player_name.capitalize()} (Year: {self.year})")
            print(f"Name: {player_data['name'].capitalize()}")
            print(f"Team: {player_data['Team']}")
            print(f"Goals Against Average (GAA): {player_data['GAA']}")
            print(f"Save Percentage (SV%): {player_data['SV%']}")
            print(f"Shutouts: {player_data['SO']}")
            print(f"Total Saves: {player_data['SV']}")
        else:
            print(f"Goalie {player_name.capitalize()} not found.")
