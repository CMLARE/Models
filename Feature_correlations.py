
# coding: utf-8

# Check correlations among features

# # Data

# RainFall data : Department of Meteorology - Sri Lanka.

# Microwave link data: Dialog Axiata, Mobile network operator company [Sri Lanka]

# In[1]:


import pandas as pd
from matplotlib import pyplot as plot
import seaborn as sb

# allow plots to appear in the notebook
get_ipython().magic('matplotlib inline')


# In[29]:


data_file = pd.read_csv("/home/cmlare/Data/RF Data/Processed/2018-07-30 to 2018-08-19_integrated_new_features_classified.csv")
# data_file_1 = pd.read_csv("/home/cmlare/Data/RF Data/Processed/2018-05-16 to 2018-05-23_integrated.csv", index_col=[1,0])
# data_file_2 = pd.read_csv("/home/cmlare/Data/RF Data/Processed/2018-05-24 to 2018-05-31_integrated.csv", index_col=[1,0])

# data_file = pd.concat([data_file, data_file_1, data_file_2])


# remove rows with precipitation 0

# In[3]:


data_file


# In[4]:


# data_file_removed_zero = data_file[data_file["precipitation(mm)"] != 0.0]


# In[30]:


data_file_less_3 = data_file.loc[lambda x: x["distance"] < 5]
data_file_less_3["PAttAvg"].apply(lambda x: x* pow(10,20))


# In[31]:


data_file_less_3["Attn_Path_len"] = data_file_less_3["PAttAvg"].div(data_file_less_3["PathLength"])
data_file_less_3["RSL_MIN_PATH_LEN"] = data_file_less_3["RSL_MIN"].div(data_file_less_3["PathLength"])
data_file_less_3["RSL_AVG_PATH_LEN"] = data_file_less_3["RSL_AVG"].div(data_file_less_3["PathLength"])


# In[32]:


# data_file_less_3


# In[33]:


data_file_less_3["Baseline_ATTN"] = data_file_less_3["Baseline"].sub(data_file_less_3["RSL_MIN"])


# In[34]:


def calculate_time(row):
    if (row["RSL_MAX"] - row["RSL_MIN"]) == 0:
        return 15
    else:
        time  = 15*(row["RSL_MAX"] - row["RSL_AVG"]) / (row["RSL_MAX"] - row["RSL_MIN"])
        return time
    
data_file_less_3["refined"] = data_file_less_3.apply(lambda x: calculate_time(x)*x["Baseline_ATTN"], axis=1)
data_file_less_3["time"] = data_file_less_3.apply(lambda x: calculate_time(x), axis=1)


# In[35]:


# correlation = data_file_less_3.corr()


# In[36]:


# correlation


# In[22]:


plot.imshow(correlation, cmap= "hot")


# In[28]:


# plotting a bar graph
# correlation = correlation.drop("ID")
correlation = correlation.drop("precipitation(mm)")


# In[38]:


correlation = data1.corr()
correlation1 = data2.corr()
correlation2 = data3.corr()
correlation3 = data4.corr()
correlation4 = data5.corr()

correlation = correlation.drop("precipitation(mm)")
correlation1 = correlation1.drop("precipitation(mm)")
correlation2 = correlation2.drop("precipitation(mm)")
correlation3 = correlation3.drop("precipitation(mm)")
correlation4 = correlation4.drop("precipitation(mm)")


# In[37]:


all_features = [ 'ID', 'Frequency', 'FrequencyBand', 'PAttAvg', 'PRAvg', 'PRmax', 'PRmin',"Attn_Path_len", "RSL_MIN_PATH_LEN","RSL_AVG_PATH_LEN",
       'PTAvg', 'PTmax', 'PTmin', 'PathLength', 'PrecipStation', 'RSL_AVG',"Baseline_ATTN", "refined",
       'RSL_MAX', 'RSL_MIN', 'SLAttn', 'TSL_AVG', 'TSL_MAX', 'TSL_MIN', 'XEnd', "time",
       'XStart', 'YEnd', 'YStart', 'distance', 'Baseline', "min_RSL_MIN" , "std", "slope_autocorr", "quantile_10", "quantile_90"]

features = ['Frequency', 'FrequencyBand', 'PAttAvg', 'PRAvg', 'PRmax', 'PRmin',"precipitation(mm)",
       'PTAvg', 'PTmax', 'PTmin', 'PathLength', 'RSL_AVG',
       'RSL_MAX', 'RSL_MIN', 'SLAttn', 'TSL_AVG', 'TSL_MAX', 'TSL_MIN']

features_2 = ['Frequency', 'FrequencyBand', 'PAttAvg', 'PRAvg', 'PRmax', 'PRmin', "precipitation(mm)",
       'PTAvg', 'PTmax', 'PTmin', 'PathLength',"Baseline", "RSL_MIN", "Baseline_ATTN"]

features_3 = ['Frequency', 'FrequencyBand', 'PAttAvg', 'PRAvg', 'PRmax', 'PRmin', "precipitation(mm)",
       'PTAvg', 'PTmax', 'PTmin', 'PathLength', "min_RSL_MIN" , "std", "slope_autocorr", 
              "quantile_10", "quantile_90" ,"RSL_MIN"]

features_4 = ['Frequency', 'FrequencyBand', 'PAttAvg', 'PRAvg', 'PRmax', 'PRmin', "precipitation(mm)",
       'PTAvg', 'PTmax', 'PTmin', 'PathLength',"Attn_Path_len", "RSL_MIN_PATH_LEN","RSL_AVG_PATH_LEN" ,"RSL_MIN"]

feature_5 = ['Frequency', 'FrequencyBand', 'PAttAvg', 'PRAvg', 'PRmax', 'PRmin', "RSL_MIN", "precipitation(mm)",
       'PTAvg', 'PTmax', 'PTmin', 'PathLength',"refined", "time", "Baseline_ATTN"]

data1 = data_file_less_3[features]
data2 = data_file_less_3[features_2]
data3 = data_file_less_3[features_3]
data4 = data_file_less_3[features_4]
data5 = data_file_less_3[feature_5]


# In[39]:


(correlation4["precipitation(mm)"].sort_values(ascending=False).plot.barh())


# In[14]:


correlation


# In[15]:


sb.pairplot(data_file_less_3, x_vars=["RSL_MIN", "PAttAvg", "FrequencyBand", "distance"], y_vars=["precipitation(mm)"], size=7, aspect = 0.7)


# In[16]:


sb.pairplot(data_file_less_3, x_vars=["RSL_MIN_PATH_LEN", "Attn_Path_len"], y_vars=["precipitation(mm)"], size=10)


# In[17]:


specific_link = data_file_less_3.loc[2221]


# In[18]:


# specific_link["PAttAvg"].apply(lambda x: x* pow(10,20))


# In[19]:


sb.pairplot(specific_link, x_vars=["RSL_MIN", "PAttAvg", "FrequencyBand", "distance"], y_vars=["precipitation(mm)"], size=10, aspect = 0.7, kind="reg")

