from helpers.constants.icons import ICONS

def render_icon(icon_key: str) -> str:
    """
    Returns the streamlit material icon format for a given key.
    """
    icon_name = ICONS.get(icon_key, "help")
    return f":material/{icon_name}:"

# icons from https://fonts.google.com/icons
