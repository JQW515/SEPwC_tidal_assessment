import pandas as pd
import numpy as np
from tidal_analysis import get_longest_contiguous_data



# Creating dummy data with a gap in
times = pd.date_range("2023-01-01", periods=10, freq="H")
# Skipping 5 hours to create a gap
times2 = pd.date_range("2023-01-01 15:00:00", periods=20, freq="H")
# Merging and adding data
combined_index = times.union(times2)
df = pd.DataFrame({"Sea Level": np.random.rand(len(combined_index))}, index=combined_index)