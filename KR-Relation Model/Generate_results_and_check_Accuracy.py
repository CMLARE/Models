# This method is used to generate results using the equation

import pandas as pd
import numpy as np
import matplotlib as plt
from sklearn.metrics import accuracy_score

a_b_coefficients = pd.read_csv("/home/cmlare/Data/RF Data/Master Files/kRPowerLawData.csv")
# data_file = pd.read_csv("/home/cmlare/Dumindu/Information/1_DATA/KR_Model_data/wet_dry_2018-05-08 to 2018-05-31")
data_file = pd.read_csv("/home/cmlare/Data/RF Data/Processed/2018-05-24 to 2018-05-31_integrated_classified.csv")


data_file["Baseline_ATTN"] = data_file["Baseline"].sub(data_file["RSL_MIN"])
data_file["B_ATTN_PathLen"] = data_file["Baseline_ATTN"].div(data_file["distance"])

data_file_wet = data_file
# data_file.loc[data_file.wet_dry == "Wet"]
# data_file_dry = data_file.loc[data_file.wet_dry == "Dry"]


# a , b coeffiecints in thier order as in the data file
selected_a = []
selected_b = []
results = []


for index, row in data_file_wet.iterrows():
    frequency = row.FrequencyBand
    
    best_ab = a_b_coefficients.loc[((a_b_coefficients["f"] - frequency) < 1)]
    best_ab_2 = best_ab.loc[(best_ab["f"] - frequency) > 0]
    ab_row_selected = best_ab_2.loc[best_ab_2['f'].idxmin()]
    rainfall = (row.B_ATTN_PathLen/ ab_row_selected.a) ** (1/ab_row_selected.b)
#     filename = "/home/cmlare/Dumindu/Information/1_DATA/KR_Model_data/results.csv"
#     with open(filename, 'a') as out:
#         out.write(rainfall + '\n')
    print(rainfall)
    results.append(rainfall)

print(results)

print(max(results))
print(min(results))
data_file_wet["results_values"] = results

results_class = []
for value in results:
    if value < 0.1:
        results_class.append("A")
    elif value <= 0.5 and value >=0.1:
        results_class.append("B")
    elif value <= 1 and value > 0.5:
        results_class.append("C")
    elif value <= 2.5 and value >1:
        results_class.append("D")
    elif value <= 5 and value >2.5:
        results_class.append("E")
    elif value <= 7 and value >5:
        results_class.append("F")
    elif value <= 10 and value >7:
        results_class.append("G")
    elif value >10:
        results_class.append("H")

data_file_wet["results_class"] = results_class

wet_data_only = data_file_wet.loc[data_file_wet["class"] != "A"]
dry_data_only = data_file_wet.loc[data_file_wet["class"] == "A"]



accuracy_only_wet = accuracy_score(wet_data_only["class"], wet_data_only.results_class)
print(accuracy_only_wet)
accuracy_only_dry = accuracy_score(dry_data_only["class"], dry_data_only.results_class)
print(accuracy_only_dry)

accuracy = accuracy_score(data_file_wet["class"], data_file_wet.results_class)

print(accuracy)

# plotting the results


import pandas as pd 
import folium
from folium.plugins import HeatMap


for_map = pd.read_csv('/home/cmlare/Data/RF Data/Processed/2018-05-08 to 2018-05-15_integrated_classified.csv')


for_map

max_amount = float(for_map['TSL_MIN'].max())
max_amount

hmap = folium.Map(location=[6.917200, 79.913300], zoom_start=7, )

hm_wide = HeatMap( list(zip(for_map.XEnd.values, for_map.YEnd.values, for_map.TSL_MIN.values)),
                   min_opacity=0.8,
                   max_val=max_amount,
                   radius=17, blur=15, 
                   max_zoom=1, 
                 )

# folium.GeoJson(district23).add_to(hmap)
hmap.add_child(hm_wide)

