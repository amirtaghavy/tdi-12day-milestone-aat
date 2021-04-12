import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from alpha_vantage.timeseries import TimeSeries

import config
# from dotenv import load_dotenv
# load_dotenv()


def get_stock_chart(ticker):
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

    show_vol = st.sidebar.checkbox('show volume', value=False)
    chart_on = st.sidebar.button('Generate my '+chart_opt+' chart!')
    if chart_on:
        if chart_opt == 'daily':
            msg = 'Daily chart for $'+ticker + \
                ' ending on: '+str(data.index[-1].date())
        else:
            msg = 'Intraday '+itvl[itvl_opt]+' chart for $' + \
                ticker+'('+str(data.index[-1].date())+'):'
        st.subheader(msg)
        trace1 = go.Candlestick(x=data['time'],
                                open=data['1. open'],
                                high=data['2. high'],
                                low=data['3. low'],
                                close=data['4. close'],
                                name=ticker)
        trace2 = go.Bar(x=data['time'], y=data['5. volume'],
                        name='volume', yaxis='y2',
                        marker={'color': data['5. volume'], 'colorscale': 'Portland'})
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(trace1)
        if show_vol:
            fig.add_trace(trace2, secondary_y=True)
        # fig = go.Figure(data=[go.Candlestick(x=data['time'],
        #                                      open=data['1. open'],
        #                                      high=data['2. high'],
        #                                      low=data['3. low'],
        #                                      close=data['4. close'],
        #                                      name=ticker)])
        fig.update_xaxes(type='date')
        fig.update_layout(height=500, title=chart_opt.title()+' price chart',
                          yaxis=dict(showgrid=False, zeroline=False,
                                     showline=True, showticklabels=True),
                          xaxis=dict(showline=True, showgrid=False, showticklabels=True,
                                     linecolor='rgb(100,150,200)', linewidth=3, ticks='outside',
                                     tickfont=dict(family='Arial', size=14, color='rgb(82,82,82)')),
                          plot_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
        st.write(data.sort_index(ascending=False))
        st.write(" \n")
        # st.write(metadata)
    st.markdown('''
        **Aknowledgment**: \n
        - *Data source*: Timeseries data were acquired from [Alpha Vantage](https: // www.alphavantage.co /) \n
        - *Educational resource*: Content found on Derrick Sherrill's [YouTube Channel](https: // www.youtube.com/channel/UCJHs6RO1CSM85e8jIMmCySw) were particularly helpful for implementing stock charts.
                    ''')
