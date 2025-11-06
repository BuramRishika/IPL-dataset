#!/usr/bin/env python
# coding: utf-8

# Rishika

# In[1]:


import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Title
st.title("IPL Data Analysis Dashboard")

# Load the dataset
data = pd.read_csv("matches(1).csv")
uploaded_file = st.file_uploader("Upload your IPL CSV file", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)  # optional
    st.success("✅ File uploaded successfully!")
else:
    st.info("Please upload your IPL dataset (.csv) file.")
# Show dataset preview
st.subheader("Dataset Preview")
st.dataframe(data.head())
st.subheader("Matches Played by Season")
matches_by_season = data['YEAR'].value_counts().sort_index()
plt.figure(figsize=(10, 5))
matches_by_season.plot(kind='bar')
plt.xlabel('YEAR')
plt.ylabel('Number of Matches')
st.pyplot(plt)

st.subheader("Filter by Team")
team = st.selectbox("Select a Team", sorted(data["Team 1"].unique()))
filtered = data[(data["Team 1"] == team) | (data["Team 2"] == team)]
st.write(filtered)




# In[3]:


data.head()


Which team won the most matches in 2008?

# In[91]:


matches_2008 = data[data['YEAR'] == 2008]
most_wins_2008 = matches_2008['Winners'].value_counts().idxmax()
most_wins_2008


# Which city hosted the highest number of matches?

# In[94]:


most_city = data['City'].value_counts().idxmax()
most_city


# Which team won more often while batting first?

# In[99]:


a=(data[data['Toss_Decision'] == 'bat'].groupby('Winners').size().idxmax())
a


# Which team won more often while fielding first?

# In[100]:


a=(data[data['Toss_Decision'] == 'field'].groupby('Winners').size().idxmax())
a


# Does winning the toss increase the chance of winning the match?

# In[105]:


print((data['Toss_Winner'] == data['Winners']).value_counts(normalize=True) * 100)


# Which toss decision (bat or field) leads to more wins?

# In[8]:


winner=data.groupby('Toss_Decision')['YEAR'].count()
winner


# Which stadium hosted the most matches in the dataset?

# In[19]:


a=data.groupby('Location')['Date'].count().idxmax()
a


# Which venue saw the most wins for home teams?

# In[56]:


a=data[data['Winners'] == data['Team 1']]['Location'].value_counts().idxmax()
a


# Which venue saw the most wins for away teams?

# In[55]:


a=data[data['Winners'] == data['Team 2']]['Location'].value_counts().idxmax()
a


# Is there any relationship between toss winner and match winner?

# In[57]:


a=((data['Toss_Winner'] == data['Winners']).value_counts(normalize=True) * 100)
a


# Which team had the highest win percentage in this dataset?

# In[106]:


win_percentage=data['Winners'].value_counts()
a=win_percentage/100
a


# How often did the team winning the toss lose the match?

# In[107]:


toss_count=data['Toss_Winner']==data['Winners']
loss_match=toss_count.value_counts()[False]
loss_match


# Which city’s teams performed the best overall?

# In[108]:


city_teams=data.groupby('City')['Winners'].value_counts()
city_teams.sort_values(ascending=False).idxmax()


# What percentage of matches were won by batting first versus fielding first?

# In[109]:


won=data.groupby('Toss_Decision')['Winners'].count()
a=won/100
a


# Which team lost the most tosses but still won matches?

# In[110]:


lost_toss_won_match=data[data['Toss_Winner'] != data['Winners']]
win=lost_toss_won_match['Winners'].value_counts()
win


# Are there cities where fielding first gives a higher chance of winning?

# In[111]:


field_first = data[data['Toss_Decision'] == 'field']
field_first_wins = field_first[field_first['Toss_Winner'] == field_first['Winners']]
field_success_city = field_first_wins['City'].value_counts() / field_first['City'].value_counts() * 100
print(field_success_city.sort_values(ascending=False).dropna())


# Which toss decision is more successful at each venue?

# In[112]:


decision_success = data[data['Toss_Winner'] == data['Winners']].groupby(['City', 'Toss_Decision']).size().unstack(fill_value=0)
decision_success['Best Decision'] = decision_success.idxmax(axis=1)
print(decision_success[['Best Decision']])


# Which team won matches most frequently in their home city?

# In[68]:


a=data.groupby('Team 1')['Winners'].value_counts()
a


# Which opponent teams faced each other most often in this dataset?

# In[71]:


a=data.groupby(['Team 1', 'Team 2']).size().idxmax()
a


# Are there any stadiums where the same team keeps winning?

# In[86]:


a=data.groupby(['Location', 'Winners']).size().sort_values(ascending=False).head(1)
a


# What is the average number of matches played per city?

# In[122]:


a= data['City'].value_counts().mean()
a


# Which teams appeared in the most matches?

# In[129]:


print(pd.concat([data['Team 1'], data['Team 2']]).value_counts())


# Which team won the most matches after losing the toss?

# In[134]:


a=(data[data['Toss_Winner'] != data['Winners']]['Winners'].value_counts().idxmax())
a


# Are there cities or venues where the toss winner always won the match?

# In[142]:


print(data.groupby('City').agg({'Toss_Winner': list, 'Winners': list}).query('Toss_Winner == Winners'))


# What percentage of matches were won by the team that chose to bat?

# In[146]:


print((data[(data['Toss_Decision'] == 'bat') & (data['Toss_Winner'] == data['Winners'])].shape[0] / data.shape[0]) * 100)


# What percentage of matches were won by the team that chose to field?

# In[147]:


print((data[(data['Toss_Decision'] == 'field') & (data['Toss_Winner'] == data['Winners'])].shape[0] / data.shape[0]) * 100)


# Which city has the most balanced win distribution among teams?

# In[148]:


a=data.groupby(['City', 'Winners']).size().groupby('City').std().idxmin()
a


# Are there any cities where one team dominated completely?

# In[149]:


print(data.groupby('City')['Winners'].nunique()[data.groupby('City')['Winners'].nunique() == 1])


# What are the overall toss-winning trends for top-performing teams?

# In[150]:


print(data[data['Winners'].isin(data['Winners'].value_counts().head(5).index)].groupby(['Winners', 'Toss_Decision']).size())


# Based on current data, what would be the ideal toss decision for a team playing in each city?

# In[151]:


print(data[data['Toss_Winner']==data['Winners']].groupby(['City','Toss_Decision']).size().unstack(fill_value=0).assign(ideal_decision=lambda x: x.idxmax(axis=1))['ideal_decision'])


# In[ ]:




