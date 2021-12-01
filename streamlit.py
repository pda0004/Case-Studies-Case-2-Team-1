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
    
    all_crops = ['Chickpea','Apple','Papaya','Kidney Beans','Pigeon Peas','Muskmelon','Coffee','Bananas','Rice',
                'Mungbean','Watermelon','Jute','Maize','Lentil','Mangos','Grapes','Moth Beans','Oranges','Blackgram','Cotton',
                'Pomegranates','Coconuts']
    prim = st.selectbox("First Choice Crop",all_crops)
    
    crops = st.multiselect("Other Crops to compare", all_crops)

    
    st.subheader("Additional Parameters")
    
    currency = st.selectbox("Currency",["US Dollars ($)", "Indian Rupee (₹)"])
    
    field_length = st.number_input("Length of Field (m)",min_value = 6, step = 6)
    field_width = st.number_input("Width of Field (m)",min_value = 6, step = 6)
    
    field_size = field_length * field_width
    
    if st.button("Run Model"):
        if crops != [] and crops != [prim]:
            if len(crops) <= 5:
                mode = "res"
            else:
                st.warning("Please select at most 5 crops to compare to")
        else:
            st.warning("You must select at least one crop that is NOT the primary crop to compare to!")
if(mode == "res"):
    crop_num = len(crops) 
    
    ## CROP VALUES HERE
    

    #sample values for demos, DELETE BEFORE FINAL SUBMISSION
    crop_vals = {
        'Chickpea':489,
        'Apple':4092
        'Papaya':2489,
        'Kidney Beans':756,
        'Pigeon Peas':266,
        'Muskmelon':2401,
        'Coffee':2220,
        'Bananas':2339,
        'Rice':533,
        'Mungbean':197,
        'Watermelon':489,
        'Jute':325,
        'Maize':294,
        'Lentil':489,
        'Mangos':5671,
        'Grapes':2245,
        'Moth Beans':667,
        'Oranges':441,
        'Blackgram':498,
        'Cotton':836,
        'Pomegrantes':2836,
        'Coconuts':934
    }
    
    crop_costs = {
        'Chickpea':88,
        'Apple':578,
        'Papaya':1868,
        'Kidney Beans':133,
        'Pigeon Peas':124,
        'Muskmelon':800,
        'Coffee':982,
        'Bananas':498,
        'Rice':244,
        'Mungbean':122,
        'Watermelon':444,
        'Jute':44,
        'Maize':135,
        'Lentil':53,
        'Mangos':1000,
        'Grapes':1104,
        'Moth Beans':124,
        'Oranges':966,
        'Blackgram':119,
        'Cotton':80,
        'Pomegrantes':1067,
        'Coconuts':489
    }
    
    dol_to_INR = 75.12
    
    field_units = field_size / 36
    
    for crop in crop_vals:
        crop_vals[crop] = (crop_vals[crop] / dol_to_INR) *field_units
    for crop in crop_costs:
        crop_costs[crop] = (crop_costs[crop] / dol_to_INR) * field_units
    
    prim_val = crop_vals[prim] 
    prim_cost = crop_costs[prim]
    ## MODEL OUTPUT HERE
    #yield = {MODEL OUTPUT IN DICT FORM}
    #for key in crop_vals.keys():
        #crop_vals[key] = float(crop_vals[key]) * yield[key]
    #prim_val = crop_vals[prim] * yield[key]
    
    
    
    if prim in crops:
        crops.remove(prim)
        
    
    
    
    
    currency_key = currency.split("(")[1][0]
    
    if (currency_key == "₹"):
        prim_val = prim_val * dol_to_INR
        prim_cost = prim_cost * dol_to_INR
        for crop in crop_vals:
            crop_vals[crop] = crop_vals[crop] * dol_to_INR
            crop_costs[crop] = crop_costs[crop] * dol_to_INR
    
    st.subheader(prim)
    st.metric("Expected Profit" ,currency_key + str('%.2f'%prim_val))
    st.metric("Cost of Cultivation" ,currency_key + str('%.2f'%prim_cost))
    
    st.subheader("Alternatives")
    
    cols = st.columns(crop_num)
    col_num = 0
    for crop in crops:
        column = cols[col_num]
        column.subheader(crop)
        column.metric("Price",currency_key + str('%.2f'%crop_vals[crop]),'%.2f'%(crop_vals[crop]-prim_val))
        column.metric("Cost of Cultivation",currency_key + str('%.2f'%crop_costs[crop]),'%.2f'%(crop_costs[crop]-prim_cost),delta_color = "inverse")
        column.metric("% Yield","100%",0)
        col_num+=1
    if st.button("Return"):
        mode = "input"
       
    