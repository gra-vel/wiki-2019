"""
Created on Wed Aug  5 14:16:28 2020

@author: Gabriel Velástegui
"""

import wiki_func
import urllib.request, json
import pandas as pd

# Importing monthly data
def month_data(lang, access, year):
    '''
    lang: string (en, es, de, etc.)
    access: string (all-access, desktop, mobile-app, mobile-web)
    year: string (YYYY)
    lang is the language of the project. access is the platform of access
    year is the year of query
    converts json to dataframe and saves it as csv file.
    '''
	initial_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/top/"
	proj = lang + ".wikipedia.org/"
	user_access = access + "/"
	base_url = initial_url + proj + user_access + year + "/"	
	for i in range(1,13):
		print("importing: " + lang + " " + str(i) + "-" + year)
		with urllib.request.urlopen(base_url + str(i).zfill(2) + "/all-days") as url:
			data = json.loads(url.read().decode())
			df = pd.json_normalize(data["items"][0]["articles"])
			df = df.iloc[0:50]
			df = df[~df.article.str.contains('Wikipedia:|Especial:|Special:|Spécial:|Anexo:|Martina_Stoessel|Lali_Espósito')].reset_index(drop = True)
			df = df.iloc[0:15] #_increased to 15 because of bot searches
			df.to_csv("dataset\\" + year + "_" + str(i).zfill(2) + "_" + lang + "_wikimonth.csv", index = False, encoding = 'latin')

# Importing daily data
def daily_data(lang, access, agent, year, month):
    df = pd.read_csv("dataset\\" + year + "_" + month + "_" + lang + "_wikimonth.csv", encoding = "latin1")
    df = df.iloc[0:10]
    top_articles = df.article.to_list()
    #loop for articles
    base_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
    user_access = access + "/"
    user_agent = agent + "/"
    pre_url = base_url + lang + ".wikipedia.org/" + user_access + user_agent
    st = 0
    for article in top_articles:
        #looping over month
        start_date, end_date = wiki_func.daterange(year, month)
        wiki_url = pre_url + quote(article) + "/daily/" + start_date + "/" + end_date
        #importing daily data
        with urllib.request.urlopen(wiki_url) as url:
            data = json.loads(url.read().decode())
        df1 = pd.json_normalize(data["items"])
        df1 = df1.iloc[:,[1,3,6]]        
        if st == 0:
            df_month = df1
            st +=1
        else:
            df_month = pd.concat([df_month, df1])
    return df_month