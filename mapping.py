import pandas as pd

class DataFrameColumnRenamer:
    def __init__(self, df_clean, df_stan):
        """
        Initialize the DataFrameColumnRenamer class.

        Parameters:
        - df_clean (DataFrame): The DataFrame with cleaned data.
        - df_stan (DataFrame): The DataFrame with standard column names.
        """
        self.df_clean = df_clean
        self.df_stan = df_stan

    def exchange_keys_values(self):
        """
        Exchange keys and values in the standard DataFrame to create a mapping.

        Returns:
        - dict: A dictionary mapping standard column names to cleaned column names.
        """
        # Convert df_stan to a dictionary
        data_dict = self.df_stan.to_dict(orient='records')[0]

        # Exchange keys and values in the dictionary
        flipped_dict = {v: k for k, v in data_dict.items()}

        return flipped_dict

    def rename_columns(self):
        """
        Rename columns of the cleaned DataFrame using the standard column names.

        Returns:
        - DataFrame: The cleaned DataFrame with updated column names.
        """
        # Exchange keys and values to create a mapping
        flipped_dict = self.exchange_keys_values()

        # Rename the columns of df_clean using the mapping
        self.df_clean.rename(columns=flipped_dict, inplace=True)

        return self.df_clean

# Example usage:
# data_clean = {
#     'Old Column 1': [1, 2, 3, 4],
#     'Old Column 2': ['A', 'B', 'C', 'D'],
#     'Old Column 3': [9, 10, 11, 12]
# }
# data_stan = {
#     'Standard Column 1': [1],
#     'Standard Column 2': ['A'],
#     'Standard Column 3': [9]
# }
# df_clean = pd.DataFrame(data_clean)
# df_stan = pd.DataFrame(data_stan)

# Create an instance of the class
# renamer = DataFrameColumnRenamer(df_clean, df_stan)

# # Rename columns
# updated_df = renamer.rename_columns()

# # Print the updated DataFrame
# print(updated_df)
