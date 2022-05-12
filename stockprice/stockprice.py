import streamlit as st
import yfinance as yf
import streamlit as st
import pandas as pd

## markdown cheat sheet


st.write('''
# Simple stock price app

Below shown are **closing price** of stocks and its volume''')

tickerSymbol = 'GOOGL'
tickerdata = yf.Ticker(tickerSymbol)
tickerdf = tickerdata.history(period='1D',start='2010-01-22',end='2020-01-22')

st.write('''Closing Price''')
st.line_chart(tickerdf.Close)

st.write('''Volume Price''')
st.line_chart(tickerdf.Volume)