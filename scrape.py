import requests
import pandas as pd
import time

# Base URL for team stats
base_url = "https://fantasydata.com/nfl/team-stats"

# User-Agent header (adjust if needed)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# ---------------------------
# Scrape Offense Data
# ---------------------------
all_dfs_offense = []

for year in range(1986, 2025):
    for phase in ["REG", "POST"]:
        season_phase = f"{year}_{phase}"
        url = f"{base_url}?sp={season_phase}&category=offense&split=totals"
        print(f"Scraping Offense URL: {url}")
        try:
            response = requests.get(url, headers=headers)
            # Use pandas to extract all tables from the page
            tables = pd.read_html(response.text)
            if tables:
                df = tables[0]
                # Add extra columns for season, phase, and category
                df["Season"] = year
                df["Phase"] = phase
                df["Category"] = "offense"
                all_dfs_offense.append(df)
            else:
                print(f"No table found for {url}")
        except Exception as e:
            print(f"Error scraping {url}: {e}")
        time.sleep(1)

if all_dfs_offense:
    final_offense_df = pd.concat(all_dfs_offense, ignore_index=True)
    final_offense_df.to_csv("nfl_team_stats_offense_1986_2024.csv", index=False)
    print("Offense data saved to nfl_team_stats_offense_1986_2024.csv")
else:
    print("No offense data was scraped.")

# ---------------------------
# Scrape Defense Data
# ---------------------------
all_dfs_defense = []

for year in range(1986, 2025):
    for phase in ["REG", "POST"]:
        season_phase = f"{year}_{phase}"
        url = f"{base_url}?sp={season_phase}&category=defense&split=totals"
        print(f"Scraping Defense URL: {url}")
        try:
            response = requests.get(url, headers=headers)
            tables = pd.read_html(response.text)
            if tables:
                df = tables[0]
                df["Season"] = year
                df["Phase"] = phase
                df["Category"] = "defense"
                all_dfs_defense.append(df)
            else:
                print(f"No table found for {url}")
        except Exception as e:
            print(f"Error scraping {url}: {e}")
        time.sleep(1)

if all_dfs_defense:
    final_defense_df = pd.concat(all_dfs_defense, ignore_index=True)
    final_defense_df.to_csv("nfl_team_stats_defense_1986_2024.csv", index=False)
    print("Defense data saved to nfl_team_stats_defense_1986_2024.csv")
else:
    print("No defense data was scraped.")

