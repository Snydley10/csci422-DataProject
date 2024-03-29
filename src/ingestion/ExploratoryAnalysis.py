# %% ExploratoryAnalysis.py - script to do EDA (exploratory data analysis) on the two primary data sets for the project. 
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from azure.storage.filedatalake import DataLakeServiceClient

# Read in the two dataframes
prices_df = pd.read_csv("src\RawData\EIATotalEnergyPricesByState.csv")
renewables_df = pd.read_csv("src\RawData\EIARenewablesByState.csv")

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
