#Selenium imports here
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
#Other imports here
import re
import string
import os
import wget
import requests
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import re
import string
import streamlit as st
header = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 OPR/83.0.4254.70'
    }

filename = 'finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))
records = []
results = []
rev = []    
rev1=[]
records_name = []
def get_url(search_term):
    template = 'https://www.amazon.in/s?k={}&crid=2U21CDDK65IB9&ref=nb_sb_noss_2'
    search_term = search_term.replace(' ','+')
    return template.format(search_term)

def get_asin(driver,no,no_prod):
    soup = BeautifulSoup(driver.page_source,'html.parser')
    for i in soup.find_all('div',{'data-component-type':'s-search-result'})[:no]:
        records.append(i['data-asin'])
        records_name.append(i.h2.a.text.strip()) #================================heading============================
    for i in records:
        results.append(f"https://www.amazon.in/dp/product-reviews/{i}")
    for i in results:
        driver.get(i)
    reviews_unit(results,no_prod)

def clear_reviews(rev):
    for i in rev:
        text = i.lower()
        text = re.sub('\[.*?\]','',text)
        text = re.sub('[%s]'% re.escape(string.punctuation),'',text)
        text = re.sub('\w*\d\w*','',text)
        text = re.sub(r'\b\w{1,2}\b', '', text)
        text = text.strip('\n')
        text = text.strip('\t')
        text=re.sub(r'@\w+', ' ', text)
        text=re.sub(r'http\S+', ' ', text)
        text = re.sub(r'[^a-z A-Z]', ' ',text)
        text= re.sub(r'\b\w{1,2}\b', '', text)
        text= re.sub(r' +', ' ', text)
        text = text.strip(" ")
        if text:
            rev1.append(text)  

dicton_reviews={}
def reviews_unit(results,no_prod):
    for j in range(len(results)):
        lst_rev = []
        page=requests.get(results[j],headers=header)
        soup=BeautifulSoup(page.content)
        for i in soup.findAll("span",{'data-hook':"review-body"})[:no_prod]:

            rev.append(i.text)
            lst_rev.append(i.text)
        dicton_reviews[records_name[j]]=lst_rev
    print(dicton_reviews)
    clear_reviews(rev) 



def app():
    driver = webdriver.Edge(r'C:/Users/Hansel/Desktop/edgedriver_win64/msedgedriver.exe')
    st.title("AMAZON")

    term =  st.text_input("Enter what you want:")
    no = st.number_input("Enter the number of Products:",0,100,10)
    no_prod = st.number_input("Enter No of reviews per Product: ",0,100,10)
    url = get_url(term)
    print(url)
    driver.get(url)
    get_asin(driver,no,no_prod)
    # st.write(len(rev1))
    # st.table(rev1)


    
    pol = {'0':'negative','1':'positive'}
    if rev1:
        for i in rev1:
            val = loaded_model.predict([i])
            val = int(str(val)[1:2])
            st.write("Text : " + str(i))
            st.write("polarity : " + pol[str(val-1)])
    else:
        st.write("Enter the text for getting the results")

app()