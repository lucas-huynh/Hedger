import pandas as pd

# ---------------------------
# Load Game-Level Data
# ---------------------------
games = pd.read_csv("nfl_data_cleaned.csv")
games["schedule_season"] = games["schedule_season"].astype(int)
games["PHASE"] = games["schedule_playoff"].apply(lambda x: "POST" if x else "REG")

# ---------------------------
# Load Team-Level Offense and Defense Data
# ---------------------------
offense = pd.read_csv("nfl_team_stats_offense_1986_2024.csv")
defense = pd.read_csv("nfl_team_stats_defense_1986_2024.csv")

# ---------------------------
# Merge Offense Stats
# ---------------------------
# Merge home team offense data
games = games.merge(
    offense,
    left_on=["team_home_id", "schedule_season", "PHASE"],
    right_on=["team_id", "YEAR", "PHASE"],
    how="left",
    suffixes=("", "_home_offense")
)

# Merge away team offense data
games = games.merge(
    offense,
    left_on=["team_away_id", "schedule_season", "PHASE"],
    right_on=["team_id", "YEAR", "PHASE"],
    how="left",
    suffixes=("", "_away_offense")
)

# ---------------------------
# Merge Defense Stats
# ---------------------------
# Merge home team defense data
games = games.merge(
    defense,
    left_on=["team_home_id", "schedule_season", "PHASE"],
    right_on=["team_id", "YEAR", "PHASE"],
    how="left",
    suffixes=("", "_home_defense")
)

# Merge away team defense data
games = games.merge(
    defense,
    left_on=["team_away_id", "schedule_season", "PHASE"],
    right_on=["team_id", "YEAR", "PHASE"],
    how="left",
    suffixes=("", "_away_defense")
)

# ---------------------------
# Clean the Merged Data
# ---------------------------
# Drop duplicate rows and any rows with null values
games = games.drop_duplicates()

# Drop redundant columns as specified:
drop_columns = [
    "YEAR_away_defense", "CATEGORY_away_defense", "team_id_away_defense", "GP_away_defense",
    "YEAR_home_defense", "CATEGORY_home_defense", "team_id_home_defense", "GP_home_defense",
    "YEAR_away_offense", "CATEGORY_away_offense", "team_id_away_offense", "GP_away_offense",
    "YEAR", "CATEGORY", "team_id", "GP", "PHASE"
]
games.drop(columns=[col for col in drop_columns if col in games.columns], inplace=True)

# Rename the home offense columns to include the "_home_offense" suffix
rename_dict = {
    "RK": "RK_home_offense",
    "PTS/G": "PTS/G_home_offense",
    "PTS": "PTS_home_offense",
    "PLAYS": "PLAYS_home_offense",
    "YDS": "YDS_home_offense",
    "YDS/PLAY": "YDS/PLAY_home_offense",
    "1ST DWN": "1ST DWN_home_offense",
    "PENALTY": "PENALTY_home_offense",
    "P YDS": "P YDS_home_offense",
    "TOP": "TOP_home_offense",
    "+/- TOV": "+/- TOV_home_offense"
}
games.rename(columns=rename_dict, inplace=True)

# ---------------------------
# Save the Final Merged Data
# ---------------------------
games.to_csv("nfl_data_with_team_stats.csv", index=False)
print("Merged data with team stats saved to nfl_data_with_team_stats.csv")
