import os
import pandas as pd
import datetime
import re

def merge_csv_files(source_dir, output_dir):
    # Ensure the source directory exists
    if not os.path.exists(source_dir):
        print(f"Source directory {source_dir} does not exist.")
        return
    
    # Initialize a list to store DataFrames
    dataframes = []

    # Walk through the directory structure and collect all CSV files
    csv_files = []
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.csv') and '_part_' in file:
                csv_files.append(os.path.join(root, file))

    # Sort files based on the numerical part after "_part_"
    csv_files.sort(key=lambda x: int(re.search(r"_part_(\d+)\.csv$", x).group(1)))

    # Load each CSV file into DataFrame and append to list
    for file_path in csv_files:
        try:
            # Specify no header in the CSV file and set column names manually
            df = pd.read_csv(file_path, header=None, names=['Domain', 'IP Address'])
            dataframes.append(df)
            print(f"Loaded {file_path}")
        except pd.errors.EmptyDataError:
            print(f"Skipped empty or invalid CSV file: {file_path}")
        except Exception as e:
            print(f"An error occurred while reading {file_path}: {e}")

    # Check if any CSV files were found and loaded
    if not dataframes:
        print("No valid CSV files found.")
        return

    # Concatenate all dataframes into one
    merged_df = pd.concat(dataframes, ignore_index=True)

    # Sort the DataFrame by 'Domain' in ascending order
    merged_df = merged_df.sort_values(by='Domain', ascending=True)

    # Get the current month as a folder name
    current_month = datetime.datetime.now().strftime("%B")

    # Create the output path with the month name subfolder
    output_path = os.path.join(output_dir, current_month)
    os.makedirs(output_path, exist_ok=True)

    # Save the sorted DataFrame as a new CSV file in the results directory
    output_file_path = os.path.join(output_path, "sorted_merged_output.csv")
    merged_df.to_csv(output_file_path, index=False)
    print(f"Sorted merged CSV saved as {output_file_path}")

# Directory paths
source_directory = 'in-progras-end'
output_directory = 'results'

# Call the function
merge_csv_files(source_directory, output_directory)
