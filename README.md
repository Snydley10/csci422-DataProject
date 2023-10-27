[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-718a45dd9cf7e7f842a935f5ebbe5719a5e09af4491e668f4dbf3b35d5cca122.svg)](https://classroom.github.com/online_ide?assignment_repo_id=12462577&assignment_repo_type=AssignmentRepo)
# CSCI 422 Project - Brandon Snyder
# Renewable Energy Adoption and Impact on Energy Prices Analysis
## Business Goal
The primary goal of this analysis is to investigate the impact of renewable energy adoption on the total average price of energy, specifically assessing whether increased production and consumption of renewable energy sources over time has led to significant changes to average energy prices on a state-by-state basis. 

Shifting from conventional energy sources towards renewables is of course very important for mitigating anthropogenic greenhouse gas emissions and global climate change. This analysis is going to look at the impact of renewable energy sources on overall energy prices. Key questions to be answered with this analysis include: 

* How has the adoption of renewable energy sources evolved over time at the state level, and what are the trends in renewable energy production and consumption? 

* Are regions with higher levels of renewable energy adoption experiencing a significant reduction in energy prices compared to regions that rely more on conventional energy sources? 

* What is the relationship between renewable energy production and consumption within a state, and how does the balance or disparity between these factors affect the average energy prices in that state? 

## Ingestion
This project uses two datasets that are both ingested from the US Energy Information Administration (EIA) programmatically using their API. The US EIA provides independent and impartial energy data, analyses, and forecasts. This data will be used to analyze trends in renewable energy adoption (Dataset #1) and total average energy prices (Dataset #2) on a state-by-state basis. In my Exploratory Data Analysis I also pivoted the datasets so that they are potentially more usable for the next stages of the project.

#### Pivoted Datasets column names:

#### Dataset #1
* Year, State, TotalEnergyPriceTransportation, TotalEnergyPriceCommercial, TotalEnergyPriceIndustrial, TotalEnergyPriceResidential, TotalEnergyPrice, TotalEndUseEnergyPrice

#### Dataset #2
* Year, State, BiofuelsProduction, BiomassConsumption, GeothermalProduction, GeothermalConsumption, HydropowerConsumption, HydropowerProduction, SolarConsumption, SolarProduction, WoodWasteProduction, WindConsumption, WindProduction

#### Storage
Upon ingestion, the datasets get uploaded and stored in an Azure Data Lake Storage Blob programmatically using an account key. The Raw Data is stored in the RawData folder of the project storage blob.  The pivoted datasets have been stored to the PivotedData folder of the project storage blob.
