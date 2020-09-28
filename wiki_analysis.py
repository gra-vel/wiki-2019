"""
Created on Mon Sep 28 12:06:17 2020

@author: Gabriel Velástegui
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class wiki_all_access(object):
    """
    Data analysis of most viewed Wikipedia articles by access and month
    """
    def __init__(self, filename, encoding):
        '''
        Initialize an instance, which reads data from csv file. Adds column for days
        Args:
            filename: name of csv file (str)
            encoding: encoding of csv file - latin1/utf-16 (str)
        '''
        self.df = pd.read_csv("dataset\\" + filename, encoding = encoding)
        self.df['days'] = self.df.groupby(["month", "article"]).cumcount()
        
    
    def get_df(self):
        '''
        Returns:
            dataframe with raw data
        '''
        return self.df
    
    
    def access_analysis(self):
        '''
        Calculate total views and percent of views by each method of access.
        Normalize monthly views by each method of access.
        Changes format of 'timestamp'
        Returns:
            dataframe with percent and normalized data
        '''
        #total and percent views
        df_analysis = self.df.assign(total = self.df['desktop'] + self.df['mobile-app'] + self.df['mobile-web'],
                                     desk = self.df['desktop']/(self.df['desktop'] + self.df['mobile-app'] + self.df['mobile-web']),
                                     app = self.df['mobile-app']/(self.df['desktop'] + self.df['mobile-app'] + self.df['mobile-web']),
                                     web = self.df['mobile-web']/(self.df['desktop'] + self.df['mobile-app'] + self.df['mobile-web']))
        
        #normalized data
        df_analysis = df_analysis.rename(columns = {'desktop':'norm_desk',
                                                    'mobile-app':'norm_app',
                                                    'mobile-web':'norm_web'})
        
        grouper = df_analysis.groupby(['month','article'])['norm_desk']
        maxes = grouper.transform('max')
        mins = grouper.transform('min')
        df_analysis = df_analysis.assign(norm_desk=(df_analysis.norm_desk- mins)/(maxes - mins))
        
        grouper = df_analysis.groupby(['month','article'])['norm_app']
        maxes = grouper.transform('max')
        mins = grouper.transform('min')
        df_analysis = df_analysis.assign(norm_app=(df_analysis.norm_app - mins)/(maxes - mins))
        
        grouper = df_analysis.groupby(['month','article'])['norm_web']
        maxes = grouper.transform('max')
        mins = grouper.transform('min')
        df_analysis = df_analysis.assign(norm_web=(df_analysis.norm_web- mins)/(maxes - mins))
        
        #format of timestamp
        df_analysis['timestamp'] = pd.to_datetime(df_analysis['timestamp'], format='%Y%m%d%H')
        df_analysis['week']= [d.isoweekday() for d in df_analysis['timestamp']]
        
        df_analysis = df_analysis[['article', 'timestamp', 'month', 'days', 'desk', 'app', 'web', 'total', 'norm_desk', 'norm_app', 'norm_web', 'week']]            
        return df_analysis
    
    
    def df_plot(self, month):
        '''
        Gathers columns into rows for plotting.
        Args:
            month: month of analysis (int)
        Returns:
            dataframe sliced by month
        '''
        df_plot = pd.melt(self.access_analysis().drop(columns=['timestamp', 'desk', 'app', 'web', 'total']),
                          id_vars=['article', 'days', 'week', 'month'],
                          var_name='access',
                          value_name='views')
        df_plot = df_plot[df_plot['month'].isin([month])]
        return df_plot
        
    
    def histogram_month(self, month):
        '''
        Plots histogram of articles' views (normalized) by month.
        Args:
            month: month of analysis (int)
        Returns:
            histogram
        '''
        g = sns.FacetGrid(self.df_plot(month), col='article', row='access', hue='article', margin_titles=True)
        g.map(sns.barplot, 'days', 'views', order=list(range(1,32)))
        g.set_titles(col_template='{col_name}', size=8.5)
        g.set(xticks=[5,15,25])
        
                           
    def article_heatmap(self, article, month):
        '''
        Plots two heatmaps per article. One with the daily percent of views by access.
        Another with the monthly normalized views by access.
        Note that not all articles are available for all months. In raw data there are
        ten articles per month.
        Args:
            article: name of the article. spaces are replaced by '_' (str)
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
            
            fig,(ax1,ax2) = plt.subplots(1,2)
            #first heatmap
            sns.heatmap(df_heatmap[df_heatmap['article'].isin([article])][['desk','app','web']],
                        cmap=sns.color_palette('viridis'),
                        annot=True,
                        robust=False,
                        ax=ax1)
            ax1.set_title(article + '/' + str(month) + ": by access (percentage per day)")
            #second heatmap
            sns.heatmap(df_heatmap[df_heatmap['article'].isin([article])][['norm_desk', 'norm_app', 'norm_web']],
                        cmap=sns.diverging_palette(220, 20, as_cmap=True),
                        ax=ax2)
            ax2.set_title(article + '/' + str(month) + ": views (normalized per month)")
            ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0)
        
        except ValueError:
            plt.close(fig)
            print("article not found. use '_' to connect words.")