import pandas as pd
import numpy as np
from glob import glob

# THIS FILE IS USED FOR PACKAGING THE PROCESSING OF EACH TICKER'S DATA


IS_ACCOUNTS = ["Net sales", "Cost of goods sold", "Gross Profit", "Financial expenses", "Of which: Interest expense",
               "Cost of sales", "Enterprise cost management", "Total Operating Expenses",
               "Total revenue financing activities",
               "Net profit from business activities", "Profit", "Profit before tax",
               "Present corporate income tax expenses",
               "Deferred income taxes expenses", "The interests of minority shareholders", "Total Cost of profits",
               "Profit after tax corporate income", "Volume", "Close of Quarter", "EPS", "Non-adjusted EPS", "PE",
               "Book Price"]

ASSETS = ["SHORT-TERM ASSETS", "Cash and cash equivalents", "Cash", "Cash equivalents",
          "Short-term financial investments",
          "Available for sale securities", "Provision for diminution in value of available for sale securities (*)",
          "Held to maturity investments", "Short-term receivables", "Short-term trade accounts receivable",
          "Short-term prepayments to suppliers", "Short-term inter-company receivables",
          "Construction contract progress receipts due from customers",
          "Short-term loan receivables", "Other short-term receivables", "Provision for short-term doubtful debts (*)",
          "Assets awaiting resolution", "Inventories", "Inventories", "Provision for decline in value of inventories",
          "Other short-term assets", "Short-term prepayments", "Value added tax to be reclaimed",
          "Taxes and other receivables from state authorities", "Government bonds", "Other short-term assets",
          "LONG-TERM ASSETS",
          "Long-term receivables", "Long-term trade receivables", "Long-term prepayments to suppliers",
          "Capital at inter-company",
          "Long-term inter-company receivables", "Long-term loan receivables", "Other long-term receivables",
          "Provision for long-term doubtful debts", "Fixed assets", "Tangible fixed assets", "Cost",
          "Accumulated depreciation",
          "Financial leased fixed assets", "Cost", "Accumulated depreciation", "Intangible fixed assets", "Cost",
          "Accumulated depreciation", "Investment properties", "Cost", "Accumulated depreciation",
          "Long-term assets in progress",
          "Long-term production in progress", "Construction in progress", "Long-term financial investments",
          "Investments in subsidiaries", "Investments in associates, joint-ventures", "Investments in other entities",
          "Provision for diminution in value of long-term investments", "Held to maturity investments",
          "Other long-term investments", "Other long-term assets", "Long-term prepayments",
          "Deferred income tax assets",
          "Long-term equipment, supplies, spare parts", "Other long-term assets", "Goodwill", "TOTAL ASSETS"]

LIABILITIES = ["LIABILITIES", "Short -term liabilities", "Short-term trade accounts payable",
               "Short-term advances from customers",
               "Taxes and other payables to state authorities", "Payable to employees", "Short-term acrrued expenses",
               "Short-term inter-company payables", "Construction contract progress payments due to suppliers",
               "Short-term unearned revenue", "Other short-term payables", "Short-term borrowings and financial leases",
               "Provision for short-term liabilities", "Bonus and welfare fund", "Price stabilization fund",
               "Government bonds", "Long-term liabilities", "Long-term trade payables",
               "Long-term advances from customers",
               "Long-term acrrued expenses", "Inter-company payables on business capital",
               "Long-term inter-company payables",
               "Long-term unearned revenue", "Other long-term liabilities", "Long-term borrowings and financial leases",
               "Convertible bonds", "Preferred stock (Debts)", "Deferred income tax liabilities",
               "Provision for long-term liabilities",
               "Fund for technology development", "Provision for severance allowances"]

EQUITY = ["OWNER'S EQUITY", "Owner's equity", "Owner's capital", "Common stock with voting right", "Preferred stock",
          "Share premium",
          "Convertible bond option", "Other capital of owners", "Treasury shares", "Assets revaluation differences",
          "Foreign exchange differences", "Investment and development fund", "Fund to support corporate restructuring",
          "Other funds from owner's equity", "Undistributed earnings after tax",
          "Accumulated retained earning at the end of the previous period",
          "Undistributed earnings in this period", "Reserves for investment in construction", "Minority's interest",
          "Financial reserves", "Other resources and funds", "Subsidized not-for-profit funds",
          "Funds invested in fixed assets",
          "MINORITY'S INTEREST", "TOTAL OWNER'S EQUITY AND LIABILITIES"]

