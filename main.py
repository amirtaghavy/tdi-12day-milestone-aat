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
import requests
import plotly.graph_objects as go

from alpha_vantage.timeseries import TimeSeries

import tweepy
import config

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
    # q = 'https://api.stocktwits.com/api/2/search/symbols.json?access_token=<access_token> \'q='+ticker+'\''
    # st.write(q)
    # res = requests.get(q)
    # st.write(res)
    # title = res['results']['title']
    # st.header('\''+dash_option+'\' on '+title + '($'+ticker+'):')
    st.header('\''+dash_option+'\' on $'+ticker+':')
    if dash_option == 'charts':
        ts = TimeSeries(key=config.ALPHA_VANTAGE_API_KEY,
                        output_format='pandas')
        chart_opt = st.sidebar.selectbox(
            'chart type:', ('daily', 'intraday'), 0)
        if chart_opt == 'daily':
            data, metadata = ts.get_daily(symbol=ticker, outputsize='full')
        elif chart_opt == 'intraday':
            itvl_opt = st.sidebar.slider(
                'increase time interval', min_value=1, max_value=5, value=1)
            itvl = {1: "1min", 2: "5min", 3: "15min", 4: "30min", 5: "60min"}
            data, metadata = ts.get_intraday(
                symbol=ticker, interval=itvl[itvl_opt], outputsize='compact')
            first_day = data.index[-1].date()
            last_day = data.index[0].date()
            # st.write(data)
            if first_day != last_day:
                for idx, row in data.iterrows():
                    # st.write('Here is the first row index:')
                    # st.write(idx)
                    if idx.date() != last_day:
                        data.drop(index=idx, inplace=True)

        # st.write(data.shape)
        data_index = data.index.to_pydatetime()
        if chart_opt == 'daily':
            data['time'] = [idx.date() for idx in data_index]
        else:
            data['time'] = [idx.time() for idx in data_index]
        data.sort_index(inplace=True)

        chart_on = st.sidebar.button('Generate my '+chart_opt+' chart!')
        if chart_on:
            if chart_opt == 'daily':
                msg = 'Daily chart for $'+ticker + \
                    ' ending on: '+str(data.index[-1].date())
            else:
                msg = 'Intraday '+itvl[itvl_opt]+' chart for $'+ticker+':'
            st.subheader(msg)
            fig = go.Figure(data=[go.Candlestick(x=data['time'],
                                                 open=data['1. open'],
                                                 high=data['2. high'],
                                                 low=data['3. low'],
                                                 close=data['4. close'],
                                                 name=ticker)])
            fig.update_xaxes(type='category')
            fig.update_layout(height=1000)
            st.plotly_chart(fig, use_container_width=True)
            st.write(data.sort_index(ascending=False))
            # st.write(metadata)
        '''
            **Aknowledgment**: \n 
            - *Data source*: Timeseries data were acquired from [Alpha Vantage](https: // www.alphavantage.co /) \n 
            - *Educational resource*: Content found on Derrick Sherrill's [YouTube Channel](https: // www.youtube.com/channel/UCJHs6RO1CSM85e8jIMmCySw) were particularly helpful for implementing stock charts.
                        '''
    elif dash_option == 'stocktwits':
        # stock_twits(ticker)
        rq_adress = 'https://api.stocktwits.com/api/2/streams/symbol/{}.json'.format(
            ticker)
        # st.write(rq_adress)
        response = requests.get(rq_adress)
        data = response.json()
        # st.write(data)
        i = 0
        for msg in data['messages']:
            i += 1
            outp = str(i)+'. *'+msg['user']['username']+'* (**' + \
                str(msg['user']['followers'])+'** followers): '+msg['body']
            st.markdown(outp)
        '''
    **Aknowledgment**: \n 
    - *Data source*: Textual data/methods were acquired from [Stocktwits API](https://api.stocktwits.com/developers/docs/api) \n 
    - *Educational resource*: Content found on [YouTube Channel](https://www.youtube.com/channel/UCY2ifv8iH1Dsgjrz-h3lWLQ) "Part Time Larry" were particularly helpful for implementation of this feature.
                '''
    elif dash_option == 'twitter':
        auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY,
                                   config.TWITTER_CONSUMER_SECRET)
        auth.set_access_token(config.TWITTER_ACCESS_TOKEN,
                              config.TWITTER_ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        show_opt = st.sidebar.selectbox(
            'Show me most recent tweets...', ('on $'+ticker, 'by popular traders [feeling lucky]!'), 0)
        if show_opt == 'on $'+ticker:
            st.subheader('Recent tweets on $'+ticker+': ')
            tweets = api.search('$'+ticker, lang='en', count=50)
            i = 0
            for tweet in tweets:
                i += 1
                st.markdown(str(i)+'. ***'+tweet.user.screen_name+'*** (*' +
                            str(tweet.user.followers_count)+' followers*):'+tweet.text)
        else:  # feeling lucky option
            # tweak this to also extract a list of symbols from this twitter accounts + finviz charts
            st.subheader(
                'What highly followed traders are tweeting about today:')
            i = 0
            for user in config.TWITTER_USERNAMES:
                twts = api.user_timeline(user, count=10)
                for tweet in twts:
                    if '$' in tweet.text:
                        i += 1
                        st.markdown(str(i)+'. ***'+tweet.user.screen_name+'*** (*' +
                                    str(tweet.user.followers_count)+' followers*):'+tweet.text)
        '''
    **Aknowledgment**: \n 
    - *Data source*: Textual data/methods were acquired from [Tweepy API](https://docs.tweepy.org/en/latest/api.html) \n 
    - *Educational resource*: Content found on [YouTube Channel](https://www.youtube.com/channel/UCY2ifv8iH1Dsgjrz-h3lWLQ) "Part Time Larry" were particularly helpful for implementation of this feature.
                '''
        pass

# df = pd.DataFrame(np.random.randn(50, 20), columns=(
#     'col %d' % i for i in range(20)))
# st.dataframe(df)
