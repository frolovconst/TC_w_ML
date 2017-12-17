import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.dates as mdts
import matplotlib.pyplot as plt
from geopy.distance import vincenty


def plot_flow_w_incidents(flow_data, incdnt_data, frw_no, station_no, chrstc_to_plot = 'Avg Speed'):
    hours = mdts.HourLocator()
    datemin = dt.datetime(year=2017, month=10, day=11, hour=8)
    datemax = dt.datetime(year=2017, month=10, day=11, hour=20)
    data_srs_no_null = flow_data.dropna(subset=[chrstc_to_plot])
    data_incdnts_by_frw = incdnt_data[incdnt_data['Freeway']==frw_no]
    dates = data_srs_no_null[(data_srs_no_null['Freeway'] == frw_no) & (data_srs_no_null['Station'] == station_no)]['Timestamp']
    speed = data_srs_no_null[(data_srs_no_null['Freeway'] == frw_no) & (data_srs_no_null['Station'] == station_no)][chrstc_to_plot]
    fig,ax = plt.subplots(figsize=[15,10])
    fig.figsize = [15,10]
    plt.plot_date(dates, speed, fmt='-', tz='EST')
    for x in data_incdnts_by_frw['Timestamp']:
        plt.axvline(x)
    ax.xaxis.set_major_locator(hours)
    fig.autofmt_xdate()
    ax.xaxis.set_major_formatter(mdts.DateFormatter('%H:%M'))
    ax.set_xlim(datemin, datemax)
    plt.grid()
    plt.show()
    
def plot_station_data_w_nearest_incds(flow_data, incdnt_data, stations_data, station_no, vicinity_km, chrstc_to_plot = 'Avg Speed'):
    hours = mdts.HourLocator()
    datemin = dt.datetime(year=incdnt_data.Timestamp.dt.year[0], month=incdnt_data.Timestamp.dt.month[0], day=incdnt_data.Timestamp.dt.day[0], hour=0)
    datemax = dt.datetime(year=incdnt_data.Timestamp.dt.year[0], month=incdnt_data.Timestamp.dt.month[0], day=incdnt_data.Timestamp.dt.day[0], hour=22)
    # filter only data for one station and w/o nans
    data_srs_no_null = flow_data[flow_data['Station'] == station_no]
    data_srs_no_null = data_srs_no_null.dropna(subset=[chrstc_to_plot])
    # station of interest coords
    station_coords = np.asarray(stations_data[stations_data['ID'] == station_no][['Latitude', 'Longitude']])
    # incidents closest to the station
    data_incdnts_nearest = incdnt_data[incdnt_data.apply(lambda x: vincenty((x['Latitude'], x['Longitude']), station_coords).kilometers < vicinity_km, axis=1)]
    # x-values
    dates = data_srs_no_null['Timestamp']
    # y-values
    speed = data_srs_no_null[chrstc_to_plot]
    fig,ax = plt.subplots(figsize=[15,10])
    fig.figsize = [15,10]
    plt.plot_date(dates, speed, fmt='-', tz='EST')
    for x in data_incdnts_nearest['Timestamp']:
        plt.axvline(x)
    ax.xaxis.set_major_locator(hours)
    fig.autofmt_xdate()
    ax.xaxis.set_major_formatter(mdts.DateFormatter('%H:%M'))
    ax.set_xlim(datemin, datemax)
    plt.grid()
    plt.show()
    
    
def plot_two_station_data_w_nearest_incds(flow_data, incdnt_data, stations_data, station_no1, station_no2, vicinity_km, chrstc_to_plot = 'Avg Speed'):
    hours = mdts.HourLocator()
    datemin = dt.datetime(year=incdnt_data.Timestamp.dt.year[0], month=incdnt_data.Timestamp.dt.month[0], day=incdnt_data.Timestamp.dt.day[0], hour=0)
    datemax = dt.datetime(year=incdnt_data.Timestamp.dt.year[0], month=incdnt_data.Timestamp.dt.month[0], day=incdnt_data.Timestamp.dt.day[0], hour=23)
    # filter only data for one station and w/o nans
    data_srs_no_null_1 = flow_data[flow_data['Station'] == station_no1]
    data_srs_no_null_2 = flow_data[flow_data['Station'] == station_no2]
