# import ====================================

import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import networkx as nx

import os
import warnings

import plotly.graph_objects as go
import plotly.express as px

import streamlit as st

# グラフが全体に表示される
st.set_page_config(layout="wide")

data_load_state = st.text('Loading data...')

# ID data -------------------------------------
idd = pd.read_csv("OneDrive - Kyoto University/Download/Scripts/Python Scripts/20210423_卒論/data/CorpID.csv")
idd = idd.set_index("ID",drop=False) # give ID index to the column
CountryID = pd.read_csv("OneDrive - Kyoto University/Download/Scripts/Python Scripts/20210423_卒論/data/CountryID.csv",index_col=0)
IndustryID = pd.read_csv("OneDrive - Kyoto University/Download/Scripts/Python Scripts/20210423_卒論/data/IndustryID.csv",index_col=0)
OwnerTypeID = pd.read_csv("OneDrive - Kyoto University/Download/Scripts/Python Scripts/20210423_卒論/data/OwnerTypeID.csv",index_col=0)

# data -----------------------------------------

iso3_in = pd.read_csv("OneDrive - Kyoto University/Download/Scripts/Python Scripts/20210423_卒論/data/investment_of_country/iso3_in.csv")
iso3_out = pd.read_csv("OneDrive - Kyoto University/Download/Scripts/Python Scripts/20210423_卒論/data/investment_of_country/iso3_out.csv")

# delete dev0
iso3_in["2017/2007"] = iso3_in["2017"]/iso3_in["2007"]
iso3_out["2017/2007"] = iso3_out["2017"]/iso3_out["2007"]

# main ========================================

data_load_state.text("")

st.header("Investment of country")

# show data -------------------------------------

st.subheader("Data")

st.write("**Inward**")
st.write(iso3_in)
st.write("**Outward**")
st.write(iso3_out)

inv = st.multiselect("Choose the contents", ["Investment amount","Growth rate","Outward/Inward"])

# if st.checkbox("Investment amount"):
st.subheader("Investment amount")

col1,col2 = st.columns(2) # set column in order to set the plot separately

with col1:
    values = st.slider('Select a color range of values',5.0,15.0, (8.0,13.0),key=1)
    iso3_in["2017_log"] = iso3_in["2017"].map(np.log10)
    fig = px.choropleth(iso3_in, locations="ISO3", locationmode="ISO-3",
                        hover_name="Country", color="2017_log",
                        range_color=values,
                        projection="natural earth", title="Inward 2017 (Log)")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    values = st.slider('Select a color range of values',5.0,15.0, (8.0,13.0), key=2) # key allows the same slider
    iso3_out["2017_log"] = iso3_out["2017"].map(np.log10)
    fig = px.choropleth(iso3_out, locations="ISO3", locationmode="ISO-3",
                        hover_name="Country", color="2017_log",
                        range_color=values,
                        projection="natural earth", title="Outward 2017 (Log)")
    st.plotly_chart(fig, use_container_width=True)
    
# if st.checkbox("Growth rate"):
st.subheader("Growth rate")
col1,col2 = st.columns(2)
with col1:
    fig = px.choropleth(iso3_in, locations="ISO3", locationmode="ISO-3",
                        hover_name="Country", color="2017/2007",
                        color_continuous_midpoint=1,
                        range_color=(0,3),
                        projection="natural earth", title="Inward Growing Rate")
    st.plotly_chart(fig, use_container_width=True)
with col2:
    fig = px.choropleth(iso3_out, locations="ISO3", locationmode="ISO-3",
                        hover_name="Country", color="2017/2007",
                        color_continuous_midpoint=1,
                        range_color=(0,3),
                        projection="natural earth", title="Outward Growing Rate")
    st.plotly_chart(fig, use_container_width=True)
    
# if st.checkbox("Outward/Inward"):
st.subheader("Outward/Inward")
iso3_out["outward/inward"] = iso3_out["2017"]/iso3_in["2017"]

fig = px.choropleth(iso3_out, locations="ISO3", locationmode="ISO-3",
                    hover_name="Country", color="outward/inward",
                    range_color=(0,2),
                    projection="natural earth", title="Outward/Inward")
st.plotly_chart(fig, use_container_width=True)

