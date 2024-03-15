import numpy as np


class HardcodeColumns:


    def process_values(self, data_dict, df_mapped, formulas_dict):
        """
        Process the values in the DataFrame based on the provided dictionary.

        - If a value is 'Calculation', it is replaced with 'WILLDO'.
        - If a value is '-', it is replaced with NaN (null).
        - For other values, they are assigned to all rows for the corresponding column.

        Returns:
        - DataFrame: The DataFrame with updated values.
        """

        for key, value in  data_dict.items():
            if value == 'Calculation':
                try:
                    local_vars = locals()
                    
                    exec(formulas_dict[key], globals(), local_vars)
                    print('try success')
                    # Retrieve the 'result' variable from the local context
                    result = local_vars.get('result', 'N/A')
                    
                    # Assign the result to the DataFrame column
                    df_mapped[key] = result
                except Exception as e:
                    # Handle the exception here, e.g., log the error message
                    print(f"Error for key '{key}': {str(e)}")
                    df_mapped[key] = f"Error for key '{key}': {str(e)}"
            elif value == '-':
                df_mapped[key] = np.nan
            else:
                # Assign the value to all rows for the current key
                df_mapped[key] = value

        return df_mapped
    

