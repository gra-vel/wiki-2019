"""
Created on Fri Sep 18 09:42:12 2020

@author: Gabriel Velástegui
"""

import wiki_func
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Analysis of views per language (ex. for English Wikipedia)
df_month_en = pd.read_csv("dataset\\2019_en_wikidaily.csv", encoding = "utf-16")
df_month_en['days'] = df_month_en.groupby(["month", "article"]).cumcount()

df_monthly = wiki_func.all_access_analysis(df_month_en)

# Distribution barplot from normalized values
df_graph = pd.melt(df_monthly.drop(columns=['timestamp', 'desk', 'app', 'web', 'total']),
                   id_vars=['article', 'days', 'month'],
                   var_name='access',
                   value_name='views')
df_graph = df_graph[df_graph['month'].isin([10])]

g = sns.FacetGrid(df_graph, col='article', row='access', margin_titles=True)
g.map(sns.barplot,'days', 'views', order=list(range(1,32)))
g.set_titles(col_template="{col_name}", size=8.5)
g.set(xticks=[5,15,25])


#Heatmaps for article
df2 = df_monthly[df_monthly['month'].isin([10])]
df2.set_index('timestamp', inplace = True)
fig, (ax1,ax2) = plt.subplots(1,2)
sns.heatmap(df2[df2['article'].isin(["Joker_(2019_film)"])][['desk', 'app', 'web']], 
            annot = True,
            robust = False,
            ax = ax1)
sns.heatmap(df2[df2['article'].isin(["Joker_(2019_film)"])][['norm_desk', 'norm_app', 'norm_web']], 
            ax = ax2)
plt.show()


df_monthly[df_monthly['article'].isin(['Luke_Perry'])][['article', 'timestamp', 'desk', 'app', 'web']]
df_monthly[['article']]