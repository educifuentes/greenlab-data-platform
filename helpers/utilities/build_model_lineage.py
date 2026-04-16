import inspect
import ast
import os

def build_model_lineage():
    """
    Scans the caller's file to extract the model name and imported models.
    """
    # 1. Get the caller's frame to find the filename
    stack = inspect.stack()
    if len(stack) > 1:
        caller_filename = stack[1].filename
    else:
        caller_filename = __file__
        
    # 2. Extract model name from filename (removes leading underscores if any)
    base_name = os.path.basename(caller_filename)
    model_name, _ = os.path.splitext(base_name)
    if model_name.startswith('_'):
        model_name = model_name[1:]
        
    models_dict = {}

    # 3. Concatenate lineage from previous dataframes in the caller's local variables
    try:
        if len(stack) > 1:
            caller_frame = stack[1].frame
            for var_name, var_val in list(caller_frame.f_locals.items()):
                prev_models = None
                
                # Check for DataFrame-like objects with .attrs
                if hasattr(var_val, 'attrs') and isinstance(var_val.attrs, dict):
                    prev_models = var_val.attrs.get("models", {})
                
                # Also check for simple dicts that have a 'models' dict (like saved attrs)
                elif isinstance(var_val, dict) and "models" in var_val and isinstance(var_val["models"], dict):
                    prev_models = var_val["models"]
                    
                if isinstance(prev_models, dict):
                    for prev_layer, prev_list in prev_models.items():
                        if prev_layer not in models_dict:
                            models_dict[prev_layer] = []
                        for m_name in prev_list:
                            if m_name not in models_dict[prev_layer]:
                                models_dict[prev_layer].append(m_name)
    except Exception:
        pass

    # 4. Parse the caller file to find direct imports from 'models'
    try:
        with open(caller_filename, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=caller_filename)
            
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module and node.module.startswith('models'):
                    for alias in node.names:
                        src = alias.name
                        
                        # Determine layer
                        if src.startswith('stg_'):
                            layer = 'staging'
                        elif src.startswith('int_'):
                            layer = 'intermediate'
                        elif src.startswith('fct_') or src.startswith('dim_'):
                            layer = 'marts'
                        elif src.startswith('exp_'):
                            layer = 'exposures'
                        else:
                            continue # Ignore non-model imports
                            
                        if layer not in models_dict:
                            models_dict[layer] = []
                        if src not in models_dict[layer]:
                            models_dict[layer].append(src)
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id == 'load_source_dataframe':
                        if node.args:
                            arg0 = node.args[0]
                            if isinstance(arg0, ast.Constant) and isinstance(arg0.value, str):
                                src_name = arg0.value
                            elif hasattr(ast, 'Str') and isinstance(arg0, getattr(ast, 'Str')):
                                src_name = arg0.s
                            else:
                                continue
                                
                            layer = 'source'
                            if layer not in models_dict:
                                models_dict[layer] = []
                            if src_name not in models_dict[layer]:
                                models_dict[layer].append(src_name)
                    elif node.func.id == 'get_source_metadata':
                        if len(node.args) >= 2:
                            arg0 = node.args[0]
                            arg1 = node.args[1]
                            
                            table_name = None
                            if isinstance(arg0, ast.Constant) and isinstance(arg0.value, str):
                                table_name = arg0.value
                            elif hasattr(ast, 'Str') and isinstance(arg0, getattr(ast, 'Str')):
                                table_name = arg0.s
                                
                            yaml_path = None
                            if isinstance(arg1, ast.Constant) and isinstance(arg1.value, str):
                                yaml_path = arg1.value
                            elif hasattr(ast, 'Str') and isinstance(arg1, getattr(ast, 'Str')):
                                yaml_path = arg1.s
                                
                            if table_name and yaml_path:
                                try:
                                    import yaml
                                    if not os.path.isabs(yaml_path):
                                        proj_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                                        abs_yaml_path = os.path.join(proj_root, yaml_path)
                                    else:
                                        abs_yaml_path = yaml_path
                                        
                                    if os.path.exists(abs_yaml_path):
                                        with open(abs_yaml_path, 'r', encoding='utf-8') as yf:
                                            yml_data = yaml.safe_load(yf)
                                            
                                        found_path = None
                                        for source in yml_data.get('sources', []):
                                            for table in source.get('tables', []):
                                                if table.get('name') == table_name:
                                                    found_path = table.get('path')
                                                    break
                                            if found_path:
                                                break
                                                
                                        if found_path:
                                            src_name = os.path.basename(found_path)
                                            layer = 'source'
                                            if layer not in models_dict:
                                                models_dict[layer] = []
                                            if src_name not in models_dict[layer]:
                                                models_dict[layer].append(src_name)
                                except Exception:
                                    pass
    except Exception:
        pass # Fail gracefully if file cannot be parsed
        
    return {
        "model_name": model_name,
        "models": models_dict
    }