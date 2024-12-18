import json
import os
from pathlib import Path

config_dir = Path.home() / ".prompt_llm"
CURRENT_CONFIG_FILE = 'config.json'

def get_profile_path(profile: str=''):
    if profile:
        return config_dir / profile if '.json' in profile else config_dir / (profile + '.json')
    else:
        return config_dir / CURRENT_CONFIG_FILE

def add_to_config(key:str, value: str):
    """Set config such as api_key"""
    # Ensure the directory exists
    config_dir.mkdir(parents=True, exist_ok=True)

    # Load existing config if it exists
    if get_profile_path().exists():
        with open(get_profile_path(), "r") as file:
            config_data = json.load(file)
    else:
        config_data = {}

    # Add or update the API key
    config_data[key] = value

    # Save the updated config
    with open(get_profile_path(), "w") as file:
        json.dump(config_data, file, indent=4)

def remove_from_config(key:str):
    """Remove config such as api_key"""
    # Ensure the directory exists
    config_dir.mkdir(parents=True, exist_ok=True)

    # Load existing config if it exists
    if get_profile_path().exists():
        with open(get_profile_path(), "r") as file:
            config_data = json.load(file)
            if key in config_data:
                del config_data[key]

    # Save the updated config
    with open(get_profile_path(), "w") as file:
        json.dump(config_data, file, indent=4)

def remove_profile(profile: str):
    """Remove config such as api_key"""
    os.remove(get_profile_path(profile))
    return True

def load_config(profile: str = ''):
    # Load config from profile
    config_file = get_profile_path(profile)
    app_config = {}
    if config_file.exists():
        with open(config_file, "r") as file:
            app_config = json.load(file)

    return app_config

def save_config_to(profile: str):
    # Save a config to a profile
    current_config_file = get_profile_path() # default current profile
    if current_config_file.exists():
        with open(current_config_file, "r") as file:
            app_config = json.load(file)
            new_config_file = get_profile_path(profile)
            with open(new_config_file, 'w') as new_file:
                new_file.write(json.dumps(app_config, sort_keys=True, indent=4))
        return True
    
    return False

def load_config_from(profile: str):
    # Save a config to a profile
    new_config_file = get_profile_path(profile)
    if new_config_file.exists():
        with open(new_config_file, "r") as file:
            app_config = json.load(file)
            current_config_file = get_profile_path()
            with open(current_config_file, 'w') as new_file:
                new_file.write(json.dumps(app_config, sort_keys=True, indent=4))
        return True
    return False

def load_profiles():
    return [profile.replace(".json", "") for profile in os.listdir(config_dir)]

def print_response(response, provider):

    print(f"{provider}:\n---\n")

    if hasattr(response, "content"):
        print(response.content)