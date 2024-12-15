import os
import subprocess
import platform
import requests

def download_install_script():
    """Download install.sh from GitHub if not present."""
    url = "https://raw.githubusercontent.com/blueraymusic/LingoShell/main/Install.sh"
    script_path = os.path.join(os.path.dirname(__file__), 'inst', 'install.sh')
    
    if not os.path.exists(script_path):
        print(f"Downloading install.sh from GitHub...")
        try:
            response = requests.get(url)
            response.raise_for_status()
            os.makedirs(os.path.dirname(script_path), exist_ok=True)  # Ensure directory exists
            with open(script_path, 'wb') as f:
                f.write(response.content)
            print("install.sh downloaded successfully.")
        except requests.RequestException as e:
            print(f"Error downloading install.sh: {e}")
            return False
    return True


def run_install_script():
    """
    Detects the OS and runs the appropriate install script.
    """
    system_platform = platform.system()
    script_name = None
    command = []

    if system_platform == "Darwin":  # macOS
        script_name = "install.sh"
        command = ["bash"]
    elif system_platform == "Windows":  # Windows
        script_name = "install.ps1"
        command = ["powershell", "-ExecutionPolicy", "Bypass", "-File"]
    else:
        print(f"Unsupported platform: {system_platform}")
        return

    # Download the script if it's not present
    if not download_install_script():
        return

    # Path to the script
    script_path = os.path.join(os.path.dirname(__file__), 'inst', script_name)

    # Execute the install script
    if os.path.exists(script_path):
        try:
            print(f"Executing {script_name} for {system_platform}...")
            subprocess.run(command + [script_path], check=True)
            print(f"{script_name} executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing {script_path}: {e}")
    else:
        print(f"Installer script {script_name} not found at: {script_path}")

if __name__ == "__main__":
    run_install_script()
