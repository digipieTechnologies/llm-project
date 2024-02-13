import os
import pathlib
import pandas as pd
from census import Census
import censusgeocode as cg 
from time import process_time
start_time      = process_time()

"""
Known issue - number of columns for subject and chain files need to be dynamic but currently they are not.  If you add a column it will mess up the index of columns we are using to
    come up with store_row error_row.  Right now it is set number of -3 for subject and -4 for chains (they have Visits column)

Code can run 12-15 calls (location2) per minute 
"""
api_key         = 'ab135576f4f133254bea96b2a86eed2b1950467f'
c               = Census(api_key)
# Demos list used later to filter columns for only fields we want
demos           = ['DP02_0016E','DP02_0062PE','DP02_0065PE','DP03_0002PE','DP03_0008PE','DP03_0009PE','DP03_0054PE','DP03_0055PE','DP03_0056PE','DP03_0057PE','DP03_0058PE','DP03_0059PE','DP03_0060PE','DP03_0061PE','DP03_0062E','DP05_0002E','DP05_0002PE','DP05_0003E','DP05_0003PE','DP05_0009PE','DP05_0010PE','DP05_0011PE','DP05_0012PE','DP05_0013PE','DP05_0014PE','DP05_0015PE','DP05_0016PE','DP05_0017PE','DP05_0018E','DP05_0018PE','NAME','LAT','LNG']
# Fields list not yet used
fields          = ['Estimate HOUSEHOLDS BY TYPE Total households Average household size  ','Percent Est EDUCATIONAL ATTAINMENT Population 25 years and over High school graduate (includes equivalency)  ','Percent Est EDUCATIONAL ATTAINMENT Population 25 years and over Bachelors degree  ','Percent Est EMPLOYMENT STATUS Population 16 years and over In labor force  ','Percent Est EMPLOYMENT STATUS Civilian labor force   ','Percent Est EMPLOYMENT STATUS Civilian labor force Unemployment Rate  ','Percent Est INCOME AND BENEFITS (IN 2021 INFLATION-ADJUSTED DOLLARS) Total households $15,000 to $24,999  ','Percent Est INCOME AND BENEFITS (IN 2021 INFLATION-ADJUSTED DOLLARS) Total households $25,000 to $34,999  ','Percent Est INCOME AND BENEFITS (IN 2021 INFLATION-ADJUSTED DOLLARS) Total households $35,000 to $49,999  ','Percent Est INCOME AND BENEFITS (IN 2021 INFLATION-ADJUSTED DOLLARS) Total households $50,000 to $74,999  ','Percent Est INCOME AND BENEFITS (IN 2021 INFLATION-ADJUSTED DOLLARS) Total households $75,000 to $99,999  ','Percent Est INCOME AND BENEFITS (IN 2021 INFLATION-ADJUSTED DOLLARS) Total households $100,000 to $149,999  ','Percent Est INCOME AND BENEFITS (IN 2021 INFLATION-ADJUSTED DOLLARS) Total households $150,000 to $199,999  ','Percent Est INCOME AND BENEFITS (IN 2021 INFLATION-ADJUSTED DOLLARS) Total households $200,000 or more  ','Estimate INCOME AND BENEFITS (IN 2021 INFLATION-ADJUSTED DOLLARS) Total households Median household income (dollars)  ','Estimate SEX AND AGE Total population Male  ','Percent Est SEX AND AGE Total population Male  ','Estimate SEX AND AGE Total population Female  ','Percent Est SEX AND AGE Total population Female  ','Percent Est SEX AND AGE Total population 20 to 24 years  ','Percent Est SEX AND AGE Total population 25 to 34 years  ','Percent Est SEX AND AGE Total population 35 to 44 years  ','Percent Est SEX AND AGE Total population 45 to 54 years  ','Percent Est SEX AND AGE Total population 55 to 59 years  ','Percent Est SEX AND AGE Total population 60 to 64 years  ','Percent Est SEX AND AGE Total population 65 to 74 years  ','Percent Est SEX AND AGE Total population 75 to 84 years  ','Percent Est SEX AND AGE Total population 85 years and over  ','Estimate SEX AND AGE Total population Median age (years)  ','Percent Est SEX AND AGE Total population Median age (years)  ']

"""
Folder read is Subject_File
Folder written to is Subject_Census
RUN setup() IF THIS IS THE FIRST TIME TO RUN
"""

