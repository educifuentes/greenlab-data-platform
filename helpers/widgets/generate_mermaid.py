def generate_mermaid(df):
    """
    Builds the Mermaid flow chart starting from a model's metadata.
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

    model_name = df.attrs.get('model_name', 'Unknown')
    sources = df.attrs.get('sources', [])

    def get_class(name):
        if name.startswith("stg_"): return "staging"
        elif name.startswith("int_"): return "intermediate"
        return "final"

    main_cls = get_class(model_name)
    nodes.add(f'    {model_name}["{model_name}"]:::{main_cls}')

    for src in sources:
        src_cls = get_class(src)
        nodes.add(f'    {src}["{src}"]:::{src_cls}')
        edges.add(f'    {src} --> {model_name}')

    mermaid_lines = ["graph TD"] + styles + list(nodes) + list(edges)
    return "\n".join(mermaid_lines)