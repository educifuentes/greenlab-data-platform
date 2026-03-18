import inspect
import ast
import os

def set_lineage(df):
    """
    Stamps the dataframe with its name and its parent sources by introspecting the caller's file.
    It reads the caller's imports to find any imported models and categorizes them into layers.
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
        
    df.attrs['model_name'] = model_name
    
    # 3. Parse the caller file to find imports from 'models'
    sources_list = []
    models_dict = {}
    
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
                        elif src.startswith('fct_') or src.startswith('final_'):
                            layer = 'final'
                        else:
                            continue # Ignore non-model imports
                            
                        if layer not in models_dict:
                            models_dict[layer] = []
                        if src not in models_dict[layer]:
                            models_dict[layer].append(src)
                        if src not in sources_list:
                            sources_list.append(src)
    except Exception:
        pass # Fail gracefully if file cannot be parsed
        
    df.attrs['sources'] = sources_list
    df.attrs['models'] = models_dict
    
    return df