import streamlit as st


def diseminate(feed_flwr_list_2dim):
    feed_flwr_list_2dim.sort(reverse=True, key=lambda item: item[1])
    i = 0
    for item in feed_flwr_list_2dim:
        i += 1
        st.markdown(str(i)+item[0])
