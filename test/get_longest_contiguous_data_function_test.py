# Copyright (c) 2026 Toby Read
# Some rights reserved
# AI Assistance Notice: Developed with assistance from Gemini (Google AI)


import pandas as pd
import numpy as np
from tidal_analysis import get_longest_contiguous_data


def test_longest_contiguous_logic():
    # Creating dummy data with a gap in
    times = pd.date_range("2023-01-01", periods=10, freq="h")
    # Skipping 5 hours to create a gap
    times2 = pd.date_range("2023-01-01 15:00:00", periods=20, freq="h")
    # Merging and adding data
    combined_index = times.union(times2)
    df = pd.DataFrame({"Sea Level": np.random.rand(len(combined_index))}, index=combined_index)
    # Sending gapped data into the function
    longest = get_longest_contiguous_data(df)
    # Checking the function is correct, the second block of data is longer
    assert len(longest) == 20
    
