import pandas as pd
import os

def calculate_average_percent_change(input_directory, output_file):
    """
    Calculates the average 24-hour percent change for each cryptocurrency
    across multiple Step 3 output files.
    Args:
        input_directory (str): Path to the directory containing the Step 3 output files.
        output_file (str): Path to the output CSV file where the summary will be saved.
    """
    # Step 1: Identify all relevant files from Step 3
    files = [f for f in os.listdir(input_directory) if f.startswith("btc_relationship_") and f.endswith(".csv")]
    if not files:
        raise FileNotFoundError(f"No Step 3 files found in {input_directory}.")

    # Step 2: Combine data from all Step 3 files
    combined_data = pd.DataFrame()
    for file in files:
        file_path = os.path.join(input_directory, file)
        data = pd.read_csv(file_path)
        combined_data = pd.concat([combined_data, data], ignore_index=True)

    # Step 3: Calculate the average percent change
    if "percent_change_24h" not in combined_data.columns:
        raise KeyError("'percent_change_24h' column is missing in the combined data.")

    average_changes = combined_data.groupby("symbol")["percent_change_24h"].mean().reset_index()
    average_changes.rename(columns={"percent_change_24h": "average_percent_change_24h"}, inplace=True)

    # Step 4: Save the summary to a CSV file
    average_changes.to_csv(output_file, index=False)
    print(f"Average percent change summary saved to {output_file}")


def main():
    # Example usage
    input_directory = "."  # Directory where Step 3 CSV files are stored
    output_file = "average_percent_change_summary.csv"
    calculate_average_percent_change(input_directory, output_file)


if __name__ == "__main__":
    main()