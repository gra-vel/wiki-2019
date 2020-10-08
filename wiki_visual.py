"""
Created on Fri Sep 18 09:42:12 2020

@author: Gabriel Velástegui
"""

import pandas as pd
import plotly.express as px
import plotly.io as pio 
pio.renderers.default='browser' 


def lang_plot(df, access, language):
    '''
    Plots a line graph for each month of the dataframe
    Dataframe comes from class wiki_analysis.wiki_all_access
    Args:
        df: dataframe from get_df() or access_analysis()
        access: desktop, mobile-app, mobile-web or total (str)
        language: English, Spanish, German, Russian (str)
    '''
    month_views={}
    for i in range(1,13):
        month_views[i] = df[df['month'].isin([i])]
        month_views[i] = month_views[i].rename(columns={'article':'Article',
                                                        'timestamp':'Date',
                                                        access:'Views'})
        month_views[i]['Date'] = pd.to_datetime(month_views[i]['Date'], format='%Y%m%d%H')
        month_views[i]['Article'] = month_views[i]['Article'].str.replace('_',' ')        
    
    # print('Adding traces...')
    fig = px.line(month_views[1], x='Date', y='Views', color='Article', template='plotly_white') #hover_name='Article', hover_data=['Views']
    # print('Month: 1')
    for j in range(2, 13):
        # print('Month: ' + str(j))
        for i in range(0,10):
            fig.add_trace(px.line(month_views[j], x='Date', y='Views', color='Article').data[i])
    
    # print('Update menus')
    updatemenus = [dict(type = 'buttons',
                        direction = 'right', 
                        xanchor = 'left', 
                        yanchor = 'bottom', 
                        x = 0, 
                        y = -0.15, 
                        font = dict(size=9, color='#000000'),
                        buttons = list([
                            dict(args=[{'visible':[True if x > 0 and x < 121 else False for x in range(1,121)]},
                                       ],
                                 label = "All", method = "restyle"),
                            dict(args=[{'visible':[True if x > 0 and x < 11 else False for x in range(1,121)]},
                                       ],
                                 label = "January", method = "restyle"),
                            dict(args=[{'visible':[True if x > 10 and x < 21 else False for x in range(1,121)]},
                                       ],
                                 label = "February", method = "restyle"),
                            dict(args=[{'visible':[True if x > 20 and x < 31 else False for x in range(1,121)]},
                                       ],
                                 label = "March", method = "restyle"),
                            dict(args=[{'visible':[True if x > 30 and x < 41 else False for x in range(1,121)]},
                                       ],
                                 label = "April", method = "restyle"),
                            dict(args=[{'visible':[True if x > 40 and x < 51 else False for x in range(1,121)]},
                                       ],
                                 label = "May", method = "restyle"),
                            dict(args=[{'visible':[True if x > 50 and x < 61 else False for x in range(1,121)]},
                                       ],
                                 label = "June", method = "restyle"),
                            dict(args=[{'visible':[True if x > 60 and x < 71 else False for x in range(1,121)]},
                                       ],
                                 label = "July", method = "restyle"),
                            dict(args=[{'visible':[True if x > 70 and x < 81 else False for x in range(1,121)]},
                                       ],
                                 label = "August", method = "restyle"),
                            dict(args=[{'visible':[True if x > 80 and x < 91 else False for x in range(1,121)]},
                                       ],
                                 label = "September", method = "restyle"),
                            dict(args=[{'visible':[True if x > 90 and x < 101 else False for x in range(1,121)]},
                                       ],
                                 label = "October", method = "restyle"),
                            dict(args=[{'visible':[True if x > 100 and x < 111 else False for x in range(1,121)]},
                                       ],
                                 label = "November", method = "restyle"),
                            dict(args=[{'visible':[True if x > 110 and x < 121 else False for x in range(1,121)]},
                                       ],
                                 label = "December", method = "restyle"),                            
                            ])),
                   ]
    
    fig.update_layout(
        width=1000,
        height=700,
        autosize=False,
        title = language + ' Wikipedia for 2019',
        titlefont=dict(size=20,
                       color='#7f7f7f'),
        xaxis_title="",
        hoverlabel=dict(font_size=11), 
        hovermode='x',
        updatemenus = updatemenus,        
        legend_title_text='Articles'
        )
    
    fig.update_traces(mode="lines", hovertemplate='Views: %{y:,.0f}') #<extra></extra>
    
    fig.show()

