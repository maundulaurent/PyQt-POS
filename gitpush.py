import subprocess
import time
from datetime import datetime

# Configuration
INTERVAL_SECONDS = 30  # Set the interval for pushing in seconds

def git_push():
    try:
        # Add all changes
        subprocess.run(["git", "add", "."], check=True)
        
        # Commit changes with current time as the commit message
        commit_message = f"Made Changes on My POS, making content dynamic {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        
        # Push changes
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
        
        print(f"Push successful: {commit_message}")
        
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        
def main():
    while True:
        git_push()
        time.sleep(INTERVAL_SECONDS)
        
if __name__ == "__main__":
    main()
