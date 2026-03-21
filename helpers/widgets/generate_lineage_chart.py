def generate_lineage_chart(df):
    """
    Builds the Mermaid flow chart starting from a model's metadata.
    Uses subgraphs to visually separate layers.
    """
    model_name = df.attrs.get('model_name', 'Unknown')
    models_dict = df.attrs.get('models', {})

    def get_layer(name):
        if name.startswith("stg_"): return "staging"
        elif name.startswith("int_"): return "intermediate"
        elif name.startswith("fct_"): return "marts"
        elif name.startswith("exp_"): return "exposures"
        return "source"

    # Collect all nodes by layer
    layers = {"source": set(), "staging": set(), "intermediate": set(), "marts": set(), "exposures": set()}
    
    main_layer = get_layer(model_name)
    if main_layer in layers:
        layers[main_layer].add(model_name)
        
    for layer_name, sources in models_dict.items():
        for src in sources:
            src_layer = get_layer(src)
            if src_layer in layers:
                layers[src_layer].add(src)

    mermaid_lines = ["graph LR"]
    
    # Generate Subgraphs dynamically
    layer_display_names = {
        "source": "Source",
        "staging": "Staging",
        "intermediate": "Intermediate",
        "marts": "Marts",
        "exposures": "Exposures"
    }

    for layer_key in layer_display_names.keys():
        if layers[layer_key]:
            mermaid_lines.append(f"    subgraph {layer_key.capitalize()}_Layer [{layer_display_names[layer_key]}]")
            for node in sorted(list(layers[layer_key])):
                mermaid_lines.append(f'        {node}["{node}"]')
            mermaid_lines.append("    end")

    mermaid_lines.append("")
    mermaid_lines.append("    %% Lineage Connections")
    ordered_layers = ["source", "staging", "intermediate", "marts", "exposures"]
    populated_layers = [lyr for lyr in ordered_layers if layers.get(lyr)]
    
    for i in range(len(populated_layers) - 1):
        current_layer = populated_layers[i]
        next_layer = populated_layers[i + 1]
        for src in sorted(list(layers[current_layer])):
            for tgt in sorted(list(layers[next_layer])):
                mermaid_lines.append(f"    {src} --> {tgt}")

    mermaid_lines.append("")
    mermaid_lines.append("    %% Styling")
    
    # Modern minimal node styles
    mermaid_lines.append("    classDef source fill:transparent,stroke:#5c6bc0,stroke-width:1.5px,rx:6px,ry:6px,color:#5c6bc0;")
    mermaid_lines.append("    classDef staging fill:transparent,stroke:#2e7d32,stroke-width:1.5px,rx:6px,ry:6px,color:#2e7d32;")
    mermaid_lines.append("    classDef intermediate fill:transparent,stroke:#1565c0,stroke-width:1.5px,rx:6px,ry:6px,color:#1565c0;")
    mermaid_lines.append("    classDef marts fill:transparent,stroke:#f57f17,stroke-width:1.5px,rx:6px,ry:6px,color:#f57f17;")
    mermaid_lines.append("    classDef exposures fill:transparent,stroke:#e91e63,stroke-width:1.5px,rx:6px,ry:6px,color:#e91e63;")
    
    # Minimal subgraph styles
    for layer_key in layer_display_names.keys():
        if layers[layer_key]:
            mermaid_lines.append(f"    style {layer_key.capitalize()}_Layer fill:transparent,stroke:#cfd8dc,stroke-width:1px,stroke-dasharray: 4 4,color:#78909c;")

    # Apply classes
    for layer_key in layer_display_names.keys():
        if layers[layer_key]:
            mermaid_lines.append(f"    class {','.join(layers[layer_key])} {layer_key};")

    mermaid_lines.append("")
    mermaid_lines.append("    %% Highlight Current Model")
    mermaid_lines.append(f"    style {model_name} stroke-width:4px,stroke:#333333,color:#333333,fill:#fff59d;")

    return "\n".join(mermaid_lines)