# from alpha_vantage import
'''
pip3 install -r requirements.txt
requests    #inquiring some online APIs
tweepy      #interacting w/ twitter for python
'''
# on the terminal run this command:
# streamlit run <fname>
#    this will create a web server and a running app which can be rerun
#    any time a change is made in the source files.'''

import streamlit as st

import pandas as pd
import numpy as np
import time
import datetime
# import requests
# import plotly.graph_objects as go
#
# from alpha_vantage.timeseries import TimeSeries

import tweepy
import config
from stock_chart import get_stock_chart
from stocktwits_feed import get_stocktwits_feed
from twitter_feed import get_twitter_feed

st.title('TDI 12Day Milestone Project')
st.subheader('Created by: A. Taghavey - April, 2021')
''' '''
st.markdown(
    'This app displays a series publically available data on user defined **stock tickers**.')
st.markdown(
    'This App was developed using [*Streamlit*](https://streamlit.io/) platform as the program entry project for [**the Data Incubator**](https://www.thedataincubator.com/) fellowship program.')
# st.write('I will try to deploy this app on Heroku')

# Side bar design
st.sidebar.image('https://paganresearch.io/images/streamlit.png',
                 caption='https://streamlit.io/', width=100, clamp=False)  # width is given in pixels
st.sidebar.header('Stock search bar')
ticker = st.sidebar.text_input(label='Stock ticker: ', max_chars=5, value='CHPT', key='$',
                               help='Look up tickers from: https://www.marketwatch.com/tools/quotes/lookup.asp').upper()

dash_option = st.sidebar.selectbox('Select search platform:', (
    'charts', 'twitter', 'stocktwits'), 0)

if len(dash_option) > 0:
    st.header('\''+dash_option+'\' on $'+ticker+':')
    if dash_option == 'charts':
        get_stock_chart(ticker)
    elif dash_option == 'stocktwits':
        get_stocktwits_feed(ticker)
    elif dash_option == 'twitter':
        get_twitter_feed(ticker)
