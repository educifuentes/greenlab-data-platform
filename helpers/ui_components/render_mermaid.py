import streamlit_mermaid as st_mm

def render_mermaid(mermaid_code: str, height: int = 400):
    """
    Renders a Mermaid diagram using the streamlit_mermaid component.
    """
    st_mm.st_mermaid(mermaid_code, height=height)
