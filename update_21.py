# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 12:21:39 2022

@author: G3
"""
import wiki_import
import wiki_analysis
import wiki_visual
import pandas as pd

### 2020 Update

# Importing monthly data
# wiki_import.month_data("es", "all-access", 2021)
wiki_import.month_data("en", "all-access", 2021)
# wiki_import.month_data("de", "all-access", 2021)
# wiki_import.month_data("ru", "all-access", 2021)

# Importing daily data
# es_daily = wiki_import.daily_data("es", "all-access", 2021)
en_daily = wiki_import.daily_data("en", "all-access", 2021)
# de_daily = wiki_import.daily_data("de", "all-access", 2021)
# ru_daily = wiki_import.daily_data("ru", "all-access", 2021)

# Save new files
# es_daily.to_csv("dataset\\2021_es_wikidaily.csv", index = False, encoding = "latin1")
en_daily.to_csv("dataset\\2021_en_wikidaily.csv", index = False, encoding = "utf-16")
# de_daily.to_csv("dataset\\2021_de_wikidaily.csv", index = False, encoding = "utf-16")
# ru_daily.to_csv("dataset\\2021_ru_wikidaily.csv", index = False, encoding = "utf-16")

# Analysis
#es_daily = pd.read_csv("dataset\\2021_es_wikidaily.csv", encoding = "latin1")
es_wiki21 = wiki_analysis.Wiki_all_access("2021_es_wikidaily.csv", "latin1")
es_wiki21.barplot_month(12)
es_wiki21.article_heatmap("Caso Wanninkhof", 11)

#en_daily = pd.read_csv("dataset\\2021_en_wikidaily.csv", encoding = "utf-16")
en_wiki21 = wiki_analysis.Wiki_all_access("2021_en_wikidaily.csv", "utf-16")
en_wiki21.barplot_month(5)
en_wiki21.article_heatmap("Charles Sobhraj", 4)


# Visualization
wiki_visual.lang_plot(es_wiki21.get_df(), "total", "Spanish", 2021)
# wiki_visual.lang_plot(en_wiki20.get_df(), "total", "English", 2021)
# wiki_visual.lang_plot(ru_wiki20.get_df(), "total", "Russian", 2021)
# wiki_visual.lang_plot(de_wiki20.get_df(), "total", "German", 2021)
