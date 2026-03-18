def set_lineage(df, model_name, sources=None):
    """
    Stamps the dataframe with its name and its parent sources.
    Handles cases where sources might be a single string or a list.
    """
    df.attrs['model_name'] = model_name
    
    if sources is None:
        df.attrs['sources'] = []
    elif isinstance(sources, str):
        df.attrs['sources'] = [sources]
    else:
        df.attrs['sources'] = list(sources)
        
    return df