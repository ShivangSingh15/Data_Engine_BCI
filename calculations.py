import openai
import os
import pandas as pd
import re
from dotenv import load_dotenv
load_dotenv()


# openai.api_key = os.getenv('OPENAI_API_KEY')


class FormulaConverter:
    def __init__(self):
        load_dotenv()
        self.openai = openai
        # self.openai.api_type="azure"
        # self.openai.api_base=os.getenv("OPENAI_API_ENDPOINT")
        # self.api_version="2023-05-15"
        self.openai.api_key=os.getenv("OPENAI_API_KEY")

        self.prompt = '''
        Convert the below spreadsheet(.csv) expressions into a compile ready python script. Follow the below examples:

        1.  INPUT : IF(or(loan_delinquency_status > 6, loan_current_outstanding_balance=0),"Ineligible","Eligible")

            OUTPUT :  def check_eligibility(row):
                        if row['loan_delinquency_status'] > 6 or row['loan_current_outstanding_balance'] == 0:
                            return "Ineligible"
                        else:
                            return "Eligible"

                    result = df_mapped.apply(check_eligibility, axis=1)

        Understand the above examples and follow the instructions given below:

            1. Remember strictly return only the python executable script as given in examples don't return any other text with it.
            2. Strictly keep the format with regards to the rules on python coding , rules like indentation, initiation, etc.
            3. The format must be the same as the above given few shot examples. 
            4. Return only the converted python code.
            5. You are not helping me if you include any spreadsheet expression in final code.

        '''
        self.ques_prmpt = '''
        Here you go:\n
        '''

    def convert_expression(self, sp_ex):
        """
        Convert a spreadsheet expression to a Python script.

        Args:
            sp_ex (str): The spreadsheet expression to convert.

        Returns:
            str: The converted Python script.
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            # engine="gpt-4-32k",
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": self.ques_prmpt + sp_ex}
            ]
        )

        converted_code = response['choices'][0]['message']['content']
        return self.clean_code(converted_code)

    @staticmethod
    def clean_code(code):
        """
        Clean the Python code by removing triple quotes.

        Args:
            code (str): Python code to clean.

        Returns:
            str: Cleaned Python code.
        """
        cleaned_code = re.sub(r'"""|\'\'\'', '', code)
        return cleaned_code

    def convert(self, df):
        """
        Convert expressions from a CSV file and save the results to CSV, JSON, and TXT files.

        Args:
            input_csv_file (str): The input CSV file containing expressions.
            output_csv_file (str): The output CSV file to save the converted data.
            output_json_file (str): The output JSON file to save the converted data.
            output_txt_file (str): The output TXT file to save the converted data.
        """
        df_expr = df['Calculations']
        expressions = df_expr.to_list()

        converted_code = []
        for expr in expressions:
            val = self.convert_expression(expr)
            converted_code.append(val)

        df['Function_code'] = converted_code

        result_dict = df.set_index('Field Name')['Function_code'].to_dict()
        # with open(output_json_file, "w") as fp:
        #     json.dump(result_dict, fp)  # Encode dict into JSON

        # print("Files have been created and written.")
        print(result_dict)
        return result_dict

