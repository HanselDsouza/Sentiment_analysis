#Selenium imports here
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
#Other imports here
import os
import wget
import requests
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import re
import string
import streamlit as st

filename = 'finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

def app():
    user_input = st.text_input("Enter text!!!")
    if user_input:  
        print(type(user_input))
        val = loaded_model.predict([user_input])
        val = int(str(val)[1:2])
        print(val)
        print("1 - negative\n2 - positive")
        st.write("input: " + str(user_input))
        st.write("polarity: " + str(val-1))
        print("hello world")
    else:
        st.write("Enter the text for getting the results")

ex = ["This bad. bad for work from home. The actual screen size is 32 cm x 70 cm. This is good for software people. Video play is also bad."]
app()