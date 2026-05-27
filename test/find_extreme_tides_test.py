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
    