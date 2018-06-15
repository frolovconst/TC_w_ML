#!/bin/bash

cd inc/
mkdir det
mkdir inc
mkdir series
mkdir stations
mkdir inc/raw
mkdir inc/light
mkdir series/light
mkdir series/smoothed
mkdir series/st_blacklist
unzip 'all*.zip' 
mv all_text_chp_incident_det* det
mv all_text_chp_incident_day* inc/raw
cd inc/raw
gunzip *.gz
cd ../../det
gunzip *.gz
cd ../
rm all*
