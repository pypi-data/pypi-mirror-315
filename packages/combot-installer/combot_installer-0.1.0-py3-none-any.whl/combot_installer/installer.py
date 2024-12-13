import os
import subprocess
import urllib.request
import sys

# URL of the Install.sh script
INSTALL_SCRIPT_URL = "https://raw.githubusercontent.com/blueraymusic/Combot/main/Install.sh"
SCRIPT_NAME = "Install.sh"

def download_script(url, target_path):
    """Download the shell script from the provided URL."""
    try:
        print(f"Downloading script from {url}...")
        urllib.request.urlretrieve(url, target_path)
        os.chmod(target_path, 0o755)  # Make it executable
        print(f"Downloaded and saved as {target_path}")
    except Exception as e:
        print(f"Error downloading script: {e}")
        sys.exit(1)

def execute_script(script_path):
    """Run the shell script."""
    try:
        print(f"Executing {script_path}...")
        subprocess.run([script_path], check=True)
        print("Script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error while executing the script: {e}")
        sys.exit(1)

def main():
    """Main function to manage the installation process."""
    script_path = os.path.join(os.getcwd(), SCRIPT_NAME)
    download_script(INSTALL_SCRIPT_URL, script_path)
    execute_script(script_path)

if __name__ == "__main__":
    main()
