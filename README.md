# wiki-2019

## Wikipedia searches 2019

The goal of this project is to analyze the trend of articles’ views in Wikipedia for four languages (English, Spanish, German and Russian) in 2019. The code for this analysis is limited to this specific project and works best if all ways of accessing Wikipedia are taken into account (desktop, mobile app and mobile web).

**The interactive plots are displayed in nbviewer -- [Jupyter notebook](https://nbviewer.jupyter.org/github/gra-vel/wiki-2019/blob/master/wiki_2019.ipynb)**

There are three main parts in the project: import and wrangling, analysis and visualization. I used `pandas`, `plotly` and `seaborn`.

### Import and wrangling

For this purpose, I created two functions in `wiki_import`.

For data import, I used the Wikimedia REST API v1.0.0. Data comes in JSON format and it gets turned into a data frame. First, I import the top viewed articles for each month applying a filter to remove certain articles or pages that are not relevant or that may get their views from an automated program. The names of these articles are in a dictionary to separate them by language. 

Next, I import daily data for each article in each month. The views for each article are classified according access method (desktop, mobile app and mobile web). I implemented time intervals when importing this data, as it helps not to lose connection with the server. This error kept appearing at the start of the project.

The data frame for monthly and daily data was saved as csv file in the folder dataset. I used this process to create a dataset for each of the four languages and making sure to use encoding when saving files, so I would not lose any special characters in articles’ titles. 

### Analysis

This section refers to the script `wiki_analysis`. The goal of this part is to identify articles, for which its views may come from automated programs. In this way, I can include these articles in the exception dictionary from the previous script.

The class wiki_all_access is initialized by importing the csv file from the output of wiki_import, which is the data frame with daily data. There are three main methods in this class: one for analysis and two to visualize preliminary data.

For analysis, the corresponding method calculates the proportion of views of all articles by access method. Next, it normalizes data from articles’ views by month, so it is possible to identify the points in the month when each article was viewed the most.

One method produces a bar plot of the normalized views of all articles in a month. Each article has three plots, one by each method of access. The second method produces two heat maps; one for the daily percentage of views by method of access and another for the normalized views per month.

### Visualization

After excluding the articles that may have had its views from automated programs, I create a line chart with plotly in the script `wiki_visual`. The plot has the ten most viewed articles each month. Views come from all methods of access and it is possible to check individual months to have a clearer view of individual trends. Plots are individual for each language.

`wiki_func` has helper functions for the scripts.

### Further development

The scripts could be adapted for additional years. Each year would need its own analysis to determine which articles should be excluded, due to possible automated views. It would be possible to add an additional function capable of sorting out which articles may have automated views. 

 ### Update 2020
 
 Data from year 2020 was added.
