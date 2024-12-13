from .skater import Skater
from .goalie import Goalie

def get_player_stats():
    """Gets the users input to dtermine which information they would like displayed"""
    while True:
        year = input("Enter the year to search NHL stats (2020, 2021, 2022, 2023, 2024): ")
        if year in ['2020', '2021', '2022', '2023', '2024']:
            year = int(year)
            break
        else:
            print("Invalid year. Please enter a valid year.")
    
    
    player_type = input("Enter player type (skater/goalie): ").strip().lower()
    
   
    if player_type not in ['skater', 'goalie']:
        print("Invalid player type. Please enter either 'skater' or 'goalie'.")
        return
    
    
    if player_type == 'skater':
        player = Skater(year)
    else:
        player = Goalie(year)
    
    player.load_data()  
    
    player_name = input("Enter the player's name: ").strip().lower()
    
    
    stat_type = input("Would you like to display basic stats or advanced stats? (basic/advanced): ").strip().lower()
    
    if stat_type == 'basic':
        player.basic_stats(player_name)
    elif stat_type == 'advanced':
        player.advanced_stats(player_name)
    else:
        print("Invalid choice. Please choose either 'basic' or 'advanced'.")


