import pandas as pd

def load_complaints_data():
    # Load the Excel file
    excel_file_path = '/content/insurancedata/complaints_data.xlsx'

    # Load all three sheets into separate DataFrames
    twitter_df = pd.read_excel(excel_file_path, sheet_name='Twitter')
    forums_df = pd.read_excel(excel_file_path, sheet_name='Forums')
    trustpilot_df = pd.read_excel(excel_file_path, sheet_name='Trustpilot')

    # Add 'Site Name' column to each DataFrame
    twitter_df['Site Name'] = 'Twitter'
   
    # Concatenate all the DataFrames into one
    merged_df = pd.concat([twitter_df, forums_df, trustpilot_df])

    # Optional: Reset the index if you want a continuous index
    merged_df.reset_index(drop=True, inplace=True)

    # Filter rows containing 'insurance' in the 'Mention Content' column
    filtered_df = merged_df[merged_df['Mention Content'].str.contains('insurance', case=False, na=False)]

    # Columns to fill with 'NA'
    col_to_fill = ['Title', 'Site Name', 'Sentiment', 'Media Type']

    # Replace NaN values with appropriate defaults
    filtered_df['Star Rating'].fillna(0.00, inplace=True)
    filtered_df[col_to_fill] = filtered_df[col_to_fill].fillna('NA')
    filtered_df['Country'].fillna('United Kingdom', inplace=True)

    # Replace 'Not available' with 'United Kingdom' in the 'Country' column
    filtered_df['Country'] = filtered_df['Country'].replace('Not available', 'United Kingdom')

    return filtered_df

# Usage example
df = load_complaints_data()
print(df)