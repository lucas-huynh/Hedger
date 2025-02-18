import pandas as pd

# Load the nfl_teams dataset (assumes columns: team_name_short, team_id)
nfl_teams = pd.read_csv("nfl_teams.csv")

# Create a mapping from team_name_short (e.g., 'Bengals') to team_id (e.g., 'CIN')
mapping = nfl_teams.set_index("team_name_short")["team_id"].to_dict()

def map_team(team):
    # If the team name is "Commanders", return "WAS" manually.
    if team == "Commanders":
        return "WAS"
    # Otherwise, return the mapped team_id, or keep the original value if not found.
    return mapping.get(team, team)

# Process the offense dataset
offense_df = pd.read_csv("nfl_team_stats_offense_1986_2024.csv")
offense_df["TEAM"] = offense_df["TEAM"].apply(map_team)
offense_df.rename(columns={"TEAM": "team_id"}, inplace=True)
offense_df.to_csv("nfl_team_stats_offense_1986_2024.csv", index=False)

# Process the defense dataset
defense_df = pd.read_csv("nfl_team_stats_defense_1986_2024.csv")
defense_df["TEAM"] = defense_df["TEAM"].apply(map_team)
defense_df.rename(columns={"TEAM": "team_id"}, inplace=True)
defense_df.to_csv("nfl_team_stats_defense_1986_2024.csv", index=False)

print("Updated offense and defense CSV files have been saved with team_id (with Commanders mapped to WAS).")
