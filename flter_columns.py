import pandas as pd
import math
import logging

class ColumnExtractor:
    def __init__(self, raw_df, stan_df, calc_df):
        """
        Initialize the ColumnExtractor class.

        Args:
            raw_df (DataFrame): The raw data DataFrame.
            stan_df (DataFrame): The standard data DataFrame.
            calc_df (DataFrame): The calculations data DataFrame.
        """
        self.raw_df = raw_df
        self.stan_df = stan_df
        self.calc_df = calc_df
        # self.file_name = file_name

    def get_useful_columns(self, file_name):
        """
        Get useful columns from the raw data using the standard and calculation files.

        Returns:
            DataFrame: A DataFrame containing the useful columns.
        """
        barlowmarshall_column_names = [
            "Borrower",
            "Date Of Report",
            "Advance B/F",
            "Fixed Fee B/F",
            "Total Client Receipts During Period",
            "Client Share",
            "BM Repayments",
            "Principal Repayments",
            "Fixed Fee Repayments",
            "Cumilative BM Repayments",
            "Of Which Principal",
            "Of Which Fixed Fee",
            "Principle Outstanding",
            "Fixed Fee Outstanding",
            "BM Principle Contribution Outstanding",
            "Advance Date",
            "Advance Made",
            "Fixed Fee",
            "Repayment Due",
            "Advance Rate",
            "Split Amount (<12 months)",
            "Split Amount (>12 months)",
            "Minimum Monthly Revenue",
            "Loan Status",
            "Sector",
            "Renewal Number",
            "Default Date",
            "Default Amount"
        ]


        carmoola_column_names = [
            "LOAN ID",
            "OUTSTANDING PRINCIPAL BALANCE (£)",
            "LOAN AMOUNT (£)",
            "ORIGINAL DURATION OF LOAN",
            "NUMBER OF DAYS IN ARREARS",
            "PRODUCT",
            "REGION",
            "LOAN TO VALUE AT INCEPTION (%)",
            "CREDIT SCORE",
            "LIVE DATE",
            "DEFAULT AMOUNT (£)",
            "MERCHANT NAME",
            "VEHICLE MAKE",
            "VEHICLE MODEL",
            "VEHICLE MODEL DERIVATIVE",
            "GLASSES GUIDE RETAIL PRICE TRANSACTED (£)",
            "CURRENT APR (%)",
            "DEFAULT DATE",
            "Is the loan eligible to be funded?",
            "LOAN PRIMARY STATE",
            "PURCHASE PRICE (£)",
            "CASH DEPOSIT (£)",
            "INTEREST CHARGES (£)",
            "ORIGINAL MONTHLY REPAYMENT (£)",
            "ARREARS START DATE",
            "MATURITY DATE"
        ]
        ffy_column_names = [
            "Agreement Number",
            "Nationality",
            "Customer Net Income",
            "Years in Employment",
            "Home Owner",
            "Age Of Borrower",
            "Customer Credit Score",
            "Broker",
            "Vehicle Make",
            "Vehicle Model",
            "Vehicle Age",
            "Vehicle Fuel Type",
            "Vehicle Mileage",
            "Current Valuation",
            "Loan Status",
            "Start Date",
            "Date Funded",
            "Term",
            "Remaining Term",
            "Close Date",
            "Lending Payment Frequency",
            "Amount Financed",
            "Deposit",
            "Loan To Value",
            "Annual Percentage Rate",
            "Interest Received",
            "Capital Received",
            "Fees Received",
            "Other Fees",
            "Current Principle o/s",
            "Arrears Amount",
            "Payments in Arrears",
            "Date Defaulted",
            "Recoveries From Car Sale",
            "Other Recoveries",
            "Total Recoveries",
            "Gross Balance Defaulted",
            "Net Balance Defaulted",
            "Principal Defaulted Balance",
            "Net Principal Defaulted Balance",
            "Qualified",
            "Loan Eligibility Classification",
            "Loan RPA Classification"
        ]

        ffysmart_column_names = [
            "Agreement Number",
            "Current Principle o/s",
            "Amount Financed",
            "Eligibility Summary",
            "Term",
            "Product",
            "Customer Credit Score",
            "Start Date",
            "Annual Percentage Rate",
            "Payment Frequency",
            "Date Defaulted",
            "Loan Status",
            "Remaining Term_v1",
            "Close Date",
            "Fixed Contractual Repayment",
            "Interest Received",
            "Capital Received",
            "Payments in Arrears",
            "Last Payment Missed Date"
        ]

        fnpl_columbn_names = [
            "Application Date",
            "Contractual Monthly Instalment",
            "Current Ltv",
            "Final Statement Date",
            "Settlement Date",
            "Credit limit",
            "Monthly repayment amount",
            "Origination Date",
            "Deposit %",
            "Upfront Fee %",
            "Account Code",
            "Actual Closing Balance",
            "Loan Amount",
            "Loan_Term_v1",
            "Days In Arrears",
            "Product Name",
            "Territory",
            "Credit Score",
            "Take On Date",
            "Apr",
            "Eligible?",
            "Settlement Status",
            "Channel",
            "Currency",
            "Settlement Amount"
        ]

        instrumentalCatalogue_column_names = [
            "Unique Identifier for track",
            "Artist",
            "Original Advance Amount",
            "Additional Recoupable Costs",
            "Total Recoupable Costs",
            "Currency",
            "Contract Start Date",
            "Advance Date",
            "First Revenue Date",
            "Contract Term (in Months)",
            "Contracted Artist Split",
            "Year 1 Expected Revenue",
            "Year 2 Expected Revenue",
            "Year 3 Expected Revenue",
            "Year 4 Expected Revenue",
            "Year 5 Expected Revenue",
            "Total Gross Royalty Revenue Earned",
            "Total Instrumental Split of Revenue",
            "Total Artist Revenue",
            "Total Revenue Paid to Artist",
            "Total Expected Revenue to date",
            "Actual to Expected Revenue",
            "Total Outstanding Principal / Advance",
            "Revenue Month (i.e. number of months receiving revenue)",
            "EXCEPTION LOAN",
            "ELIGIBILITY CRITERIA CHECK",
            "STATUS",
            "3/9 Month Average monthly collections",
            "Remaining Term",
            "Remaining PV Term",
            "Future 3 / 5 yr Revenue",
            "Revenue until Artist Recoups",
            "Future Cashflows 3 / 5 years"
        ]

        instrumentalHotTracks_column_names = [
            "Unique Identifier for track",
            "Artist",
            "Track name",
            "Original Advance Amount",
            "Additional Recoupable Costs",
            "Total Recoupable Costs",
            "Currency",
            "Release Date",
            "First Revenue Date",
            "Contractual Artist Split",
            "Contractual Artist Split After Recoupment",
            "Contract Term (months)",
            "1 Year Cum Expected Revenue",
            "2 Year Cum Expected Revenue",
            "3 Year Cum Expected Revenue",
            "Number of Streams & YouTube Views (as of pool cut date)",
            "Total Gross Royalty Revenue Earned",
            "Total Instrumental Split of Revenue",
            "Total Artist Revenue",
            "Total Revenue Paid to Artist",
            "Total Expected Revenue to date",
            "Actual to Expected Revenue",
            "Outstanding principal / advance",
            "Revenue Month (i.e. number of months receiving revenue)",
            "ELIGIBILITY CRITERIA CHECK",
            "EXCEPTION LOAN",
            "STATUS",
            "Monthly Revenue Collected",
            "3/9 Month Average monthly collections",
            "Remaining Term",
            "Remaining PV Term",
            "Future Revenue",
            "Revenue until Artist Recoups",
            "Future Cashflows 3 years"
        ]

        instrumentalPerpetuityST_column_names = [
            "Unique Identifier for track",
            "Artist",
            "Track name",
            "Original Advance Amount",
            "Additional Recoupable Costs",
            "Total Recoupable Costs",
            "Currency",
            "Release Date",
            "First Revenue Date",
            "Contractual Artist Split",
            "Contractual Artist Split After Recoupment",
            "Contract Term (months)",
            "1 Year Cum Expected Revenue",
            "2 Year Cum Expected Revenue",
            "3 Year Cum Expected Revenue",
            "4 Year Expected Revenue",
            "5 Year Expected Revenue",
            "Number of Streams & YouTube Views (as of pool cut date)",
            "Total Gross Royalty Revenue Earned",
            "Total Instrumental Split of Revenue",
            "Total Artist Revenue",
            "Total Revenue Paid to Artist",
            "Total Expected Revenue to date",
            "Actual to Expected Revenue",
            "Outstanding principal / advance",
            "Revenue Month (i.e. number of months receiving revenue)",
            "ELIGIBILITY CRITERIA CHECK",
            "EXCEPTION LOAN",
            "STATUS",
            "Monthly Revenue Collected",
            "3/9 Month Average monthly collections",
            "Remaining PV Term",
            "Future Revenue",
            "Revenue until Artist Recoups",
            "Future Cashflows 3 years"
        ]

        lantern_column_names = [
            "Portfolio Name",
            "Current 36m ERC Total",
            "Purchase Price",
            "Month Purchased",
            "Withdrawn Portfolio"
        ]

        liberisEUCombinedbb_column_names = [
            "Contract ID",
            "Capital portion of balance",
            "Advance Amount",
            "Classification",
            "Geographical Region",
            "CUR",
            "Contract Start Date",
            "Current Renewal Number",
            "Factor Rate",
            "Industry",
            "Contract Term",
            "Latest transaction date",
            "Days Paying",
            "Expected Daily Pay",
            "Average Daily Pay",
            "Estimated Days Left",
            "%_Paid_off",
            "Amount_Left_£",
            "Withholding percentage"
        ]

        liberisEUWos_column_names = [
            "Contract ID",
            "Capital portion of balance",
            "Advance Amount",
            "Geographical Region",
            "CURR",
            "Contract Start Date",
            "Current Renerwal Number",
            "Factor Rate",
            "Industry",
            "Contract Term",
            "Latest transaction date",
            "Date_written_off",
            "Amount_written_off"
        ]

        liberisukbca_column_names = [
            "Contract ID",
            "Type",
            "Region",
            "Contract Start Date",
            "Witholding Percentage",
            "Advance Amount",
            "Purchased Amount",
            "Amount Left",
            "Capital portion of balance",
            "Factor Rate",
            "Days_paying",
            "Expected Daily Pay",
            "Average Daily Pay",
            "Contract Term (Days)",
            "Estimated Days Left",
            "% Paid off",
            "Last Transaction Date",
            "Current Renewal Number",
            "% of Expectation",
            "Credit score",
            "Product Type",
            "Classification",
            "In borrowing base?"
        ]

        liberisukSecuritised_column_names = [
            "Contract ID",
            "Type",
            "Region",
            "Contract Start Date",
            "Witholding Percentage",
            "Advance Amount",
            "Purchased Amount",
            "Amount Left",
            "Capital portion of balance",
            "Factor Rate",
            "Days_paying",
            "Expected Daily Pay",
            "Average Daily Pay",
            "Contract Term (Days)",
            "Estimated Days Left",
            "% Paid off",
            "Last Transaction Date",
            "Current Renewal Number",
            "% of Expectation",
            "Credit score",
            "Product Type",
            "Classification",
            "In borrowing base?"
        ]

        liberisukwos_column_names = [
            "Industry",
            "Contract Number Created",
            "Contract Start Date",
            "Witholding_Percentage",
            "Advance Amount",
            "Purchased Amount",
            "Expected Daily Pay",
            "Average Daily Pay",
            "Days Paying",
            "Current Renewal Number",
            "Last Transaction Date",
            "Date Written Off",
            "Amount at Write Off",
            "Capital portion of balance",
            "Geographical Region",
            "Factor Rate",
            "Estimated Days Left"
        ]


        prodigyABS_column_names = [
            "application_id",
            "university_name",
            "school_type",
            "course_name",
            "course_duration",
            "application_margin",
            "application_apr",
            "application_first_repayment_date",
            "series_name",
            "repayment_period_months",
            "application_total_admin_fee",
            "series_currency",
            "loan_original_grace_period_months",
            "original_loan_term",
            "loan_baserate",
            "loan_baserate_type",
            "loan_delinquency_status",
            "loan_months_on_book",
            "loan_total_disbursed_amount",
            "loan_remaining_grace_period_months",
            "loan_months_in_repayment",
            "loan_remaining_repayment_period_months",
            "loan_current_outstanding_balance",
            "loan_principal_admin_balance",
            "loan_interest_grace_balance",
            "loan_interest_after_grace_balance",
            "loan_remaining_term_months",
            "loan_full_term_months",
            "application_approved_amount",
            "course_mba_flag",
            "residence_at_application",
            "course_type",
            "loan_interest_rate_applied",
            "Settled"
        ]

        prodigyDFC_column_names = [
            "application_id",
            "university_name",
            "school_type",
            "course_name",
            "course_duration",
            "application_margin",
            "application_apr",
            "application_first_repayment_date",
            "series_name",
            "repayment_period_months",
            "application_total_admin_fee",
            "series_currency",
            "loan_original_grace_period_months",
            "original_loan_term",
            "loan_baserate",
            "loan_baserate_type",
            "loan_delinquency_status",
            "loan_months_on_book",
            "loan_total_disbursed_amount",
            "loan_remaining_grace_period_months",
            "loan_months_in_repayment",
            "loan_remaining_repayment_period_months",
            "loan_current_outstanding_balance",
            "loan_principal_admin_balance",
            "loan_interest_grace_balance",
            "loan_interest_after_grace_balance",
            "loan_remaining_term_months",
            "loan_full_term_months",
            "application_approved_amount",
            "course_mba_flag",
            "residence_at_application",
            "course_type",
            "loan_interest_rate_applied",
            "Settled"
        ]

        prodigyWarehouse_column_names = [
            "application_id",
            "university_name",
            "school_type",
            "course_name",
            "course_duration",
            "application_margin",
            "application_apr",
            "application_first_repayment_date",
            "series_name",
            "repayment_period_months",
            "application_total_admin_fee",
            "series_currency",
            "loan_original_grace_period_months",
            "original_loan_term",
            "loan_baserate",
            "loan_baserate_type",
            "loan_delinquency_status",
            "loan_months_on_book",
            "loan_total_disbursed_amount",
            "loan_remaining_grace_period_months",
            "loan_months_in_repayment",
            "loan_remaining_repayment_period_months",
            "loan_current_outstanding_balance",
            "loan_principal_admin_balance",
            "loan_interest_grace_balance",
            "loan_interest_after_grace_balance",
            "loan_remaining_term_months",
            "loan_full_term_months",
            "application_approved_amount",
            "course_mba_flag",
            "residence_at_application",
            "course_type",
            "loan_interest_rate_applied",
            "Settled"
        ]

        liberisUSPortfolio_column_names = [
            'Contract ID',
            'Industry',
            'Contract Start Date',
            'Withholding Percentage',
            'PP',
            'PA',
            'Amount Left',
            'Capital Balance',
            'Factor Rate',
            'Days Paying',
            'Exp Daily Pay',
            'Avg Daily Pay',
            '% Exp.',
            'Term (Days)',
            'Est Days Left',
            'Last Tran.Date',
            'Status',
            'Current Renewal Number',
            'Classification'
        ]

        liberisUSWOs_column_names = [
            'Contract ID',
            'Deal Start Date',
            'WO Date',
            'Contract Status',
            'Sum of Amount Left',
            'Sum of Purchased Amount'
        ]

        oakbrookares_column_names = [
            'StartDate',
            'LOB',
            'APR',
            'LoanTerm',
            'LoanSize',
            'AccountOriginationSource',
            'DueMonthlyPayment',
            'DelphiScore',
            'BorrowerIncome',
            'DebtToIncome',
            'Region',
            'Age',
            'YearMonthStatus',
            'MonthsOnBook',
            'RemainingTerm',
            'DQbucket',
            'CumulativePrincipalDefault',
            'DefaultYearMonth',
            'PrincipalPayments',
            'NonPrincipalPayments',
            'PrincipalBalance',
            'NonPrincipalBalance',
            'Eligible',
            'AgreementRef'
        ]

        oakbrookjpm_column_names = [
            'StartDate',
            'LOB',
            'APR',
            'LoanTerm',
            'LoanSize',
            'AccountOriginationSource',
            'DueMonthlyPayment',
            'DelphiScore',
            'BorrowerIncome',
            'DebtToIncome',
            'Region',
            'Age',
            'YearMonthStatus',
            'MonthsOnBook',
            'RemainingTerm',
            'DQbucket',
            'CumulativePrincipalDefault',
            'DefaultYearMonth',
            'PrincipalPayments',
            'NonPrincipalPayments',
            'PrincipalBalance',
            'NonPrincipalBalance',
            'Eligible',
            'AgreementRef'
        ]

        verdam_column_names = [
            'UniqueLoanID',
            'PurposeOfLoan',
            'Employer',
            'CreditScore',
            'LoanStatus',
            'LoanStartDate',
            'AmountApproved',
            'APRApproved',
            'TermApproved',
            'TermOutstanding',
            'MonthlyPayment',
            'TotalCapitalDue',
            'TotalCapitalPaid',
            'TotalInterestPaid',
            'OutstandingBalance',
            'BorrowerStatus',
            'MaxArrears',
            'MaxArrearsDate',
            'Bucket',
            'DelinquentEver',
            'DelinquentEverDate',
            'Seasoning',
            'CCJ_LTM',
            'DefaultBalance',
            'SeniorLoanStatus',
            'Servicer Fee',
            'Default - Servicer Definition',
            'DefaultEverDate',
            'RecoveriesApplicableToWrittenOffBalance',
            'Product',
            'DelinquentAccountStatus'
        ]

        all_files = {
                    'barlowmarshall' : barlowmarshall_column_names, 
                    'carmoola' : carmoola_column_names,
                    'ffy' : ffy_column_names,
                    'ffysmart' : ffysmart_column_names,
                    'fnpl' : fnpl_columbn_names,
                    'instrumentalCatalogue' : instrumentalCatalogue_column_names,
                    'instrumentalHotTracks' : instrumentalHotTracks_column_names,
                    'instrumentalPerpetuityST' : instrumentalPerpetuityST_column_names,
                    'lantern' : lantern_column_names,
                    'liberisEUCombinedbb' : liberisEUCombinedbb_column_names,
                    'liberisEUWos' : liberisEUWos_column_names,
                    'liberisukbca' : liberisukbca_column_names,
                    'liberisukSecuritised' : liberisukSecuritised_column_names,
                    'liberisukwos' : liberisukwos_column_names,
                    'prodigyABS' : prodigyABS_column_names,
                    'prodigyDFC' : prodigyDFC_column_names,
                    'prodigyWarehouse' : prodigyWarehouse_column_names,
                    'liberisUSPortfolio' : liberisUSPortfolio_column_names,
                    'liberisUSWOs' : liberisUSWOs_column_names,
                    'oakbrookares' : oakbrookares_column_names,
                    'oakbrookjpm' : oakbrookjpm_column_names,
                    'verdam' : verdam_column_names
                }
        
        extracted_name = file_name[:file_name.find("_")].lower()

        # Print the extracted name
        # print(extracted_name)  # Output: LiberisUSPortfolio
        self.raw_df.columns = [col.strip() for col in self.raw_df.columns]
        column_names = self.raw_df.columns.tolist()

        # Create a dictionary to store prefixes as keys and column names as values
        matched_column_name = []
        try:
        # Your existing code to extract the file name and check for a match
            for key, value in all_files.items():
                if extracted_name == key.lower():
                    matched_column_name = value
                    break

            if not matched_column_name :
                matched_column_name = column_names
                # st.write('Reduced field not found')
                # print("Matched column names:", matched_column_name)
                # Use matched_column_name

        except Exception as e:
            logging.error(f"An error occurred: {e}")

        

        

        common_columns = list(set(column_names).intersection(set(matched_column_name)))
        # Get a list of all columns in the raw data
        list_full = self.raw_df.columns.tolist()

        
        # we will use this dictionary in hardcoded_fields file to update the new columns in our dataframe which are hardcoded or calculated or are null
        data_dict = self.stan_df.to_dict(orient='records')[0]
        # Dictionary to map old column names to new standard column names
      
        # Get the common columns between filtered_list and the raw data columns
        # common_columns = list(set(filtered_list).intersection(list_full))

        filtered_dict = {key: value for key, value in data_dict.items() if value not in common_columns}

        # Create the final DataFrame with useful columns
        df_final = self.raw_df[common_columns]

        return df_final, filtered_dict

# Example usage:
# raw_file_path = 'prodigy.csv'
# stan_df = pd.read_csv('standard_data.csv')  # Replace with your standard data file
# calc_df = pd.read_csv('calculations_data.csv')  # Replace with your calculations data file

# extractor = ColumnExtractor(raw_file_path, stan_df, calc_df)
# useful_columns = extractor.get_useful_columns()

# Now 'useful_columns' contains the DataFrame with the useful columns.
# You can further process or display this DataFrame as needed.
