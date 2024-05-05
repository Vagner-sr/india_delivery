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
from haversine import haversine
from streamlit_folium import folium_static
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title='Restaurant View', layout='wide')

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

def distance(df2):
    df2['distance']= df2.apply(lambda x: haversine((x['restaurant_latitude'], x['restaurant_longitude'] ), 
                                    (x['delivery_location_latitude'], x['delivery_location_longitude'])), axis=1)
    distance_mean = df2['distance'].mean().round(2)
    return distance_mean

def delivery_time_festival(df2, festival):
    """
    For festival, input Yes or No
    """
    df_aux = df2[['festival', 'time_taken(min)']].groupby('festival').mean().reset_index()
    df_aux = df_aux.rename(columns={'time_taken(min)': 'time_mean'})
    df_aux = np.round(df_aux.loc[df_aux['festival'] == festival, 'time_mean'], 2)
    return df_aux

def avg_delivery_city(df2):
    df_aux = df2[['time_taken(min)', 'city']].groupby('city').agg({'time_taken(min)': ['mean', 'std']})
    df_aux.columns = ['time_mean', 'time_std']
    df_aux = df_aux.reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(name='Control', x= df_aux['city'], y= df_aux['time_mean'], error_y= dict(type='data', array= df_aux['time_std'])))
    fig.update_layout(barmode='group')
    return fig 


def avg_delivery_order_type(df2):
    df_aux = df2[['time_taken(min)', 'city', 'type_of_order']].groupby(['city', 'type_of_order']).agg({'time_taken(min)': ['mean', 'std']})
    df_aux.columns = ['time_mean', 'time_std']
    df_aux = df_aux.reset_index()
    df_aux = df_aux.groupby('city').apply(lambda x: x.sort_values('time_mean', ascending= False)).reset_index(drop=True)
    return df_aux

def avg_delivery_by_city(df2):
    df2['distance']= df2.apply(lambda x: haversine((x['restaurant_latitude'], x['restaurant_longitude'] ), 
                                        (x['delivery_location_latitude'], x['delivery_location_longitude'])), axis=1)
    
    df_aux = df2[['distance', 'city']].groupby('city').mean().reset_index()
    fig = px.pie(df_aux, names='city', values= 'distance')
    return fig

def avg_deviation_by_city(df2):
    df_aux = df2[['time_taken(min)', 'city', 'road_traffic_density']].groupby(['city', 'road_traffic_density']).agg({'time_taken(min)': ['mean', 'std']})
    df_aux.columns = ['time_mean', 'time_std']
    df_aux = df_aux.reset_index()
    df_aux = df_aux.groupby('city').apply(lambda x: x.sort_values('time_mean', ascending= False)).reset_index(drop=True)

    fig = px.sunburst(df_aux, path=['city', 'road_traffic_density'], values= 'time_mean',
        color= 'time_std', color_continuous_scale='RdBu_r', 
        color_continuous_midpoint= np.average(df_aux['time_std']))
    return fig

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
st.header('Restaurant View')

with st.container():
    st.markdown("""___""")
    st.header('Overal Metrics')

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Deliverers', df2['delivery_person_id'].nunique())

    with col2:
        avg_distance = distance(df2)
        st.metric('Average Distance Km', avg_distance)

    with col3:
        df_aux = delivery_time_festival(df2, 'Yes')
        st.metric('Delivery Time - Festival', df_aux)
        
    with col4:
        df_aux = delivery_time_festival(df2, 'No')
        st.metric('Delivery Time - No Festival', df_aux)


with st.container():
    st.markdown("""___""")
    col1, col2 = st.columns(2)

    with col1:
        st.header('Average Delivery Time by City')
        fig = avg_delivery_city(df2)
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.header('Delivery Time by Order Type')
        df_aux = avg_delivery_order_type(df2)
        st.dataframe(df_aux, use_container_width=True)


with st.container():
    st.markdown("""___""")

    col1, col2 = st.columns(2)
    with col1:
        st.header('Mean delivery time by City')
        fig = avg_delivery_by_city(df2)
        st.plotly_chart(fig, use_container_width=True)
        

    with col2:
        st.header('Standard Deviation by City and Traffic')
        fig = avg_deviation_by_city(df2)
        st.plotly_chart(fig, use_container_width=True)


        

        
        
    