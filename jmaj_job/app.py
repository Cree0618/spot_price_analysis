import streamlit as st
import pandas as pd

# Load the data
file_path = 'mesicni_ceny_a_kvartaly.csv'  # Update this with your actual file path
data = pd.read_csv(file_path)

# Convert 'Date' column to datetime
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')

# Display title
st.title('Electricity Prices with Quarterly Averages')

# Display dataframe
st.write('## Original Data')
st.write(data)

# Filter by year
years = data['Year'].unique()
selected_year = st.selectbox('Select Year', years)

# Filter data based on selected year
filtered_data = data[data['Year'] == selected_year]

# Display filtered data
st.write(f'## Data for {selected_year}')
st.write(filtered_data)

# Plot the data
st.write('## Monthly Average Prices')
st.line_chart(filtered_data.set_index('Date')['Monthly_Average'])

# Show quarterly averages
st.write('## Quarterly Averages')
quarters = ['Q1', 'Q2', 'Q3', 'Q4']
quarterly_averages = filtered_data[quarters].mean()
st.bar_chart(quarterly_averages)