CF_indirect = ['net_profit_before_tax', 'adjustments', 'depreciation_amortization', 'provisions',
               'net_profit_from_investment_in_joint_venture',
               'write_off_fixed_assets', 'unrealised_foreign_exchange_profit', 'profit_from_disposals_of_fixed_assets',
               'profit_from_investing_activities', 'profit_from_deposit', 'interest_income', 'interest_expense',
               'payments_direct_from_profit', 'operating_profit_before_working_capital_changes',
               'increase_decrease_in_receivables',
               'increase_decrease_in_inventories', 'increase_decrease_in_payables',
               'increase_decrease_in_prepaid_expense',
               'increase_decrease_in_current_assets', 'cash_paid_for_interest', 'cash_paid_for_taxes',
               'other_cash_from_operating_activities', 'other_payments_from_operating_activities',
               'net_cash_from_operating',
               'cash_paid_for_new_PPE', 'cash_collected_from_PPE_sales', 'cash_paid_for_loans',
               'cash_collected_from_loans',
               'investment_in_joint_venture', 'purchases_of_short_term_investment',
               'cash_paid_for_investments_in_other_companies',
               'cash_collected_from_investments_in_other_companies', 'interest_collected_from_deposits',
               'cash_collected_from_interest', 'purchases_of_minority equity', 'net_cash_from_investing',
               'cash_collected_from_issuing_shares', 'cash_paid_for_capital_contribution',
               'cash_paid_for_short_term_borrowing',
               'cash_paid_for_principles', 'cash_paid_for_financial_lease', 'other_cash_paid_for_financial_activities',
               'purchase_from_capitalization_issues', 'dividends_paid', 'minority_equity_in_joint_venture',
               'social_welfare_expenses', 'net_cash_from_financing', 'net_cash_flow', 'cash_cash_equivalent_begin',
               'effects_of_exchange_rate', 'cash_cash_equivalent_end']

CF_direct = ['cash_collected_from_customers', 'cash_paid_for_suppliers', 'cash_paid_for_employees',
             'cash_paid_for_interest',
             'cash_paid_for_taxes', 'cash_paid_for_VAT', 'other_cash_collected_for_operating_activities',
             'other_cash_paid_for_operating_activities', 'net_cash_from_operating', 'cash_paid_for_new_PPE',
             'cash_collected_from_PPE_sales', 'cash_paid_for_loans', 'cash_collected_from_loans',
             'cash_paid_for_investments_in_other_companies', 'cash_collected_from_investments_in_other_companies',
             'cash_collected_from_interest', 'net_cash_from_investing', 'cash_collected_from_issuing_shares',
             'cash_paid_for_capital_contribution', 'cash_paid_for_short_term_borrowing', 'cash_paid_for_principles',
             'cash_paid_for_PPE_lease', 'cash_paid_for_financial_lease', 'dividends_paid', 'cash_paid_for_firm_funds',
             'net_cash_from_financing', 'net_cash_flow', 'cash_cash_equivalent_begin', 'effects_of_exchange_rate',
             'cash_cash_equivalent_end']

financial_index = ['current_ratio', 'quick_ratio', 'cash_ratio', 'long_term_debt_to_equity', 'total_debt_to_equity',
                   'debt_ratio',
                   'financial_leverage', 'interest_coverage', 'net_profit_margin', 'operating_profit_margin',
                   'gross_profit_margin', 'pretax_margin', 'average_total_assets', 'ROA', 'operating_ROA',
                   'average_total_capital',
                   'ROC', 'average_total_equity', 'ROE', 'average_receivables', 'receivables_turnover',
                   'average_inventory',
                   'inventory_turnover', 'average_payables', 'payables_turnover', 'book_value_per_share',
                   'price_earnings',
                   'book_price', 'cash_ROA', 'cash_flow_on_revenue', 'cash_ROE', 'cash_on_income', 'debt_coverage',
                   'cash_interest_coverage',
                   'reinvestment', 'total_net_accruals', 'cash_earnings']

headers = IS_ACCOUNTS + ASSETS + LIABILITIES + EQUITY + list(set(CF_indirect + CF_direct)) + financial_index

view_IS = IS_ACCOUNTS

view_BS = ASSETS + LIABILITIES + EQUITY

view_CF = list(set(CF_indirect + CF_direct))

view_financial_index = list(set(financial_index) - {'average_total_assets', 'average_total_capital',
                                                    'average_total_equity', 'average_receivables', 'average_inventory',
                                                    'average_payables'})


### ALGORITHMS FOR PROCESSING NaNs
# GET DATAPOINT FROM AN ACCOUNT, TREATING 'N/A' AS np.nan
def process_array(row, status, account):
    if row[status][account] == 'N/A':
        return np.nan
    else:
        return row[status][account]


