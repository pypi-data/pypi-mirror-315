import os
import subprocess
from setuptools import setup
from setuptools.command.install import install


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
    name="Shelley",
    version="0.1",
    packages=["shelley"],  # updated package name here
    install_requires=[
        # Your dependencies here
    ],
    include_package_data=True,
    cmdclass={
        'install': PostInstallCommand,
    },
    entry_points={
        'console_scripts': [
            'lingoshell=shelley.__main__:lingoshell',  # updated entry point here
        ],
    },
)
