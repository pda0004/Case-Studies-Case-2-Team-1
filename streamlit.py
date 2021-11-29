import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pickle



#Theme

primaryColor="#6eb52f"
backgroundColor="#f0f0f5"
secondaryBackgroundColor="#e0e0ef"
textColor="#262730"
font="sans serif"

st.title("Crop Value Dashboard")
crops = []

results = False

mode = "input"

if (mode == "input"):
    st.header("Growing Condition Inputs")

    st.subheader("Soil Information")

    n_lvl = st.number_input("Soil Nitrogen")
    p_lvl = st.number_input("Soil Phosphorous")
    k_lvl = st.number_input("Soil Potassium")
    ph_lvl = st.number_input("Soil pH")

    st.subheader("Climate Information")

    temp = st.number_input("Avg Temperature")
    hum = st.number_input("Avg Humidity")
    rain = st.number_input("Average Rainfall")

    st.subheader("Viable Crops")
    
    all_crops = ['Corn','Rice','Beans','Grapes']
    prim = st.selectbox("First Choice Crop",all_crops)
    
    crops = st.multiselect("Other Crops to compare", all_crops)

    
    if st.button("Run Model"):
        if crops != [] and crops != [prim]:
            mode = "res"
        else:
            st.warning("You must select at least one crop that is NOT the primary crop to compare to!")
if(mode == "res"):
    crop_num = len(crops) 
    
    ## CROP VALUES HERE
    

    #sample values for demos, DELETE BEFORE FINAL SUBMISSION
    crop_vals = {
        'Corn':1.00,
        'Rice':2.00,
        'Beans':3.00,
        'Grapes':4.00
    }
    
    prim_val = crop_vals[prim] 
    ## MODEL OUTPUT HERE
    #yield = {MODEL OUTPUT IN DICT FORM}
    #for key in crop_vals.keys():
        #crop_vals[key] = float(crop_vals[key]) * yield[key]
    #prim_val = crop_vals[prim] * yield[key]
    
    st.subheader("Primary Crop")
    st.metric(prim,"$" + str('%.2f'%prim_val))
    
    if prim in crops:
        crops.remove(prim)
        
    st.subheader("Alternatives")
    
    dol_to_INR = 75.12
    INR_vals = {}
    
    for crop in crop_vals:
        INR_vals[crop] = crop_vals[crop] * dol_to_INR
    
    cols = st.columns(crop_num)
    col_num = 0
    for crop in crops:
        column = cols[col_num]
        column.subheader(crop)
        column.metric("Price ($)","$" + str('%.2f'%crop_vals[crop]),'%.2f'%(crop_vals[crop]-prim_val))
        column.metric("Price (₹)",str('%.2f'%INR_vals[crop]) + "₹",'%.2f'%(INR_vals[crop]-(prim_val*dol_to_INR)) + "₹")
        column.metric("% Yield","100%",0)
        col_num+=1
    if st.button("Return"):
        mode = "input"
       
    