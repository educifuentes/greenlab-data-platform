def generate_mermaid(df):
    """
    Builds the Mermaid flow chart starting from a model's metadata.
    Uses subgraphs to visually separate Staging, Intermediate, and Final layers.
    """
    model_name = df.attrs.get('model_name', 'Unknown')
    models_dict = df.attrs.get('models', {})

    def get_layer(name):
        if name.startswith("stg_"): return "staging"
        elif name.startswith("int_"): return "intermediate"
        return "final"

    # Collect all nodes by layer
    layers = {"staging": set(), "intermediate": set(), "final": set()}
    
    main_layer = get_layer(model_name)
    if main_layer in layers:
        layers[main_layer].add(model_name)
        
    for layer_name, sources in models_dict.items():
        for src in sources:
            src_layer = get_layer(src)
            if src_layer in layers:
                layers[src_layer].add(src)

    mermaid_lines = ["graph LR"]
    
    # Subgraph Staging
    if layers["staging"]:
        mermaid_lines.append("    subgraph Staging_Layer [Staging]")
        mermaid_lines.append("        direction TB")
        for node in sorted(list(layers["staging"])):
            mermaid_lines.append(f'        {node}["{node}"]')
        mermaid_lines.append("    end")

    # Subgraph Intermediate
    if layers["intermediate"]:
        mermaid_lines.append("    subgraph Intermediate_Layer [Intermediate]")
        mermaid_lines.append("        direction TB")
        for node in sorted(list(layers["intermediate"])):
            mermaid_lines.append(f'        {node}["{node}"]')
        mermaid_lines.append("    end")

    # Subgraph Final
    if layers["final"]:
        mermaid_lines.append("    subgraph Final_Layer [Final]")
        mermaid_lines.append("        direction TB")
        for node in sorted(list(layers["final"])):
            mermaid_lines.append(f'        {node}["{node}"]')
        mermaid_lines.append("    end")

    mermaid_lines.append("")
    mermaid_lines.append("    %% Lineage Connections")
    for layer_name, sources in models_dict.items():
        for src in sources:
            mermaid_lines.append(f"    {src} --> {model_name}")

    mermaid_lines.append("")
    mermaid_lines.append("    %% Styling")
    
    # Modern minimal node styles (transparent backgrounds, rounded corners)
    mermaid_lines.append("    classDef staging fill:transparent,stroke:#2e7d32,stroke-width:1.5px,rx:6px,ry:6px,color:#2e7d32;")
    mermaid_lines.append("    classDef intermediate fill:transparent,stroke:#1565c0,stroke-width:1.5px,rx:6px,ry:6px,color:#1565c0;")
    mermaid_lines.append("    classDef final fill:transparent,stroke:#f57f17,stroke-width:1.5px,rx:6px,ry:6px,color:#f57f17;")
    
    # Minimal subgraph styles (transparent, dashed borders)
    if layers["staging"]:
        mermaid_lines.append("    style Staging_Layer fill:transparent,stroke:#cfd8dc,stroke-width:1px,stroke-dasharray: 4 4,color:#78909c;")
    if layers["intermediate"]:
        mermaid_lines.append("    style Intermediate_Layer fill:transparent,stroke:#cfd8dc,stroke-width:1px,stroke-dasharray: 4 4,color:#78909c;")
    if layers["final"]:
        mermaid_lines.append("    style Final_Layer fill:transparent,stroke:#cfd8dc,stroke-width:1px,stroke-dasharray: 4 4,color:#78909c;")

    # Apply classes
    if layers["staging"]:
        mermaid_lines.append(f"    class {','.join(layers['staging'])} staging;")
    if layers["intermediate"]:
        mermaid_lines.append(f"    class {','.join(layers['intermediate'])} intermediate;")
    if layers["final"]:
        mermaid_lines.append(f"    class {','.join(layers['final'])} final;")

    return "\n".join(mermaid_lines)