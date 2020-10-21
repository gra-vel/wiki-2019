"""
Created on Wed Aug  5 16:54:44 2020

@author: Gabriel Velástegui
"""

import datetime
import pandas as pd


def daterange(year, month):
    '''
    creates start and end date for daily data fn
    year: string
    month: string
    return: string for date
    '''
    first_day = datetime.date(int(year), int(month), 1)
    if int(month) < 12:
        last_day = datetime.date(int(year), int(month)+1, 1) - datetime.timedelta(days=1)
    else:
        last_day = datetime.date(int(year)+1, 1, 1) - datetime.timedelta(days=1)
    return (first_day.strftime("%Y%m%d"), last_day.strftime("%Y%m%d"))


def create_url(lang, access, agent):
    '''
    creates list with urls for api
    lang: string
    access: string
    agent: string
    return: list of strings
    '''
    all_url = []
    initial_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/" + lang + ".wikipedia.org"    
    l_access = ['desktop','mobile-app','mobile-web']    
    if access == "all-access":
        for each_access in l_access:
            all_url.append(initial_url + "/" + each_access + "/" + agent + "/")
    else:
        all_url.append(initial_url + "/" + access + "/" + agent + "/")
    return all_url


def change_view_access(df, access, sf):
    '''
    changes name of column 'views' to string in 'access'
    df: dataframe
    access: string
    sf: int
    return: df
    '''
    dict_agents = {0:"desktop", 1:"mobile-app", 2:"mobile-web"}
    if access == "all-access":        
        df = df.rename(columns={'views':dict_agents[sf]})        
    else:
        pass    
    return df


def format_analysis(df):
    '''
    changes format of columns in dataframe
    df: dataframe
    return: df
    '''
    #for timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%d%H')
    df['week'] = [d.isoweekday() for d in df['timestamp']]
    #for article
    df['article'] = df['article'].str.replace('_', ' ')
    df = df.rename(columns = {'desktop_1':'desktop'})
    return df