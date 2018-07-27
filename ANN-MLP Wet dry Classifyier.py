
# coding: utf-8

# In[2]:


import pandas as pd


data_root = "/home/cmlare/Data/RF Data/Processed/"
# rainfall_mapped_df_1 = pd.read_csv(data_root+"2018-05-08 to 2018-05-15_integrated.csv")
print("Loading Data..")


# In[3]:


selected_feature_types = ["FrequencyBand","PathLength","wet_dry","RSL_AVG","RSL_MIN","RSL_MAX","TSL_MAX"]


# In[4]:


rainfall_classified_1 = pd.read_csv(data_root+"2018-05-08 to 2018-05-15_integrated_classified.csv")
rainfall_classified_2 = pd.read_csv(data_root+"2018-05-16 to 2018-05-23_integrated_classified.csv")
rainfall_classified_3 = pd.read_csv(data_root+"2018-05-24 to 2018-05-31_integrated_classified.csv")
rainfall_classified_4 = pd.read_csv(data_root+"2018-06-01 to 2018-06-10_integrated_classified.csv")
rainfall_classified = pd.concat([rainfall_classified_1, rainfall_classified_2, rainfall_classified_3,rainfall_classified_3,rainfall_classified_4])


# In[5]:


rainfall_classified["wet_dry"] = rainfall_classified["class"].map({"A":"DRY","B":"WET","C":"WET","D":"WET","E":"WET","F":"WET","G":"WET","H":"WET"})


# In[6]:


rainfall_classified["Baseline_ATTN"] = rainfall_classified["Baseline"].sub(rainfall_classified["RSL_MIN"])


# In[7]:


selected_features = rainfall_classified[selected_feature_types]


# In[8]:


rainfall_classified_test_data = pd.read_csv(data_root+"2018-06-11 to 2018-07-07_integrated_classified.csv")
rainfall_classified_test_data["wet_dry"] = rainfall_classified_test_data["class"].map({"A":"DRY","B":"WET","C":"WET","D":"WET","E":"WET","F":"WET","G":"WET","H":"WET"})
rainfall_classified_test_data["Baseline_ATTN"] = rainfall_classified_test_data["Baseline"].sub(rainfall_classified_test_data["RSL_MIN"])


# In[9]:


X = selected_features.drop(['wet_dry'],axis = 1)
y = selected_features['wet_dry']


# ** Preprocessing **

# In[10]:


from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
# Fit only to the training data
print("Fitting data..")
# scaler.fit(X_train)
scaler.fit(X)
print("Data fitting finished.")
StandardScaler(copy=True, with_mean=True, with_std=True)
# Now apply the transformations to the data:
# X_train = scaler.transform(X_train)
# X_test = scaler.transform(X_test)
X = scaler.transform(X)


# ** Training model **

# In[12]:


from sklearn.neural_network import MLPClassifier

mlp = MLPClassifier(hidden_layer_sizes=(10,40),max_iter=500,activation="logistic")
print("Training the model..")
# mlp.fit(X_train,y_train)
mlp.fit(X,y)
print("Model training finished.")


# ** Predictions and evaluation **

# In[13]:


print("Running Predictions on train data..")
# predictions = mlp.predict(X_test)
predictions = mlp.predict(X)
print("Running predictions finished.")


# Evaluation

# In[14]:


from sklearn.metrics import classification_report,confusion_matrix
# print(confusion_matrix(y_test,predictions))
print(confusion_matrix(y,predictions))


# In[15]:


# print(classification_report(y_test,predictions))
print(classification_report(y,predictions))


# ** Saving the Model ** 

# In[16]:


import pickle
filename = "/home/cmlare/Data/Models/"+'mlp_ANN_wet_dry h-13 RSL_MIN,RSL_MAX,RSL_AVG,TSL_MAX L-10,40,activation-sgd.sav'
print("Saving model to "+ filename)
pickle.dump(mlp, open(filename, 'wb'))
print("Model Saved!")


# ** Test Data prediction **

# In[17]:


selected_features_test = rainfall_classified_test_data[selected_feature_types]
X_test = selected_features_test.drop(['wet_dry'],axis = 1)
y_test = selected_features_test['wet_dry']

print("Fitting test data..")
scaler.fit(X_test)
print("Test data fitting finished.")
StandardScaler(copy=True, with_mean=True, with_std=True)

# Now apply the transformations to the data:
X_test = scaler.transform(X_test)

print("Running Predictions on test data..")
predictions_test = mlp.predict(X_test)
print("Running predictions on test data finished.")


# In[18]:


print(confusion_matrix(y_test,predictions_test))


# In[19]:


test_classification_report = classification_report(y_test,predictions_test)
print(test_classification_report)

