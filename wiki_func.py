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


def create_url(lang, access, agent):
    all_url = []
    initial_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/" + lang + ".wikipedia.org"    
    l_access = ['desktop','mobile-app','mobile-web']
    l_agent = ['user','spider','automated']
    if access == "all_access" and agent == "all_agent":
        for each_access in l_access:
            for each_agent in l_agent:
                all_url.append(initial_url + "/" + each_access + "/" + each_agent + "/")
    elif access == "all_access":
        for each_access in l_access:
            all_url.append(initial_url + "/" + each_access + "/" + agent + "/")
    elif agent == "all_agent":
        for each_agent in l_agent:
            all_url.append(initial_url + "/" + access + "/" + each_agent + "/")
    else:
        all_url.append(initial_url + "/" + access + "/" + agent + "/")
    return all_url