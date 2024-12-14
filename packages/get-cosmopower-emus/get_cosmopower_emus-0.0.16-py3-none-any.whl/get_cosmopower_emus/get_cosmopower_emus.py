import os
import subprocess

# Define the expected repositories
EXPECTED_REPOS = [
    "lcdm",
    "mnu",
    "mnu-3states",
    "ede",
    "neff",
    "wcdm"
]

# Base URL for the repositories
BASE_URL = "https://github.com/cosmopower-organization/"

def check_repos_in_dir(directory):
    """Check if all expected repositories are present in the directory."""
    return all(os.path.exists(os.path.join(directory, repo)) for repo in EXPECTED_REPOS)

def set_class_sz_data_env(path):
    """Set the PATH_TO_CLASS_SZ_DATA environment variable."""
    os.environ["PATH_TO_CLASS_SZ_DATA"] = path
    # print(f"PATH_TO_CLASS_SZ_DATA is set to {path}")

def delete_pkl_files(directory):
    """Recursively find and delete all .pkl files in the directory."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".pkl"):
                file_path = os.path.join(root, file)
                print(f"Deleting: {file_path}")
                os.remove(file_path)
                
def set_path():
    # Check if PATH_TO_CLASS_SZ_DATA is already set
    path_to_class_sz_data = os.getenv("PATH_TO_CLASS_SZ_DATA")

    if path_to_class_sz_data:
        # Avoid appending 'class_sz_data_directory' multiple times
        if not path_to_class_sz_data.endswith("class_sz_data_directory"):
            path_to_class_sz_data = os.path.join(path_to_class_sz_data, "class_sz_data_directory")
        # print(f"Using PATH_TO_CLASS_SZ_DATA: {path_to_class_sz_data}")

        # Check if the directory exists; if not, fall back to default
        if not os.path.exists(path_to_class_sz_data):
            print(f"Directory {path_to_class_sz_data} does not exist. Falling back to default path.")
            path_to_class_sz_data = None
    else:
        print("PATH_TO_CLASS_SZ_DATA not set. Setting it now...")

    # If no valid path is set or if the path didn't exist, fall back to the default
    if not path_to_class_sz_data:
        home_dir = os.path.expanduser("~")
        path_to_class_sz_data = os.path.join(home_dir, "class_sz_data_directory")
        print(f"Defaulting to: {path_to_class_sz_data}")

    # Now check if the class_sz_data_directory directory exists and contains the expected repositories
    if os.path.exists(path_to_class_sz_data) and check_repos_in_dir(path_to_class_sz_data):
        # print(f"Found class_sz_data_directory directory with all repositories at: {os.path.realpath(path_to_class_sz_data)}")
        
        # Set the environment variable if it's not already set
        current_path = os.getenv("PATH_TO_CLASS_SZ_DATA")
        if current_path != path_to_class_sz_data:
            # print("PATH_TO_CLASS_SZ_DATA is not correctly set. Setting it now...")
            set_class_sz_data_env(path_to_class_sz_data)
        # else:
        #     print("PATH_TO_CLASS_SZ_DATA is already correctly set.")
    else:
        print("--> class_sz_data_directory directory or repositories not found. Cloning repositories in your system!")

        # Create the class_sz_data_directory directory if it doesn't exist
        if not os.path.exists(path_to_class_sz_data):
            os.mkdir(path_to_class_sz_data)

        os.chdir(path_to_class_sz_data)

        # Clone all repositories using EXPECTED_REPOS and BASE_URL
        for repo in EXPECTED_REPOS:
            repo_url = os.path.join(BASE_URL, f"{repo}.git")
            subprocess.run(["git", "clone", repo_url])

        # After cloning, delete all .pkl files
        for repo in EXPECTED_REPOS:
            repo_path = os.path.join(path_to_class_sz_data, repo)
            delete_pkl_files(repo_path)

        # Set the environment variable
        set_class_sz_data_env(path_to_class_sz_data)