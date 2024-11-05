import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

#Global Variables
data_path = 'data/DayAheadPrices_12.1.D'
file_matter = 'DayAheadPrices_12.1.D.csv'
nordlink_opening = datetime(2020, 12, 9)

def total_filtered_data(path, matter, first_year=2019, last_year=2023):
    df = []
    price_list = []
    physical_list = []
    for year in range(first_year, last_year +1):
        for month in range(1, 13):

            #Defining File Name
            file = f'{year}_{month:02}_{matter}'

            #Construct File Path
            file_path = os.path.join(path, file)

            #Checking File Existance
            if os.path.isfile(file_path):
                df = pd.read_csv(file_path, delimiter='\t')

                #Converting DateTime into Datetime Format
                df['DateTime'] = pd.to_datetime(df['DateTime'])

                if 'Prices' in matter:

                    #Filter Data For NO2, DE_LU, PT60M
                    df = df[(df['MapCode'].isin(['NO2', 'DE_LU'])) & (df['ResolutionCode'] == 'PT60M')]
                    price_list.append(df[['MapCode', 'Price', 'DateTime']])

                elif 'Physical' in matter:
                    #Filter Data for 
                    df = df[(df['InMapCode'].isin(['NO2', 'DE_LU'])) & (df['OutMapCode'].isin(['NO2', 'DE_LU']))]
                    physical_list.append(df[['DateTime', 'InMapCode', 'OutMapCode', 'FlowValue']])
            else:
                    raise ValueError(f'Not found: {file_path}')
    
    #Concatenate All Months, in Each Year into one DataFrame
    full_data_price_list = pd.concat(price_list, ignore_index=True) if price_list else pd.DataFrame()
    full_data_physical_list = pd.concat(physical_list, ignore_index=True) if physical_list else pd.DataFrame()
    return {'price_data': full_data_price_list, 'physical_data': full_data_physical_list}

data = total_filtered_data(data_path, file_matter, 2019, 2023)
price_data = data['price_data']

if __name__ == "__main__":
    print(price_data.head(5))

#Selecting Data Rows NO2 and DE_LU Seperately
data_no2 = price_data[price_data['MapCode'] == 'NO2']
data_delu = price_data[price_data['MapCode'] == 'DE_LU']

if __name__ == "__main__":
    print(data_no2.head(5))
    print(data_delu.head(5))

if __name__ == "__main__":
    #Plotting
    fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    #Plot NO2 Data
    axs[0].plot(data_no2['DateTime'], data_no2['Price'], color='blue', label='NO2 Price')
    axs[0].axvline(nordlink_opening, color='red', linestyle='--', label='Nordlink Opening')
    axs[0].set_title('Hourly Electricity Price in NO2')
    axs[0].set_ylabel('Price (EUR/MWh)')
    axs[0].legend()

    #Plot DE_LU Data
    axs[1].plot(data_delu['DateTime'], data_delu['Price'], color='green', label='Germany Price')
    axs[1].axvline(nordlink_opening, color='red', linestyle='--', label='Nordlink Opening')
    axs[1].set_title('Hourly Electricity Price in Germany')
    axs[1].set_xlabel('Date')
    axs[1].set_ylabel('Price (EUR/MWh)')
    axs[1].legend()

    # Save the figure
    plt.tight_layout()
    plt.savefig('figure_task1.png')
    plt.show()