import streamlit as st
import json

def load_data(file_paths):
    all_announcements = []
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            data = json.load(file)
            all_announcements.extend(data.get('data', []))
    return all_announcements

file_paths = ['./data/1AE.json','./data/1MC.json','./data/AEE.json','./data/NRZ.json','./data/REZ.json']

announcements = load_data(file_paths)

tickers = ['1AE', '1MC', 'AEE', 'NRZ', 'REZ']

def get_announcements_by_ticker(ticker):
    return [announcement for announcement in announcements if announcement['issuer_code'] == ticker]

def has_trading_halt(ticker):
    return any(announcement['header'] == 'Trading Halt' for announcement in get_announcements_by_ticker(ticker))


st.title('ASX Announcements Dashboard') # Streamlit UI


selected_ticker = st.selectbox('Select Ticker Symbol:', sorted(tickers)) # Ticker selection


filtered_announcements = get_announcements_by_ticker(selected_ticker) # Filter announcements by selected ticker


st.subheader(f'Announcements for {selected_ticker}') # Display announcements

if filtered_announcements:
    for announcement in filtered_announcements:
        st.write(f"**{announcement['header']}**")
        st.write(f"Date: {announcement['document_date']}")
        st.write(f"[View Document]({announcement['url']})")
        st.write("---")
else:
    st.write("No announcements found.")

st.subheader('Tickers with Trading Halt Announcements')
tickers_with_trading_halt = [ticker for ticker in tickers if has_trading_halt(ticker)] # Identify and display tickers with Trading Halt

if tickers_with_trading_halt:
    st.write(", ".join(tickers_with_trading_halt))
else:
    st.write("No tickers with Trading Halt announcements found.")