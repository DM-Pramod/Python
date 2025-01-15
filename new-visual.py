import pandas as pd

# Initialize the Final DataFrame
final_df = pd.DataFrame(columns=['column_id', 'col B', 'col C', 'col D', 'col E', 'col F', 'col G', 'col H', 'col I', 'col J'])

# Define the Function to Process Each DataFrame
def process_dataframe(df, mapping):
    # Create a dictionary to rename columns
    rename_dict = {m.split('(')[0]: m.split('(')[1][:-1] for m in mapping}
    # Extract and rename columns
    df_processed = df[list(rename_dict.keys())].rename(columns=rename_dict)
    return df_processed

# List of DataFrames and their corresponding mappings
dataframes = [df1, df2, df3, df4, df5, df6, df7, df8, df9, df10]
mappings = [
    ['id(column_id)', 'col B', 'col C', 'col D', 'col E', 'col F', 'col G'],
    ['ids(column_id)', 'hexa_col(col B)', 'beta_col(col C)', 'other_col(col D)'],
    # Add mappings for other dataframes
]

# Iterate Through Each DataFrame and Merge
for df, mapping in zip(dataframes, mappings):
    processed_df = process_dataframe(df, mapping)
    final_df = final_df.merge(processed_df, on='column_id', how='outer')

# Ensure Uniqueness
final_df = final_df.drop_duplicates(subset='column_id')

# Display the final dataframe
print(final_df)
