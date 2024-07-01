import os
import csv
import socket

# Define the paths for the start and end directories
start_dir = "in-progres-start"
end_dir = "in-progras-end"

# Step 1: Look in the folder "in-progres-start" and use the top folder
top_folder = sorted(os.listdir(start_dir))[0]
top_folder_path = os.path.join(start_dir, top_folder)

# Step 2: List CSV files in the top folder and ask which one to use
csv_files = [f for f in os.listdir(top_folder_path) if f.endswith('.csv')]
print("CSV files available:")
for i, file in enumerate(csv_files):
    print(f"{i + 1}. {file}")

file_choice = int(input("Enter the number of the CSV file you want to use: ")) - 1
chosen_csv = csv_files[file_choice]
chosen_csv_path = os.path.join(top_folder_path, chosen_csv)

# Step 3: Extract domain names from the chosen CSV file and resolve to IP addresses
domains = []
with open(chosen_csv_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        domains.append(row['domain'])

resolved_ips = []
for domain in domains:
    try:
        ip_address = socket.gethostbyname(domain)
        resolved_ips.append((domain, ip_address))
    except socket.gaierror:
        resolved_ips.append((domain, 'Could not resolve'))

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

print(f"Resolved IP addresses saved to {output_file_path}")
