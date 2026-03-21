import toml
import os

CONFIG_PATH = ".streamlit/config.toml"

def get_current_theme():
    """
    Reads the Streamlit config.toml and returns the current theme's base setting.
    Defaults to 'dark' if it can't be read.
    """
    if not os.path.exists(CONFIG_PATH):
        return "dark"
        
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = toml.load(f)
            return config.get("theme", {}).get("base", "dark")
    except Exception:
        return "dark"

def set_theme(theme_name):
    """
    Writes to config.toml to change the theme base. 
    Streamlit will auto-reload when this file changes.
    """
    config = {}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r') as f:
                config = toml.load(f)
        except Exception:
            pass
            
    if "theme" not in config:
        config["theme"] = {}
        
    config["theme"]["base"] = theme_name
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    
    with open(CONFIG_PATH, 'w') as f:
        toml.dump(config, f)
