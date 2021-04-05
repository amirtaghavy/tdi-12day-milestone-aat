import streamlit as st
import requests


def get_stocktwits_feed(ticker):
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
    st.markdown('''
    **Aknowledgment**: \n 
    - *Data source*: Textual data/methods were acquired from [Stocktwits API](https://api.stocktwits.com/developers/docs/api) \n 
    - *Educational resource*: Content found on [YouTube Channel](https://www.youtube.com/channel/UCY2ifv8iH1Dsgjrz-h3lWLQ) "Part Time Larry" were particularly helpful for implementation of this feature.
                ''')
