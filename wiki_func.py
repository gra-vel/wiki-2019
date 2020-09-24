"""
Created on Wed Aug  5 16:54:44 2020

@author: Gabriel Velástegui
"""

import datetime
import matplotlib.pyplot as plt
import seaborn as sns

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


def all_access_analysis(df):
    '''
    for all-access dataframe. gets views percentage according each access per day.
    also normalizes views per article and month.
    df: dataframe
    return: df
    '''
    df = df.assign(total = df['desktop'] + df['mobile-app'] + df['mobile-web'],
                   desk = df['desktop']/(df['desktop'] + df['mobile-app'] + df['mobile-web']),
                   app = df['mobile-app']/(df['desktop'] + df['mobile-app'] + df['mobile-web']),
                   web = df['mobile-web']/(df['desktop'] + df['mobile-app'] + df['mobile-web']))
    
    df = df.rename(columns = {'desktop':'norm_desk',
                              'mobile-app':'norm_app',
                              'mobile-web':'norm_web'})
    
    grouper = df.groupby(['month','article'])['norm_desk']
    maxes = grouper.transform('max')
    mins = grouper.transform('min')
    df = df.assign(norm_desk=(df.norm_desk- mins)/(maxes - mins))
    
    grouper = df.groupby(['month','article'])['norm_app']
    maxes = grouper.transform('max')
    mins = grouper.transform('min')
    df = df.assign(norm_app=(df.norm_app - mins)/(maxes - mins))
    
    grouper = df.groupby(['month','article'])['norm_web']
    maxes = grouper.transform('max')
    mins = grouper.transform('min')
    df = df.assign(norm_web=(df.norm_web- mins)/(maxes - mins))
    
    df = df[['article', 'timestamp', 'month', 'days', 'desk', 'app', 'web', 'total', 'norm_desk', 'norm_app', 'norm_web']]
    return df
    

def article_heatmap(df, article, month):
    '''
    creates heatmap for method of access and number of views
    df: dataframe
    article: str
    month: int
    '''
    try:
        df = df[df['month'].isin([month])]
        df.loc[:,'Date'] = df['timestamp'].apply(lambda x:x.strftime('%m/%d'))
        df = df.drop(columns=['timestamp'])
        df.set_index('Date', inplace = True)
        fig, (ax1,ax2) = plt.subplots(1,2)
        sns.heatmap(df[df['article'].isin([article])][['desk', 'app', 'web']],
            cmap=sns.color_palette('viridis'),
            annot = True,
            robust = False,
            ax = ax1)
        ax1.set_title(article + "/" + str(month) + ": by access (percentage per day)")
        sns.heatmap(df[df['article'].isin([article])][['norm_desk', 'norm_app', 'norm_web']], 
            cmap=sns.diverging_palette(220, 20, as_cmap=True),
            ax = ax2)
        ax2.set_title(article + "/" + str(month) + ": views (normalized per month)")
        ax2.set_xticklabels(ax2.get_xticklabels(),rotation=0)
        plt.show()
    except ValueError:
        plt.close(fig)
        print("ValueError: article not found. use '_' to connect words.")