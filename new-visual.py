import json

def dataframe_to_json(df, columns, keys, output_file):
    if len(columns) != len(keys):
        raise ValueError("The number of columns must match the number of keys.")

    selected_columns = df[columns]
    
    unique_rows = selected_columns.drop_duplicates()
    
    json_list = []
    for index, row in unique_rows.iterrows():
        json_dict = {keys[i]: row[columns[i]] for i in range(len(columns))}
        json_list.append(json_dict)
    
    with open(output_file, 'w') as json_file:
        json.dump(json_list, json_file, indent=4)

    
columns = ['commodity', 'category', 'source', 'market']
keys = ['name', 'product_type', 'source', 'market']

output_file = 'commodity.json'

dataframe_to_json(purchased_commodity_df, columns, keys, output_file)


import json
import pandas as pd
import re

def parse_id_column(id_value):
    try:
        parts = id_value.split('+')
        v_id = parts[0]
        bt = parts[1]
        
        # Extract v_vol using regex to handle cases like "35kt@st"
        v_vol_match = re.search(r'\d+k', parts[2])
        v_vol = v_vol_match.group(0) if v_vol_match else None
        
        # Extract place by removing the volume part and any surrounding parentheses
        place = re.sub(r'{{{{\(.*\)}}}}', '', parts[2]).strip()
        
        return {
            'v_id': v_id,
            'bt': bt,
            'v_vol': v_vol,
            'place': place
        }
    except IndexError:
        raise ValueError(f"ID format is incorrect: {id_value}")

def dataframes_to_json(dataframes, output_file):
    # Extract the 'id' column from each dataframe
    id_columns = [df[['id']] for df in dataframes]
    
    # Concatenate all id columns into a single dataframe
    concatenated_df = pd.concat(id_columns, ignore_index=True)
    
    # Drop duplicates to ensure uniqueness
    unique_ids = concatenated_df.drop_duplicates()
    
    # Parse the id column to extract required values
    json_list = []
    for index, row in unique_ids.iterrows():
        parsed_data = parse_id_column(row['id'])
        json_list.append(parsed_data)
    
    # Write the result to a JSON file
    with open(output_file, 'w') as json_file:
        json.dump(json_list, json_file, indent=4)

# Example usage with multiple dataframes
dataframes = [df1, df2, df3, df4, df5, df6, df7]
output_file = 'commodity.json'
dataframes_to_json(dataframes, output_file)

_vessel_inventory_df['vessel_market'] = _vessel_inventory_df['vessel_index'].str.split(pat='+',n=2).str[2]
