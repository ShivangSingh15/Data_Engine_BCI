import pandas as pd
import re
from dateutil import parser

class DataCleaner:
    def __init__(self, df):
        """
        Initialize the DataCleaner class with a DataFrame.

        Parameters:
        - df (DataFrame): The DataFrame to be cleaned.
        """
        self.df = df
        self.currency_symbols = {}

    def detect_currency_columns(self):
        """
        Detect columns with currency symbols ('$€£¥').

        Returns:
        - List of column names with currency symbols.
        """
        currency_columns = []
        for column in self.df.columns:
            if self.df[column].apply(lambda x: re.search(r'[$€£¥]', str(x)) if pd.notnull(x) else False).any():
                currency_columns.append(column)
        return currency_columns

    def detect_columns_with_spaces(self):
        """
        Detect columns with spaces in their names.

        Returns:
        - List of column names with spaces.
        """
        columns_with_spaces = [column for column in self.df.columns if ' ' in column]
        return columns_with_spaces

    def detect_columns_with_percentage(self):
        """
        Detect columns with percentage signs (%).

        Returns:
        - List of column names with percentage signs.
        """
        columns_with_percentage = [col for col in self.df.columns if self.df[col].apply(lambda x: '%' in str(x)).any()]
        return columns_with_percentage

    def detect_date_columns(self):
        """
        Detect columns with names containing "date" (case insensitive).

        Returns:
        - List of column names with "date" in their names.
        """
        date_columns = []
        for column in self.df.columns:
            if 'date' in column.lower():
                date_columns.append(column)
        return date_columns

    def remove_currency_symbols(self, columns_with_currency):
        """
        Remove currency symbols ('$€£¥') from specified columns.

        Parameters:
        - columns_with_currency (list): List of column names with currency symbols.
        """
        for column in columns_with_currency:
            self.df[column] = self.df[column].apply(lambda x: re.sub('[^\d.]', '', str(x)) if pd.notnull(x) else x)
            self.currency_symbols[column] = ''.join(re.findall(r'[$€£¥]', str(self.df[column].iloc[0])))

    def remove_percentage_symbols(self, columns_with_percentage):
        """
        Remove percentage symbols (%) from specified columns.

        Parameters:
        - columns_with_percentage (list): List of column names with percentage signs.
        """
        for column in columns_with_percentage:
            self.df[column] = self.df[column].str.replace('%', '')

    def extract_currency_symbols(self, column_name):
        """
        Extract currency symbols ('$€£¥') from a specified column.

        Parameters:
        - column_name (str): The name of the column containing currency symbols.

        Returns:
        - Series: A Series of extracted currency symbols.
        """
        return self.df[column_name].str.extract(r'([$€£¥])')[0]

    def convert_currency_symbols(self, currency_symbols, conversion_rates):
        """
        Convert currency symbols to currency names using conversion rates.

        Parameters:
        - currency_symbols (Series): A Series of currency symbols.
        - conversion_rates (dict): A dictionary mapping currency symbols to currency names.

        Returns:
        - Series: A Series of converted currency names.
        """
        return currency_symbols.map(conversion_rates)

    def parse_and_format_date(self, date_str):
        """
        Parse and format date strings in a specified format.

        Parameters:
        - date_str (str): The date string to be parsed.

        Returns:
        - str: The parsed and formatted date string in 'YYYY-MM-DD' format.
        """
        try:
            parsed_date = parser.parse(date_str, dayfirst=True, yearfirst=True)
            return parsed_date.strftime('%Y-%m-%d')
        except:
            return date_str

    def remove_extra_spaces(self):
        """
        Remove leading and trailing spaces from column names.
        """
        self.df.columns = self.df.columns.str.strip()

    def clean_data(self, conversion_rates):
        """
        Clean the DataFrame based on detected patterns.

        Parameters:
        - conversion_rates (dict): A dictionary mapping currency symbols to currency names.

        Returns:
        - DataFrame: The cleaned DataFrame.
        """
        currency_columns = self.detect_currency_columns()
        if currency_columns:
            self.df['Currency_Symbol'] = self.extract_currency_symbols(currency_columns[0])
            self.df['Currency_Name'] = self.convert_currency_symbols(self.df['Currency_Symbol'], conversion_rates)
            self.df.drop(['Currency_Symbol'], axis=1, inplace=True)
            self.remove_currency_symbols(currency_columns)

        percentage_columns = self.detect_columns_with_percentage()
        if percentage_columns:
            self.remove_percentage_symbols(percentage_columns)

        date_columns = self.detect_date_columns()
        if date_columns:
            for column in date_columns:
                self.df[column] = self.df[column].apply(self.parse_and_format_date)

        self.remove_extra_spaces()
        cleaned_df = self.df.copy()
        return cleaned_df

# Example usage:
# data = {
#     'Amount_USD': ['$100.00', '€200.50', '$300.75'],
#     'Date': ['11-05-2023', '10/09/2023', '1/09/2023'],
#     '   Column with Spaces   ': [1,  2 , 3],
#     'Column%WithPercentage': ['10%', '20%', '30%']
# }

# df = pd.DataFrame(data)

# # Conversion rates for currency symbols
# conversion_rates = {'$': 'USD', '€': 'EUR', '£': 'GBP'}

# # Create an instance of DataCleaner
# cleaner = DataCleaner(df)

# # Clean the data
# cleaned_df = cleaner.clean_data(conversion_rates)
# print(cleaned_df)
