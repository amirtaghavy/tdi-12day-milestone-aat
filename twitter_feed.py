import streamlit as st
import tweepy
import config


def get_twitter_feed(ticker):
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
    st.markdown('''
    **Aknowledgment**: \n 
    - *Data source*: Textual data/methods were acquired from [Tweepy API](https://docs.tweepy.org/en/latest/api.html) \n 
    - *Educational resource*: Content found on [YouTube Channel](https://www.youtube.com/channel/UCY2ifv8iH1Dsgjrz-h3lWLQ) "Part Time Larry" were particularly helpful for implementation of this feature.
                ''')
