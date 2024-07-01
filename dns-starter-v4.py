import os
import subprocess
import time

def main():
    # Path to the "in-progres-start" directory
    base_path = "in-progres-start"

    # Check if the directory exists
    if not os.path.exists(base_path):
        print(f"Directory not found: {base_path}")
        return

    # List directories in the "in-progres-start" folder
    try:
        directories = next(os.walk(base_path))[1]
    except StopIteration:
        print("No subdirectories found.")
        return

    # Check if there are any directories found
    if not directories:
        print("No directories found in 'in-progres-start'.")
        return

    # Sort directories to get the top one (alphabetically first)
    top_directory = sorted(directories)[0]
    top_directory_path = os.path.join(base_path, top_directory)

    # Check contents of the top directory
    files = os.listdir(top_directory_path)
    if not files:
        # If directory is empty, delete it
        os.rmdir(top_directory_path)
        print(f"Empty directory {top_directory} deleted.")
        return
    else:
        # Count files in the top directory
        file_count = len([f for f in files if os.path.isfile(os.path.join(top_directory_path, f))])

    # Print the file count
    print(f"Found {file_count} files in the directory {top_directory}")

    # Path to the DNS resolver script
    script_path = "dns-resolver-v6.py"

    # Start the DNS resolver script as many times as there are files
    for i in range(file_count):
        subprocess.Popen(['python3', script_path])
        print(f"Started 'dns-resolver-v6.py' instance {i + 1}")
        time.sleep(2)

    # Continuously check if the directory is empty
    while True:
        # Refresh the directory listing
        if not os.listdir(top_directory_path):
            # Directory is empty, delete it
            os.rmdir(top_directory_path)
            print(f"Directory {top_directory} is now empty and has been deleted.")
            break
        time.sleep(1)  # Check every second

if __name__ == "__main__":
    main()
