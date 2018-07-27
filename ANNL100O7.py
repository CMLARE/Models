
# coding: utf-8

# In[ ]:


import pandas as pd
#from matplotlib import pyplot as plot
#import seaborn as sb


# In[ ]:


data_root = "/home/cmlare/Data/RF Data/Processed/"


# In[ ]:


# rainfall_mapped_df_1 = pd.read_csv(data_root+"2018-05-08 to 2018-05-15_integrated.csv")
print("Loading Data..")


# In[ ]:


rainfall_classified_1 = pd.read_csv(data_root+"2018-05-08 to 2018-05-15_integrated_classified.csv")


# In[ ]:


# rainfall_classified_1


# In[ ]:


rainfall_classified_2 = pd.read_csv(data_root+"2018-05-16 to 2018-05-23_integrated_classified.csv")


# In[ ]:


rainfall_classified_3 = pd.read_csv(data_root+"2018-05-24 to 2018-05-31_integrated_classified.csv")


# In[ ]:


rainfall_classified_4 = pd.read_csv(data_root+"2018-06-01 to 2018-06-10_integrated_classified.csv")


# In[ ]:


rainfall_classified = pd.concat([rainfall_classified_1, rainfall_classified_2, rainfall_classified_3,rainfall_classified_3,rainfall_classified_4])


# In[ ]:


# rainfall_classified = rainfall_classified.loc[lambda x: x["distance"] < 5]


# ** Resampling the Non Zero Attenuation **

# In[ ]:


non_rainy = rainfall_classified.loc[rainfall_classified["precipitation(mm)"]!=0]
#Oversampled 7 times
rainfall_classified = pd.concat([rainfall_classified,non_rainy,non_rainy,non_rainy, non_rainy,non_rainy, non_rainy,non_rainy])


# In[ ]:


specific_data_frame = rainfall_classified
print("Loading of data finished.")


# **Uncomment line below for testing.**

# In[ ]:


# specific_data_frame = rainfall_classified.loc[rainfall_classified.ID==1454]
# specific_data_frame.date_time


# In[ ]:


specific_data_frame["Baseline_ATTN"] = specific_data_frame["Baseline"].sub(specific_data_frame["RSL_MIN"])


# In[ ]:


# specific_data_frame["Baseline_ATTN"].plot(x=specific_data_frame["date_time"], y=specific_data_frame.Baseline_ATTN)

# specific_data_frame["precipitation(mm)"].plot(x=specific_data_frame["date_time"], y=specific_data_frame["precipitation(mm)"])


# In[45]:


print(specific_data_frame.describe().transpose())


# In[46]:


#specific_data_frame.columns


# In[ ]:


selected_feature_frame = specific_data_frame[["FrequencyBand","Baseline_ATTN","class","PathLength"]]


# In[ ]:


#selected_feature_frame.shape


# In[ ]:


X = selected_feature_frame.drop('class',axis = 1)


# In[ ]:


y = selected_feature_frame['class']


# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


# X_train, X_test, y_train, y_test = train_test_split(X,y )


# **Data Preprocessing**

# In[ ]:


from sklearn.preprocessing import StandardScaler


# In[ ]:


scaler = StandardScaler()


# In[ ]:


# Fit only to the training data
print("Fitting data..")
# scaler.fit(X_train)
scaler.fit(X)
print("Data fitting finished.")


# In[ ]:


StandardScaler(copy=True, with_mean=True, with_std=True)


# In[ ]:


# Now apply the transformations to the data:
# X_train = scaler.transform(X_train)
# X_test = scaler.transform(X_test)
X = scaler.transform(X)


# Training The Model

# In[ ]:


from sklearn.neural_network import MLPClassifier


# In[ ]:


mlp = MLPClassifier(hidden_layer_sizes=(100,100,100),max_iter=500)


# In[ ]:


print("Training the model..")
# mlp.fit(X_train,y_train)
mlp.fit(X,y)
print("Model training finished.")


# **Predictions and Evaluation**

# In[ ]:


print("Running Predictions on train data..")
# predictions = mlp.predict(X_test)
predictions = mlp.predict(X)
print("Running predictions finished.")


# In[ ]:


from sklearn.metrics import classification_report,confusion_matrix


# Evaluation

# In[62]:


# print(confusion_matrix(y_test,predictions))
print(confusion_matrix(y,predictions))


# In[63]:


# print(classification_report(y_test,predictions))
print(classification_report(y,predictions))


# **Saving the Model**

# In[65]:


import pickle


# In[66]:


filename = "/home/cmlare/Data/Models/"+'mlp_ANN_h-100_o-7.sav'
print("Saving model to "+ filename)
pickle.dump(mlp, open(filename, 'wb'))
print("Model Saved!")

