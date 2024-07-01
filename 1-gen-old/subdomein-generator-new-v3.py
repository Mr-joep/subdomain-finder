import csv
import string
import itertools
import time
import os

def count_subdomains(domain, max_length):
    count = 0
    characters = string.ascii_lowercase + string.digits
    for length in range(1, max_length + 1):
        count += len(characters) ** length
    return count

def generate_subdomains(domain, max_length, progress_callback=None, update_interval=1):
    characters = string.ascii_lowercase + string.digits
    total_subdomains = count_subdomains(domain, max_length)
    subdomains_generated = 0
    start_time = time.time()
    
    for length in range(1, max_length + 1):
        for subset in itertools.product(characters, repeat=length):
            subdomain = ''.join(subset)
            yield subdomain + '.' + domain
            subdomains_generated += 1
            progress = subdomains_generated / total_subdomains
            current_time = time.time()
            if progress_callback and current_time - start_time >= update_interval:
                progress_callback(progress * 100)
                start_time = current_time

def save_subdomains_to_csv(subdomains, filename, chunk_size=1000):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Subdomain"])
        chunk = []
        for subdomain in subdomains:
            chunk.append([subdomain])
            if len(chunk) == chunk_size:
                writer.writerows(chunk)
                chunk = []
        if chunk:
            writer.writerows(chunk)

def main():
    request_folder = "request"
    request_files = [f for f in os.listdir(request_folder) if f.startswith("request-") and f.endswith(".csv")]
    if not request_files:
        print("No request files found.")
        return
    request_file = os.path.join(request_folder, request_files[0])  # Use the first request file

    with open(request_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            domain, max_length = row[0], int(row[1])
            break  # Read only the first row
    
    total_subdomains = count_subdomains(domain, max_length)
    print(f"Total number of subdomains to be generated: {total_subdomains}")
    
    def progress_callback(progress):
        print(f"Generating... {progress:.2f}% complete", end='\r')

    # Ensure directory exists
    domain_folder = os.path.join("domains", domain)  # Path to the domain folder
    os.makedirs(domain_folder, exist_ok=True)  # Create the folder if it doesn't exist
    
    start_time = time.time()
    subdomains = generate_subdomains(domain, max_length, progress_callback)
    filename = os.path.join(domain_folder, "subdomains.csv")  # Update the filename to include the path
    save_subdomains_to_csv(subdomains, filename)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nGenerated subdomains are saved in '{filename}'.")
    print(f"Total time taken: {elapsed_time:.2f} seconds.")

    # Delete the request file
    os.remove(request_file)
    print(f"Deleted the request file: {request_file}")

if __name__ == "__main__":
    main()
