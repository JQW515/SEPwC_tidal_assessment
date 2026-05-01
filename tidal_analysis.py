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
    # filter data for a specific year
    year_data = data[data.index.year == year]
    
    

    return 


def extract_section_remove_mean(start, end, data):

    return year_data


def join_data(data1, data2):

    return 

def sea_level_rise(data):

    return

def tidal_analysis(data, constituents, start_datetime):

    return

def get_longest_contiguous_data(data):

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
