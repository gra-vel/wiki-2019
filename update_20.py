# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 11:23:01 2021

@author: G3
"""
import wiki_import
import wiki_analysis
import wiki_visual
import pandas as pd

### 2020 Update

# Importing monthly data
#wiki_import.month_data("es", "all-access", 2020)
#wiki_import.month_data("en", "all-access", 2020)
wiki_import.month_data("de", "all-access", 2020)
wiki_import.month_data("ru", "all-access", 2020)

# Importing daily data
#es_daily = wiki_import.daily_data("es", "all-access", 2020)
#en_daily = wiki_import.daily_data("en", "all-access", 2020)
de_daily = wiki_import.daily_data("de", "all-access", 2020)
ru_daily = wiki_import.daily_data("ru", "all-access", 2020)

# Save new files
#es_daily.to_csv("dataset\\2020_es_wikidaily.csv", index = False, encoding = "latin1")
#en_daily.to_csv("dataset\\2020_en_wikidaily.csv", index = False, encoding = "utf-16")
de_daily.to_csv("dataset\\2020_de_wikidaily.csv", index = False, encoding = "utf-16")
ru_daily.to_csv("dataset\\2020_ru_wikidaily.csv", index = False, encoding = "utf-16")


# Analysis
#es_daily = pd.read_csv("dataset\\2020_es_wikidaily.csv", encoding = "latin1")
es_wiki20 = wiki_analysis.Wiki_all_access("2020_es_wikidaily.csv", "latin1")
es_wiki20.barplot_month(12)
es_wiki20.article_heatmap("Francisco Sagasti", 11)
#Lali Espósito 1,2,4
#Pandemia de gripe de 1918 4
#Zoidaco <,7,9,10
#Cleopatra 9,10,11,12
#Traducción 9,10
#YouTube 9

en_wiki20 = wiki_analysis.Wiki_all_access("2020_en_wikidaily.csv", "utf-16")
en_wiki20.barplot_month(12)
en_wiki20.article_heatmap("2009 flu pandemic", 3)
#Media 1
#United States Senate 2,3,4
#Wikipedia 2
#Bible 5,6,7,8,9,10,11
#Template: 5
    #Under_arms 1
    #Laptop 3
    #Cleopatra 12

#Visualization
wiki_visual.lang_plot(es_wiki20.get_df(), "total", "Spanish")
wiki_visual.lang_plot(en_wiki20.get_df(), "total", "English")
