# TO RUn THE APP:  streamlit run app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit import components
import pygwalker as pyg
from pygwalker.api.streamlit import StreamlitRenderer
import streamlit as st

st.set_page_config(
    page_title="Elektřina PST dashboard",
    layout="wide",
    
    menu_items=None,
)


# Load the new data
file_path = "jmaj_job/USETHIS_modifiedmesicni.csv"
#file_path = "MAIN_DATAFRAME_v2.csv"

data = pd.read_csv(file_path)

# Ensure data integrity by checking for duplicates and only working with the loaded rows
data = data.drop_duplicates()

# Convert 'Date' column to datetime
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m')

# Extract year and month from the 'Date' column
data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month

# Define a function to determine the quarter
def get_quarter(month):
    if month in [1, 2, 3]:
        return 'Q1'
    elif month in [4, 5, 6]:
        return 'Q2'
    elif month in [7, 8, 9]:
        return 'Q3'
    elif month in [10, 11, 12]:
        return 'Q4'

# Apply the function to create a 'Quarter' column
data['Quarter'] = data['Month'].apply(get_quarter)

# Calculate the average price for each quarter of each year
quarterly_avg = data.groupby(['Year', 'Quarter'])['Monthly_Average'].mean().reset_index()

# Merge the quarterly averages back into the original dataframe
data = data.merge(quarterly_avg, on=['Year', 'Quarter'], suffixes=('', '_Quarter_Avg'))

# Calculate the average price for each month across all years
monthly_trend = data.groupby(['Month'])['Monthly_Average'].mean().reset_index()

# Calculate the average price for each year
yearly_avg = data.groupby(['Year'])['Monthly_Average'].mean().reset_index()


# Adjust the width of the Streamlit page

pyg_app = StreamlitRenderer(data)
 
pyg_app.explorer()




# Streamlit app
st.title('Elektřina PST dashboard 📊')



# Display average prices for each year
st.write('## Průměrné ceny pro každý rok [Kč/MW]')
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(yearly_avg['Year'], yearly_avg['Monthly_Average'], marker='o', label='Yearly Average')
ax.set_xlabel('Year')
ax.set_ylabel('Average Price')
ax.set_title('Yearly Average Prices')
ax.legend()
ax.grid(True)
ax.set_xticks(yearly_avg['Year'])
ax.set_xticklabels(yearly_avg['Year'].astype(int), rotation=45)
st.pyplot(fig)

# Filter by year
years = data['Year'].unique()
selected_year = st.selectbox('Vyberte rok 👇', years)

# Filter data based on selected year
filtered_data = data[data['Year'] == selected_year]

# Display filtered data
st.write(f'## Data pro rok {selected_year}')
st.write(filtered_data)

# Plot the monthly average prices
st.write(f'## Měsíční průměrné ceny v roce {selected_year}')
st.line_chart(filtered_data.set_index('Date')['Monthly_Average'])

# Show quarterly averages for the selected year
st.write(f'## Kvartální průměrná cena rok {selected_year}')
quarterly_averages = filtered_data.groupby('Quarter')['Monthly_Average_Quarter_Avg'].mean()
st.bar_chart(quarterly_averages)

# Visualize the quarterly averages over the years
st.write('## Kvartální ceny v průběhu let')
fig, ax = plt.subplots(figsize=(10, 6))
for quarter in ['Q1', 'Q2', 'Q3', 'Q4']:
    if quarter in quarterly_avg['Quarter'].unique():
        ax.plot(quarterly_avg[quarterly_avg['Quarter'] == quarter]['Year'], 
                quarterly_avg[quarterly_avg['Quarter'] == quarter]['Monthly_Average'], 
                marker='o', label=quarter)

ax.set_xlabel('Year')
ax.set_ylabel('Average Price')
ax.set_title('Quarterly Average Prices')
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Show average prices for each month through the years
st.write('## Průměrné ceny pro každý měsíc v průběhu let [Kč/MW]')
st.line_chart(monthly_trend.set_index('Month')['Monthly_Average'])

# Add monthly trend graph
st.write('## Průměrný měsíční trend')
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(monthly_trend['Month'], monthly_trend['Monthly_Average'], marker='o', label='Monthly Trend')

ax.set_xlabel('Month')
ax.set_ylabel('Average Price')
ax.set_title('Monthly Trend of Average Prices Across All Years')
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Add yearly average graph
st.write('## Průměrné roční ceny')
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(yearly_avg['Year'], yearly_avg['Monthly_Average'], marker='o', label='Yearly Average')

ax.set_xlabel('Year')
ax.set_ylabel('Average Price')
ax.set_title('Yearly Average Prices')
ax.legend()
ax.grid(True)
ax.set_xticks(yearly_avg['Year'])
ax.set_xticklabels(yearly_avg['Year'].astype(int), rotation=45)
st.pyplot(fig)

# Add histogram of monthly prices
st.write('## Histogram měsíčních cen')
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(data['Monthly_Average'], bins=30, edgecolor='black')
ax.set_xlabel('Monthly Average Price')
ax.set_ylabel('Frequency')
ax.set_title('Histogram of Monthly Average Prices')
st.pyplot(fig)

# Add box plot of monthly prices by year
st.write('## Box plot měsíčních cen podle roku')
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x='Year', y='Monthly_Average', data=data, ax=ax)
ax.set_xlabel('Year')
ax.set_ylabel('Monthly Average Price')
ax.set_title('Box Plot of Monthly Average Prices by Year')
ax.set_xticks(data['Year'].unique())
ax.set_xticklabels(data['Year'].unique().astype(int), rotation=45)
st.pyplot(fig)

# Add bar chart of average prices by quarter for each year
st.write('## Průměrné ceny podle čtvrtletí pro každý rok')
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Year', y='Monthly_Average', hue='Quarter', data=quarterly_avg, ci=None, ax=ax)
ax.set_xlabel('Year')
ax.set_ylabel('Average Price')
ax.set_title('Average Prices by Quarter for Each Year')
ax.set_xticks(data['Year'].unique())
ax.set_xticklabels(data['Year'].unique().astype(int), rotation=45)
st.pyplot(fig)

# Add heatmap of monthly average prices
st.write('## Heatmap průměrných měsíčních cen')
heatmap_data = data.pivot_table(index='Year', columns='Month', values='Monthly_Average')
fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlGnBu", ax=ax)
ax.set_xlabel('Month')
ax.set_ylabel('Year')
ax.set_title('Heatmap of Monthly Average Prices')
st.pyplot(fig)

# Display the image měsíční_průměrná_hodinová_spotřeba.png
st.write('## Měsíční průměrná hodinová spotřeba Gamma')
image_file = 'jmaj_job/měsíční_průměrná_hodinová_spotřeba.png'
st.image(image_file)

# Display the Plotly heatmap
st.write('## Heatmapa SPOT cen v roce 2024')
heatmap_file = 'jmaj_job/heatmap_price.html'  # Update with the actual path to your heatmap.html file
with open(heatmap_file, 'r') as f:
    heatmap_html = f.read()
st.components.v1.html(heatmap_html, height=900, width=1000)

st.write('## Gamma Heatmapa spotřeby v roce 2024')
heatmap_consumption_file = 'jmaj_job/heatmap_consumption.html'  # Update with the actual path to your heatmap.html file
with open(heatmap_consumption_file, 'r') as f:
    heatmap_c_html = f.read()
st.components.v1.html(heatmap_c_html, height=2000, width=1000, scrolling=True, resize=True)