#     data_srs_no_null = data_srs_no_null.dropna(subset=[chrstc_to_plot])
    # station of interest coords
    station_coords = np.asarray(stations_data[stations_data['ID'] == station_no1][['Latitude', 'Longitude']])
    # incidents closest to the station
    data_incdnts_nearest = incdnt_data[incdnt_data.apply(lambda x: vincenty((x['Latitude'], x['Longitude']), station_coords).kilometers < vicinity_km, axis=1)]
    # x-values
    dates1 = data_srs_no_null_1['Timestamp']
    dates2 = data_srs_no_null_2['Timestamp']
    # y-values
    speed1 = data_srs_no_null_1[chrstc_to_plot]
    speed2 = data_srs_no_null_2[chrstc_to_plot]
    fig,ax = plt.subplots(figsize=[15,10])
    fig.figsize = [15,10]
    plt.plot_date(dates1, speed1, fmt='-', tz='EST')
    plt.plot_date(dates2, speed2, fmt='-', tz='EST', color='r')
    for x in data_incdnts_nearest['Timestamp']:
        plt.axvline(x)
    ax.xaxis.set_major_locator(hours)
    fig.autofmt_xdate()
    ax.xaxis.set_major_formatter(mdts.DateFormatter('%H:%M'))
    ax.set_xlim(datemin, datemax)
    plt.grid()
    plt.show()
    
    
def isImpacted(srs, ts, ticks_to_count=3, slowing_coef = .66):
    srs_b4 = srs[srs['Timestamp'] < ts].sort_values(by='Timestamp', ascending=True).iloc[-ticks_to_count:]
    srs_after = srs[srs['Timestamp'] > ts].sort_values(by='Timestamp', ascending=True).iloc[:ticks_to_count]
    if(slowing_coef * srs_b4['Avg Speed'].mean() > srs_after['Avg Speed'].mean()):
        return True
    return False
isImpacted_vec = np.vectorize(isImpacted, excluded=[1,2])


def isImpactedWithNextSt(stationID, n_stationID, srs, ts, ticks_to_count=4, slowing_coef = .9):
    srs_b4 = srs[(srs['Timestamp'] < ts) & (srs['Station']==stationID)].sort_values(by='Timestamp', ascending=True).iloc[-ticks_to_count:]
    n_srs_b4 = srs[(srs['Timestamp'] < ts) & (srs['Station']==n_stationID)].sort_values(by='Timestamp', ascending=True).iloc[-ticks_to_count:]
    srs_after = srs[(srs['Timestamp'] > ts) & (srs['Station']==stationID)].sort_values(by='Timestamp', ascending=True).iloc[:ticks_to_count]
    n_srs_after = srs[(srs['Timestamp'] > ts) & (srs['Station']==n_stationID)].sort_values(by='Timestamp', ascending=True).iloc[:ticks_to_count]
    cond1 = n_srs_b4['Avg Speed'].as_matrix().dot(srs_b4['Avg Speed'].as_matrix())
    cond2 = n_srs_after['Avg Speed'].as_matrix().dot(srs_after['Avg Speed'].as_matrix())
    cond3 = slowing_coef*n_srs_after['Avg Speed'].mean() > srs_after['Avg Speed'].mean()
    if slowing_coef*cond1 > cond2 and cond3: 
        return True
    return False


def isDownstream(incident, station):
    if incident['Freeway_direction'] == 'N':
        return station['Latitude']<incident['Latitude'] #and cond_fwy_match
    elif incident['Freeway_direction'] == 'E':
        return station['Longitude']<incident['Longitude'] #and cond_fwy_match
    elif incident['Freeway_direction'] == 'S':
        return station['Latitude']>incident['Latitude'] #and cond_fwy_match
    elif incident['Freeway_direction'] == 'W':
        return station['Longitude']>incident['Longitude'] #and cond_fwy_match
    return False


