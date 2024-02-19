[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-718a45dd9cf7e7f842a935f5ebbe5719a5e09af4491e668f4dbf3b35d5cca122.svg)](https://classroom.github.com/online_ide?assignment_repo_id=12462577&assignment_repo_type=AssignmentRepo)
# CSCI 422 - Fundamentals of Data Engineering Project 
# By Brandon Snyder
# Renewable Energy Adoption and Impact on Energy Prices Analysis
## Business Solution
The primary goal of this analysis is to investigate the impact of renewable energy adoption on the total average price of energy, specifically assessing whether increased production and consumption of renewable energy sources over the last 30 years has led to significant changes to average energy prices on a state-by-state basis. This analysis uses data from the Energy Information Administration from 1991 - 2021

Shifting from conventional energy sources towards renewables is of course very important for mitigating anthropogenic greenhouse gas emissions and global climate change. This analysis looks at at the impact of renewable energy sources on overall energy prices. Key questions answered by this analysis include: 

* Q1: Do regions with higher renewable energy adoption experience significant reductions or increases in energy prices?
  * Answer: Regions with higher renewable usage do not experience significant energy price reductions.


* Q2: What are the trends in renewable energy production and consumption?
  * Answer: Trending upwards over time with both almost doubling in the last 30 years.
    * Biomass almost doubled
    * Hydropower had slight decline
    * Wind and Solar had huge increases
    * Geothermal is basically the same


* Q3: How has the adoption of renewable energy sources evolved over time at the state level?
  * It varies some by state but most states have been strongly increasing production and consumption


## Analysis Outcome
### Full Power BI Report: [Project Analysis](https://app.powerbi.com/groups/5cce6a8a-a406-4090-9ed7-9a4878a1f1a9/reports/43661b24-1b11-45c8-b8fb-0a51191083d2/ReportSection3d9d241876f68bcdb6ea?experience=power-bi)

Images from Report:

![Total Renewable Production/Consumption with Total Average Energy Price by Year](https://github.com/dfroslie-ndsu-org/f23-project-Snydley10/assets/101298486/1f6797c0-7327-40a1-ad3e-832cea4c18b9)
Insights:
* Doubling overall in production/consumption
* Energy prices experience overall increase. Past 15 years somewhat stayed the same ($16-$23 range)
* Doesn’t seem to be much correlation between price and renewables.
  * 1991-2007 Production/Consumption was somewhat stagnant yet prices more than doubled
<p>&nbsp;</p>

![Total Renewable Production/Consumption with Total Average Energy Price by State](https://github.com/dfroslie-ndsu-org/f23-project-Snydley10/assets/101298486/e23aa161-aea8-4d28-9563-c52045fd73ae)
Insights:
* This graph gives a clearer look on a state-by-state basis
* Prices seem to be all over the place
  * Higher peaks towards right side but also some of lowest points
* Maybe some slight correlation between higher renewable usage and lower prices
<p>&nbsp;</p>

![Total Production by Energy Source (Billion Btu)](https://github.com/dfroslie-ndsu-org/f23-project-Snydley10/assets/101298486/0c5dc398-6cc5-465a-9720-595237f47665)
![Total Consumption by Energy Source (Billion Btu)](https://github.com/dfroslie-ndsu-org/f23-project-Snydley10/assets/101298486/d75589d2-cebc-49f7-8c5e-be2846702b34)
Insights:
* Biomass usage is about 1.8 times higher than 30 years ago
* Hydropower sees slight decline in past 30 years
* Wind and Solar have huge increases in past 30 years
* Geothermal usage is basically the same
<p>&nbsp;</p>

1991
<p align="center">
  <img src="https://github.com/dfroslie-ndsu-org/f23-project-Snydley10/assets/101298486/d484c9b4-4b59-47a0-8245-5880ef71e1be" width="410" height="220">
  <img src="https://github.com/dfroslie-ndsu-org/f23-project-Snydley10/assets/101298486/7b8d33ae-9617-4902-80ef-13fb62c186e7" width="410" height="220">
</p>

* Biomass: 73% of Production / 46% of Consumption
* Hydropower: 26% of Production / 50% of Consumption


2021
<p align="center">
  <img src="https://github.com/dfroslie-ndsu-org/f23-project-Snydley10/assets/101298486/d5f3874f-fdfc-46a3-81aa-baa96d57595e" width="410" height="220">
  <img src="https://github.com/dfroslie-ndsu-org/f23-project-Snydley10/assets/101298486/ead26fdb-ea5c-48e6-ad3d-8090d68fd618" width="410" height="220">
</p>

* Biomass: 64% of Production / 40% of Consumption
* Hydropower: 11% of Production / 18% of Consumption
* Wind: 17% of Production / 28% of Consumption
* Solar: 7% of Production / 13% of Consumption
* Geothermal: remains around 0-3%
<p>&nbsp;</p>

## Technical Solution
#### High-level Architechture Diagram
![Architechture Diagram](https://github.com/dfroslie-ndsu-org/f23-project-Snydley10/assets/101298486/5c864e4d-1cf9-43f9-92cb-79cb60114337)

#### Technologies Used
![Technologies](https://github.com/dfroslie-ndsu-org/f23-project-Snydley10/assets/101298486/5b0f5796-a6d7-4688-b66b-6038d3081e2e)
<p>&nbsp;</p>

### Ingestion
This project uses two datasets that are both ingested from the US Energy Information Administration (EIA). The US EIA provides independent and impartial energy data, analyses, and forecasts. Datasets were retrieved programmatically using the EIA's API with batch and offset because of the large size of the data. Queries were developed using their website’s API Explorer. The datasets were stored in Pandas Dataframes and then converted to CSV files. This data is used to analyze trends in renewable energy adoption (Dataset #1) and total average energy prices (Dataset #2) on a state-by-state basis.

#### Dataset #1 - EIARenewablesByState.csv
* Year, State, Energy Source Production/Consumption, Unit

#### Dataset #2 - EIATotalEnergyPricesByState.csv
* Year, State, Total Average Energy Price for Sector, Unit

#### Storage
Upon ingestion, the datasets get uploaded and stored in an Azure Data Lake Storage Blob programmatically using an account key. The Raw Data is stored in the RawData folder of the project storage blob.  
<p>&nbsp;</p>

### Transformation
Most transformation took place during the Exploratory Data Analysis (EDA).

Transformations:
* Converted all energy values to Billion Btu (some were million kWh)
* Pivoted datasets so each row contains all values for year/state pair
* Added Units column back
* Changed column names from acronyms to more descriptive names
* Set any null values to zero (only a few)
* Some minor transformation in Power BI to prepare for visualization

#### Transformed Dataset #1
* Each row has all renewable energy source production/consumption values for year/state pair
* Columns: Year, State, BiofuelsProduction, BiomassConsumption, GeothermalProduction, GeothermalConsumption, HydropowerConsumption, HydropowerProduction, SolarConsumption, SolarProduction, WoodWasteProduction, WindConsumption, WindProduction

#### Transformed Dataset #2
* Each row has all total average energy prices in each sector for year/state pair
*  Columns: Year, State, TotalEnergyPriceTransportation, TotalEnergyPriceCommercial, TotalEnergyPriceIndustrial, TotalEnergyPriceResidential, TotalEnergyPrice, TotalEndUseEnergyPrice

#### Storage
After transformations, the datasets get uploaded and stored in an Azure Data Lake Storage Blob programmatically using an account key. The Transformed Data is stored in the PivotedData folder of the project storage blob.  
<p>&nbsp;</p>

### Serving
* Uploaded pivoted datasets to Power BI from Azure Blob Storage
* Created new aggregate column of year/state in each dataset to create 1 to 1 relationship
* Did some minimal cleaning up of datasets for better visualization
* Created four Power BI pages to fully visualize and explore datasets and their relationship
<p>&nbsp;</p>

## Implementation Details

### Repo Structure
Source Code located in src directory with a folder for ingestion, transformation, and serving. Raw and Pivoted Datasets also located in src.
* ingestion contains DataSet1.py, DataSet2.py, and ExploratoryAnalysis.py
* transformation contains Transformation.py
* serving contains ProjectAnalysis.pbix

### Project Reproduction
In order to reproduce the project, keep the information below in mind.

* Cloud Resources
  * Need Azure Storage Account with blob storage set up for storing of datasets.
    * Note: datasets may be stored locally as well if you do not wish to use an Azure Storage Account
  * Set up an EIA account in order to get an API key
  * In your repo you will need to create .config files for your Azure and EIA keys

* Ingestion
  * DataSet1.py and DataSet2.py need to be edited to upload to your specific Azure Blob Storage
  * The API calls need to be edited to use your EIA account key .config file
  * Datasets can be refreshed by changing API call to a newer year
 
* Transformation
  * Transformation.py needs to be edited to upload to your specific Azure Blob Storage
  * Everything else should work seamlessly for transforming the data
 
* Serving
  * Connect Power BI to your Azure Blob Storage to get the data
  * If the datasets change or get updated in Azure, Power BI should reflect that or else the refresh button can be clicked
