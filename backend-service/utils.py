import json
import pandas as pd

def flatten_json(data, parent_key='', sep='_'):
    """Recursively flattens a nested JSON object into a single-level dictionary."""
    items = {}
    if isinstance(data, dict):
        for key, value in data.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            if isinstance(value, dict):
                items.update(flatten_json(value, new_key, sep=sep))
            elif isinstance(value, list):
                if all(isinstance(i, dict) for i in value):  
                    for i, sub_value in enumerate(value):
                        items.update(flatten_json(sub_value, f"{new_key}_{i}", sep=sep))
                else:  
                    items[new_key] = ', '.join(map(str, value)) if value else '*'
            else:
                items[new_key] = value if value is not None else '*'
    return items

def convert_json_to_csv(json_data):
    """Converts JSON data into a structured CSV-compatible format."""
    expanded_data = []

    if isinstance(json_data, dict):
        if all(isinstance(v, list) for v in json_data.values()):
            if not any(json_data.values()):
                return None
            
            max_length = max(len(v) for v in json_data.values())

            for idx in range(max_length):
                row = {}
                for key, value in json_data.items():
                    if isinstance(value, list) and len(value) > idx:
                        item = value[idx]
                        row.update(flatten_json(item, key) if isinstance(item, dict) else {key: item})
                    else:
                        row[key] = '*'
                expanded_data.append(row)
        else:
            expanded_data.append(flatten_json(json_data))  

    elif isinstance(json_data, list):
        if all(isinstance(entry, dict) for entry in json_data):
            expanded_data = [flatten_json(entry) for entry in json_data]
        else:
            return None

    df = pd.DataFrame(expanded_data).fillna('*')

    return df
