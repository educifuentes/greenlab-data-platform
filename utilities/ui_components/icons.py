ICONS = {
    # branding
    "logo": "energy_program_saving",
    
    # tables
    "person": "person",
    "hogares": "family_group",
    "bases_ccu": "assignment",
    "contratos": "contract",
    
    # VALIDATIONS   
    "check": "check_box",
    "warning": "warning",
    "close": "close",
    
    # pages
    "documentation": "article",
    "metrics": "calculate",
    "not_apply": "circle",
    "query": "query_stats",
    "catalog": "view_list",
    "dashboard": "dashboard",
    "search": "search",
    "layers": "layers_clear",
    "settings": "settings_input_component",
    "database": "database",
    # dev data build
    "staging": "steppers",
    "intermediate": "factory",
    "finals": "rocket",
    "bi_tables": "bar_chart_4_bars"
}

def render_icon(icon_key: str) -> str:
    """
    Returns the streamlit material icon format for a given key.
    """
    icon_name = ICONS.get(icon_key, "help")
    return f":material/{icon_name}:"


# icons from https://fonts.google.com/icons