1. Download data from http://pems.dot.ca.gov/?dnode=Clearinghouse
1.1. Download series data

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
          -Apr  
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
