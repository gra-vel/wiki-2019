"""
Created on Wed Aug  5 14:16:28 2020

@author: Gabriel Velástegui
"""

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
