1. Download the data for the period of interest from http://pems.dot.ca.gov/?dnode=Clearinghouse (choose district 7 wherever possible; scripts from *_download folders can be used).  
  1.1. Download series data: section "Station 5-Minute".  
  1.2. Download incidents data: sections "CHP Incidents Day" and "CHP Incidents Month".  
  1.3. Download stations data: section "Stations Metadata".
2. Create 'data -> PeMS -> Incidents -> work_folder -> Months -> inc' folders (names must match) in your project root folder. Place unzipping.sh file into 'Months'.  
3. Place the downloaded all_text_chp_incidents_day_yyyy_mm_dd.txt.zip files and all_text_chp_incidents_month_yyyy_mm.txt.zip file for the month of interest into 'inc' folder.  
4. Run unzipping.sh in terminal with 'Months' folder as working directory.  

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
