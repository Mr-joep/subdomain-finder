import os
import csv
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
import shutil

# Define the paths for the start, in-progress, and end directories
start_dir = "in-progres-start"
in_progress_dir = "in-progres"
end_dir = "in-progras-end"

# Step 1: Look in the folder "in-progres-start" and use the top folder
top_folder = sorted(os.listdir(start_dir))[0]
top_folder_path = os.path.join(start_dir, top_folder)

# Step 2: List CSV files in the top folder and automatically choose the top one
csv_files = sorted([f for f in os.listdir(top_folder_path) if f.endswith('.csv')])
chosen_csv = csv_files[0] if csv_files else None

if not chosen_csv:
    print("No CSV files found in the directory.")
    exit(1)

chosen_csv_path = os.path.join(top_folder_path, chosen_csv)

# Move the chosen file to the "in-progres" folder
in_progress_csv_path = os.path.join(in_progress_dir, chosen_csv)
os.makedirs(in_progress_dir, exist_ok=True)
shutil.move(chosen_csv_path, in_progress_csv_path)

# Step 3: Extract domain names from the moved CSV file and resolve to IP addresses
domains = []
with open(in_progress_csv_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row:
            domains.append(row[0])

def resolve_domain(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return domain, ip_address
    except socket.gaierror:
        return domain, 'Could not resolve'

# Use ThreadPoolExecutor to resolve domains concurrently
resolved_ips = []
with ThreadPoolExecutor(max_workers=125) as executor:
    futures = {executor.submit(resolve_domain, domain): domain for domain in domains}
    for future in as_completed(futures):
        domain, ip_address = future.result()
        resolved_ips.append((domain, ip_address))

# Step 4: Save the domains and IP addresses to a new CSV file
output_file_name = chosen_csv
output_folder_path = os.path.join(end_dir, top_folder)
os.makedirs(output_folder_path, exist_ok=True)
output_file_path = os.path.join(output_folder_path, output_file_name)

with open(output_file_path, mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['domain', 'ip_address'])
    for domain, ip_address in resolved_ips:
        writer.writerow([domain, ip_address])

# Delete the CSV file from the "in-progres" folder after processing
os.remove(in_progress_csv_path)

print(f"Resolved IP addresses saved to {output_file_path}")
