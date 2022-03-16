from __future__ import annotations
from matplotlib.pyplot import annotate
import requests
import pandas as pd
import pycountry 
import plotly.express as px

# Get the data from Worldometer
URL = requests.get("https://www.worldometers.info/coronavirus/#main_table")
df = pd.read_html(URL.text, displayed_only=False)

# Save currently data, yesterday data, and 2 days ago data
df_now = df[0]
df_yesterday = df[1]
df_2days = df[2]

# Select columns
df_now = df_now.loc[:,['Country,Other', 'TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths',
       'TotalRecovered', 'NewRecovered', 'ActiveCases', 'Population']]
df_yesterday = df_yesterday.loc[:,['Country,Other', 'TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths',
       'TotalRecovered', 'NewRecovered', 'ActiveCases', 'Population']]
df_2days = df_2days.loc[:,['Country,Other', 'TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths',
       'TotalRecovered', 'NewRecovered', 'ActiveCases', 'Population']]

# Drop unwanted rows
df_now = df_now[df_now["Country,Other"].str.contains("Asia|North America|South America|Europe|Oceania|World|Total:")==False]
df_now = df_now[df_now["Country,Other"] != "Africa"]
df_yesterday = df_yesterday[df_yesterday["Country,Other"].str.contains("Asia|North America|South America|Europe|Oceania|World|Total:")==False]
df_yesterday = df_yesterday[df_yesterday["Country,Other"] != "Africa"]
df_2days = df_2days[df_2days["Country,Other"].str.contains("Asia|North America|South America|Europe|Oceania|World|Total:")==False]
df_2days = df_2days[df_2days["Country,Other"] != "Africa"]

# Reset the index number
df_now.reset_index(drop=True, inplace=True)
df_yesterday.reset_index(drop=True, inplace=True)
df_2days.reset_index(drop=True, inplace=True)

# Rename columns
column_names = ['Country', 'Total Cases', 'New Cases', 'Total Deaths', 'New Deaths', 'Total Recovered', 'New Recovered', 'Active Cases', 'Population']
df_now.columns = column_names
df_yesterday.columns = column_names
df_2days.columns = column_names

# Sort the data in descending
df_now.sort_values(by=['Total Cases'], ascending=False, inplace=True)
df_yesterday.sort_values(by=['Total Cases'], ascending=False, inplace=True)
df_2days.sort_values(by=['Total Cases'], ascending=False, inplace=True)

# Remove extra characters in the data
for col in df_now.columns[1:]:
    df_now[col].replace(regex=True,inplace=True,to_replace=r'\D',value=r'')

for col in df_yesterday.columns[1:]:
    df_yesterday[col].replace(regex=True,inplace=True,to_replace=r'\D',value=r'')

for col in df_2days.columns[1:]:
    df_2days[col].replace(regex=True,inplace=True,to_replace=r'\D',value=r'')

# Change country's name so that we can use PyCountry
df_now.replace('UK', 'United Kingdom', inplace=True)
df_now.replace('Russia', 'Russian Federation', inplace=True)
df_now.replace('DRC', 'COD', inplace=True)
df_now.replace('S. Korea', 'South Korea', inplace=True)
df_now.replace('St. Vincent Grenadines', 'Saint Vincent and the Grenadines', inplace=True)
df_now.replace('St. Barth', 'Saint Barthélemy', inplace=True)
df_now.replace('Iran', 'Iran, Islamic Republic of', inplace=True)
df_now.replace('CAR', 'CAF', inplace=True)
df_now.replace('Laos', "Lao People's Democratic Republic", inplace=True)
df_now.replace('UAE', 'United Arab Emirates', inplace=True)
df_now.replace('Syria', 'Syrian Arab Republic', inplace=True)

