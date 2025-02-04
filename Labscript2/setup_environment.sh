#!/bin/bash


# Define paths and environment variables
BASE_DIR="labscript-suite"
ENV_YAML="environment.yml"
CUSTOM_ENV_DIR="$BASE_DIR/envs"
POST_SETUP_SCRIPT="post_setup.py"
ENV_NAME=""


# Function to initialize Conda in the script
initialize_conda() {
    if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
        source "$HOME/miniconda3/etc/profile.d/conda.sh"
    elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
        source "$HOME/anaconda3/etc/profile.d/conda.sh"
    else
        echo "Conda initialization script not found. Ensure Conda is installed and available."
        exit 1
    fi
}


# Function to extract environment name from YAML
get_env_name() {
    if [ -f "$ENV_YAML" ]; then
        ENV_NAME=$(grep '^name:' "$ENV_YAML" | awk '{print $2}')
    else
        echo "No '${ENV_YAML}' file found. Cannot proceed."
        exit 1
    fi
}


# Function to set up the environment directory
setup_custom_env_dir() {
    mkdir -p "$CUSTOM_ENV_DIR"
    echo "Created directory: $CUSTOM_ENV_DIR"
}


# Function to create or update the Conda environment
create_or_update_env() {
    echo "Setting up Conda environment in custom directory: $CUSTOM_ENV_DIR"

    if conda env list | grep -q "^${ENV_NAME} "; then
        echo "Conda environment '${ENV_NAME}' already exists. Updating it with new dependencies..."
        conda env update -f "$ENV_YAML" --prune --prefix "$CUSTOM_ENV_DIR/$ENV_NAME"
        echo "Environment updated successfully."
    else
        echo "Conda environment '${ENV_NAME}' not found. Creating a new environment..."
        conda env create -f "$ENV_YAML" --prefix "$CUSTOM_ENV_DIR/$ENV_NAME"
        echo "Environment created successfully."
    fi

    # Activate the environment
    conda activate "$CUSTOM_ENV_DIR/$ENV_NAME"
}


# Function to run post-setup script
run_post_setup_script() {
    if [ -f "$POST_SETUP_SCRIPT" ]; then
        echo "Running post-setup script..."
        python "$POST_SETUP_SCRIPT"
        echo "Post-setup script completed."
    else
        echo "Post-setup script '${POST_SETUP_SCRIPT}' not found. Skipping."
    fi
}


# Main script logic
initialize_conda
get_env_name
setup_custom_env_dir
create_or_update_env
run_post_setup_script

echo "DONE!"
