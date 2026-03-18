Pandas-dbt Lineage Metadata System"
Role: Senior Data Architect & Streamlit Expert.

Context: I am building a custom ELT platform using Python (Pandas) and Streamlit that mimics the dbt (data build tool) architecture. My data is processed through three layers: staging, intermediate, and final. Each model is a standalone .py file that returns a DataFrame.

Objective: Implement a Metadata Embedding Strategy using Pandas df.attrs to track data lineage (parent-child relationships) and visualize this lineage dynamically in Streamlit using Mermaid.js.

Requirements:
Metadata Strategy: Use the df.attrs dictionary to "stamp" every DataFrame. Every model must store its own model*name and a list of its sources (parent model names).
Component 1: Lineage Helper (helpers/set_lineage.py)
Create a function set_lineage(df, model_name, sources=None) that updates df.attrs.
Ensure it handles cases where sources might be a single string or a list.
Component 2: Mermaid Generator (helpers/widgets/generate_mermaid.py)
Implement a function generate_mermaid(final_df, all_models_dict).
This function must recursively trace back through the sources stored in .attrs.
Assign different Mermaid Styles (CSS) based on the layer prefix:
stg* (Staging): Green
int* (Intermediate): Blue
fct* / final\_ (Final): Gold
Component 3: UI Renderer (helpers/ui_components/render_lineage.py)
A Streamlit function that takes the final_df and the global models_registry.

It should render the Mermaid diagram and provide an expander to view the raw metadata.
Project Structure:
Provide the implementation assuming this folder structure:

├── models/
│ ├── staging/ # e.g., stg_orders.py
│ ├── intermediate/ # e.g., int_orders_joined.py
│ └── final/ # e.g., fct_monthly_sales.py
├── helpers/
│ ├── set_lineage.py
│ ├── widgets/
│ │ └── generate_mermaid.py
│ └── ui_components/
│ └── render_lineage.py
└── app.py

Recommended Mermaid Logic Enhancements
To make your flowchart look professional for "Data Governance," I suggest adding subgraphs or node styling to the generate_mermaid logic so the layers are visually distinct.

Proposed Implementation for generate_mermaid.py
Since you have the base logic, here is the "polished" version with styling included:

def generate_mermaid(final_df, all_models_dict):
nodes = set()
edges = set()

    # Styles definition
    styles = [
        "classDef staging fill:#d4edda,stroke:#28a745,color:#155724",
        "classDef intermediate fill:#cfe2ff,stroke:#0d6efd,color:#084298",
        "classDef final fill:#fff3cd,stroke:#ffc107,color:#856404"
    ]

    def trace(name):
        if name not in all_models_dict:
            nodes.add(f'{name}["{name} (External)"]')
            return

        df = all_models_dict[name]
        sources = df.attrs.get('sources', [])

        # Determine Class
        if name.startswith("stg_"): cls = "staging"
        elif name.startswith("int_"): cls = "intermediate"
        else: cls = "final"

        nodes.add(f'{name}["{name}"]::: {cls}')

        for src in sources:
            edges.add(f'{src} --> {name}')
            trace(src)

    initial_name = final_df.attrs.get('model_name', 'Final_Output')
    trace(initial_name)

    mermaid_lines = ["graph TD"] + styles + list(nodes) + list(edges)
    return "\n".join(mermaid_lines)
