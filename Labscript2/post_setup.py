import subprocess
import sys
import os
import yaml

# Define the environment YAML file path
ENV_YAML = "environment.yml"


def run_command(command, shell=True):
    """Helper function to run shell commands and handle errors."""
    try:
        subprocess.run(command, check=True, shell=shell)
    except subprocess.CalledProcessError as e:
        print(f"Error: Command '{command}' failed with error: {e}")
        sys.exit(1)


def get_expected_env_name():
    """Extract the environment name from the environment.yml file."""
    try:
        with open(ENV_YAML, "r") as file:
            env_data = yaml.safe_load(file)
            env_name = env_data.get("name")
            if not env_name:
                print(f"Error: No 'name' field found in '{ENV_YAML}'.")
                sys.exit(1)
            return env_name
    except FileNotFoundError:
        print(f"Error: '{ENV_YAML}' file not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Failed to parse '{ENV_YAML}' - {e}")
        sys.exit(1)


def verify_conda_env(expected_env_name):
    """Verify that the script is running inside the expected Conda environment."""
    conda_prefix = os.environ.get("CONDA_PREFIX", None)

    if not conda_prefix:
        print("Error: This script is not running inside a Conda environment.")
        sys.exit(1)

    current_env_name = os.path.basename(conda_prefix)
    if current_env_name != expected_env_name:
        print(
            f"Error: This script is running in the '{current_env_name}' environment instead of '{expected_env_name}'.")
        sys.exit(1)

    print(f"Running inside the correct Conda environment: '{current_env_name}'.")


def main():
    # Get the expected environment name from the YAML file
    expected_env_name = get_expected_env_name()

    # Verify that we are in the correct Conda environment
    verify_conda_env(expected_env_name)

    # Upgrade pip, setuptools, and wheel
    print("Upgrading pip, setuptools, and wheel...")
    run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])

    # Run labscript profile creation
    print("Running 'labscript-profile-create'...")
    run_command("labscript-profile-create")

    # Install desktop apps
    print("Installing desktop apps...")
    run_command("desktop-app install blacs lyse runmanager runviewer")

    print("Post-setup steps completed successfully.")


if __name__ == "__main__":
    main()
