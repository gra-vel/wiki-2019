"""
Created on Mon Sep 28 12:06:17 2020

@author: Gabriel Velástegui
"""

import wiki_func
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class Wiki_all_access(object):
    """
    Data analysis of most viewed Wikipedia articles by access and month
    """
    def __init__(self, filename, encoding):
        '''
        Initialize an instance, which reads data from csv file. Adds column for days.
        csv file has to come from wiki_import.daily_data
        Args:
            filename: name of csv file (str)
            encoding: encoding of csv file - latin1/utf-16 (str)
        '''
        self.df = pd.read_csv("dataset\\" + filename, encoding = encoding)
        self.df['days'] = self.df.groupby(["month", "article"]).cumcount()+1
        
    
    def get_df(self):
        '''
        Returns:
            dataframe with raw data plus total views
        '''
        self.df = self.df.assign(total = self.df['desktop'] + self.df['mobile-app'] + self.df['mobile-web'])
        return self.df
    
    
    def access_analysis(self):
        '''
        Calculate total views and percent of views by each method of access.
        Normalize monthly views by each method of access.
        Changes format of 'timestamp' and 'article'
        Returns:
            dataframe with percent and normalized data
        '''
        #total and percent views
        df_analysis = self.df.assign(total = self.df['desktop'] + self.df['mobile-app'] + self.df['mobile-web'],
                                     desktop_1 = self.df['desktop']/(self.df['desktop'] + self.df['mobile-app'] + self.df['mobile-web']),
                                     app = self.df['mobile-app']/(self.df['desktop'] + self.df['mobile-app'] + self.df['mobile-web']),
                                     web = self.df['mobile-web']/(self.df['desktop'] + self.df['mobile-app'] + self.df['mobile-web']))
        
        #normalized data
        df_analysis = df_analysis.rename(columns = {'desktop':'desktop_norm',
                                                    'mobile-app':'app_norm',
                                                    'mobile-web':'web_norm'})
        
        grouper = df_analysis.groupby(['month','article'])['desktop_norm']
        maxes = grouper.transform('max')
        mins = grouper.transform('min')
        df_analysis = df_analysis.assign(desktop_norm=(df_analysis.desktop_norm - mins)/(maxes - mins))
        
        grouper = df_analysis.groupby(['month','article'])['app_norm']
        maxes = grouper.transform('max')
        mins = grouper.transform('min')
        df_analysis = df_analysis.assign(app_norm=(df_analysis.app_norm - mins)/(maxes - mins))
        
        grouper = df_analysis.groupby(['month','article'])['web_norm']
        maxes = grouper.transform('max')
        mins = grouper.transform('min')
        df_analysis = df_analysis.assign(web_norm=(df_analysis.web_norm - mins)/(maxes - mins))
        
        #format of timestamp and article
        df_analysis = wiki_func.format_analysis(df_analysis)        
        
        df_analysis = df_analysis[['article', 'timestamp', 'month', 'days', 'desktop', 'app', 'web', 'total', 'desktop_norm', 'app_norm', 'web_norm', 'week']]
        return df_analysis
    
    
    def df_plot(self, month):
        '''
        Gathers columns into rows for plotting.
        Args:
            month: month of analysis (int)
        Returns:
            dataframe sliced by month
        '''
        df_plot = pd.melt(self.access_analysis().drop(columns=['timestamp', 'desktop', 'app', 'web', 'total']),
                          id_vars=['article', 'days', 'week', 'month'],
                          var_name='access',
                          value_name='views')
        df_plot = df_plot[df_plot['month'].isin([month])]
        return df_plot
        
    
    def barplot_month(self, month):
        '''
        Plots histogram of articles' views (normalized) by month.
        Args:
            month: month of analysis (int)
        Returns:
            histogram
        '''
        g = sns.FacetGrid(self.df_plot(month), col='article', row='access', hue='article', margin_titles=True)
        g.map(sns.barplot, 'days', 'views', order=list(range(1,32)))
        #fixes overlayed subtitles
        for ax in g.axes.flat:
            plt.setp(ax.texts, text="")
        g.set_titles(col_template='{col_name}', size=10)
        g.set(xticks=[6,13,20,27],
              xticklabels=(['7','14','21','28']))
        
                           
    def article_heatmap(self, article, month):
        '''
        Plots two heatmaps per article. One with the daily percent of views by access.
        Another with the monthly normalized views by access.
        Note that not all articles are available for all months. In raw data there are
        ten articles per month.
        Args:
            article: name of the article (str)
            month: month of analysis (int)
        Returns:
            heatmaps for article
        '''
        try:
            df_heatmap = self.access_analysis()
            df_heatmap = df_heatmap[df_heatmap['month'].isin([month])]
            df_heatmap.loc[:,'Date'] = df_heatmap['timestamp'].apply(lambda x:x.strftime('%m/%d'))
            df_heatmap = df_heatmap.drop(columns=['timestamp'])
            df_heatmap.set_index('Date', inplace = True)
            
            df_heatmap.desktop = df_heatmap.desktop.mul(100)
            df_heatmap.app = df_heatmap.app.mul(100)
            df_heatmap.web = df_heatmap.web.mul(100)
            
            #plt.rcParams['figure.dpi'] = 100 #it's global
            fig,(ax1,ax2) = plt.subplots(1,2,  figsize=(16, 10))
            fig.subplots_adjust(wspace=0.3)
            
            #first heatmap
            sns.heatmap(df_heatmap[df_heatmap['article'].isin([article])][['desktop','app','web']],
                        cmap=sns.color_palette('viridis'),
                        annot=True,
                        annot_kws={"size":10},
                        fmt='.2f',
                        robust=False,
                        cbar_kws={'format': '%.0f%%'}, #changes colorbar label to percentage
                        ax=ax1)
            for t in ax1.texts: t.set_text(t.get_text() + " %") #adds percentage(%) to value
            ax1.set_title(article + ' - month ' + str(month) + "\nviews (percentage per day)")
            #second heatmap
            sns.heatmap(df_heatmap[df_heatmap['article'].isin([article])][['desktop_norm', 'app_norm', 'web_norm']],
                        cmap=sns.diverging_palette(220, 20, as_cmap=True),
                        ax=ax2)
            ax2.set_title(article + ' - month ' + str(month) + "\nviews (normalized per month)")
            ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0)
        
        except ValueError:
            plt.close(fig)
            print("article not found in month " + str(month))