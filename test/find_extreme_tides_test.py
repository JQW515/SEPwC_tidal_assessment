# -*- coding: utf-8 -*-
"""
Created on Wed May 27 12:54:15 2026

@author: tobyr
"""

def test_find_extreme_tides(self):
    """ Test to verify that find_extreme_tides identifies the correct
    maximum and minimum data"""
    # Creating fake data sets 
    timestamps = pd.to_datetime([
            '2026-01-01 00:00:00',
            '2026-01-01 01:00:00',
            '2026-01-01 02:00:00',
            '2026-01-01 03:00:00'
        ])
    # Setting sea levels
    sea_levels = [1.2, 0.5, 5.5, 3.4]
    
    # Calling extreme tides function with new fake data
    max_val, max_time, min_val, min_time = find_extreme_tides(fake_data)
    
    # Assert (verify) that the outputs match exactly what we expect
    assert max_val == 5.5, f"Expected max level 5.5, but got {max_val}"
    assert max_time == pd.Timestamp('2026-01-01 02:00:00'), f"Expected max time 02:00, but got {max_time}"
        
    assert min_val == 0.5, f"Expected min level 0.5, but got {min_val}"
    assert min_time == pd.Timestamp('2026-01-01 01:00:00'), f"Expected min time 01:00, but got {min_time}"