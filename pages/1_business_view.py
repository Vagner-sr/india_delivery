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

st.set_page_config(page_title='Business View', layout='wide')

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


def order_metric(df2):
    # 2.1.1 Quantity orders per day
    df_aux = df2.groupby('order_date')['id'].count().reset_index(name='count')
    fig = px.bar(df_aux, x='order_date', y='count')

    return fig 

def order_distribution_traffic(df2):
    # 2.1.3 Orders distribution per traffic
    df_aux = df2.groupby('road_traffic_density')['id'].count().reset_index()
    df_aux['percentage'] = df_aux['id'] / df_aux['id'].sum() * 100
    fig = px.pie(df_aux, names= 'road_traffic_density',values='percentage')
    return fig

def traffic_order_city(df2):
    # 2.1.4 Comparison of order volume by city and traffic
    df_aux = df2.groupby(['city', 'road_traffic_density'])['id'].count().reset_index()
    fig = px.scatter(df_aux, x='city', y='road_traffic_density', size='id', color='city')
    return fig

def order_by_week(df2):
    # 2.1.2 Quantity orders per week
    df2['week_of_year'] = df2['order_date'].dt.strftime('%U')
    df_aux = df2.groupby('week_of_year')['id'].count().reset_index()
    fig = px.line(df_aux, 'week_of_year', 'id')
    return fig

def delivery_person_by_week(df2):
    # 2.1.5 Deliveries quantity by deliverer person per week
    df2['week_of_year'] = df2['order_date'].dt.strftime('%U')
    df_aux01 = df2[['id', 'week_of_year']].groupby('week_of_year').count().reset_index()
    df_aux02 = df2[['week_of_year', 'delivery_person_id']].groupby('week_of_year').nunique().reset_index()
    df_aux = pd.merge(df_aux01, df_aux02, how='inner')
    df_aux['deliveries_per_person'] = df_aux['id'] / df_aux['delivery_person_id']
    fig = px.line(df_aux, x='week_of_year', y='deliveries_per_person')
    return fig

def country_map(df2):
    # 2.1.6 Central localization of each city by traffic 
    df_aux = df2[['city', 'road_traffic_density', 'delivery_location_latitude', 'delivery_location_longitude']].groupby(['city', 'road_traffic_density']).median().reset_index()
    df_aux = df_aux.head()

    map = folium.Map()

    for index, i in df_aux.iterrows():
        folium.Marker([i['delivery_location_latitude'], i['delivery_location_longitude']], popup= i[['city', 'road_traffic_density']]).add_to(map)

    folium_static(map, width=1024, height=600)

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

st.header('Company View')

tab1, tab2, tab3 = st.tabs(['Management View', 'Tactical View', 'Geographic View'])

with tab1:
    with st.container():
        fig = order_metric(df2)
        st.header('Orders by Day')
        st.plotly_chart(fig, use_container_width=True)
   
        
    with st.container():
            col1, col2 = st.columns(2)

            with col1:
                fig = order_distribution_traffic(df2)
                st.header('Orders Distribution per Traffic')
                st.plotly_chart(fig, use_container_width=True)
                

            with col2:
                fig = traffic_order_city(df2)
                st.header('Order Volume by City and Traffic')
                st.plotly_chart(fig, use_container_width=True)
                

with tab2:
    with st.container():
        fig = order_by_week(df2)
        st.header('Orders by Week')
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        fig = delivery_person_by_week(df2)
        st.header('Deliveries by Person per Week')
        st.plotly_chart(fig, use_container_width=True)


with tab3:
    st.header('Country Map')
    country_map(df2)

    