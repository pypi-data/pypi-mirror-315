import os
import subprocess
import platform


def install():
    """
    Detects the operating system and runs the appropriate installation script.
    """
    # Identify the user's operating system
    system_platform = platform.system()

    if system_platform == "Darwin":  # macOS
        install_script = "install.sh"
        command = ["bash"]
    elif system_platform == "Windows":  # Windows
        install_script = "install.ps1"
        command = ["powershell", "-ExecutionPolicy", "Bypass", "-File"]
    else:
        print(f"Unsupported platform: {system_platform}")
        return

    # Determine the path to the script
    script_path = os.path.join(os.path.dirname(__file__), '..', 'inst', install_script)
    if not os.path.exists(script_path):
        print(f"Installer script {install_script} not found at: {script_path}")
        return

    # Execute the script
    try:
        print(f"Executing {install_script} for {system_platform}...")
        subprocess.run(command + [script_path], check=True)
        print(f"{install_script} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing the script: {e}")


if __name__ == "__main__":
    install()