def setup():
    file_path    = pathlib.Path('Subject_File')
    file_path.mkdir(parents=True, exist_ok=True)
    file_path    = pathlib.Path('Subject_Census')
    file_path.mkdir(parents=True, exist_ok=True)
    data = [['test location', 29.8360472, -95.3025319]]
    df = pd.DataFrame(data, columns=['Name', 'lat', 'lng'], index=None) 
    df.to_csv('Subject_File/Subject_File.csv')

# setup()                                                   # run this formula if it is the first time and no files or directories exist

target = ['Subject']                                        # target is a file that has one or more locations to add census data to

"""
Code starts here
"""
counter = 0                                                 # counter is used to give user an idea of the progess of the analysis

for item in target:                                         # run code for each file type(subject location)
    
    target_folder           = item + '_File/'               # has original target file
    target_census_folder    = item + '_Census/'             # has original files with census data added
        
    for file in os.listdir(target_folder):                  # runs code on each file in the folder
        target_df       = pd.read_csv(target_folder + file,
                                      index_col = False)    # create dataframe for file to get census data for
        len_target      = len(target_df)                    # set row number to a variable
        census          = pd.DataFrame()                    # create final dataframe for census data
        wide_target     = target_df.count(1)                # finds the number of columns in dataframe (subject file) not currently used for anything
        counter_stores  = (len(target_df))
        for row in range(len_target):                       # for each row in the target file
            
            lat         = target_df['lat'][row]             # set variable for latitude
            long        = target_df['lng'][row]             # set variable for longitude
            Name        = target_df['Name'][row]            # set variable for adderess
            
            if item == 'Chain':                             # if using a Chain file then set variable for total visits
                visits = target_df['Total Visits'][row] 

            result  = cg.coordinates(x=long, y=lat)         # get census location data from lat, long
            state   = result['States'][0]['STATE']          # set variable for state per the given lat, long
            cnty    = result['Census Tracts'][0]['COUNTY']  # set variable for county per the given lat, long
            tract   = result['Census Tracts'][0]['TRACT']   # set variable for tract per the given lat, long
            group   = ['DP02','DP03','DP04','DP05']         # idenitify data tables from census
            cen = pd.DataFrame()                            # create dataframe for indivisual rows in target file
                
            for group_id in group:  # for each census group run an API call, write results to dataframe
                try:
                    url             = f'https://api.census.gov/data/2021/acs/acs5/profile?get=group({group_id})&&for=tract:{tract}&in=state:{state}%20county:{cnty}&key={api_key}'
                    df              = pd.read_csv(url)
                    census_columns  = -6
                    column_headers  = list(df.columns.values)
                    if column_headers[census_columns] != 'GEO_ID':                                          # code was built for certain column number and this will check to see if that ever changes
                        print('Census columns have changed for ',group_id,' readjust census_columns variable')
                    else:
                        pass    
                    df.iloc[:, 0]   = df.iloc[:, 0].map(lambda x: x.strip('["'))                            # cleanup unwanted characters in dataframe data #CODE_LEVEL_UP
                    df              = df.replace(to_replace={-666666666:0,-888888888:0})                    # POSSIBLE KNOCK ON EFFECTS UNKNOWN AT THIS TIME cleanup unwanted number in dataframe data #CODE_LEVEL_UP
                    cols            = len(df.axes[1])                                                       # count number of coluumns in dataframe to use as index
                    df              = df.iloc[:,:census_columns]                                            # remove non data related columns from dataframe (significant refactor from earlier version n archive)
                    cen             = pd.concat([cen, df], axis = 1, verify_integrity = False, sort = True) # create dataframe with all groups
                except:
                 pass

            # Add name, Lat, Lng columns to dataframe - if more info is to come from Subject file it needs to be added to Subject Census here
            cen['NAME'] = Name
            cen['LAT']  = lat
            cen['LNG']  = long
        
            census = pd.concat([census, cen], axis = 0, verify_integrity = False, sort = False) # combine rows into one dataframe
                        
            census              = census.filter(regex='E$|"$|T$|G$|S$', axis="columns") # removes unwanted columns based on how the name ends #CODELEVELUP
            counter             += 1
            print(counter, ' ',counter_stores, ' ', Name)
            counter_stores      -= 1
            census              = census[demos]                             # filter columns so that only select demos are used
            census.to_csv(target_census_folder + 'Subject_census_data.csv') # save Subjects results to file
            
       

stop_time = process_time()
print("Elapsed time is:", stop_time - start_time)                                      

