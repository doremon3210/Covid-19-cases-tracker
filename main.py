from __future__ import annotations
from matplotlib.pyplot import annotate
import requests
import pandas as pd
import pycountry 
import plotly.express as px
from datetime import date

# Get the data from Worldometer
URL = requests.get("https://www.worldometers.info/coronavirus/#main_table")
df = pd.read_html(URL.text, displayed_only=False)

# Promt user to choose what data time they want
print("When do you want to know the cases (Enter 0-2):")
print("0: Now")
print("1: Yesterday")
print("2: 2 days ago")
choice = int(input())
print()

# Save currently data, yesterday data, and 2 days ago data
df = df[choice]

# Select columns
df = df.loc[:,['Country,Other', 'TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths',
       'TotalRecovered', 'NewRecovered', 'ActiveCases', 'Population']]

# Drop unwanted rows
df = df[df["Country,Other"].str.contains("Asia|North America|South America|Europe|Oceania|World|Total:")==False]
df = df[df["Country,Other"] != "Africa"]

# Reset the index number
df.reset_index(drop=True, inplace=True)

# Rename columns
column_names = ['Country', 'Total Cases', 'New Cases', 'Total Deaths', 'New Deaths', 'Total Recovered', 'New Recovered', 'Active Cases', 'Population']
df.columns = column_names


# Sort the data in descending
df.sort_values(by=['Total Cases'], ascending=False, inplace=True)


# Remove extra characters in the data
for col in df.columns[1:]:
    df[col].replace(regex=True,inplace=True,to_replace=r'\D',value=r'')

# Change country's name so that we can use PyCountry
df.replace('UK', 'United Kingdom', inplace=True)
df.replace('Russia', 'Russian Federation', inplace=True)
df.replace('DRC', 'COD', inplace=True)
df.replace('S. Korea', 'South Korea', inplace=True)
df.replace('St. Vincent Grenadines', 'Saint Vincent and the Grenadines', inplace=True)
df.replace('St. Barth', 'Saint Barthélemy', inplace=True)
df.replace('Iran', 'Iran, Islamic Republic of', inplace=True)
df.replace('CAR', 'CAF', inplace=True)
df.replace('Laos', "Lao People's Democratic Republic", inplace=True)
df.replace('UAE', 'United Arab Emirates', inplace=True)
df.replace('Syria', 'Syrian Arab Republic', inplace=True)

# Convert cells data type to number
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col])

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
df['CODE'] = alpha3code(df.Country)

# Save the data to excel file or csv file
def storeTheFile(file_choice):
    # This dictionary helps in saving the file name
    choice_dict = {0: "now", 1: "yesterday", 2: "2_days_ago"}
    # This line helps in saving the file name
    today = date.today().strftime("%Y_%m_%d")
    
    if (file_choice == 1):
        df.to_excel("covid_cases_{}_{}.xlsx".format(choice_dict[choice], today))
        print("Successfully storing the file.")
    elif (file_choice == 2):
        df.to_csv("covid_cases_{}_{}.csv".format(choice_dict[choice], today))
        print("Successfully storing the file.")


print("Do you want to the store the data? (Enter 0-2)")
print("0: No, don't save it")
print("1: Yes, in Excel file")
print("2: Yes, in CSV file")

file_choice = int(input())
storeTheFile(file_choice)
print()


def plotGraph():
    # Promt the user to enter the data of the plot
    print("What data do you want to plot? (Enter 0-7)")
    print("0: Total Cases")
    print("1: New Cases")
    print("2: Total Deaths")
    print("3: New Deaths")
    print("4: Total Recovered")
    print("5: New Recovered")
    print("6: Active Cases")
    print("7: Population")
    data_choice = int(input())
    print("Displaying the plot...")
    print()

    # These dictionaries help for naming the title of the plot and select the data
    data_dict = {0: "Total Cases", 1: "New Cases", 2: "Total Deaths", 3: "New Deaths", 4: "Total Recovered", 5: "New Recovered", 6: "Active Cases", 7: "Population"}
    choice_dict = {0: "Now", 1: "Yesterday", 2: "2 Days Ago"}

    # Use light sequence color for "Total Recovered" and "New Recovered" data
    if (data_choice == 4 or data_choice == 5):
        fig = px.choropleth(df, locations="CODE", color=data_dict[data_choice], hover_name="Country", color_continuous_scale=px.colors.sequential.Emrld)
    # Use hot sequence color for everything else
    else:
        fig = px.choropleth(df, locations="CODE", color=data_dict[data_choice], hover_name="Country", color_continuous_scale=px.colors.sequential.YlOrRd)
    fig.update_layout(title_text='COVID-19 {} {}'.format(data_dict[data_choice], choice_dict[choice]), annotations=[dict(x=0.5,y=0,xref='paper',yref='paper',text='Source: <a href="https://www.worldometers.info/coronavirus/">\
                #Worldometer</a>', showarrow=False)])
    # Save the demo file            
    # fig.write_html("demo.html")
    fig.show()

print("Do you want to display the plot? (Enter 0-1)")
print("0: No")
print("1: Yes")
plot_choice = int(input())
print()

if (plot_choice == 1):
    plotGraph()

print("Exiting the program...")