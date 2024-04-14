#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

#nltk.download('stopwords')
#nltk.download('punkt')


# In[2]:


# Function to preprocess text data
def preprocess_text(text):
    
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.lower() not in stop_words]
    tokens = [word for word in tokens if word not in string.punctuation]
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text


# In[3]:




# Load the xgb_classifier object
with open('xgb_classifier.pkl', 'rb') as f:
    xgb_classifier_loaded = pickle.load(f)

# Now you can use xgb_classifier_loaded as your loaded object
print(xgb_classifier_loaded)


# In[4]:


#from sklearn.feature_extraction.text import TfidfVectorizer

# Assuming you have already trained your TfidfVectorizer
#tfidf_vectorizer = TfidfVectorizer()
#X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
import joblib
tfidf_vectorizer_loaded = joblib.load('tfidf_vectorizer_model.pkl')

# You can now use tfidf_vectorizer_loaded to transform new data
#X_test_tfidf = tfidf_vectorizer_loaded.transform(X_test)


# In[8]:

def  rating_predictor(input_text):
                test_review = input_text
                preprocessed_review = preprocess_text(test_review)
                test_review_tfidf =tfidf_vectorizer_loaded.transform([preprocessed_review])
                predicted_rating = xgb_classifier_loaded.predict(test_review_tfidf)[0]
                print("Predicted Rating for the test review:", predicted_rating)

                return predicted_rating






