# %% Transformation.py - script to do transformation on the two primary data sets for the project. 
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from azure.storage.filedatalake import DataLakeServiceClient

# Read in the two dataframes
prices_df = pd.read_csv("RawData/EIATotalEnergyPricesByState.csv")
renewables_df = pd.read_csv("RawData/EIARenewablesByState.csv")

# Convert million kilowatthours to billion Btu so all values are same unit in renewables_df
mil_kwh_to_bil_btu = 3.412142
mask = (renewables_df['unit'] == 'Million kilowatthours')
renewables_df.loc[mask, 'value'] = renewables_df.loc[mask, 'value'] * mil_kwh_to_bil_btu
renewables_df.loc[mask, 'unit'] = 'Billion Btu'

print(prices_df.head)
print(renewables_df.head)
# %% Pivot the DataFrames to get each row containing all values for the year/state combination
prices_df = prices_df.pivot_table(index=['period', 'stateId'], columns='seriesId', values='value', aggfunc='first').reset_index()
renewables_df = renewables_df.pivot_table(index=['period', 'stateId'], columns='seriesId', values='value', aggfunc='first').reset_index()

# Original column names
original_price_columns = ["period", "stateId", "TEACD", "TECCD", "TEICD", "TERCD", "TETCD", "TETXD"]
original_renewables_columns = ["period", "stateId", "BFPRB", "BMTCB", "GEEGP", "GETCB", "HYTCB", "HYTCP", "SOTCB", "SOTGP", "WWPRB", "WYTCB", "WYTCP"]

# New column names for better description
new_price_columns = ["Year", "State", "TotalEnergyPriceTransportation", "TotalEnergyPriceCommercial", "TotalEnergyPriceIndustrial", "TotalEnergyPriceResidential", "TotalEnergyPrice", "TotalEndUseEnergyPrice"]
new_renewables_columns = ["Year", "State", "BiofuelsProduction", "BiomassConsumption", "GeothermalProduction", "GeothermalConsumption", "HydropowerConsumption", "HydropowerProduction", "SolarConsumption", "SolarProduction", "WoodWasteProduction", "WindConsumption", "WindProduction"]

# Rename the columns
prices_df.columns = new_price_columns
renewables_df.columns = new_renewables_columns

# Add a units column
prices_df['Unit'] = 'Dollars per million Btu'
renewables_df['Unit'] = 'Billion Btu'

# Set the few null values to zero
prices_df.fillna(0, inplace=True)
renewables_df.fillna(0, inplace=True)

# %% Upload the pivoted datasets to Azure

# Method to connect to an Azure storage account with an account key.
def initialize_storage_account(storage_account_name, storage_account_key):
    
    try:  
        global service_client

        service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
            "https", storage_account_name), credential=storage_account_key)
    
    except Exception as e:
        print(e)

# Connect to Azure project storage account with account key
storage_account_name = "projectstorage1"

with open("keys/ADLSKey.config") as f:
    storage_account_key=f.readline()

initialize_storage_account(storage_account_name, storage_account_key)

print(service_client)        

# Convert Dataframes to CSV files
prices_df.to_csv("PivotedData/EIATotalEnergyPricesByStatePivoted.csv")
renewables_df.to_csv("PivotedData/EIARenewablesByStatePivoted.csv")


# Directory and file client creation for upload to Azure
container_name = "project"
folder_name = "PivotedData"
file_name = "EIATotalEnergyPricesByStatePivoted.csv"
file_name2 = "EIARenewablesByStatePivoted.csv"


# Create a directory client
directory_client = service_client.get_directory_client(container_name, folder_name)

# Create a file client within the directory
file_client = directory_client.create_file(file_name)
file_client2 = directory_client.create_file(file_name2)

print("Files created in ADLS")

# Upload the CSV files to Azure directory
upload_file_path = "PivotedData/EIATotalEnergyPricesByStatePivoted.csv"
upload_file_path2 = "PivotedData/EIARenewablesByStatePivoted.csv"
upload_file = open(upload_file_path,'r')
upload_file2 = open(upload_file_path2, 'r')

file_contents = upload_file.read()
file_contents2 = upload_file2.read()

file_client.upload_data(file_contents, overwrite=True)
file_client2.upload_data(file_contents2, overwrite=True)

print(upload_file_path, "and ", upload_file_path2, " has been successfully uploaded to ADLS")
        
# Connect to Azure project storage account with account key
storage_account_name = "projectstorage1"

with open("keys/ADLSKey.config") as f:
    storage_account_key=f.readline()

initialize_storage_account(storage_account_name, storage_account_key)

print(service_client)

# %% Print out basic info about the dataframes
prices_df.info()
renewables_df.info()

# %% Create a line plot for Total Average Energy Price of all states
plt.figure(figsize=(10, 6))

# Group the data by 'State' and iterate through each group
for state, state_data in prices_df.groupby('State'):
    plt.plot(state_data['Year'], state_data['TotalEnergyPrice'], label=state)

# Add labels and title
plt.xlabel('Year')
plt.ylabel('Total Average Energy Price (Dollars per Million Btu)')
plt.title('Total Average Energy Price Over Time for All States')

# Add a legend
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))  # Adjust legend position

# Show the plot
plt.grid(True)
plt.show()

# %% Create a line plot for WindProduction of all states
plt.figure(figsize=(10, 6))

# Group the data by 'State' and iterate through each group
for state, state_data in renewables_df.groupby('State'):
    plt.plot(state_data['Year'], state_data['WindProduction'], label=state)

# Add labels and title
plt.xlabel('Year')
plt.ylabel('Wind Production (Billion Btu)')
plt.title('Wind Production Over Time for All States')

# Add a legend
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))  # Adjust legend position

# Show the plot
plt.grid(True)
plt.show()