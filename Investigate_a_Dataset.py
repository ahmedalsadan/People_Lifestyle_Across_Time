#!/usr/bin/env python
# coding: utf-8

# # Project: Investigate a Dataset - [Gapminder World]
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# ### Dataset Description 
# 
# > Gapminder has collected a lot of information about how people live their lives in different countries, tracked across the years, and on a number of different indicators. The tables used are child mortality(0-5 year-olds dying per 1000 born), income per person (GDP per Capita, PPP-dollar inflation-adjusted), and life expectancy years(the average number of years a newborn child would live).
# 
# 
# ### Questions for Analysis
# >Have certain regions of the world been growing in some indicators better than others? 
# 
# >Are there trends that can be observed between the indicators? 

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
plt.style.use('seaborn')


# <a id='wrangling'></a>
# ## Data Wrangling
# 

# In[298]:


# Loading and printing out the three tables
df1 = pd.read_excel('child_mortality_0_5_year_olds_dying_per_1000_born.xlsx')
df1.head()


# In[9]:


df1.shape


# In[299]:


df2 = pd.read_excel('income_per_person_gdppercapita_ppp_inflation_adjusted.xlsx')
df2.head()


# In[10]:


df2.shape


# In[300]:


df3 = pd.read_excel('life_expectancy_years.xlsx')
df3.head()


# In[20]:


df3.shape


# In[301]:


df1=df1.melt(id_vars=["country"],var_name="year") # reshaping the tables to display the years and the indicators in columns
df2=df2.melt(id_vars=["country"],var_name="year")
df3=df3.melt(id_vars=["country"],var_name="year")


# In[118]:


df1.head()


# In[119]:


df2.head()


# In[120]:


df3.head()


# In[302]:


df12=pd.merge(df1,df2,on=['country','year']) # merging the first two tables
df=pd.merge(df12,df3,on=['country','year']) # merging the the third table with them


# In[167]:


df.head()


# In[303]:


df.rename(columns = {'value_x':'child_mortality_per_1000_born', 'value_y':'income_per_person',
                              'value':'life_expectancy_years'}, inplace = True) # renaming the indicators columns
df.head()


# In[39]:


df.value_counts(df['country']).tail(11)


# In[44]:


df.info()


# In[45]:


df.isna().sum() # checking missing values


# In[304]:


df=df.dropna().reset_index(drop=True) # dropping the missing values
df.head()


# In[51]:


df.value_counts(df['country']).tail(11) # there are some countries having incomplete data for the whole duration of the years


# In[305]:


df=df[df['country'].isin(['Hong Kong, China','Andorra','Dominica','Nauru','Marshall Islands',
'Tuvalu','Monaco','St. Kitts and Nevis','Palau','San Marino']) == False].reset_index(drop=True)
df.head()                                             # dropping the countries having incomplete data


# In[63]:


df.dtypes # the type of the income_per_person column is object. So, it has to be converted into a numeric type


# In[306]:


income=[]                                                      # converting the object type of the column into a numeric type
for i in df['income_per_person']:
    if type(i)==str:
            i=i.replace('k','')
            income.append(float(i)*1000)
    else:
        income.append(i)


# In[310]:


df['income_per_person']=income             # replacing the object column with the numeric column
df


# In[313]:


avg_child_mortality=[]
avg_income=[]
avg_life_years=[]
for i in df['country'][:185] :        
    avg_child_mortality_value=df[df['country']==i]['child_mortality_per_1000_born'].rolling(20, min_periods=1).mean()
    avg_child_mortality.append(avg_child_mortality_value)
    
    avg_income_value=df[df['country']==i]['income_per_person'].rolling(20, min_periods=1).mean()
    avg_income.append(avg_income_value)
    
    avg_life_years_value=df[df['country']==i]['life_expectancy_years'].rolling(20, min_periods=1).mean()
    avg_life_years.append(avg_life_years_value)                   # calculating 20-year moving averages for the three indicators


# In[314]:


avg_child_mortality=avg_child_mortality[0].append(avg_child_mortality[1:]).sort_index()
avg_income=avg_income[0].append(avg_income[1:]).sort_index() # making every list as one list instead of list of lists
avg_life_years=avg_life_years[0].append(avg_life_years[1:]).sort_index() 


# In[331]:


df.insert(3,"avg_child_mortality",avg_child_mortality) # adding the columns of the moving averages
df.insert(5,"avg_income",avg_income)
df.insert(7,"avg_life_years",avg_life_years)
df.head()


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# 
# ### Have certain regions of the world been growing in some indicators better than others?

# In[419]:


def plot(countries,indicator):
    for i in countries:
        plt.rcParams["figure.figsize"] = (20,10)
        plt.plot(df['year'].unique(),df[df['country']==i][indicator],label=i)
        plt.xlabel('year', fontsize=18)
        if indicator=='avg_child_mortality':
            plt.title('20-Year MA of child mortality per 1000 born', fontsize=22)
            plt.ylabel('child mortality per 1000 born', fontsize=18)
            
        elif indicator=='avg_income':
            plt.title('20-Year MA of income per person', fontsize=22)
            plt.ylabel('income per person', fontsize=18)
            
        elif indicator=='avg_life_years':
            plt.title('20-Year MA of life expectancy years', fontsize=22)
            plt.ylabel('life expectancy years', fontsize=18)
            
                    # defining a function for visualizing the moving averages of the indicators of countries across years
        plt.legend(fontsize=20)


# ##### The plot below clarifies that the Scandinavian countries have been shrinking in child mortality much better than the Latin American countries, especially in the last two centuries.

# In[420]:


plot(['Norway','Sweden','Denmark','Brazil','Panama','Bolivia'],'avg_child_mortality')


# ##### The plot below clarifies that the countries of East Asia have been growing in incomes much better than the African countries beginning from the second half of the twentieth century.

# In[421]:


plot(['Malaysia','South Korea','Japan','Benin','Nigeria','Kenya'],'avg_income')


# ##### The plot below clarifies that the Western countries have been growing in life expectancy years much better than the countries of Central Asia, including the last two centuries and the first half of the current century.

# In[422]:


plot(['Tajikistan','Kazakhstan','Uzbekistan','Switzerland','Canada','United Kingdom'],'avg_life_years')


# ### Are there trends that can be observed between the indicators?

# ##### In the plots below, it can be observed that there are a negative correlation between the average child mortality and the average incomes, a negative correlation between the average child mortality and the average life expectency years, and a positive correlation between the average incomes and the average life expectency years.

# In[496]:


sns.heatmap(df[['avg_child_mortality','avg_income','avg_life_years']].corr());


# In[467]:


sns.pairplot(df[['avg_child_mortality','avg_income','avg_life_years']],height=4);


# ##### The table below shows the correlation coefficients of the indicators.

# In[461]:


df[['avg_child_mortality','avg_income','avg_life_years']].corr()


# <a id='conclusions'></a>
# ## Conclusions
# 
# > There are increases in incomes and decreases in child mortality and life expectency years across time in all of the world.
# 
# > The East Asia and Western countries have positive indicators much better than the African, Central Asia and Latin Americans countries. 
# 
# > The correlation coefficients of the indicators are -0.55 for the correlation which is between the average child mortality and the average incomes, -0.95 for the correlation which is between the average child mortality and the average life expectency years, and 0.62 for the correllation which is between the average incomes and the average life expectency years.
# 
# > The limitation of the dataset is that some countries have missing values in their data.

# <a id='references'></a>
# ## References
# 
# > stackoverflow, geeksforgeeks, w3schools, pandas, and towardsdatascience websites.
