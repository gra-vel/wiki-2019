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
    encode_lang = {'en':'utf-16', 'es': 'latin1', 'de':'utf-16', 'ru':'utf-16'}
    exceptions_lang = {'es':'Wikipedia:|Especial:|Special:|Spécial:|Anexo:|Martina_Stoessel|Lali_Espósito|Kayden_Boche',
                       'en':'Wikipedia:|Especial:|Special:|Spécial:|Anexo:|Main_Page|Portal:|File:|XHamster|Grover|Louis_Tomlinson|Rheology|Line_shaft|William_Murdoch|Kayden_Boche',
                       'de':'Wikipedia:|Especial:|Special:|Spécial:|Spezial:|Benutzer:|Datei:|Hauptseite|Anthocyane|Antoni_Tàpies|Formelsammlung_Trigonometrie|Pornhub|XHamster|Tobias_Sammet|Edguy|Avantasia|St�ckgut|Sch�ttgut|F�rdertechnik',
                       'ru':'Wikipedia:|Especial:|Special:|Заглавная_страница|Служебная:|Википедия:|Файл:|Borderlands:_The_Pre-Sequel!|YouTube'}
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
            df = df[~df.article.str.contains(exceptions_lang[lang])].reset_index(drop = True)
            # if lang == 'es':
            #     df = df[~df.article.str.contains('Wikipedia:|Especial:|Special:|Spécial:|Anexo:|Martina_Stoessel|Lali_Espósito|Kayden_Boche')].reset_index(drop = True)
            df = df.iloc[0:15] #_increased to 15 because of bot searches
            df['month'] = str(i).zfill(2)            
            if i == 1:                
                ini_df = df
            else:
                ini_df = pd.concat([ini_df, df])
    ini_df.to_csv("dataset\\" + year + "_" + lang + "_wikimonth.csv", index = False, encoding = encode_lang[lang])

# month_data("es", "all-access", "2019")
# month_data("en", "all-access", "2019")
# month_data("de", "all-access", "2019")
# month_data("ru", "all-access", "2019")

# Importing daily data
def daily_data(lang, access, year, agent='user'):
    '''
    retrieves daily data based on output of month_data fn
    lang: string (en, es, de, etc.) / language of the project
    access: string (all-access, desktop, mobile-app, mobile-web) / platform of access
    agent : string (all-agents, user, spider, automated) / agent type
    year: string (YYYY) / year of query
    month: string (MM) / month of query
    
    return: dataframe
    '''
    #check language for encoding
    encode_lang = {'en':'utf-16', 'es':'latin1', 'de':'utf-16', 'ru':'utf-16'}
    #read csv with monthly data
    df1 = pd.read_csv("dataset\\" + year + "_" + lang + "_wikimonth.csv", encoding = encode_lang[lang])
    month_loop = 0
    #loop for months
    for i in range(1,13):
        df = df1[df1['month'].isin([i])]
        df = df.iloc[0:10]
        top_articles = df.article.to_list()
        url_list = wiki_func.create_url(lang, access, agent)
        sf = 0
        #loop for urls (depends on access and agents)
        for each_url in url_list:
            start_date, end_date = wiki_func.daterange(year, str(i))
            st = 0
            #loop for articles
            for article in top_articles:
                print('retrieving: ' + article + ' views for ' + str(i) + '/' + year)
                wiki_url = each_url + quote(article) + "/daily/" + start_date + "/" + end_date
                with urllib.request.urlopen(wiki_url) as url:
                    data = json.loads(url.read().decode())
                df2 = pd.json_normalize(data["items"])
                df2 = df2.iloc[:,[1,3,6]]
                df2['month'] = i
                #appends data for different articles
                if st == 0:
                    df_month = df2
                    st +=1
                else:                    
                    df_month = pd.concat([df_month, df2]).reset_index(drop=True)
            #merges data for same month, different access
            if sf == 0:
                df3 = wiki_func.change_view_access(df_month, access, sf)
                sf += 1
            else:
                df_month = wiki_func.change_view_access(df_month, access, sf)
                df_month = df_month.iloc[:,2]
                df3 = pd.merge(df3, df_month, left_index=True, right_index=True)
                sf += 1            
        #appends complete data for different months
        if month_loop == 0:
            df_end = df3
            month_loop += 1
        else:
            df_end = pd.concat([df_end, df3])
    return df_end

df_month_es = daily_data("es", "all-access", "2019")
df_month_en = daily_data("en", "all-access", "2019")
df_month_de = daily_data("de", "all-access", "2019")
df_month_ru = daily_data("ru", "all-access", "2019")

df_month_es.to_csv("dataset\\" + "2019" + "_" + "es" + "_wikidaily.csv", index = False, encoding = 'latin')
