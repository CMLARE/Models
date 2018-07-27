
# coding: utf-8

# In[3]:


import pandas as pd
# from matplotlib import pyplot as plot
# import seaborn as sb


# In[4]:


data_root = "/home/cmlare/Data/RF Data/Processed/"


# In[5]:


# rainfall_mapped_df_1 = pd.read_csv(data_root+"2018-05-08 to 2018-05-15_integrated.csv")


# In[6]:


rainfall_classified_1 = pd.read_csv(data_root+"2018-05-08 to 2018-05-15_integrated_classified.csv")


# In[7]:


rainfall_classified_2 = pd.read_csv(data_root+"2018-05-16 to 2018-05-23_integrated_classified.csv")


# In[8]:


rainfall_classified_3 = pd.read_csv(data_root+"2018-05-24 to 2018-05-31_integrated_classified.csv")


# In[14]:


rainfall_classified = pd.concat([rainfall_classified_1, rainfall_classified_2, rainfall_classified_2])


# In[15]:


rainfall_classified_near = rainfall_classified.loc[lambda x: x["distance"] < 5]


# In[ ]:


specific_data_frame = rainfall_classified_near


# **Uncomment line below for testing.**

# In[16]:


# specific_data_frame = rainfall_classified_near.loc[rainfall_classified_near.ID==1454]


# In[17]:


specific_data_frame["Baseline_ATTN"] = specific_data_frame["Baseline"].sub(specific_data_frame["RSL_MIN"])


# In[18]:


# specific_data_frame["Baseline_ATTN"].plot(x=specific_data_frame["date_time"], y=specific_data_frame.Baseline)

# specific_data_frame["precipitation(mm)"].plot(x=specific_data_frame["date_time"], y=specific_data_frame["precipitation(mm)"])


# In[ ]:


print(specific_data_frame.describe().transpose())


# In[19]:


#specific_data_frame.columns


# In[27]:


selected_feature_frame = specific_data_frame[["FrequencyBand","Baseline_ATTN","class","PathLength"]]


# In[28]:


#selected_feature_frame.shape


# In[29]:


X = selected_feature_frame.drop('class',axis = 1)


# In[33]:


y = selected_feature_frame['class']


# In[34]:


from sklearn.model_selection import train_test_split


# In[36]:


X_train, X_test, y_train, y_test = train_test_split(X,y )


# **Data Preprocessing**

# In[37]:


from sklearn.preprocessing import StandardScaler


# In[38]:


scaler = StandardScaler()


# In[39]:


# Fit only to the training data
print("Fitting data..")
scaler.fit(X_train)
print("Data fitting finished.")


# In[40]:


StandardScaler(copy=True, with_mean=True, with_std=True)


# In[41]:


# Now apply the transformations to the data:
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)


# Training The Model

# In[42]:


from sklearn.neural_network import MLPClassifier


# In[43]:


mlp = MLPClassifier(hidden_layer_sizes=(13,13,13),max_iter=500)


# In[44]:


print("Training the model..")
mlp.fit(X_train,y_train)
print("Model training finished.")


# **Predictions and Evaluation**

# In[ ]:


print("Running Predictions on train data..")
predictions = mlp.predict(X_test)
print("Running predictions finished.")


# In[ ]:


from sklearn.metrics import classification_report,confusion_matrix


# Evaluation

# In[ ]:


print(confusion_matrix(y_test,predictions))


# In[ ]:


print(classification_report(y_test,predictions))


# **Saving the Model**

# In[ ]:


import pickle


# In[ ]:


filename = "/home/cmlare/Data/Models/"+'mlp_ANN_REDUCED_DATA.sav'
print("Saving model to "+ filename)
pickle.dump(mlp, open(filename, 'wb'))
print("Model Saved!")

