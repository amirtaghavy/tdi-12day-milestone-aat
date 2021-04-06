import streamlit as st
import requests
import pandas as pd

from diseminate import diseminate


def get_stocktwits_feed(ticker):
    # stock_twits(ticker)
    rq_adress = 'https://api.stocktwits.com/api/2/streams/symbol/{}.json'.format(
        ticker)
    # st.write(rq_adress)
    response = requests.get(rq_adress)
    data = response.json()
    # st.write(data)
    i = 0
    outp = []
    for msg in data['messages']:
        i += 1
        feed = str(i)+'. *'+msg['user']['username']+'* (**' + \
            str(msg['user']['followers'])+'** followers): '+msg['body']
        flwrs = msg['user']['followers']
        outp.append([feed, flwrs])
    diseminate(outp)
    outp.sort(reverse=True, key=lambda item: item[1])
    for item in outp:
        st.markdown(item[0])
    st.markdown('''
    **Aknowledgment**: \n 
    - *Data source*: Textual data/methods were acquired from [Stocktwits API](https://api.stocktwits.com/developers/docs/api) \n 
    - *Educational resource*: Content found on [YouTube Channel](https://www.youtube.com/channel/UCY2ifv8iH1Dsgjrz-h3lWLQ) "Part Time Larry" were particularly helpful for implementation of this feature.
                ''')
