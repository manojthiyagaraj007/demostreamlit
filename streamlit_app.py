import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px



st.set_page_config(layout= "wide")


with open('style.css', 'r') as css_file:
    st.markdown(f'<style>{css_file.read()}</style>',unsafe_allow_html= True)

st.sidebar.image("logo.png")
coinSelected = st.sidebar.selectbox("Select any Coin",["BitCoin","Ethereum","DOGECoin"])






col1, col2, col3 = st.columns(3)

#bitcon Section

bitcoin = pd.read_csv("BTC.csv").sort_values(by='date', ascending=False).head(100)
bitcoin_sorted_rows = bitcoin.head(2)
bitcoin_latest_price = bitcoin.iloc[0]['close']
bitcoin_price_before = bitcoin.iloc[1]['close']
bitcoin_increase_or_decrese = bitcoin_latest_price - bitcoin_price_before
grouped_btc_data = bitcoin.groupby('ticker')['close'].sum().reset_index()

bitcoin['date'] = pd.to_datetime(bitcoin['date'])

date_filter = st.sidebar.date_input(label= "Filter the price of coin by date",max_value=bitcoin['date'].max(),min_value=bitcoin['date'].min(),value=bitcoin['date'].max())

# Ethereum Section
ethereum= pd.read_csv("ETH.csv").sort_values(by='date', ascending=False).head(100)
ethereum_sorted_rows = ethereum.head(2)
ethereum_latest_price = ethereum.iloc[0]['close']
ethereum_price_before = ethereum.iloc[1]['close']
ethereum_increase_or_decrese = ethereum_latest_price - ethereum_price_before
grouped_eth_data = ethereum.groupby('ticker')['close'].sum().reset_index()
ethereum['date'] = pd.to_datetime(ethereum['date'])


#Doge Price Section
doge= pd.read_csv("DOGE.csv").sort_values(by='date', ascending=False).head(100)
doge_sorted_rows = doge.head(2)
doge_latest_price = doge.iloc[0]['close']
doge_price_before = doge.iloc[1]['close']
doge_increase_or_decrese = doge_latest_price - doge_price_before
doge['date'] = pd.to_datetime(doge['date'])



combined_df = pd.concat([ethereum, bitcoin ,  doge], ignore_index=True)

grouped_combined_df = combined_df.groupby('ticker')['close'].sum().reset_index()

  # Sidebar widget for selecting the cryptocurrencies to compare
selected_crypto = st.sidebar.multiselect('Select cryptocurrencies to compare', combined_df['ticker'].unique())

with col1:
    btc_logo,btc_status = st.columns([1,1.5])
    with btc_logo:
        
        st.image("bitcoin.png",width=63)
        
    with btc_status:
        st.metric("BitCoin", f"$ {round(bitcoin_latest_price,2)}", f" { round(bitcoin_increase_or_decrese, 2)}")
    
with col2:
    eth_logo,etch_status = st.columns([1,1.5])
    with eth_logo:
        st.image("etherium.png",width=63)
    with etch_status:
        st.metric("Ethereum", f"$ {round(ethereum_latest_price,2)}", f" { round(ethereum_increase_or_decrese, 2)}")

with col3:
    doge_logo,doge_status = st.columns([1,1.5])
    with doge_logo:
        st.image("doge.png",width=63)
    with doge_status:
        st.metric("Doge Coin", f"$ {round(doge_latest_price,2)}", f" { round(doge_increase_or_decrese, 2)}")

