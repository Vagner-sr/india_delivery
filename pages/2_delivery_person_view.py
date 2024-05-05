# Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import plotly.express as px
from datetime import datetime
import streamlit as st
import folium
from streamlit_folium import folium_static
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title='Delivery Person View', layout='wide')

# =========================
# FUNCTIONS
# =========================

def clean_data(df1):

    # Setting columns to lower
    df1.columns = [i.lower() for i in df1.columns ]

    # Removing N/A and converting to int - delivery_person_age'
    lines = df1['delivery_person_age'] != 'NaN '
    df1 = df1.loc[lines, :].copy()
    df1['delivery_person_age'] = df1['delivery_person_age'].astype('int64')

    # Removing N/A - road_traffic_density
    lines = df1['road_traffic_density'] != 'NaN '
    df1 = df1.loc[lines, :].copy()

    # Removing N/A - festival
    lines = df1['festival'] != 'NaN '
    df1 = df1.loc[lines, :].copy()

    # Removing N/A - city
    lines = df1['city'] != 'NaN '
    df1 = df1.loc[lines, :].copy()

    # Transforming time taken in int
    df1['time_taken(min)'] = df1['time_taken(min)'].str[-2:].astype('int64')

    # Converting to float and replacing N/A with "" - delivery_person_ratings
    df1['delivery_person_ratings'].fillna("", inplace=True)
    df1['delivery_person_ratings'] = df1['delivery_person_ratings'].astype(float)

    # Converting to datetime - order_date
    df1['order_date'] = pd.to_datetime(df1['order_date'], format='%d-%m-%Y')

    # Removing N/A and converting to int - multiple_deliveries
    lines = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[lines, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype('int64')

    # Removing spaces in object features
    df1 = df1.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    return df1


def top_deliverers(df2, top_asc):
    df_aux = (df2[['delivery_person_id', 'time_taken(min)', 'city']].groupby(['city', 'delivery_person_id'])
                                                        .mean()
                                                        .sort_values(['city','time_taken(min)'], ascending= top_asc)
                                                        .groupby('city')
                                                        .head(10)
                                                        .reset_index()
                                                        )
    return df_aux

# ------------------------------- Logical Structure ------------------------------

# Import Dataset
df_raw = pd.read_csv('train.csv')
df1 = df_raw.copy()

# Cleaning Dataset
df1 = clean_data(df1)

df2 = df1.copy()

# =========================
# Sidebar Layoyt
# =========================

img = Image.open('logo.jpg')
st.sidebar.image(img, width=120)

st.sidebar.markdown('# India Delivery')
st.sidebar.markdown('## Best delivery in town')
st.sidebar.markdown("""___""")

# Date Input
date_slider = st.sidebar.slider('Select a date', 
                    value= datetime(2022, 4, 13),
                    min_value= datetime(2022, 2, 11), 
                    max_value= datetime(2022, 4, 6), 
                    format=('DD-MM-YYYY'))

st.sidebar.markdown("""___""")

# Traffic Input
traffic_condition = st.sidebar.multiselect('Traffic Condition', ['Jam', 'High', 'Low', 'Medium'], 
                                            default= ['Jam', 'High', 'Low', 'Medium'])

# Weather Input
weather_condition = st.sidebar.multiselect('Weather Condition', ['conditions Sunny', 'conditions Stormy', 'conditions Sandstorms',
                                    'conditions Cloudy', 'conditions Fog', 'conditions Windy'], default= ['conditions Sunny', 'conditions Stormy', 'conditions Sandstorms',
                                    'conditions Cloudy', 'conditions Fog', 'conditions Windy'])

# =========================
# Linking Filter
# =========================

# Date Filter
selected_lines= df2['order_date'] < date_slider
df2 = df2.loc[selected_lines, :]

# Traffic Filter
selected_lines = df2['road_traffic_density'].isin(traffic_condition)
df2 = df2.loc[selected_lines, :]

# Weather Filter
selected_lines = df2['weatherconditions'].isin(weather_condition)
df2 = df2.loc[selected_lines, :]


# =========================
# Streamlit Layoyt
# =========================
st.header('Delivery Person View')


with st.container():
    st.header('Overall Metrics')

col1, col2, col3, col4 = st.columns(4)
with col1:
    # 2.2.1 The youngest and oldest age of the delivery people.
    col1.metric('Youngest', df2['delivery_person_age'].min())

with col2:
    # 2.2.1 The youngest and oldest age of the delivery people.
    col2.metric('Oldest', df2['delivery_person_age'].max())

with col3:
    # 2.2.2 The worst and best condition of vehicles
    col3.metric('Best Vehicle Condition', df2['vehicle_condition'].max())

with col4:
    # 2.2.2 The worst and best condition of vehicles
    col4.metric('Worst Vehicle Condition', df2['vehicle_condition'].min())


with st.container():
    st.markdown("""___""")
    st.header('Reviews')

col1, col2 = st.columns(2)
with col1:
    st.markdown('##### Average rating per person')
    df_aux = df2[['delivery_person_ratings', 'delivery_person_id']].groupby('delivery_person_id').mean().reset_index()
    st.dataframe(df_aux)

with col2:
    st.markdown('##### Average rating per traffic')
    df_aux = df2[['delivery_person_ratings', 'road_traffic_density']].groupby('road_traffic_density').agg({'delivery_person_ratings': ['mean', 'std']})
    df_aux.columns = ['rating_mean', 'rating_std']
    df_aux = df_aux.reset_index()
    st.dataframe(df_aux)

    st.markdown('##### Average rating per weather')
    df_aux = df2[['delivery_person_ratings', 'weatherconditions']].groupby('weatherconditions').agg({'delivery_person_ratings': ['mean', 'std']})
    df_aux.columns = ['rating_mean', 'rating_std']
    df_aux = df_aux.reset_index()
    st.dataframe(df_aux)

with st.container():
    st.markdown("""___""")
    st.header('Delivery Speed')

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(' ##### Top Fastest delivery people')
        df_aux = top_deliverers(df2, top_asc= True)
        st.dataframe(df_aux)
    with col2:
        st.markdown(' ##### Top Slowest delivery people')
        df_aux = top_deliverers(df2, top_asc= False)
        st.dataframe(df_aux)


