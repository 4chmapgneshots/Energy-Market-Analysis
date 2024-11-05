import pandas as pd

def physical_flow(dataframe, period='year', purpose='overview', first_year=2019, last_year=2023):
    # Filter Years
    dataframe = dataframe[(dataframe['DateTime'].dt.year >= first_year) & 
                          (dataframe['DateTime'].dt.year <= last_year)]
    
    #Mark Exports or Imports
    dataframe['FlowType'] = dataframe.apply(
        lambda row: 'export' if row['OutMapCode'] == 'NO2' and row['InMapCode'] == 'DE_LU' else
                    'import' if row['OutMapCode'] == 'DE_LU' and row['InMapCode'] == 'NO2' else None, axis=1)
    
    #Drop Irrelevant Data
    dataframe = dataframe[dataframe['FlowType'].notna()]

    #Exports are Positive, Imports are Negative, Aids Net Calculation
    dataframe['FlowValue'] = dataframe.apply(lambda x: x['FlowValue'] if x['FlowType'] == 'export' else -x['FlowValue'], axis=1)

    #Handle Different Operations
    if purpose == 'overview' and period == 'year':
        annual_imports = dataframe[dataframe['FlowType'] == 'import'].groupby(dataframe['DateTime'].dt.year)['FlowValue'].sum().abs()
        annual_exports = dataframe[dataframe['FlowType'] == 'export'].groupby(dataframe['DateTime'].dt.year)['FlowValue'].sum()
        overview_data = pd.DataFrame({'imports': annual_imports, 'exports': annual_exports})
        return overview_data

    elif purpose == 'net' and period == 'week':
        # Weekly net exports: exports - imports
        weekly_net = dataframe.resample('W', on='DateTime')['FlowValue'].sum()
        weekly_net_df = weekly_net.reset_index()
        weekly_net_df.columns = ['Date', 'Net Export']
        return weekly_net_df

    else:
        raise ValueError("Invalid combination of period and purpose. Use 'year' for period with 'overview' or 'week' for period with 'net'.")
