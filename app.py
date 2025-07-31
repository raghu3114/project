import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import datetime

# --- Page Configuration ---
st.set_page_config(page_title="SRRstocks", layout="wide")

# --- App Header ---
st.markdown("<h1 style='text-align: center; color: #3366cc;'>📊 SRRstocks: Smart Stock Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- Sidebar Menu ---
menu = st.sidebar.radio("📂 Menu", ["📈 Stocks", "📊 Mutual Funds", "⭐ Watchlist", "⚙️ Settings"])

# --- Global Constants ---
wallet_balance = 50000
profit = 14000
total_value = wallet_balance + profit

# --- Common Wallet Section ---
with st.container():
    col1, col2, col3 = st.columns(3)
    col1.metric("💼 Wallet Balance", f"₹{wallet_balance:,.2f}")
    col2.metric("📈 Profit", f"₹{profit:,.2f}", delta=f"+{(profit/wallet_balance)*100:.2f}%")
    col3.metric("📊 Total Value", f"₹{total_value:,.2f}")

# --- Sample Holdings ---
holdings_data = {
    "Stock": ["MOTISONS", "GANGAFORGE", "AAPL", "TSLA", "TATASTEEL"],
    "Quantity": [200, 95, 5, 3, 10],
    "Avg Buy Price (₹)": [112.50, 18.90, 145.00, 750.00, 126.00],
}

st.subheader("📦 Your Holdings")
holdings_df = pd.DataFrame(holdings_data)
st.dataframe(holdings_df, use_container_width=True)

# --- Trade Simulator ---
st.subheader("🛒 Trade Simulator")
with st.form("trade_form"):
    col1, col2, col3 = st.columns(3)
    action = col1.selectbox("Action", ["Buy", "Sell"])
    symbol_input = col2.text_input("Stock Symbol (e.g. AAPL, TATASTEEL)")
    qty_input = col3.number_input("Quantity", min_value=1, step=1)
    submitted = st.form_submit_button("Execute")
    if submitted and symbol_input:
        st.success(f"{action} order placed for {qty_input} shares of {symbol_input.upper()} (Simulated)")

# --- Search and Symbol List ---
all_symbols = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "IBM", "INTC",
    "TATASTEEL.NS", "RELIANCE.NS", "DIXON.NS", "INFY.NS", "NIFTYBEES.NS"
]

search_query = st.sidebar.text_input("🔍 Search Stocks")
filtered_symbols = [s for s in all_symbols if search_query.upper() in s] if search_query else all_symbols

# --- Stocks Section ---
if menu == "📈 Stocks":
    symbols = st.sidebar.multiselect(
        "✅ Select Stocks",
        filtered_symbols,
        default=["AAPL", "TATASTEEL.NS"]
    )

    # Time range
    range_choice = st.sidebar.radio("📆 Time Range", ["1D", "1M", "3M", "6M", "1Y"], index=4)
    end_date = datetime.date.today()
    if range_choice == "1D":
        start_date = end_date - datetime.timedelta(days=1)
    elif range_choice == "1M":
        start_date = end_date - datetime.timedelta(days=30)
    elif range_choice == "3M":
        start_date = end_date - datetime.timedelta(days=90)
    elif range_choice == "6M":
        start_date = end_date - datetime.timedelta(days=180)
    else:
        start_date = end_date - datetime.timedelta(days=365)

    if symbols:
        all_data = yf.download(symbols, start=start_date, end=end_date)
        all_data.columns = ['_'.join(col).strip('_') if isinstance(col, tuple) else col for col in all_data.columns]
        all_data.reset_index(inplace=True)

        st.subheader("📅 Stock Data Preview")
        st.dataframe(all_data.head(), use_container_width=True)

        # Closing Price Chart
        st.subheader("📈 Closing Price")
        fig1 = px.line()
        for symbol in symbols:
            fig1.add_scatter(
                x=all_data['Date'],
                y=all_data[f'Close_{symbol}'],
                mode='lines',
                name=symbol
            )
        fig1.update_layout(xaxis_title="Date", yaxis_title="Price")
        st.plotly_chart(fig1, use_container_width=True)

        # Volume Traded
        st.subheader("📊 Volume Traded")
        fig2 = px.area()
        for symbol in symbols:
            fig2.add_scatter(
                x=all_data['Date'],
                y=all_data[f'Volume_{symbol}'],
                mode='lines',
                stackgroup='one',
                name=symbol
            )
        fig2.update_layout(xaxis_title="Date", yaxis_title="Volume")
        st.plotly_chart(fig2, use_container_width=True)

        # Avg Close Bar Chart
        st.subheader("📉 Average Closing Price")
        avg_prices = {symbol: all_data[f'Close_{symbol}'].mean() for symbol in symbols}
        avg_df = pd.DataFrame(list(avg_prices.items()), columns=["Stock", "Avg Close Price"])
        fig3 = px.bar(avg_df, x="Stock", y="Avg Close Price", color="Stock")
        st.plotly_chart(fig3, use_container_width=True)

# --- Mutual Funds Section ---
elif menu == "📊 Mutual Funds":
    st.subheader("💼 Popular Mutual Funds")
    mf_data = {
        "Fund Name": [
            "Nippon India Small Cap Fund",
            "Parag Parikh Flexi Cap Fund",
            "SBI Bluechip Fund",
            "HDFC Mid-Cap Opportunities Fund"
        ],
        "Category": ["Small Cap", "Flexi Cap", "Large Cap", "Mid Cap"],
        "Returns (5Y)": ["32.5%", "23.4%", "13.2%", "20.8%"],
        "AUM (₹ Cr)": ["46,832", "54,219", "38,920", "35,112"]
    }
    st.table(pd.DataFrame(mf_data))
    st.info("Live NAV not connected. Use APIs for real-time mutual fund integration.")

# --- Watchlist Section ---
elif menu == "⭐ Watchlist":
    st.subheader("⭐ My Watchlist")
    watchlist = ["DIXON.NS", "NVDA", "TATASTEEL.NS", "NIFTYBEES.NS"]
    st.write(pd.DataFrame({"Stock": watchlist}))

# --- Settings Section ---
elif menu == "⚙️ Settings":
    st.subheader("⚙️ Account Settings")
    with st.form("settings_form"):
        col1, col2 = st.columns(2)
        bank_acc = col1.text_input("Bank Account Number")
        mobile = col2.text_input("Mobile Number")
        dob = col1.date_input("Date of Birth")
        nominee = col2.text_input("Nominee Name")
        submitted = st.form_submit_button("Save Settings")
        if submitted:
            st.success("Settings saved (simulated).")

    st.subheader("📜 Past Transactions (Simulated)")
    tx_data = {
        "Date": ["2025-07-25", "2025-07-20", "2025-07-15"],
        "Stock": ["AAPL", "GANGAFORGE", "TSLA"],
        "Action": ["Buy", "Sell", "Buy"],
        "Qty": [5, 20, 3],
        "Price": [145, 21.5, 745]
    }
    st.dataframe(pd.DataFrame(tx_data))
