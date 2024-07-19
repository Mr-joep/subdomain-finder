import subprocess

def run_script(script_name):
    """Run a script using Python and wait for it to complete before starting the next one."""
    print(f"Starting {script_name}...")
    # The subprocess.run function blocks execution until the called script finishes.
    subprocess.run(['python3', script_name], check=True)
    print(f"Finished running {script_name}.")

def main():
    # List of scripts to run in sequence, ensuring one script completes before the next starts
    scripts = [
        'subdomein-generator-new-v4.py',
        'splitter-v3.py',
        'dns-starter-v5.py',
        'combind-v8.py'
    ]

    for script in scripts:
        run_script(script)  # This call will only start the next script once the current one has completed

if __name__ == '__main__':
    main()
