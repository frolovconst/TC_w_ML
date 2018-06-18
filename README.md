The code found in the files with WHITE_ prefix in the 'incidents_touch' folder should only be used; code from other files is not guaranteed to run smoothly.  
# Downloading and organising data
1. Download the data for the period of interest from http://pems.dot.ca.gov/?dnode=Clearinghouse (choose district 7 wherever possible; scripts from the '*_download' folders can be used).  
  1.1. Download series data: section "Station 5-Minute".  
  1.2. Download incidents data: sections "CHP Incidents Day" and "CHP Incidents Month".  
  1.3. Download stations data: section "Stations Metadata".
2. Create 'data -> PeMS -> Incidents -> work_folder -> Months -> inc' folders (names must match) in your project root folder. Place unzipping.sh file into 'Months'.  
3. Place the downloaded all_text_chp_incidents_day_yyyy_mm_dd.txt.zip files and all_text_chp_incidents_month_yyyy_mm.txt.zip file for the month of interest into 'inc' folder.  
4. Run unzipping.sh in terminal with 'Months' folder as working directory.  
5. Run the 'resave_incs' function from WHITE_raw_data_ordering.ipynb as shown in "Incidents convert to .csv" section of it. 
6. Run 'filter_blk_desc' function from WHITE_raw_data_ordering.ipynb as shown in "Filtering of line blocking incidents" section. All incidents not causing line blockings are removed at this step.  
7. Place the downloaded d07_text_station_5min_yyyy_mm_dd.txt.gz files for the month of interest into 'series/raw' folder.  
8. Run the 'convert_srs_to_csv' function and then the 'smooth_srs' function from WHITE_raw_data_ordering.ipynb as shown in "Series conversion and smoothing" section.  
9. Place the relevant downloaded d07_text_meta_yyyy_mm_dd.txt file into 'stations/raw' folder.  
10. Run the 'resave_stations' function from WHITE_raw_data_ordering.ipynb as shown in "Stations conversion to csv and filtering" section. 
11. Remove the 'raw' folders from 'inc', 'series', and 'stations' folders.  

For the proper functioning of the code from this project, create a 'data -> PeMS -> Incidents -> work_folder -> figs' folder. Then the file hierarchy should look as follows:  
<pre>
-root  
  -code  
    --WHITE ...  
  -data  
    -PeMS  
      -Incidents  
        -work_folder  
          -figs  
          -Months  
            -inc  
              -det  
                --all_text_chp_incident_det_month_2017_04.csv  
              -inc  
                -blkg  
                  --all_text_chp_incident_det_month_2017_04.csv  
                -light  
                  --all_text_chp_incident_day_2017_04_01.csv  
                  -- ...  
                  --all_text_chp_incident_day_2017_04_30.csv  
              -result  
              -series  
                -light  
                  --d07_text_station_5min_2017_04_01.tx.csv  
                  -- ...  
                  --d07_text_station_5min_2017_04_30.tx.csv  
                -smoothed  
                  --d07_text_station_5min_2017_04_01.tx.csv  
                  -- ...  
                  --d07_text_station_5min_2017_04_30.tx.csv  
                -st_blacklist  
                  --stations_blacklist.csv  
              -stations  
                --d07_text_meta_2017_04_29.csv  
</pre>

# Constructing the dataset
To construct the dataset use the WHITE_dataset_construction.ipynb file. The construction may take some time. In particular, the 'create_accident_windows' and 'create_accident_free_windows' functions run for several minutes for data for one month.  
There is some noise in the data. Some sensors demonstrate the same readings for different days, for instance. This has not been dealt with. The only measure for cleaning the data is taken in 'smooth_srs' function during the smoothing of series. It is the removal of sensors whose reading have low variance.  
The weather data is taken from https://accuweather.com.  
# Classifying data
The code used for accident detection over the dataset is contained in the WHITE_accident_detection.ipynb file.
