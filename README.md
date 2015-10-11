# maude2sqlite
Repository for converting Manufacturer and User Facility Device Experience Database (MAUDE) files into sqlite database

## Folder structure
rawdata -  raw data files from [MAUDE](http://www.fda.gov/MedicalDevices/DeviceRegulationandGuidance/PostmarketRequirements/ReportingAdverseEvents/ucm127891.htm) as well as table declarations and load script
db - location of resultant sqlite db

## Table Definitions
In the rawdata folder there are a series of .tbl files that contain the sql to create each table

## load_data.py
Python script which uses [PANDAS](http://pandas.pydata.org/) to do the following steps (the [Anaconda distro](https://www.continuum.io/downloads) includes all the packages needed):

1. Delete pre-existing database file
2. Create new sqlite db file
3. Process each of our 5 tables by
4. Running the .tbl script for the table
5. Loading each of the raw data files for that table into the sqlite db
6. Committing the changes before moving on to the next table
