import pandas as pd

# ---------- LOAD FILES ----------
squad_path = r"D:\FPL\XGBOOST_best_15_squad_with_starting_XI.xlsx"
gw1_path = r"D:\FPL\GW1\fpl_players_25_26_GW1Stats.xlsx"

# Load squad (with empty Points col) and GW1 stats
squad_df = pd.read_excel(squad_path, sheet_name="Squad")
gw1_df = pd.read_excel(gw1_path)

# Build Name in GW1 file
gw1_df['Name'] = gw1_df['first_name'].str.strip() + " " + gw1_df['second_name'].str.strip()

# Normalize for merging
def normalize_name(name: str) -> str:
    return (
        str(name).strip().lower()
        .replace("đ", "d")
        .replace("'", "")
        .replace("-", " ")
    )

squad_df['Name_norm'] = squad_df['Name'].apply(normalize_name)
gw1_df['Name_norm'] = gw1_df['Name'].apply(normalize_name)

# Merge GW1 points (use total_points column)
squad_df = squad_df.merge(
    gw1_df[['Name_norm', 'total_points']],
    on='Name_norm',
    how='left'
)

# Fill into existing Points column
squad_df['Points'] = squad_df['total_points']

# Apply captain bonus (double points if Captain == 'Yes')
squad_df.loc[squad_df['Captain'] == 'Yes', 'Points'] *= 2

# Team totals
total_points_squad = squad_df['Points'].sum()
total_points_starting_xi = squad_df.loc[squad_df['Starting_XI'] == 'Yes', 'Points'].sum()

# Drop helper cols
squad_df.drop(columns=['Name_norm', 'total_points'], inplace=True)

# ---------- SAVE BACK TO SAME FILE ----------
with pd.ExcelWriter(squad_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
    # Overwrite the Squad sheet with updated Points
    squad_df.to_excel(writer, index=False, sheet_name="Squad")

    # Add or update Summary sheet
    summary_df = pd.DataFrame({
        'Metric': ['GW1 Total Points (All 15)', 'GW1 Total Points (Starting XI)'],
        'Value': [total_points_squad, total_points_starting_xi]
    })
    summary_df.to_excel(writer, index=False, sheet_name="Summary")

print(f"✅ GW1 points mapped into {squad_path}")
print(f"Total GW1 Team Points (All 15): {total_points_squad}")
print(f"Total GW1 Team Points (XI only): {total_points_starting_xi}")
