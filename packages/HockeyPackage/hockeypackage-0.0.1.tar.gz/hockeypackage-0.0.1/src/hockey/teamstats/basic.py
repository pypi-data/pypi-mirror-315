#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import pkg_resources

class InvalidYearError(Exception):
    pass

def LoadData():
    """loads the correct dataset depending on chosen year"""
    
    year = input("Enter the season you would like data for: Please just enter the year the season finished (e.g., 2021/2022 enter 2022)")
    
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
        csv_path = pkg_resources.resource_stream(__name__, f"../{csv_filename}")
        TeamData = pd.read_csv(csv_path)  
        return TeamData
    except FileNotFoundError:
        print(f"Error: The file for year {year} was not found. Please ensure the file exists.")
        return None

    

def BasicStats():
    """displays specific basic stats for the chosen NHL team, depending on user input"""
    df = LoadData() # calls the loadData function to get the correct year and dataframe
    
    if df is None:
        # If LoadData fails and returns None, return early
        print("Failed to load data. Please try again.")
        return None
        
    team = input("Enter the team name: ").strip().lower()
    valid_stats = ['RK', 'GP', 'W', 'L', 'OT', 'PTS', 'PTS/GP', 'ROW', 'GF', 'GA', 'GD']
    stat = input("Enter the stat/column you want (RK, GP, W, L, OT, PTS, PTS/GP, ROW, GF, GA, GD: ").strip()

    try:
        # Check if the team exists in the dataframe
        team_data = df[df['Team'].str.lower() == team]
        
        if team_data.empty:
            raise ValueError(f"Sorry, the team was not found. Please check your spelling.")
        
        # Check if the stat exists in the dataframe columns
        if stat not in valid_stats:
            raise KeyError(f"Error: The stat '{stat}' does not exist. Please choose a valid stat from the list.")
        
        stat_value = team_data.iloc[0][stat]
        
        return stat_value

    except ValueError as e:
        # Handle invalid team (team not found in dataset)
        print(e)
        return None
    
    except KeyError as e:
        # Handle invalid stat (stat not found)
        print(e)
        return None
    
    except:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred")
        return None


def AdvancedStats():
    """displays advanced stats for the chosen team, depending on user input"""
    df = LoadData() # calls the loadData function to get the correct year and dataframe
    
    if df is None:
        print("Failed to load data. Please try again.")
        return None
        
    team = input("Enter the team name: ").strip().lower()

    team_data = df[df['Team'].str.lower() == team]

    try:
        pts = team_data.iloc[0]['PTS']
        gp = team_data.iloc[0]['GP']
        gf = team_data.iloc[0]['GF']
        ga = team_data.iloc[0]['GA']

        # Check if games played (GP) is zero to avoid division by zero error
        if gp == 0:
            print(f"Warning: The team '{team}' has 0 games played, cannot calculate advanced stats.")
            return None
        
        # Calculate advanced stats
        pts_gp = pts / gp
        gf_gp = gf / gp
        ga_gp = ga / gp

        # Create a DataFrame to display the results
        result_df = pd.DataFrame({
            'Team': [team],
            'PTS/GP': [pts_gp],
            'GF/GP': [gf_gp],
            'GA/GP': [ga_gp]
        })

        return result_df

    except KeyError as e:
        print(f"Error: Missing expected column in the dataset. {e}")
        return None
    except:
        print(f"An unexpected error occurred")
        return None