# SUM ACROSS COLUMNS. WHEN ALL COMPONENTS ARE NaN, THE SUM IS NaN
def sum_across_cols(df):
    result = df.isnull().sum(axis=1)
    result.reindex(df.index, copy=False)
    indexes = np.nonzero(result == df.shape[1])
    temp = df.fillna(0)
    result = df.sum(skipna=True, axis=1)
    result.iloc[indexes] = np.nan
    return result


### PROCESS EACH TICKER
def process_ticker(tickers, df):
    for ticker in tickers:
        IS_file = sorted(glob("jsons/IS/" + "*_{}.json".format(ticker)))[0]
        BS_file = sorted(glob("jsons/BS/" + "*_{}.json".format(ticker)))[0]
        CF_file = sorted(glob("jsons/CF/" + "*_{}.json".format(ticker)))[0]

        # print (BS_file)

        IS_df = pd.read_json(IS_file)
        IS_df['index'] = np.array([row['quarter'] for row in IS_df['data']])
        IS_df.set_index('index', inplace=True)

        BS_df = pd.read_json(BS_file)
        BS_df['index'] = np.array([row['quarter'] for row in BS_df['data']])
        BS_df.set_index('index', inplace=True)

        CF_df = pd.read_json(CF_file)
        CF_df['index'] = np.array([row['quarter'] for row in CF_df['data']])
        CF_df.set_index('index', inplace=True)

        # Income statement
        for account in IS_ACCOUNTS:
            array = np.array([process_array(row, 'income status', account) for row in IS_df['data']])
            IS_df[account] = array
        IS_df.drop('data', 1, inplace=True)

        # Balance sheet
        for account in ASSETS:
            array = np.array([process_array(row, 'assets', account) for row in BS_df['data']])
            BS_df[account] = array
        for account in LIABILITIES:
            array = np.array([process_array(row, 'liabilities', account) for row in BS_df['data']])
            BS_df[account] = array
        for account in EQUITY:
            array = np.array([process_array(row, 'equity', account) for row in BS_df['data']])
            BS_df[account] = array
        BS_df.drop('data', 1, inplace=True)

        # Cash flow statement
        if not CF_df['type'].empty:
            if CF_df['type'][0] == "indirect":
                for account in CF_indirect:
                    array = np.array([process_array(row, 'cash_flow_status', account) for row in CF_df['data']])
                    CF_df[account] = array

                CF_df['net_cash_from_operating'].fillna(
                    sum_across_cols(CF_df[['operating_profit_before_working_capital_changes',
                                           'increase_decrease_in_receivables',
                                           'increase_decrease_in_inventories',
                                           'increase_decrease_in_payables',
                                           'increase_decrease_in_prepaid_expense',
                                           'increase_decrease_in_current_assets',
                                           'cash_paid_for_interest',
                                           'cash_paid_for_taxes',
                                           'other_cash_from_operating_activities',
                                           'other_payments_from_operating_activities']]), inplace=True)
                CF_df['net_cash_from_investing'].fillna(sum_across_cols(CF_df[['cash_paid_for_new_PPE',
                                                                               'cash_collected_from_PPE_sales',
                                                                               'cash_paid_for_loans',
                                                                               'cash_collected_from_loans',
                                                                               'investment_in_joint_venture',
                                                                               'purchases_of_short_term_investment',
                                                                               'cash_paid_for_investments_in_other_companies',
                                                                               'cash_collected_from_investments_in_other_companies',
                                                                               'interest_collected_from_deposits',
                                                                               'cash_collected_from_interest',
                                                                               'purchases_of_minority equity']]))
                CF_df['net_cash_from_financing'].fillna(sum_across_cols(CF_df[['cash_collected_from_issuing_shares',
                                                                               'cash_paid_for_capital_contribution',
                                                                               'cash_paid_for_short_term_borrowing',
                                                                               'cash_paid_for_principles',
                                                                               'cash_paid_for_financial_lease',
                                                                               'other_cash_paid_for_financial_activities',
                                                                               'purchase_from_capitalization_issues',
                                                                               'dividends_paid',
                                                                               'minority_equity_in_joint_venture',
                                                                               'social_welfare_expenses']]))
            else:
                for account in CF_direct:
                    array = np.array([process_array(row, 'cash_flow_status', account) for row in CF_df['data']])
                    CF_df[account] = array

                CF_df['net_cash_from_operating'].fillna(sum_across_cols(CF_df[['cash_collected_from_customers',
                                                                               'cash_paid_for_suppliers',
                                                                               'cash_paid_for_employees',
                                                                               'cash_paid_for_interest',
                                                                               'cash_paid_for_taxes',
                                                                               'cash_paid_for_VAT',
                                                                               'other_cash_collected_for_operating_activities',
                                                                               'other_cash_paid_for_operating_activities']]))
                CF_df['net_cash_from_investing'].fillna(sum_across_cols(CF_df[['cash_paid_for_new_PPE',
                                                                               'cash_collected_from_PPE_sales',
                                                                               'cash_paid_for_loans',
                                                                               'cash_collected_from_loans',
                                                                               'cash_paid_for_investments_in_other_companies',
                                                                               'cash_collected_from_investments_in_other_companies',
                                                                               'cash_collected_from_interest']]))
                CF_df['net_cash_from_financing'].fillna(sum_across_cols(CF_df[['cash_collected_from_issuing_shares',
                                                                               'cash_paid_for_capital_contribution',
                                                                               'cash_paid_for_short_term_borrowing',
                                                                               'cash_paid_for_principles',
                                                                               'cash_paid_for_PPE_lease',
                                                                               'cash_paid_for_financial_lease',
                                                                               'dividends_paid',
                                                                               'cash_paid_for_firm_funds']]))

            CF_df['net_cash_flow'].fillna(sum_across_cols(
                CF_df[['net_cash_from_operating', 'net_cash_from_investing', 'net_cash_from_financing']]))
        CF_df.drop('data', 1, inplace=True)

        # Merge 3 DataFrames
        # IS_CF = pd.merge(IS_df, CF_df, left_index=True, right_index=True, how='outer')
        # IS_CF_BS = pd.merge(IS_CF, BS_df, left_index=True, right_index=True, how='outer')

        # Reindex
        # reindex = sorted(IS_CF_BS.index, key = lambda x: int(x.split(" ")[1]))
        # IS_CF_BS_reindexed = IS_CF_BS.reindex(reindex)

        df.loc[ticker].update(IS_df)
        df.loc[ticker].update(BS_df)
        df.loc[ticker].update(CF_df)

        # Calculate financial indices
        df.loc[ticker]['current_ratio'] = df.loc[ticker]['SHORT-TERM ASSETS'] / df.loc[ticker][
            'Short -term liabilities']
        df.loc[ticker]['quick_ratio'] = sum_across_cols(df.loc[ticker][
                                                            ['Cash and cash equivalents', 'Short-term receivables',
                                                             'Short-term trade accounts receivable',
                                                             'Short-term inter-company receivables',
                                                             'Short-term loan receivables',
                                                             'Other short-term receivables',
                                                             'Taxes and other receivables from state authorities']]) / \
                                        df.loc[ticker]['Short -term liabilities']
        df.loc[ticker]['cash_ratio'] = df.loc[ticker]['Cash and cash equivalents'] / df.loc[ticker][
            'Short -term liabilities']
        df.loc[ticker]['long_term_debt_to_equity'] = df.loc[ticker]['Long-term liabilities'] / (
            df.loc[ticker]['TOTAL OWNER\'S EQUITY AND LIABILITIES'] - df.loc[ticker]['LIABILITIES'])
        df.loc[ticker]['total_debt_to_equity'] = df.loc[ticker]['LIABILITIES'] / (
            df.loc[ticker]['TOTAL OWNER\'S EQUITY AND LIABILITIES'] - df.loc[ticker]['LIABILITIES'])
        df.loc[ticker]['debt_ratio'] = df.loc[ticker]['LIABILITIES'] / df.loc[ticker]['TOTAL ASSETS']
        df.loc[ticker]['financial_leverage'] = df.loc[ticker]['TOTAL ASSETS'] / (
            df.loc[ticker]['TOTAL OWNER\'S EQUITY AND LIABILITIES'] - df.loc[ticker]['LIABILITIES'])
        df.loc[ticker]['interest_coverage'] = sum_across_cols(
            df.loc[ticker][['Profit before tax', 'Of which: Interest expense']]) / df.loc[ticker][
                                                  'Of which: Interest expense']
        df.loc[ticker]['net_profit_margin'] = df.loc[ticker]['Profit after tax corporate income'] / \
                                              df.loc[ticker]['Net sales']
        df.loc[ticker]['operating_profit_margin'] = sum_across_cols(
            df.loc[ticker][['Profit before tax', 'Of which: Interest expense']]) / df.loc[ticker]['Net sales']
        df.loc[ticker]['gross_profit_margin'] = df.loc[ticker]['Gross Profit'] / df.loc[ticker][
            'Net sales']
        df.loc[ticker]['pretax_margin'] = df.loc[ticker]['Profit before tax'] / df.loc[ticker][
            'Net sales']

        df.loc[ticker]['average_total_assets'] = df.loc[ticker]['TOTAL ASSETS'].rolling(2,
                                                                                        min_periods=1).mean()
        df.loc[ticker]['ROA'] = df.loc[ticker]['Profit after tax corporate income'] / df.loc[ticker][
            'average_total_assets']
        df.loc[ticker]['operating_ROA'] = sum_across_cols(
            df.loc[ticker][['Profit before tax', 'Of which: Interest expense']]) / df.loc[ticker][
                                              'average_total_assets']

        df.loc[ticker]['average_total_capital'] = df.loc[ticker]['Owner\'s capital'].rolling(2,
                                                                                             min_periods=1).mean()
        df.loc[ticker]['ROC'] = sum_across_cols(
            df.loc[ticker][['Profit before tax', 'Of which: Interest expense']]) / df.loc[ticker][
                                    'average_total_capital']

        df.loc[ticker]['average_total_equity'] = (
            df.loc[ticker]['TOTAL OWNER\'S EQUITY AND LIABILITIES'] - df.loc[ticker]['LIABILITIES']).rolling(2,
                                                                                                             min_periods=1).mean()
        df.loc[ticker]['ROE'] = df.loc[ticker]['Profit after tax corporate income'] / df.loc[ticker][
            'average_total_equity']

        df.loc[ticker]['average_receivables'] = sum_across_cols(
            df.loc[ticker][['Short-term receivables', 'Short-term trade accounts receivable']]).rolling(2,
                                                                                                        min_periods=1).mean()
        df.loc[ticker]['receivables_turnover'] = df.loc[ticker]['Net sales'] / df.loc[ticker][
            'average_receivables']

        df.loc[ticker]['average_inventory'] = sum_across_cols(
            df.loc[ticker][['Inventories', 'Provision for decline in value of inventories']]).rolling(2,
                                                                                                      min_periods=1).mean()
        df.loc[ticker]['inventory_turnover'] = df.loc[ticker]['Cost of goods sold'] / df.loc[ticker][
            'average_inventory']

        df.loc[ticker]['average_payables'] = df.loc[ticker]['Short-term trade accounts payable'].rolling(
            window=2, min_periods=1).mean()
        df.loc[ticker]['payables_turnover'] = (sum_across_cols(
            df.loc[ticker][['Inventories', 'Provision for decline in value of inventories']]).diff(1).fillna(0) +
                                               df.loc[ticker]['Cost of goods sold']) / df.loc[ticker][
                                                  'average_payables']

        df.loc[ticker]['book_value_per_share'] = (df.loc[ticker]['TOTAL OWNER\'S EQUITY AND LIABILITIES'] -
                                                  df.loc[ticker]['LIABILITIES']) / df.loc[ticker][
                                                     'Volume']
        df.loc[ticker]['price_earnings'] = df.loc[ticker]['PE']
        df.loc[ticker]['book_price'] = df.loc[ticker]['Book Price']
        df.loc[ticker]['cash_ROA'] = df.loc[ticker]['net_cash_from_operating'] / df.loc[ticker][
            'average_total_assets']
        df.loc[ticker]['cash_flow_on_revenue'] = df.loc[ticker]['net_cash_from_operating'] / \
                                                 df.loc[ticker]['Net sales']
        df.loc[ticker]['cash_ROE'] = df.loc[ticker]['net_cash_from_operating'] / df.loc[ticker][
            'average_total_equity']
        df.loc[ticker]['cash_on_income'] = df.loc[ticker]['net_cash_from_operating'] / sum_across_cols(
            df.loc[ticker][['Profit before tax', 'Of which: Interest expense']])
        df.loc[ticker]['debt_coverage'] = df.loc[ticker]['net_cash_from_operating'] / df.loc[ticker][
            'LIABILITIES']
        df.loc[ticker]['cash_interest_coverage'] = sum_across_cols(
            df.loc[ticker][['net_cash_from_operating', 'cash_paid_for_interest', 'cash_paid_for_taxes']]) / \
                                                   df.loc[ticker]['cash_paid_for_interest']
        df.loc[ticker]['reinvestment'] = df.loc[ticker]['net_cash_from_operating'] / df.loc[ticker][
            'cash_paid_for_new_PPE']
        df.loc[ticker]['total_net_accruals'] = df.loc[ticker]['TOTAL ASSETS'].diff(1).fillna(0) - \
                                               df.loc[ticker]['LIABILITIES'].diff(1).fillna(0) - \
                                               df.loc[ticker]['net_cash_flow']
        df.loc[ticker]['cash_earnings'] = df.loc[ticker]['total_net_accruals'] - df.loc[ticker][
            'Profit after tax corporate income']