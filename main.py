import streamlit as st
import pandas as pd
from flter_columns import ColumnExtractor  # Assuming you have this function
from cleanings import DataCleaner  # Assuming you have this class
from mapping import DataFrameColumnRenamer  # Assuming you have this class
from hardcoded_fields import HardcodeColumns
from calculations import FormulaConverter
import os


import warnings
warnings.filterwarnings('ignore')

class FileUploaderApp:
    def __init__(self):
        self.upload_raw_file = None
        self.upload_standard_file = None
        self.upload_calculations_file = None
        # self.uploaded_file_names = []  # List to store uploaded file names
        # self.uploaded_whole_file_names = []  # List to store whole uploaded file names

    def file_upload(self):
        """
        Display file upload widgets for raw, standard, and calculations files.
        No return value.
        """
        self.upload_raw_file = st.file_uploader("Upload raw file", type="csv")
        self.upload_standard_file = st.file_uploader("Upload standard file", type="csv")
        self.upload_calculations_file = st.file_uploader("Upload calculations file", type="csv")

    def run(self):
        """
        Main execution function to run the Streamlit app.
        No return value.
        """
        st.title("CSV File Uploader and Processor")

        self.file_upload()
        submitted = st.button("Submit")

        if submitted:
            raw_df = None
            standard_df = None
            calculations_df = None

            # Read uploaded raw file if available
            if self.upload_raw_file:
                raw_df = pd.read_csv(self.upload_raw_file)
                st.write("Raw Data:")
                st.write(raw_df)
                st.write(len(raw_df.columns))

            # Read uploaded standard file if available
            if self.upload_standard_file:
                standard_df = pd.read_csv(self.upload_standard_file)
                st.write("Standard Data:")
                st.write(standard_df)
                st.write(len(standard_df.columns))

            # Read uploaded calculations file if available
            if self.upload_calculations_file:
                calculations_df = pd.read_csv(self.upload_calculations_file)
                st.write("Calculations Data:")
                st.write(calculations_df)

            # Initialize the ColumnExtractor class to get useful columns
            extractor = ColumnExtractor(raw_df, standard_df, calculations_df)
            useful_columns_data, filtered_dict = extractor.get_useful_columns(self.upload_raw_file.name)

            st.write("Useful Columns:")
            st.write(useful_columns_data)
            st.write(len(useful_columns_data.columns))




            # Initialize the DataCleaner class to clean data
            cleaner = DataCleaner(useful_columns_data)

            # Define conversion rates for currencies (example)
            conversion_rates = {'$': 'USD', '€': 'EUR', '£': 'GBP'}

            # Clean data using the defined conversion rates
            cleaned_columns_data = cleaner.clean_data(conversion_rates)

            st.write("Cleaned Columns:")
            st.write(cleaned_columns_data)
            st.write(len(cleaned_columns_data.columns))

            # cleaned_columns_data.to_csv('mapped_data.csv', index=False)
            # with open('cleaned_data.csv', 'rb') as f:
            #     data = f.read()

            # if st.button('Download CSV'):
            #     csv_data = data
            #     st.download_button(label='Download CSV', data=csv_data, key='download_button')




            # api_key = os.getenv('OPENAI_API_KEY')
            converter = FormulaConverter()
            formulas_dict = converter.convert(calculations_df)

            handler = HardcodeColumns()
            calculated_df = handler.process_values(filtered_dict, cleaned_columns_data, formulas_dict)

            st.write("Final Dataframe:")
            st.write(calculated_df)
            st.write(len(calculated_df.columns))

            # calculated_df.to_csv('calculated_data.csv', index=False)
            # with open('calculated_data.csv', 'rb') as f:
            #     data = f.read()

            # if st.button('Download CSV'):
            #     csv_data = data
            #     st.download_button(label='Download CSV', data=csv_data, key='download_button')

            # Initialize the DataFrameColumnRenamer class to rename columns
            mapper = DataFrameColumnRenamer(calculated_df, standard_df)
            df_mapped = mapper.rename_columns()

            st.write("Mapped Dataframe:")
            st.write(df_mapped)
            st.write(len(df_mapped.columns))

            df_mapped.to_csv('calculated_data.csv', index=False)
            with open('calculated_data.csv', 'rb') as f:
                data = f.read()

            if st.button('Download CSV'):
                csv_data = data
                st.download_button(label='Download CSV', data=csv_data, key='download_button')

        


            

if __name__ == "__main__":
    app = FileUploaderApp()
    app.run()
