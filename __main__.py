import pandas as pd
import numpy as np
import os

def parse_draft_board():
    input_filename = 'draft_board.csv'
    league = 0
    picks_per_round = 16

    # --- CONFIGURATION SECTION ---
    # Edit the 'filename' values below to change output names.
    # Indices correspond to CSV columns: 0=A, 1=B, 2=C, etc.
    draft_sections = [
        {'indices': (0, 1), 'filename': 'results\\pl_draft.txt'},  # Columns A & B
        {'indices': (2, 3), 'filename': 'results\\ml_draft.txt'},  # Columns C & D
        {'indices': (4, 5), 'filename': 'results\\cl_draft.txt'},  # Columns E & F
        {'indices': (6, 7), 'filename': 'results\\al_draft.txt'},  # Columns G & H
        {'indices': (8, 9), 'filename': 'results\\fl_draft.txt'}   # Columns I & J
    ]
    # -----------------------------

    if not os.path.exists(input_filename):
        print(f"Error: Could not find '{input_filename}'")
        return

    print(f"Reading '{input_filename}'...")

    try:
        df = pd.read_csv(input_filename, header=None)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # Loop through each configuration dictionary defined above
    for section in draft_sections:
        team_col_idx, player_col_idx = section['indices']
        output_file = section['filename']

        print(f"Processing Columns {team_col_idx}/{player_col_idx} -> Saving to '{output_file}'...")

        # Check if league has 16 or 32 picks per round
        if league == 0 or league == 4:
            picks_per_round = 16
        else:
            picks_per_round = 32
        league += 1

        round = 1

        with open(output_file, 'w') as f:
            for index, row in df.iterrows():
                
                # Check if column exists in data to prevent index errors
                if team_col_idx >= len(row): 
                    continue

                team_name = row.iloc[team_col_idx]
                
                # Handle missing player columns (e.g., if CSV has jagged edges)
                if player_col_idx < len(row):
                    player_name = row.iloc[player_col_idx]
                else:
                    player_name = np.nan

                pick_row_number = index + 1

                # Print round number if start of round
                if pick_row_number % picks_per_round == 1 and round <= 4:
                    f.write(f"## Start of Round {round}\n\n")
                    round += 1

                # Skip if Team Name is empty
                if pd.isna(team_name) or str(team_name).strip() == "":
                    break

                # Check if Player Name is empty
                is_player_empty = pd.isna(player_name) or str(player_name).strip() == ""

                # Write to the specific file for this column pair
                if is_player_empty:
                    f.write(f"@{team_name} Pick {pick_row_number}\n")
                    f.write("You have 60 seconds on the clock.\n\n")
                else:
                    f.write(f"@{team_name} Pick {pick_row_number}\n")
                    f.write(f"Retain {player_name}\n\n")

    print("All files generated successfully.")

if __name__ == "__main__":
    parse_draft_board()
