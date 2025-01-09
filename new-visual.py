import pandas as pd
import json

def dataframe_to_json(df, columns, keys, output_file):
    """
    Convert specified columns of a dataframe to a JSON file with unique rows.

    Parameters:
    df (pd.DataFrame): The input dataframe.
    columns (list): List of columns to pick from the dataframe.
    keys (list): List of keys for the JSON output.
    output_file (str): The name of the output JSON file.
    """
    # Ensure the number of columns matches the number of keys
    if len(columns) != len(keys):
        raise ValueError("The number of columns must match the number of keys.")
    
    # Select the specified columns
    selected_columns = df[columns]
    
    # Remove duplicate rows
    unique_rows = selected_columns.drop_duplicates()
    
    # Convert to JSON format
    json_list = []
    for index, row in unique_rows.iterrows():
        json_dict = {keys[i]: row[columns[i]] for i in range(len(columns))}
        json_list.append(json_dict)
    
    # Save to JSON file
    with open(output_file, 'w') as json_file:
        json.dump(json_list, json_file, indent=4)

# Example usage
if __name__ == "__main__":
    # Sample dataframe
    data = {
        'commodity': ['gold', 'silver', 'gold', 'platinum'],
        'category': ['precious', 'precious', 'precious', 'precious'],
        'source': ['mining', 'mining', 'mining', 'mining'],
        'market': ['global', 'global', 'global', 'global']
    }
    df1 = pd.DataFrame(data)
    
    # Define columns to pick and corresponding JSON keys
    columns = ['commodity', 'category', 'source', 'market']
    keys = ['name', 'product_type', 'source', 'market']
    
    # Output file name
    output_file = 'output.json'
    
    # Call the function
    dataframe_to_json(df1, columns, keys, output_file)
