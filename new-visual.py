import pandas as pd

def FN1(df):
    unique_lists = []
    mapping_dict = {}
    
    for column in df.columns:
        unique_values = df[column].unique()
        unique_lists.append(unique_values.tolist())
        
        value_to_code = {value: code for code, value in enumerate(unique_values)}
        mapping_dict[column] = value_to_code
        
        df[column] = df[column].map(value_to_code)
    
    return unique_lists, mapping_dict


import pandas as pd

def FN2(mapped_dict, unique_lists):
    columns = list(mapped_dict.keys())
    df_reconstructed = pd.DataFrame(columns=columns)
    
    for column, unique_values in zip(columns, unique_lists):
        code_to_value = {code: value for code, value in enumerate(unique_values)}
        df_reconstructed[column] = df_reconstructed[column].map(code_to_value)
    
    return df_reconstructed


# Example DataFrame
data = {
    'A': [1, 2, 3, 1, 2],
    'B': ['x', 'y', 'z', 'x', 'y'],
    'C': [True, False, True, False, True],
    'D': [1.1, 2.2, 3.3, 1.1, 2.2],
    'E': ['foo', 'bar', 'baz', 'foo', 'bar']
}
df1 = pd.DataFrame(data)

# Function FN1
unique_lists, mapping_dict = FN1(df1)

# Function FN2
df_reconstructed = FN2(mapping_dict, unique_lists)
