import pandas as pd

def create_mapping_and_unique_lists(df):
    unique_lists = []
    mapping_dict = {}
    
    for col in df.columns:
        unique_values = df[col].unique().tolist()
        unique_lists.append(unique_values)
        
        # Create a mapping for the column
        col_mapping = {value: code for code, value in enumerate(unique_values)}
        mapping_dict[col] = col_mapping
        
        # Replace the original data with the codes
        df[col] = df[col].map(col_mapping)
    
    return unique_lists, mapping_dict

# Example usage
data = {
    'A': [1, 2, 3, 1],
    'B': ['x', 'y', 'x', 'z'],
    'C': [10.1, 10.2, 10.1, 10.3],
    'D': ['a', 'b', 'a', 'c'],
    'E': [True, False, True, True]
}

df1 = pd.DataFrame(data)
unique_lists, mapping_dict = create_mapping_and_unique_lists(df1)

print("Unique Lists:")
for i, lst in enumerate(unique_lists):
    print(f"Column {i+1}: {lst}")

print("\nMapping Dictionary:")
for col, mapping in mapping_dict.items():
    print(f"Column {col}: {mapping}")

print("\nTransformed DataFrame:")
print(df1)
