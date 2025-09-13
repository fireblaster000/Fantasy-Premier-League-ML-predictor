import requests
import pandas as pd

# Fetch FPL data
url = "https://fantasy.premierleague.com/api/bootstrap-static/"
response = requests.get(url)
data = response.json()

# Base player data
players_df = pd.DataFrame(data['elements'])

# Team and Position Mappings
teams_df = pd.DataFrame(data['teams'])[['id', 'name']].rename(columns={'id': 'team', 'name': 'team_name'})
positions_df = pd.DataFrame(data['element_types'])[['id', 'singular_name_short']].rename(columns={'id': 'element_type', 'singular_name_short': 'position'})

# Merge team names and positions
players_df = players_df.merge(teams_df, on='team', how='left')
players_df = players_df.merge(positions_df, on='element_type', how='left')

# Select final columns
important_columns = [
    "first_name", "second_name", "web_name", "team_name", "position",
    "now_cost", "total_points", "points_per_game", "minutes", "goals_scored",
    "assists", "clean_sheets", "goals_conceded", "yellow_cards", "red_cards",
    "penalties_saved", "penalties_missed", "saves", "bonus", "bps",
    "influence", "creativity", "threat", "ict_index", "selected_by_percent",
    "form", "ep_next", "expected_goals", "expected_assists","expected_goal_involvements",
    "expected_goals_conceded", "status", "penalties_order", "defensive_contribution", "defensive_contribution_per_90", "team_join_date"
]

filtered_df = players_df[important_columns].sort_values(by="total_points", ascending=False)

# Save to Excel
filtered_df.to_excel("fpl_players_25_26_GW3Stats.xlsx", index=False)
print("Saved: fpl_players_25_26_GW2Stats.xlsx ✅")
