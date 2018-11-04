
# coding: utf-8

# In[1]:


# Step 1 : Convert the link coordinates to azimuthal equidistant cartesian coordinate system


# In[1]:


import pandas as pd
import numpy as np
from geopy.distance import lonlat,distance

data_file = pd.read_csv("/home/cmlare/Data/RF Data/Processed/2018-05-08 to 2018-05-15_integrated_classified.csv")
data_file_1 = pd.read_csv("/home/cmlare/Data/RF Data/Processed/2018-05-16 to 2018-05-23_integrated_classified.csv")
data_file_2 = pd.read_csv("/home/cmlare/Data/RF Data/Processed/2018-05-24 to 2018-05-31_integrated_classified.csv")

data_file = pd.concat([data_file, data_file_1, data_file_2])
link_file = pd.read_csv("/home/cmlare/Data/RF Data/Master Files/mapped_links.csv")


# In[2]:


data_file


# In[84]:


min(data_file["Baseline_ATTN"])


# In[57]:


max(data_file["B_ATTN_PathLen"])
A = data_file.loc[data_file["class"] == "A"]

B = data_file.loc[data_file["class"] == "B"]

C = data_file.loc[data_file["class"] == "C"]

D = data_file.loc[data_file["class"] == "D"]

E = data_file.loc[data_file["class"] == "E"]

F = data_file.loc[data_file["class"] == "F"]

G = data_file.loc[data_file["class"] == "G"]

H = data_file.loc[data_file["class"] == "H"]


# In[74]:


min(H["B_ATTN_PathLen"])


# In[3]:


data_file["Baseline_ATTN"] = data_file["Baseline"].sub(data_file["RSL_MIN"])
data_file["B_ATTN_PathLen"] = data_file["Baseline_ATTN"].div(data_file["distance"])


# In[4]:


link_file


# In[5]:


data_file


# In[24]:


distance((6.90607, 79.9149),(6.9244,79.8718)).km


# In[79]:


set1 = set([])
nearby_links = list()

# Loop to calculate unique links
for index, row in data_file.iterrows():
   set1.add(row['ID']) 


# In[80]:


#  find the nearby links
for element in set1:
    nearbylinks_list = list()
    row = pd.concat([link_file.loc[link_file.id_1 == element],link_file.loc[link_file.id_2 == element] ])
    long1 = row.longitude1.values[0]
    lat1 = row.latitude1.values[0]
    long2 = row.longitude2.values[0]
    lat2 = row.latitude2.values[0]
    
    for index2, row2 in link_file.iterrows():
        newlong1 = row2.longitude1
        newlat1 = row2.latitude1
        newlong2 = row2.longitude2
        newlat2 = row2.latitude2

#       Using the geopy library we are calculating the geodesic distance between two points.
#       rror of up to about 0.5%  
        distance1 = distance((lat1, long1), (newlat1, newlong1)).km
        distance2 = distance((lat1, long1), (newlat2, newlong2)).km
        distance3 = distance((lat2, long2), (newlat1, newlong1)).km
        distance4 = distance((lat2, long2), (newlat2, newlong2)).km
        
        condition = ((distance1 or distance2) and (distance3 or distance4))<= 5
        
        if (condition):
            nearbylinks_list.append(row2.id_1)
            nearbylinks_list.append(row2.id_2)
    nearby_links.append(nearbylinks_list)
    


# In[82]:


set1_tolist = list(set1)


# In[ ]:


wetDry = list()
for index, row in data_file.iterrows():
    current_id = row.ID
    timestamp = row.date_time
    
    index_from_ids = set1_tolist.index(current_id)
    get_nearbylinks = nearby_links[index_from_ids]
    
    if len(get_nearbylinks) <5:
        continue
    attenuation_list = list()
    attenutaion_list_with_Len = list()
    
    for link in get_nearbylinks:
        row1 = data_file.date_time
        row1 = data_file.loc[data_file.ID == link]
        print(row1)
        break
        attenuation_list.append(row1.Baseline_ATTN.values)
        attenutaion_list_with_Len.append(row1.B_ATTN_PathLen.values)
        
#     print(attenuation_list)
#     print(attenutaion_list_with_Len)
    attenuation_list = sorted(attenuation_list)
    attenutaion_list_with_Len = sorted(attenutaion_list_with_Len)
    
    median_Attn_list = np.median(attenuation_list)
    median_Attn_list_with_len = np.median(attenutaion_list_with_Len)
    
    #   -0.7 dB = 29.3 dBm     -1.4 dB = 28.6 dBm    2 dB = 32dBm
    
    if median_Attn_list > 28.6:
        wetDry.append("Wet")
    else:
        wetDry.append("Dry")
        
print(wetDry)


# In[ ]:


# for nearbylinks in nearby_links:
#     if len(nearbylinks) >= 4:
#         for eachlink in nearbylinks:
#


# In[69]:


# Radius = 5
# def WetDryNearbyLinkApMinMaxRSL():
#     x = 1

