def generate_mermaid(final_df, all_models_dict):
    """
    Recursively builds the Mermaid flow chart starting from a final model.
    Includes styling for different layers (staging, intermediate, final).
    """
    nodes = set()
    edges = set()

    # Styles definition
    styles = [
        "    classDef staging fill:#d4edda,stroke:#28a745,color:#155724",
        "    classDef intermediate fill:#cfe2ff,stroke:#0d6efd,color:#084298",
        "    classDef final fill:#fff3cd,stroke:#ffc107,color:#856404"
    ]

    def trace(name):
        if name not in all_models_dict:
            nodes.add(f'    {name}["{name} (External)"]')
            return

        df = all_models_dict[name]
        sources = df.attrs.get('sources', [])

        # Determine Class
        if name.startswith("stg_"): cls = "staging"
        elif name.startswith("int_"): cls = "intermediate"
        else: cls = "final"

        nodes.add(f'    {name}["{name}"]:::{cls}')

        for src in sources:
            edges.add(f'    {src} --> {name}')
            trace(src)

    initial_name = final_df.attrs.get('model_name', 'Final_Output')
    
    # Ensure final_df is in all_models_dict so trace can find it 
    if initial_name not in all_models_dict:
        all_models_dict[initial_name] = final_df
        
    trace(initial_name)

    mermaid_lines = ["graph TD"] + styles + list(nodes) + list(edges)
    return "\n".join(mermaid_lines)