if date_filter and selected_crypto:
    if coinSelected == "BitCoin":
        date_filter = pd.to_datetime(date_filter)
        flitered_data = bitcoin[bitcoin['date'] == date_filter]
        if not flitered_data.empty:
            st.info(f"The price of {coinSelected} on {date_filter} is: {flitered_data.iloc[0]['close']}")
        else:
            st.warning(f"No data found for the selected date {date_filter}")
            st.info(f"The price of {coinSelected} on {date_filter} is: {flitered_data.iloc[0]['close']}")

    elif coinSelected == "Ethereum":
        date_filter = pd.to_datetime(date_filter)
        flitered_data = ethereum[ethereum['date'] == date_filter]
        if not flitered_data.empty:
            st.info(f"The price of {coinSelected} on {date_filter} is: {flitered_data.iloc[0]['close']}")
        else:
            st.warning(f"No data found for the selected date {date_filter}")
            st.info(f"The price of {coinSelected} on {date_filter} is: {flitered_data.iloc[0]['close']}")

    elif coinSelected == "DOGECoin":
        date_filter = pd.to_datetime(date_filter)
        flitered_data = doge[doge['date'] == date_filter]
        if not flitered_data.empty:
            st.info(f"The price of {coinSelected} on {date_filter} is: {flitered_data.iloc[0]['close']}")
        else:
            st.warning(f"No data found for the selected date {date_filter}")
            st.info(f"The price of {coinSelected} on {date_filter} is: {flitered_data.iloc[0]['close']}")

if selected_crypto:
    # Filter the data based on selected cryptocurrencies
    filtered_data = combined_df[combined_df['ticker'].isin(selected_crypto)]

    # Create a line chart using Plotly Express
    fig = px.line(filtered_data, x='date', y='close', color='ticker', title='Cryptocurrency Price Comparison')

    # Customize the chart
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Close Price')

    # Display the chart in Streamlit
    st.plotly_chart(fig)

if coinSelected == "BitCoin":
    BtcBar,BtcPie = st.columns(2)
    # Create a bar chart using Plotly Express
    with BtcBar:
        fig = px.bar(bitcoin, x='date', y='close', title='Close BitCoin Prices Over Time')
        fig.update_xaxes(title_text='Date')
        fig.update_yaxes(title_text='Close Price')
        # Display the chart in Streamlit
        st.plotly_chart(fig)
    with BtcPie:
        figpie = px.pie(grouped_combined_df, values='close', names='ticker', title='Total Close Prices by Ticker')
        st.plotly_chart(figpie)
    fig = px.line(bitcoin, x='date', y='close', title='Bitcoin Close Price Over Time')

    # Customize the chart
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Close Price')

    fig.update_layout(width=1000) 

    # Display the chart in Streamlit
    st.plotly_chart(fig)

elif coinSelected == "Ethereum":
    EthBar,EthPie = st.columns(2)
    # Create a bar chart using Plotly Express
    with EthBar:
        fig = px.bar(ethereum, x='date', y='close', title='Close Ethereum Coin Prices Over Time')
        fig.update_xaxes(title_text='Date')
        fig.update_yaxes(title_text='Close Price')
        # Display the chart in Streamlit
        st.plotly_chart(fig)
    with EthPie:
        figpie = px.pie(grouped_combined_df, values='close', names='ticker', title='Total Close Prices by Ticker')
        st.plotly_chart(figpie)
    fig = px.line(ethereum, x='date', y='close', title='Ethereum Close Price Over Time')

    # Customize the chart
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Close Price')

    # Rotate x-axis labels for better readability
    fig.update_layout(width=1000) 

    # Display the chart in Streamlit
    st.plotly_chart(fig)

elif coinSelected == "DOGECoin":
    DOGEBar,DOGEPie = st.columns(2)
    # Create a bar chart using Plotly Express
    with DOGEBar:
        fig = px.bar(doge, x='date', y='close', title='Close DogeCoin Prices Over Time')
        fig.update_xaxes(title_text='Date')
        fig.update_yaxes(title_text='Close Price')
        # Display the chart in Streamlit
        st.plotly_chart(fig)
    with DOGEPie:
        figpie = px.pie(grouped_combined_df, values='close', names='ticker', title='Total Close Prices by Ticker')
        st.plotly_chart(figpie)

    fig = px.line(doge, x='date', y='close', title='DOGE Close Price Over Time')

    # Customize the chart
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Close Price')

    # Rotate x-axis labels for better readability
    fig.update_layout(width=1000) 

    # Display the chart in Streamlit
    st.plotly_chart(fig)

  





