import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit import components
import pygwalker as pyg
from pygwalker.api.streamlit import StreamlitRenderer
import streamlit as st

st.set_page_config(
    page_title="Use Pygwalker In Streamlit",
    layout="wide",
    
    menu_items=None,
)


# Load the new data
#file_path = "jmaj_job/USETHIS_modifiedmesicni.csv"
file_path = "MAIN_DATAFRAME_v2.csv"

data = pd.read_csv(file_path)

# Ensure data integrity by checking for duplicates and only working with the loaded rows
data = data.drop_duplicates()


# Adjust the width of the Streamlit page

pyg_app = StreamlitRenderer(data)
 
pyg_app.explorer()


