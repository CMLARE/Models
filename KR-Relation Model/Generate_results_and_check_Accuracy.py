
# coding: utf-8

# In[1]:


# This method is used to generate results using the equation


# In[16]:


import pandas as pd
import matplotlib as plt

a_b_coefficients = pd.read_csv("/home/cmlare/Data/RF Data/Master Files/kRPowerLawData.csv")
data_file = pd.read_csv("/home/cmlare/Dumindu/Information/1_DATA/KR_Model_data/wet_dry_2018-05-08 to 2018-05-31")


# In[ ]:


data_file["Baseline_ATTN"] = data_file["Baseline"].sub(data_file["RSL_MIN"])
data_file["B_ATTN_PathLen"] = data_file["Baseline_ATTN"].div(data_file["distance"])


# In[10]:


a_b_coefficients


# In[ ]:


data_file_wet = data_file.loc[data_file.wet_dry == "Wet"]
data_file_dry = data_file.loc[data_file.wet_dry == "Dry"]


# In[ ]:


# a , b coeffiecints in thier order as in the data file
selected_a = []
selected_b = []
results = []


# In[17]:


a_b_coefficients.loc[a_b_coefficients['f'].idxmin()]


# In[ ]:


for index,row in data_file_wet:
    frequency = row.FrequencyBand
    
    best_ab = a_b_coefficients.loc[(a_b_coefficients["f"] - frequency) < 1 and (a_b_coefficients["f"] - frequency) > 0]
    ab_row_selected = best_ab.loc[best_ab['FrequencyBand'].idxmin()]
        
    rainfall = ab_row_selected.a * (data_file_wet.B_ATTN_PathLen ** ab_row_selected.b)
    results.append(rainfall)


# In[ ]:


# plotting the results


# In[2]:


import pandas as pd 
import folium
from folium.plugins import HeatMap


# In[3]:


for_map = pd.read_csv('/home/cmlare/Data/RF Data/Processed/2018-05-08 to 2018-05-15_integrated_classified.csv')


# In[4]:


for_map


# In[5]:


max_amount = float(for_map['TSL_MIN'].max())
max_amount


# In[8]:


hmap = folium.Map(location=[6.917200, 79.913300], zoom_start=7, )

hm_wide = HeatMap( list(zip(for_map.XEnd.values, for_map.YEnd.values, for_map.TSL_MIN.values)),
                   min_opacity=0.2,
                   max_val=max_amount,
                   radius=17, blur=15, 
                   max_zoom=1, 
                 )


# In[ ]:


# folium.GeoJson(district23).add_to(hmap)
hmap.add_child(hm_wide)

