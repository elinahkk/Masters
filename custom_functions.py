from __future__ import print_function, division
import numpy as np
import pandas as pd
import glob

def gatherStationData():
    """
    Search the local Data/ folder for *.csv files, generate a list.
    Extract metadata (station name) from the file names, and identify the
    start and end years of each file.
    
    """
    flist = list_files()
    station_dics = {}
    print("Reading in csv data...")
    for f_in in flist:
        start,end = find_timespan(f_in)
        station = station_name(f=f_in)
        print("File: {0}   Station: {1}  {2}--{3}".format(f_in, 
                                                        station, start, end))
        station_dics[station] = read_precip(fname=f_in, 
                                label=station, start_year=start, end_year=end)
    data_list = []
    for s in station_dics:
        data_list.append(station_dics[s]) 
    return pd.concat(data_list,axis=1)


def list_files(path=None):
    """
    Return a list of  .csv files in a local folder called Data,
    or from a given path location.
    """
    if path == None:
        return glob.glob('Data/*.csv')
    else:
        return glob.glob(path+'*.csv')

    
def find_timespan(f):
    """
    Return the first and last years in any given .csv file
    """
    open_file = pd.read_csv(f)
    return int(open_file.keys()[0]), int(open_file.keys()[-1])


def read_precip(fname, label, start_year, end_year):
    """
    Read precipitation data that has the Feb 29th bug, and has been saved to csv.
    fname: string of file path
    label: string you want the station to appear as in the data frame
    """
    data_in = pd.read_csv(fname)
    #leaps = [1960+n*4 for n in range(20)]  # Create a list of leap years
    dailys = []
    for year in data_in:
        for n,day in enumerate(data_in[year].values):
            if n == 59:   # if we are looking at the 59th element (added feb 29th)
                
                if int(year)/4 % 1  == 0.0:  # year/4 modulus 1 = 0.0 (leap years)
                #if int(year) in leaps:
                    dailys.append(day)
                else:
                    pass
            else:
                dailys.append(day) 
    dailys = np.array(dailys)
    mask = dailys > 99.
    dailys[mask] = np.nan
    start_date = '01-01-'+str(start_year)
    end_date = '31-12-'+str(end_year)
    #print(start_date, end_date)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    return pd.DataFrame(data=dailys,columns=[label],index=dates)


def station_name(f):
    """
    From the file name (f), extract the station name. Gets the data
    from the file name directly and assumes the file
    name is formatted as Data/Station_info.csv.
    """
    return f.split('/')[1].split('_')[0]