"""
Created on Wed Aug  5 14:16:28 2020

@author: Gabriel Velástegui
"""

import wiki_func
import pandas as pd
import urllib.request, json
from urllib.parse import quote

# Importing monthly data
def month_data(lang, access, year):
    '''
    retrieves dataset of top viewed articles for whole year.
    converts json to dataframe and saves it as csv file.
    lang: string (en, es, de, etc.) / language of the project
    access: string (all-access, desktop, mobile-app, mobile-web) / platform of access
    year: string (YYYY) / year of query
    '''
    initial_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/top/"
    proj = lang + ".wikipedia.org/"
    user_access = access + "/"
    base_url = initial_url + proj + user_access + year + "/"
    #loop for each month of the year
    for i in range(1,13):
        print("importing: " + lang + " " + str(i) + "-" + year)
        with urllib.request.urlopen(base_url + str(i).zfill(2) + "/all-days") as url:
            data = json.loads(url.read().decode())
            df = pd.json_normalize(data["items"][0]["articles"])
            df = df.iloc[0:50]
            #exceptions
            df = df[~df.article.str.contains('Wikipedia:|Especial:|Special:|Spécial:|Anexo:|Martina_Stoessel|Lali_Espósito')].reset_index(drop = True)
            df = df.iloc[0:15] #_increased to 15 because of bot searches
            df['month'] = str(i).zfill(2)            
            if i == 1:                
                ini_df = df
            else:
                ini_df = pd.concat([ini_df, df])
    ini_df.to_csv("dataset\\" + year + "_" + lang + "_wikimonth.csv", index = False, encoding = 'latin')

# month_data("es", "all-access", "2019")

# Importing daily data
def daily_data(lang, access, agent, year):
    '''
    retrieves daily data based on output of month_data fn
    lang: string (en, es, de, etc.) / language of the project
    access: string (all-access, desktop, mobile-app, mobile-web) / platform of access
    agent : string (all-agents, user, spider, automated) / agent type
    year: string (YYYY) / year of query
    month: string (MM) / month of query
    
    return: dataframe
    '''
    encode_lang = {'en':'UTF-8', 'es': 'latin1', 'de':'UTF-8'}
    df1 = pd.read_csv("dataset\\" + year + "_" + lang + "_wikimonth.csv", encoding = encode_lang[lang])
    st = 0
    for i in range(1,13):
        df = df1[df1['month'].isin([i])]
        df = df.iloc[0:10]
        top_articles = df.article.to_list()
        #loop for articles
        initial_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
        user_access = access + "/"
        user_agent = agent + "/"
        base_url = initial_url + lang + ".wikipedia.org/" + user_access + user_agent
        for article in top_articles:
            print('retrieving: ' + article + ' views for ' + str(i) + '/' + year)
            #looping over month
            start_date, end_date = wiki_func.daterange(year, str(i))
            wiki_url = base_url + quote(article) + "/daily/" + start_date + "/" + end_date
            #importing daily data
            with urllib.request.urlopen(wiki_url) as url:
                data = json.loads(url.read().decode())
            df2 = pd.json_normalize(data["items"])
            df2 = df2.iloc[:,[1,3,6]] #picks columns of interest
            df2['month'] = i
            if st == 0:
                df_month = df2
                st +=1
            else:
                df_month = pd.concat([df_month, df2])
    return df_month

# df_month = daily_data("es", "all-access", "all-agents", "2019")
# df_month.to_csv("dataset\\" + "2019" + "_" + "es" + "_wikidaily.csv", index = False, encoding = 'latin')
