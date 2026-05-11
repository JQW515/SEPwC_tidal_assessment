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
    # df = data frame
    # Using pandas to read data
    # Skip rows gets past long header
    df = pd.read_csv(filename, sep = "\s+", skiprows = 11, header = None)
    # Giving columns useful names
    df.columns = ["Index","Date","Time","Sea Level","Residual"]
    # Cleaning the data removing non-numeric data 
    df.replace(to_replace = ".*[A-Z]$",value = {'Sea Level':np.nan},regex = True,inplace = True)
    # Ensure Sea Level is numeric
    df['Sea Level'] = pd.to_numeric(df['Sea Level'], errors = 'coerce')
    # Combining date and time strings into a single object
    df["datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"])
    # Set the new datetime column as the index
    df.set_index("datetime", inplace=True)
    
    # Return only Sea Level
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
    # Remove NaN values, uptide can't handle them
    clean_data = data.dropna()
    # Create the tide object for the specific constituents
    tide = uptide.Tides(constituents)
    # Tells uptide when the dataset begins
    tide.set_initial_time(start_datetime)
    # Convert to standard datetime index
    clean_index = clean_data.index.tz_localize(None) if clean_data.index.tz else clean_data.index
    # Make sure start_datetime is timezone-naive
    start_dt = start_datetime.replace(tzinfo=None) if hasattr(start_datetime, 'tzinfo') and start_datetime.tzinfo else start_datetime
    # Convert the DatetimeIndex into seconds since the start time
    seconds = np.array([(t - start_dt).total_seconds() for t in clean_index])
    # Performing the analysis
    amp, pha = uptide.harmonic_analysis.solve_least_squares(tide, data['Sea Level'].values, seconds)
    
    return amp, pha

def get_longest_contiguous_data(data):
    # Calculate the differnce between rows within the data
    time_diffs = data.index.to_series().diff()
    # Checks for no gaps, if there are none, data is returned
    if time_diffs.empty or len(time_diffs) <= 1:
        return data
    # Finding the mode step between data recordings
    expected_step = time_diffs.mode().iloc[0]
    # Indentifying where gaps larger than the mode gap
    gap_mask = time_diffs > expected_step
    # Assign each block of data a unique id
    group_ids = gap_mask.cumsum()
    # Finds which id block has the most rows
    largest_group_id = group_ids.value_counts().idxmax()
    # Filers out all data expect the largest block
    longest_data = data[group_ids == largest_group_id].copy()

    return longest_data


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
