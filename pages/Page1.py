import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import streamlit as st

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
#Titre, sous titre et image
st.title("First lest have a quick look at our dataset before diving in to the visuals.")
st.write(df3.head(5))
st.subheader("There is 2 different vendor ID, in order to use the data easier I devided the file by the vendorID")

st.write(Vendor_1.head(5))
st.write(Vendor_2.head(5))

st.title("Let see our first KPI :")
st.subheader("Number of fare of each vendor :")
Nb_of_Fare_V1 = len(Vendor_1.index)
Nb_of_Fare_V2 = len(Vendor_2.index)
Nb_of_Fare_Total = len(df3.index)
# Create 3 columns and display each KPI in its respective column
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Number of Fares Vendor 1", value=f"{Nb_of_Fare_V1}")

with col2:
    st.metric(label="Number of Fares Vendor 2", value=f"{Nb_of_Fare_V2}")

with col3:
    st.metric(label="Total Number of Fares", value=f"{Nb_of_Fare_Total}")

#calculate the total amount of money earned by each driver
Total_amount_Vendor_1 = Vendor_1['total_amount'].sum()
Total_amount_Vendor_2 = Vendor_2['total_amount'].sum()
Total_amount = df3['total_amount'].sum()

# Create 3 columns and display each KPI in its respective column
col4, col5, col6= st.columns(3)

with col4:
    st.metric(label="Total Amount Vendor 1", value=f"${Total_amount_Vendor_1:,.2f}")

with col5:
    st.metric(label="Total Amount Vendor 2", value=f"${Total_amount_Vendor_2:,.2f}")

with col6:
    st.metric(label="Total Amount", value=f"${Total_amount:,.2f}")