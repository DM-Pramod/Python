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
