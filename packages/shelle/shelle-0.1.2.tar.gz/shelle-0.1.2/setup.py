import os
import platform
import subprocess
from setuptools import setup, find_packages  # Import setuptools here
import setuptools.command.install  # Ensure setuptools.command.install is imported

# Post-install hook
def run_install_scripts():
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

    script_path = os.path.join(os.path.dirname(__file__), 'inst', install_script)
    if not os.path.exists(script_path):
        print(f"Installer script {install_script} not found.")
        return

    try:
        print(f"Executing {install_script} for {system_platform}...")
        subprocess.run(command + [script_path], check=True)
        print(f"{install_script} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing the script: {e}")

# Custom command for post-install
class CustomInstallCommand(setuptools.command.install.install):
    def run(self):
        setuptools.command.install.install.run(self)  # Call the original install logic
        run_install_scripts()  # Call the post-install hook

# Setup configuration
setup(
    name='shelle',
    version='0.1.2',
    description='Terminal Assisstant',
    author='Hkcode',
    author_email='sissokoadel057@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],  # Any dependencies your package needs
    cmdclass={
        'install': CustomInstallCommand,  # Use the custom install command
    },
    entry_points={
        'console_scripts': [
            'combot-installer = combot_installer.__main__:install',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
    ],
)