df_yesterday.replace('UK', 'United Kingdom', inplace=True)
df_yesterday.replace('Russia', 'Russian Federation', inplace=True)
df_yesterday.replace('DRC', 'COD', inplace=True)
df_yesterday.replace('S. Korea', 'South Korea', inplace=True)
df_yesterday.replace('St. Vincent Grenadines', 'Saint Vincent and the Grenadines', inplace=True)
df_yesterday.replace('St. Barth', 'Saint Barthélemy', inplace=True)
df_yesterday.replace('Iran', 'Iran, Islamic Republic of', inplace=True)
df_yesterday.replace('CAR', 'CAF', inplace=True)
df_yesterday.replace('Laos', "Lao People's Democratic Republic", inplace=True)
df_yesterday.replace('UAE', 'United Arab Emirates', inplace=True)
df_yesterday.replace('Syria', 'Syrian Arab Republic', inplace=True)

df_2days.replace('UK', 'United Kingdom', inplace=True)
df_2days.replace('Russia', 'Russian Federation', inplace=True)
df_2days.replace('DRC', 'COD', inplace=True)
df_2days.replace('S. Korea', 'South Korea', inplace=True)
df_2days.replace('St. Vincent Grenadines', 'Saint Vincent and the Grenadines', inplace=True)
df_2days.replace('St. Barth', 'Saint Barthélemy', inplace=True)
df_2days.replace('Iran', 'Iran, Islamic Republic of', inplace=True)
df_2days.replace('CAR', 'CAF', inplace=True)
df_2days.replace('Laos', "Lao People's Democratic Republic", inplace=True)
df_2days.replace('UAE', 'United Arab Emirates', inplace=True)
df_2days.replace('Syria', 'Syrian Arab Republic', inplace=True)

# This function create a ISO 3166 country code column. If it does not recognize, the country's code will be 'None'
def alpha3code(column):
    CODE=[]
    for country in column:
        try:
            code = pycountry.countries.lookup(country).alpha_3
            # pycountry.countries.lookup('SYR')
            # Country(alpha_2='SY', alpha_3='SYR', flag='🇸🇾', name='Syrian Arab Republic', numeric='760')
            CODE.append(code)
        except:
            CODE.append('None')
    return CODE

# Add the country's code column
df_now['CODE'] = alpha3code(df_now.Country)
df_yesterday['CODE'] = alpha3code(df_yesterday.Country)
df_2days['CODE'] = alpha3code(df_2days.Country)

# Save the data to excel file or csv file
df_now.to_excel("covid_now.xlsx")
#df_now.to_csv("covid_now.csv")
df_yesterday.to_excel("covid_yesterday.xlsx")
#df_yesterday.to_csv("covid_yesterday.csv")
df_2days.to_excel("covid_2days.xlsx")
#df_2days.to_csv("covid_2days.csv")


# Display the total COVID-19 total cases around the world
fig_now = px.choropleth(df_now, locations="CODE", color="Total Cases", hover_name="Country", color_continuous_scale=px.colors.sequential.YlOrRd)
fig_now.update_layout(title_text='Current COVID-19 Cases', annotations=[dict(x=0.5,y=0,xref='paper',yref='paper',text='Source: <a href="https://www.worldometers.info/coronavirus/">\
            Worldometer</a>',showarrow=False)])
fig_now.show()

fig_yesterday = px.choropleth(df_yesterday, locations="CODE", color="Total Cases", hover_name="Country", color_continuous_scale=px.colors.sequential.YlOrRd)
fig_yesterday.update_layout(title_text='Yesterday COVID-19 Cases', annotations=[dict(x=0.5,y=0,xref='paper',yref='paper',text='Source: <a href="https://www.worldometers.info/coronavirus/">\
            Worldometer</a>',showarrow=False)])
fig_yesterday.show()

fig_2days = px.choropleth(df_2days, locations="CODE", color="Total Cases", hover_name="Country", color_continuous_scale=px.colors.sequential.YlOrRd)
fig_2days.update_layout(title_text='2 Days Ago COVID-19 Cases', annotations=[dict(x=0.5,y=0,xref='paper',yref='paper',text='Source: <a href="https://www.worldometers.info/coronavirus/">\
            Worldometer</a>', showarrow=False)])
fig_2days.show()