def get_next_downstream_station(stations, stationID, incidents, incidentID, correction=.002):
    meta = stations[stations.ID==stationID].iloc[0][['Fwy', 'Dir', 'Latitude', 'Longitude']]
    candidates = stations[(stations['Fwy']==meta[0])&(stations['Dir']==meta[1])].drop(stations.columns[-4:], axis=1).copy()
    if meta[1] == 'S':
        candidates.loc[:,'Distance'] = meta[-2] - candidates['Latitude']
        cond1 = candidates['Latitude'] < incidents[incidents['IncidentID']==incidentID].iloc[0]['Latitude'] - correction
    elif meta[1] == 'N':
        candidates.loc[:,'Distance'] = candidates['Latitude'] - meta[-2]
        cond1 = candidates['Latitude'] > incidents[incidents['IncidentID']==incidentID].iloc[0]['Latitude'] + correction
    elif meta[1] == 'W':
        candidates.loc[:,'Distance'] = meta[-1] - candidates['Longitude']
        cond1 = candidates['Longitude'] < incidents[incidents['IncidentID']==incidentID].iloc[0]['Longitude'] - correction
    else : # meta[1] == 'E':
        candidates.loc[:,'Distance'] = candidates['Longitude'] - meta[-1]
        cond1 = candidates['Longitude'] > incidents[incidents['IncidentID']==incidentID].iloc[0]['Longitude'] + correction
    cond2 = (np.abs(candidates['Distance'])<0.025)
    return candidates[cond1 & cond2 & (candidates['Distance'] > 0)].sort_values(['Distance']).reset_index(drop=True)


def get_neighbouring_station(stations, stationID):
    meta = stations[stations.ID==stationID].iloc[0][['Fwy', 'Dir', 'Latitude', 'Longitude']]
    candidates = stations[(stations['Fwy']==meta[0])&(stations['Dir']==meta[1])].drop(stations.columns[-4:], axis=1).copy()
    if meta[1] == 'S':
        candidates.loc[:,'Distance'] = meta[-2] - candidates['Latitude']
#         cond = 
    elif meta[1] == 'N':
        candidates.loc[:,'Distance'] = candidates['Latitude'] - meta[-2]
    elif meta[1] == 'W':
        candidates.loc[:,'Distance'] = meta[-1] - candidates['Longitude']
    else : # meta[1] == 'E':
        candidates.loc[:,'Distance'] = candidates['Longitude'] - meta[-1]
    cond2 = (np.abs(candidates['Distance'])<0.020)
    return candidates[cond2].sort_values(['Distance']).reset_index(drop=True)


def plot_drctn_station_data_w_nearest_incds(flow_data, incdnt_data, stations_data, station_no, vicinity_km, chrstc_to_plot = 'Avg Speed'):
    hours = mdts.HourLocator()
    datemin = dt.datetime(year=incdnt_data.Timestamp.dt.year[0], month=incdnt_data.Timestamp.dt.month[0], day=incdnt_data.Timestamp.dt.day[0], hour=4)
    datemax = dt.datetime(year=incdnt_data.Timestamp.dt.year[0], month=incdnt_data.Timestamp.dt.month[0], day=incdnt_data.Timestamp.dt.day[0], hour=22)
    # filter only data for one station and w/o nans
    data_srs_no_null = flow_data[flow_data['Station'] == station_no]
    data_srs_no_null = data_srs_no_null.dropna(subset=[chrstc_to_plot])
    # station of interest coords
    station_coords = np.asarray(stations_data[stations_data['ID'] == station_no][['Latitude', 'Longitude']])
    # incidents closest to the station
    data_incdnts_nearest = incdnt_data[incdnt_data.apply(lambda x: vincenty((x['Latitude'], x['Longitude']), station_coords).kilometers < vicinity_km, axis=1)]
    # x-values
    dates = data_srs_no_null['Timestamp']
    # y-values
    speed = data_srs_no_null[chrstc_to_plot]
    fig,ax = plt.subplots(figsize=[15,10])
    fig.figsize = [15,10]
    plt.plot_date(dates, speed, fmt='-', tz='EST')
    for index,x in data_incdnts_nearest.iterrows():
        if isDownstream(x, stations_data[stations_data['ID'] == station_no].iloc[0]):
            plt.axvline(x['Timestamp'])
    ax.xaxis.set_major_locator(hours)
    fig.autofmt_xdate()
    ax.xaxis.set_major_formatter(mdts.DateFormatter('%H:%M'))
    ax.set_xlim(datemin, datemax)
    plt.grid()
    plt.show()
    
    
    
