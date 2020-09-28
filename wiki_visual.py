"""
Created on Fri Sep 18 09:42:12 2020

@author: Gabriel Velástegui
"""

import wiki_analysis
import pandas as pd
import plotly.express as px
import plotly.io as pio 
pio.renderers.default='browser' 
import sys
sys.exit("Neeet. Nelzya ispolsovat' takoy kommand")

wiki_en = wiki_analysis.wiki_all_access("2019_en_wikidaily.csv", "utf-16")
wiki_month_en = wiki_en.get_df()
wiki_month_en = wiki_month_en.assign(total = wiki_month_en['desktop'] + wiki_month_en['mobile-app'] + wiki_month_en['mobile-web'])

wiki_es = wiki_analysis.wiki_all_access("2019_es_wikidaily.csv", "latin1").get_df()
wiki_de = wiki_analysis.wiki_all_access("2019_de_wikidaily.csv", "utf-16").get_df()
wiki_ru = wiki_analysis.wiki_all_access("2019_ru_wikidaily.csv", "utf-16").get_df()

def lang_plot(df, access):
    month_views={}
    for i in range(1,13):
        month_views[i] = df[df['month'].isin([i])]
        month_views[i] = month_views[i].rename(columns={'article':'Article',
                                                        'timestamp':'Date',
                                                        access:'Views'})
        month_views[i]['Date'] = pd.to_datetime(month_views[i]['Date'], format='%Y%m%d%H')
    
    print('Adding traces...')
    fig = px.line(month_views[1], x='Date', y='Views', color='Article')
    for j in range(2, 13):
        for i in range(0,10):
            fig.add_trace(px.line(month_views[j], x='Date', y='Views', color='Article').data[i])
    
    print('Update menus')
    updatemenus = [dict(type = 'buttons',
                        direction = 'down',
                        buttons = list([
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
                            dict(args=[{'visible':[True if x > 0 and x < 121 else False for x in range(1,121)]},
                                       ],
                                 label = "All", method = "restyle"),
                            ])),
                   ]
    
    fig.update_layout(updatemenus = updatemenus,
                  legend_title_text='')
    
    fig.show()
        
lang_plot(wiki_month_en, 'total')

wiki_es = wiki_es.assign(total = wiki_es['desktop'] + wiki_es['mobile-app'] + wiki_es['mobile-web'])
lang_plot(wiki_es, 'total')

wiki_de = wiki_de.assign(total = wiki_de['desktop'] + wiki_de['mobile-app'] + wiki_de['mobile-web'])
lang_plot(wiki_de, 'total')

wiki_ru = wiki_ru.assign(total = wiki_ru['desktop'] + wiki_ru['mobile-app'] + wiki_ru['mobile-web'])
lang_plot(wiki_ru, 'total')



wiki_en.article_heatmap('Brooklyn',10)