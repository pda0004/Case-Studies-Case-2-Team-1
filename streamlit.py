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
    in_cols = st.columns(3)
    in_cols[0].subheader("Soil Information")

    n_lvl = in_cols[0].number_input("Soil Nitrogen", min_value=0.0,value=51.0)
    p_lvl = in_cols[0].number_input("Soil Phosphorous", min_value=0.0,value=53.0)
    k_lvl = in_cols[0].number_input("Soil Potassium", min_value=0.0,value=48.0)
    ph_lvl = in_cols[0].number_input("Soil pH", min_value=0.0,max_value=14.0,value=6.5)

    in_cols[1].subheader("Climate Information")

    temp = in_cols[1].number_input("Avg Temperature (°C)", min_value=0.0,value=26.0)
    hum = in_cols[1].number_input("Avg Humidity", min_value=0.0,max_value=100.0,value=72.0)
    rain = in_cols[1].number_input("Average Rainfall (mm)", min_value=0.0,value=103.0)
    
    xs = np.reshape([n_lvl,p_lvl,k_lvl,ph_lvl,temp,hum,rain],(1, -1))

    st.subheader("Viable Crops")
    
    all_crops = ['Chickpea','Apple','Papaya','Kidney Beans','Pigeon Peas','Muskmelon','Coffee','Bananas','Rice',
                'Mungbean','Watermelon','Jute','Maize','Lentil','Mangos','Grapes','Moth Beans','Oranges','Blackgram','Cotton',
                'Pomegranates','Coconuts']
    prim = st.selectbox("First Choice Crop",all_crops)
    
    crops = st.multiselect("Other Crops to compare (Max 5)", all_crops)

    
    in_cols[2].subheader("Additional Parameters")
    
    currency = in_cols[2].selectbox("Currency",["US Dollars ($)", "Indian Rupee (₹)"])
    
    field_length = in_cols[2].number_input("Length of Field (m)",min_value = 6, step = 6)
    field_width = in_cols[2].number_input("Width of Field (m)",min_value = 6, step = 6)
    
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
        'Apple':4092,
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
        'Pomegranates':2836,
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
        'Pomegranates':1067,
        'Coconuts':489
    }
    
    dol_to_INR = 75.12
    
    field_units = field_size / 36
    
    for crop in crop_vals:
        crop_vals[crop] = (crop_vals[crop] / dol_to_INR) *field_units
    for crop in crop_costs:
        crop_costs[crop] = (crop_costs[crop] / dol_to_INR) * field_units
    
    
    ## MODEL OUTPUT HERE
    model = pickle.load(open("models/model.sav", 'rb'))
    probs = model.predict_log_proba(xs).tolist()[0]
    
    
    yields = [min(100,max(0,-0.2*i-.4)) for i in probs]
    
    yield_dict = {
        'Chickpea':1-yields[0],
        'Apple':1-yields[1],
        'Papaya':1-yields[2],
        'Kidney Beans':1-yields[3],
        'Pigeon Peas':1-yields[4],
        'Muskmelon':1-yields[5],
        'Coffee':1-yields[6],
        'Bananas':1-yields[7],
        'Rice':1-yields[8],
        'Mungbean':1-yields[9],
        'Watermelon':1-yields[10],
        'Jute':1-yields[11],
        'Maize':1-yields[12],
        'Lentil':1-yields[13],
        'Mangos':1-yields[14],
        'Grapes':1-yields[15],
        'Moth Beans':1-yields[16],
        'Oranges':1-yields[17],
        'Blackgram':1-yields[18],
        'Cotton':1-yields[19],
        'Pomegranates':1-yields[20],
        'Coconuts':1-yields[21]
    }
    
    for key in crop_vals.keys():
        crop_vals[key] = float(crop_vals[key]) * yield_dict[key]
    
    prim_val = crop_vals[prim] 
    prim_cost = crop_costs[prim]
    
    if prim in crops:
        crops.remove(prim)
        
   
    currency_key = currency.split("(")[1][0]
    
    if (currency_key == "₹"):
        prim_val = prim_val * dol_to_INR
        prim_cost = prim_cost * dol_to_INR
        for crop in crop_vals:
            crop_vals[crop] = crop_vals[crop] * dol_to_INR
            crop_costs[crop] = crop_costs[crop] * dol_to_INR
    
    st.header("Analysis and Reccomendations")
    
    prim_val_str = ""
    prim_cost_str = ""
    
    if prim_val > 1000:
            prim_val = prim_val / 1000
            prim_val_str = "K"
            if prim_val > 1000:
                prim_val = prim_val / 1000
                prim_val_str = "M"
                if prim_val > 1000:
                    prim_val = prim_val / 1000
                    prim_val_str = "B"
                 
    if prim_cost > 1000:
            prim_cost = prim_cost / 1000
            prim_cost_str = "K"
            if prim_cost > 1000:
                prim_cost = prim_cost / 1000
                prim_cost_str = "M"
                if prim_cost > 1000:
                    prim_cost = prim_cost / 1000
                    prim_cost_str = "B"
    
    pri_cols = st.columns(2)
    pri_cols[0].subheader("Your Choice: " + prim)
    pri_cols[0].metric("Expected Profit" ,currency_key + str('%.2f'%prim_val) + prim_val_str)
    pri_cols[0].metric("Cost of Cultivation" ,currency_key + str('%.2f'%prim_cost) + prim_cost_str)
    pri_cols[0].metric("% Yield",('%.2f'%(yield_dict[prim]*100))+ "%")
    
    max_yield = max(crop_vals, key=crop_vals.get)
    
    rec_val = crop_vals[max_yield]
    rec_cost = crop_costs[max_yield]
    
    rec_val_str = ""
    rec_cost_str = ""
    
    if rec_val > 1000:
            rec_val = rec_val / 1000
            rec_val_str = "K"
            if prim_val > 1000:
                rec_val = rec_val / 1000
                rec_val_str = "M"
                if rec_val > 1000:
                    rec_val = rec_val / 1000
                    rec_val_str = "B"
                 
    if rec_cost > 1000:
            rec_cost = rec_cost / 1000
            rec_cost_str = "K"
            if rec_cost > 1000:
                rec_cost = rec_cost / 1000
                rec_cost_str = "M"
                if rec_cost > 1000:
                    rec_cost = rec_cost / 1000
                    rec_cost_str = "B"
    if not max_yield == prim:
        pri_cols[1].subheader("Reccomendation: " + max_yield)
        pri_cols[1].metric("Expected Profit" ,currency_key + str('%.2f'%rec_val) + rec_val_str)
        pri_cols[1].metric("Cost of Cultivation" ,currency_key + str('%.2f'%rec_cost) + rec_cost_str)
        pri_cols[1].metric("% Yield",('%.2f'%(yield_dict[max_yield]*100))+ "%")
    else:
        pri_cols[1].success(prim + " is the most reccommended crop")
    st.subheader("Your Selected Alternatives")
    
    cols = st.columns(crop_num)
    col_num = 0
    for crop in crops:
        column = cols[col_num]
        column.subheader(crop)
        ind_val = crop_vals[crop]
        ind_val_diff = crop_vals[crop]-prim_val
        ind_cost = crop_costs[crop]
        ind_cost_diff = crop_costs[crop]-prim_cost
        
        
        ind_val_str = ""
        ind_val_diff_str = ""
        ind_cost_str = ""
        ind_cost_diff_str = ""
        
        if ind_val > 1000:
            ind_val = ind_val / 1000
            ind_val_str = "K"
            if ind_val > 1000:
                ind_val = ind_val / 1000
                ind_val_str = "M"
                if ind_val > 1000:
                    ind_val = ind_val / 1000
                    ind_val_str = "B"
        
        if ind_val_diff > 1000:
            ind_val_diff = ind_val_diff / 1000
            ind_val_diff_str = "K"
            if ind_val_diff > 1000:
                ind_val_diff = ind_val_diff / 1000
                ind_val_diff_str = "M"
                if ind_val_diff > 1000:
                    ind_val_diff = ind_val_diff / 1000
                    ind_val_diff_str = "B"
                    
        if ind_cost > 1000:
            ind_cost = ind_cost / 1000
            ind_cost_str = "K"
            if ind_cost > 1000:
                ind_cost = ind_cost / 1000
                ind_cost_str = "M"
                if ind_cost > 1000:
                    ind_cost = ind_cost/ 1000
                    ind_cost_str = "B"
                    
        if ind_cost_diff > 1000:
            ind_cost_diff = ind_cost_diff / 1000
            ind_cost_diff_str = "K"
            if ind_cost_diff > 1000:
                ind_cost_diff = ind_cost_diff / 1000
                ind_cost_diff_str = "M"
                if ind_cost_diff > 1000:
                    ind_cost_diff = ind_cost_diff / 1000
                    ind_cost_diff_str = "B"
        
        column.metric("Price",currency_key + str('%.2f'%ind_val) + ind_val_str,'%.2f'%(ind_val_diff) + ind_val_diff_str)
        column.metric("Cost of Cultivation",currency_key + str('%.2f'%ind_cost) + ind_cost_str,'%.2f'%(ind_cost_diff) + ind_cost_diff_str,delta_color = "inverse")
        column.metric("% Yield",('%.2f'%(yield_dict[crop]*100))+ "%")
        col_num+=1
    if st.button("Return"):
        mode = "input"
       
    