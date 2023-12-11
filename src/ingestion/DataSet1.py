# %%
# DataSet1.py - script to extract data from its source and load into ADLS.
print("DataSet1 ingestion")

# Imports
import pandas as pd
from azure.storage.filedatalake import DataLakeServiceClient
import requests
import json

# %% Method to connect to an Azure storage account with an account key.
def initialize_storage_account(storage_account_name, storage_account_key):
    
    try:  
        global service_client

        service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
            "https", storage_account_name), credential=storage_account_key)
    
    except Exception as e:
        print(e)
        
# %% Connect to Azure project storage account with account key
storage_account_name = "projectstorage1"

with open("src\keys\ADLSKey.config") as f:
    storage_account_key=f.readline()

initialize_storage_account(storage_account_name, storage_account_key)

print(service_client)

# %% API call for complete dataset (energy generation and consumption for each renewable source by state and year)
with open("src\keys\EIA-Key.config") as f:
    eia_key=f.readline()

request_params = {"api_key" : eia_key,
                     "start" : "1990",
                     "end"   : "2021",
                     "sort[0][column]" : "period",
                     "sort[0][direction]" : "desc",
                     "sort[1][column]" : "stateId",
                     "sort[1][direction]" : "asc",
                     "data[]"           : "value",
                     "facets[seriesId][]": "BFPRB",
                     "facets[seriesId][]": "BMTCB",
                     "facets[seriesId][]": "GEEGP",
                     "facets[seriesId][]": "GETCB",
                     "facets[seriesId][]": "HYTCB",
                     "facets[seriesId][]": "HYTCP",
                     "facets[seriesId][]": "SOTCB",
                     "facets[seriesId][]": "SOTGP",
                     "facets[seriesId][]": "WWPRB",
                     "facets[seriesId][]": "WYTCB",
                     "facets[seriesId][]": "WYTCP",
}

data = []
api_url ="https://api.eia.gov/v2/seds/data/?frequency=annual&data[0]=value&facets[seriesId][]=BFPRB&facets[seriesId][]=BMTCB&facets[seriesId][]=GEEGP&facets[seriesId][]=GETCB&facets[seriesId][]=HYTCB&facets[seriesId][]=HYTCP&facets[seriesId][]=SOTCB&facets[seriesId][]=SOTGP&facets[seriesId][]=WWPRB&facets[seriesId][]=WYTCB&facets[seriesId][]=WYTCP&start=2013&sort[0][column]=stateId&sort[0][direction]=asc&sort[1][column]=period&sort[1][direction]=desc&offset=0&length=5000"
offset = 0
batch_size = 5000

while True:
    request_params["offset"] = offset
    request_params["length"] = batch_size

    api_response = requests.get(api_url, params=request_params)
    response_json = json.loads(api_response.content)

    data.extend(response_json['response']['data'])

    # If the number of records retrieved is less than the batch size, it means there's no more data to fetch.
    if len(response_json['response']['data']) < batch_size:
        break

    offset += batch_size

print(api_response.content)

# %% Convert to Pandas dataframe and save as CSV
renewables_df = pd.DataFrame(data)

print(renewables_df)

renewables_df.to_csv("src\RawData\EIARenewablesByState.csv")

# %% Directory and file client creation for upload to Azure
container_name = "project"
folder_name = "RawData"
file_name = "EIARenewablesByState.csv"

# Create a directory client
directory_client = service_client.get_directory_client(container_name, folder_name)

# Create a file client within the directory
file_client = directory_client.create_file(file_name)

print("File created in ADLS")

# %% Upload the CSV to Azure directory
upload_file_path = "src\RawData\EIARenewablesByState.csv"
upload_file = open(upload_file_path,'r')

file_contents = upload_file.read()

file_client.upload_data(file_contents, overwrite=True)

print(upload_file_path, " has been successfully uploaded to ADLS")