"""
Created on Wed Aug  5 16:54:44 2020

@author: Gabriel Velástegui
"""

import datetime

def daterange(year, month):
    '''
    creates start and end date for daily data fn
    year: string
    month: string
    '''
    first_day = datetime.date(int(year), int(month), 1)
    if int(month) < 12:
        last_day = datetime.date(int(year), int(month)+1, 1) - datetime.timedelta(days=1)
    else:
        last_day = datetime.date(int(year)+1, 1, 1) - datetime.timedelta(days=1)
    return (first_day.strftime("%Y%m%d"), last_day.strftime("%Y%m%d"))
    
