#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import pandas as pd
import pkg_resources

class InvalidYearError(Exception):
    pass

class InvalidRequest(Exception):
    pass

def TopTeams():
    """allows the user to choose an NHL season, and show the teams with the most points from that year"""
    year = input("Enter the season you would like data for: Please just enter the year the season finished (e.g., 2021/2022 enter 2022)").strip()

    
    valid_years = {2020, 2021, 2022, 2023, 2024}
    try:
        year = int(year)
        if year not in valid_years:
            raise InvalidYearError("Invalid year. Please enter a valid year between 2020 and 2024.")
            
    except ValueError:
        print("Invalid year format. Please enter a valid year (e.g., 2022).")
        return None
    except InvalidYearError as e:
        print(e)
        return None

    csv_filename = f"Team{year}.csv"
    
    try:
        # Try loading the dataset
        csv_path = pkg_resources.resource_stream(__name__, f"../{csv_filename}")
        TeamData = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: The file for year {year} was not found. Please ensure the file exists.")
        return None

    try:
        num_teams = int(input("Enter the number of top teams you want to display: "))
        total_teams = len(TeamData)
        if num_teams <= 0:
            raise ValueError
        elif num_teams >total_teams:
            raise InvalidRequest(f"Error: You have requested too many teams. Please enter a number less than or equal to {total_teams}.")

    except ValueError:
        print("Invalid input. Please enter a positive integer for the number of teams.")
        return None
    except InvalidRequest as e:
        print(e)
        return None
    
    top_teams = TeamData[['Team', 'PTS']].sort_values(by='PTS', ascending=False).head(num_teams)
    
    return top_teams


    
def TopAssists():
    """allows the user to choose an NHL season, and show the players with most assists from that year"""
    year = input("Enter the season you would like data for: Please just enter the year the season finished (e.g., 2021/2022 enter 2022)").strip()

    valid_years = {2020, 2021, 2022, 2023, 2024}
    try:
        year = int(year)
        if year not in valid_years:
            raise InvalidYearError("Invalid year. Please enter a valid year between 2020 and 2024.")
            
    except ValueError:
        print("Invalid year format. Please enter a valid year (e.g., 2022).")
        return None
    except InvalidYearError as e:
        print(e)
        return None

    csv_filename = f"skaters{year}.csv"

    try:
        csv_path = pkg_resources.resource_stream(__name__, f"../{csv_filename}")
        skaterData = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: The file for year {year} was not found. Please ensure the file exists.")
        return None

    try:
        num_players = int(input("Enter the number of players you want to display: "))
        filtered_data = skaterData[skaterData['situation'] == 'all']
        total_players = len(filtered_data)
        if num_players <= 0:
            raise ValueError
        elif num_players >total_players:
            raise InvalidRequest(f"Error: You have requested too many players. Please enter a number less than or equal to {total_players}.")

    except ValueError:
        print("Invalid input. Please enter a positive integer for the number of players.")
        return None
    except InvalidRequest as e:
        print(e)
        return None
        
    top_players = filtered_data[['name', 'I_F_primaryAssists', 'I_F_secondaryAssists']] \
                      .assign(total_assists=filtered_data['I_F_primaryAssists'] + filtered_data['I_F_secondaryAssists']) \
                      .sort_values(by='total_assists', ascending=False) \
                      .head(num_players)
    
    return top_players


def TopGoals():
    """allows the user to choose an NHL season, and displays the players with the most goals from that year."""
    year = input("Enter the season you would like data for: Please just enter the year the season finished (e.g., 2021/2022 enter 2022)").strip()

    valid_years = {2020, 2021, 2022, 2023, 2024}
    try:
        year = int(year)
        if year not in valid_years:
            raise InvalidYearError("Invalid year. Please enter a valid year between 2020 and 2024.")
            
    except ValueError:
        print("Invalid year format. Please enter a valid year (e.g., 2022).")
        return None
    except InvalidYearError as e:
        print(e)
        return None

    csv_filename = f"skaters{year}.csv"
    
    try:
        csv_path = pkg_resources.resource_stream(__name__, f"../{csv_filename}")
        skaterData = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: The file for year {year} was not found. Please ensure the file exists.")
        return None

    try:
        num_players = int(input("Enter the number of players you want to display: "))
        filtered_data = skaterData[skaterData['situation'] == 'all']
        total_players = len(filtered_data)
        if num_players <= 0:
            raise ValueError
        elif num_players >total_players:
            raise InvalidRequest(f"Error: You have requested too many players. Please enter a number less than or equal to {total_players}.")

    except ValueError:
        print("Invalid input. Please enter a positive integer for the number of players.")
        return None
    except InvalidRequest as e:
        print(e)
        return None

    top_players = filtered_data[['name', 'I_F_goals']].sort_values(by='I_F_goals', ascending=False).head(num_players)
    
    return top_players

