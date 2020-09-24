"""
Created on Fri Sep 18 09:42:12 2020

@author: Gabriel Velástegui
"""

import wiki_func
import pandas as pd
import seaborn as sns
import sys
sys.exit("Neeet. Nelzya ispolsovat' takoy kommand")

# Analysis of views per language (ex. for English Wikipedia)
# Importing data
df_month_en = pd.read_csv("dataset\\2019_en_wikidaily.csv", encoding = "utf-16")

# Getting count of days
df_month_en['days'] = df_month_en.groupby(["month", "article"]).cumcount()

# Apply function to get percentage of daily access and normalized values of views
df_monthly = wiki_func.all_access_analysis(df_month_en)

# Identify days of the week
df_monthly['timestamp'] = pd.to_datetime(df_monthly['timestamp'], format='%Y%m%d%H')
df_monthly['weekends']= [d.isoweekday() for d in df_monthly['timestamp']]

# Distribution barplot from normalized values
df_graph = pd.melt(df_monthly.drop(columns=['timestamp', 'desk', 'app', 'web', 'total']),
                   id_vars=['article', 'days', 'weekends', 'month'],
                   var_name='access',
                   value_name='views')
df_graph = df_graph[df_graph['month'].isin([1])] #change month

g = sns.FacetGrid(df_graph, col='article', row='access', hue = 'article', margin_titles=True)
g.map(sns.barplot,'days', 'views', order=list(range(1,32)))
g.set_titles(col_template="{col_name}", size=8.5)
g.set(xticks=[5,15,25])

#Heatmaps for article (use df_monthly)
wiki_func.article_heatmap(df_monthly, 'Ted_Bundy', 1)


