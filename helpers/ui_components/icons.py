ICONS = {
    # branding
    "logo": "energy_program_saving",
    # core pages
    "home": "home",
    "catalog": "view_list",
    "documentation": "article",
    "guides": "help_center",
    # validations   
    "check": "check_box",
    "warning": "warning",
    "close": "close",
    # schemas
    # energia
    "contaminantes": "co2",
    "censos": "family_group",
    # data pipeline stages
    "sources": "database_upload",
    "staging": "steppers",
    "intermediate": "factory",
    "marts": "rocket",
    "exposures": "bar_chart_4_bars",
    # misc
    "dashboard": "dashboard",
    "search": "search",
    "layers": "layers_clear",
    "settings": "settings_input_component",
    "database": "database",
    "projects": "rocket",
    "metrics": "calculate",
}

def render_icon(icon_key: str) -> str:
    """
    Returns the streamlit material icon format for a given key.
    """
    icon_name = ICONS.get(icon_key, "help")
    return f":material/{icon_name}:"


# icons from https://fonts.google.com/icons