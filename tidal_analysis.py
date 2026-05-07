# import the modules we need
import pandas as pd
import datetime
import os
import numpy as np
import uptide
import pytz
import math
from scipy import stats
import matplotlib.dates as mdates
import argparse


def read_tidal_data(filename):
    """df = data frame"""
    df = pd.read_csv(filename, sep = "\s+", skiprows = 11, header = None)
    df.columns = ["Index","Date","Time","Sea Level","Residual"]
    df.replace(to_replace = ".*[A-Z]$",value = {'Sea Level':np.nan},regex = True,inplace = True)
    df['Sea Level'] = pd.to_numeric(df['Sea Level'], errors = 'coerce')
    df["datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"])
    df.set_index("datetime", inplace=True)

    return df[["Sea Level"]]

    
def extract_single_year_remove_mean(year, data):
    # Convert year into integer
    year_int = int(year)
    # Filter data for a specific year
    single_year_data = data[data.index.year == year_int].copy()
    # Calculating the mean sea level for that year
    annual_mean = single_year_data ["Sea Level"].mean()
    # Subracting the mean year from the data
    single_year_data ["Sea Level"] = single_year_data ["Sea Level"] - annual_mean
    
    return single_year_data


def extract_section_remove_mean(start, end, data):
    # Slice the data at the start and end
    section_data = data.loc[start:end].copy()
    # Calculate the mean of the Sea Level within the section of data
    section_mean = section_data["Sea Level"].mean()
    # Subtract the mean from the Sea Level data
    section_data["Sea Level"] = section_data["Sea Level"] - section_mean
    
    return section_data


def join_data(data1, data2):
    #ensuring the data in continuous and in correct order
    return pd.concat([data1, data2]).sort_index()

def sea_level_rise(data):
     
    return 

def tidal_analysis(data, constituents, start_datetime):

    return

def get_longest_contiguous_data(data):
    time_diffs = data.index.to_series().diff()
    
    if time_diffs.empty or len(time_diffs) <= 1:
        return data
    expected_step = time_diffs.mode().iloc[0]
    gap_mask = time_diffs > expected_step
    group_ids = gap_mask.cumsum()
    

    return 


def main(args_list=None):

    parser = argparse.ArgumentParser(
                     prog="UK Tidal analysis",
                     description="Calculate tidal constiuents and RSL from tide gauge data",
                     )

    parser.add_argument("directory",
                    help="the directory containing txt files with data")
    parser.add_argument('-v', '--verbose',
                    action='store_true',
                    default=False,
                    help="Print progress")

    args = parser.parse_args(args_list)
    dirname = args.directory
    verbose = args.verbose

    print("Add your code here to do things!")
    

if __name__ == '__main__':
    main()
