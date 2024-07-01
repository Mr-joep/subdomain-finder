import os
import csv

def split_csv(source_folder, target_base_folder, max_lines=50000):
    # Determine the first subfolder in the source_folder
    subfolders = next(os.walk(source_folder))[1]
    if not subfolders:
        print("No subfolders found in the 'domains' folder.")
        return
    top_subfolder = subfolders[0]

    # Create the target folder inside the target base folder with the same name as the top subfolder
    target_folder = os.path.join(target_base_folder, top_subfolder)
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Find the CSV file in the selected subfolder
    path = os.path.join(source_folder, top_subfolder)
    files = [f for f in os.listdir(path) if f.endswith('.csv')]
    if not files:
        print(f"No CSV files found in the folder {path}.")
        return
    csv_file = files[0]

    # Read and split the CSV file
    full_path = os.path.join(path, csv_file)
    with open(full_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        headers = next(reader)

        file_count = 1
        csv_writer = None
        current_file_path = os.path.join(target_folder, f"{top_subfolder}_part_{file_count}.csv")
        for i, row in enumerate(reader, start=1):
            if i % max_lines == 1:
                if csv_writer:
                    output_file.close()
                current_file_path = os.path.join(target_folder, f"{top_subfolder}_part_{file_count}.csv")
                output_file = open(current_file_path, mode='w', newline='')
                csv_writer = csv.writer(output_file)
                csv_writer.writerow(headers)
                file_count += 1
            csv_writer.writerow(row)
        
        if csv_writer:
            output_file.close()

# Example usage
source_folder = 'domains'
target_base_folder = 'in-progress-start'
split_csv(source_folder, target_base_folder)
