"""Tidal analysis tools for sea level and harmonic tidal analysis."""
import argparse
import os

import numpy as np
import pandas as pd
import uptide
from scipy import stats
import glob



def read_tidal_data(filename):
    """
    Read tidal gauge data from a text file, sanitize quality flags,
    and return a DataFrame indexed by datetime.
    """
    # df = data frame
    # Using pandas to read data
    # Skip rows gets past long header
    df = pd.read_csv(filename, sep=r"\s+", skiprows=11, header=None)
    # Giving columns useful names
    df.columns = ["Index","Date","Time","Sea Level","Residual"]
    # Cleaning the data removing non-numeric data
    df.replace(to_replace = ".*[A-Z]$",value = {'Sea Level':np.nan},regex=True,inplace=True)
    # Ensure Sea Level is numeric
    df['Sea Level'] = pd.to_numeric(df['Sea Level'], errors='coerce')
    # Combining date and time strings into a single object
    df["datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"])
    # Set the new datetime column as the index
    df.set_index("datetime", inplace=True)

    # Return Sea Level and time
    return df[["Sea Level","Time"]]


def extract_single_year_remove_mean(year, data):
    """
    Filter dataset for a specific year and center the data around a zero mean.
    """
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
    """
    Slice the dataset between specific start and end dates and remove its mean.
    """
    # Slice the data at the start and end
    section_data = data.loc[start:end].copy()
    # Calculate the mean of the Sea Level within the section of data
    section_mean = section_data["Sea Level"].mean()
    # Subtract the mean from the Sea Level data
    section_data["Sea Level"] = section_data["Sea Level"] - section_mean

    return section_data


def join_data(data1, data2):
    """
    Merge two datasets together and sort them chronologically by index.
    """
    #ensuring the data in continuous and in correct order
    return pd.concat([data1, data2]).sort_index()

def sea_level_rise(data):
    """
    Perform linear regression over time to calculate the daily slope trend.
    """
    # Filt
    # Cleaning the data
    clean_data = data.dropna()
    # FIX: Use pure pandas arithmetic to get a completely linear sequence of days,
    # bypassing matplotlib's timezone/DST distortions.
    time_days = (clean_data.index - pd.Timestamp('1970-01-01')) / pd.Timedelta(days=1)
    sea_levels = clean_data['Sea Level'].values

    # Performing stable linear regression
    result = stats.linregress(time_days, sea_levels)

    return result.slope, result.pvalue



def tidal_analysis(data, constituents, start_datetime):
    """
    Decompose the sea level timeline into specific wave harmonic constituents.
    """
    # Remove NaN values, uptide can't handle them
    clean_data = data.dropna()
    # Create the tide object for the specific constituents
    tide = uptide.Tides(constituents)
    # Tells uptide when the dataset begins
    tide.set_initial_time(start_datetime)
    # Convert to standard datetime index
    clean_index = clean_data.index.tz_localize(None) if clean_data.index.tz else clean_data.index
    # Make sure start_datetime is timezone-naive
    if hasattr(start_datetime, "tzinfo") and start_datetime.tzinfo:
        start_dt = start_datetime.replace(tzinfo=None)
    else:
        start_dt = start_datetime
    # Establish our time-anchor point
    tide.set_initial_time(start_dt)
    # Convert the DatetimeIndex into seconds since the start time
    seconds = np.array([(t - start_dt).total_seconds() for t in clean_index])
    # Performing the harmonic analysis
    amp, pha = uptide.harmonic_analysis(tide, clean_data['Sea Level'].values, seconds)

    return amp, pha

def get_longest_contiguous_data(data):
    """
    Isolate and return the single longest continuous stretch of recorded data.
    """
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
    """
    Main entry point function to process gauge directory input arguments.
    """

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

    files = sorted(glob.glob(os.path.join(dirname, "*.txt")))

    # Safety fallback: If directory is empty, exit gracefully
    if not files:
        return

    # Initialize an empty DataFrame to store the master timeline of combined data
    all_data = pd.DataFrame()
    for f in files:
        # Load an individual year file and sanitize invalid characters (M, N, T)
        year_data = read_tidal_data(f)
        # Append and sort chronological timelines while filtering index duplicates
        all_data = join_data(all_data, year_data)

    # Run the linear regression engine to extract daily slope and p-value metrics
    daily_slope = sea_level_rise(all_data)
    # Calculate annual rise
    annual_rise = daily_slope * 365
    # Isolate the single longest block of gap-free measurements for harmonic fitting
    longest_stretch = get_longest_contiguous_data(all_data)
    # Identify constituents of interest mandated by the UK Tidal Database criteria
    constituents = ['M2', 'S2']
    # Run structural wave decomposition starting from the beginning of the continuous section
    amps, phases = tidal_analysis(longest_stretch, constituents, longest_stretch.index[0])

    # Conditional condenced reporting system
    if verbose:
        print(f"Sea-level rise trend: {annual_rise:.6f} m/year")
        for i, c in enumerate(constituents):
            print(f"Constituent {c} -> Amplitude: {amps[i]:.4f} m, Phase: {phases[i]:.4f}")
        else:
            # Silently capture and format analysis metrics into text file if -v is missing
            output_filename = "tidal_output.txt"
            with open(output_filename, "w") as out_file:
                out_file.write(f"Sea-level rise trend: {annual_rise:.6f} m/year\n")
                for i, c in enumerate(constituents):
                    out_file.write(
                        f"Constituent {c} -> "
                        f"Amplitude: {amps[i]:.4f} m, "
                        f"Phase: {phases[i]:.4f}\n"
                    )


if __name__ == '__main__':
    main()
