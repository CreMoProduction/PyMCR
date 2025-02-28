# app.file_handdler.settings_handler.py

import json
import os
import platform
from app.config.config import APP_TITLE



def get_user_settings(default_settings):
    """
    Retrieves user settings from a JSON file in the user's app data directory.

    Args:
        app_name: The name of the application (used for the folder name).
        default_settings: A dictionary containing the default settings.

    Returns:
        A dictionary containing the user settings, or the default settings if no 
        user settings are found.
    """
    app_name = APP_TITLE 
    try:
        if platform.system() == "Windows":
            app_data_dir = os.path.join(os.environ["LOCALAPPDATA"], app_name)
        elif platform.system() == "Darwin":  # macOS
            app_data_dir = os.path.join(os.path.expanduser("~/Library/Application Support"), app_name)
        else:  # Linux or other OS -  You might want to add a suitable path here
            app_data_dir = os.path.join(os.path.expanduser("~/.config"), app_name) # Example Linux path
            print(f"Warning: OS {platform.system()} is not fully supported in current settings path. Using a default Linux path. Please add a specific path for your OS.")

        settings_file_path = os.path.join(app_data_dir, "settings.json")

        if os.path.exists(settings_file_path):
            with open(settings_file_path, "r") as f:
                user_settings = json.load(f)
                # Merge user settings with default settings, giving priority to user settings
                merged_settings = default_settings.copy() # important to avoid modifying the default settings
                merged_settings.update(user_settings)
                return merged_settings
        else:
            return default_settings

    except Exception as e:
        print(f"Error loading settings: {e}")  # Handle potential errors (e.g., JSON decode errors)
        return default_settings

def save_user_settings(settings):
    """
    Saves user settings to a JSON file in the user's app data directory.

    Args:
        app_name: The name of the application (used for the folder name).
        settings: A dictionary containing the settings to save.
    """
    app_name = APP_TITLE  
    try:
        if platform.system() == "Windows":
            app_data_dir = os.path.join(os.environ["LOCALAPPDATA"], app_name)
            #print(app_data_dir)
        elif platform.system() == "Darwin":  # macOS
            app_data_dir = os.path.join(os.path.expanduser("~/Library/Application Support"), app_name)
        else: # Linux or other OS
            app_data_dir = os.path.join(os.path.expanduser("~/.config"), app_name) # Example Linux path
            print(f"Warning: OS {platform.system()} is not fully supported in current settings path. Using a default Linux path. Please add a specific path for your OS.")

        os.makedirs(app_data_dir, exist_ok=True)  # Create directory if it doesn't exist
        settings_file_path = os.path.join(app_data_dir, "settings.json")

        with open(settings_file_path, "w") as f:
            json.dump(settings, f, indent=4)  # Save with indentation for readability

    except Exception as e:
        print(f"Error saving settings: {e}")

def get_user_setting_value(key, default_value=None):
    """
    Retrieves the value of a specific key from the user settings.

    Args:
        key: The key whose value needs to be retrieved.
        default_value: The default value to return if the key is not found.

    Returns:
        The value of the specified key, or the default value if the key is not found.
    """
    default_settings = {}
    user_settings = get_user_settings(default_settings)
    return user_settings.get(key, default_value)

def save_user_setting_value(key, value):
    """
    Saves a specific key-value pair to the user settings.

    Args:
        key: The key to update.
        value: The value to set for the specified key.
    """
    default_settings = {}
    user_settings = get_user_settings(default_settings)
    user_settings[key] = value
    save_user_settings(user_settings)