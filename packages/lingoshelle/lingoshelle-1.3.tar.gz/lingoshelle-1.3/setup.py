import os
import subprocess
from setuptools import setup
from pathlib import Path
from setuptools.command.install import install

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        # Run the standard install process first
        install.run(self)

        # Path to the install.sh script
        script_path = os.path.join(os.path.dirname(__file__), 'inst', 'install.sh')

        # Ensure the script is executable
        if os.path.exists(script_path):
            os.chmod(script_path, 0o755)
            try:
                print("Running install.sh...")
                subprocess.check_call(["bash", script_path])
            except subprocess.CalledProcessError as e:
                print(f"Error running install.sh: {e}")
        else:
            print(f"install.sh not found at {script_path}")


setup(
    name="lingoshelle",
    version="1.3",
    packages=["lingoshelle"],  # updated package name here
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'requests>=2.25.0',       # HTTP library for making requests
        'openai>=0.27.0',         # OpenAI API library
        'python-dotenv>=0.19.0',  # For loading environment variables
        'pyyaml>=5.4.1',          # YAML parser and emitter
        'pyperclip>=1.8.2',       # Clipboard functions
        'termcolor>=1.1.0',       # For colored terminal output
        'colorama>=0.4.4',        # Cross-platform support for colored output
        'aiohttp>=3.7.4',         # Async HTTP client/server framework
        'keyring>=23.2.1',        # For securely accessing API keys
        'urllib3>=1.26.6',        # HTTP library (ensure compatibility with OpenSSL)
    ],

    include_package_data=True,
    cmdclass={
        'install': PostInstallCommand,
    },
    entry_points={
        'console_scripts': [
            'lingoshell=lingoshelle.__main__:lingoshell',  # updated entry point here
        ],
    },
)

