"""
Created on Wed Aug  5 16:54:44 2020

@author: Gabriel Velástegui
"""

from datetime import timedelta, date

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

