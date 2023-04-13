import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import streamlit as st
import time
import plotly.express as px

st.set_page_config(page_title=" TAXI DRIVER ANALYSIS", page_icon="🚕", layout="wide", initial_sidebar_state="expanded")

path2 = "https://raw.githubusercontent.com/uber-web/kepler.gl-data/master/nyctrips/data.csv"
df3 = pd.read_csv(path2, delimiter = ',')
df3['tpep_pickup_datetime'] = df3['tpep_pickup_datetime'].map(pd.to_datetime)
df3['tpep_dropoff_datetime'] = df3['tpep_dropoff_datetime'].map(pd.to_datetime) 
# define a function to get the minute from datetime object
def get_minute(datetime_obj):
    return datetime_obj.minute

def get_hour(dt):
    return dt.hour #.hour is an attribute
#calling the fonction implemented befor to create 3 new column day, weekday & hour
#CAREFUL FOR MYSTERIOUS REASON DAY 1 IS TUESDAY HERE

df3['hour'] = df3['tpep_pickup_datetime'].map(get_hour)
df3['Trip_duration'] = df3['tpep_dropoff_datetime']-df3['tpep_pickup_datetime']
df3['Trip_duration']= df3['Trip_duration'].dt.total_seconds()/60
#df3['trip_duration_min'] =df3['Trip_duration'].dt.components['minutes']
#pickup_hours = df3['Trip_duration'].dt.components['hours']
#pickup_minute = df3['Trip_duration'].dt.components['minutes']
#pickup_second = df3['Trip_duration'].dt.components['seconds']
#df3['trip_duration_hour_min'] = pickup_hours.map(str)+ ':'+pickup_minute.map(str) + ':' + pickup_second.map(lambda x: str(x).zfill(2))
#df3['Trip_duration'] = pickup_minute.map(str) + ':' + pickup_second.map(lambda x: str(x).zfill(2))
df3['locations_pickup'] = list(zip(df3['pickup_latitude'], df3['pickup_longitude']))
df3['locations_dropoff'] = list(zip(df3['dropoff_latitude'], df3['dropoff_longitude']))
# I Group my dataframe according to the driver ID, then i split it in order to create kpi easily for both driver 
groups = df3.groupby(df3.VendorID)
Vendor_1= groups.get_group(1)
Vendor_2= groups.get_group(2)

#----------------------KPI----------------------
# create two columns for charts
with st.container():
    fig1 = px.histogram(data_frame=df3, x="hour", color_discrete_sequence=['blue'], title="Histogram of Hourly Frequency")
    st.plotly_chart(fig1)

fig_col2,fig_col3 = st.columns(2)      
with fig_col2:
    st.markdown("Frequency by Hour Vendor1 - Uber - 15/01/2015")
    fig2 = px.histogram(data_frame=Vendor_1, x="hour", color_discrete_sequence=['yellow'])
    st.write(fig2)
with fig_col3:
    st.markdown("Frequency by Hour Vendor1 - Uber - 15/01/2015")
    fig3 = px.histogram(data_frame=Vendor_2, x="hour", color_discrete_sequence=['orange'])
    st.write(fig3)
