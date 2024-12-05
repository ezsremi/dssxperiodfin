import streamlit as st
import pandas as pd
import matplotlib as plt

# Set up styling and color scheme
st.set_page_config(page_title="DSS x Period Financial Dashboard", layout="wide")
st.markdown("<h1 style='text-align: center; color: #B22222;'>DSS x Period Automated Dashboard</h1>", unsafe_allow_html=True)
if st.button("Documentation"):
    st.write("Click [here](https://example.com/documentation) for the full documentation.")
    # or use st.markdown directly to open link in new tab:
    st.markdown("[Documentation](https://example.com/documentation)", unsafe_allow_html=True)
# Load cleaned data from preprocessed balance sheet and profit/loss
balance_sheet_data = pd.DataFrame({
    "Category": ["Current Assets", "Fixed Assets", "Other Assets"],
    "Amount": [250448.58, 50000.00, 35000.00]
})

profit_loss_data = pd.DataFrame({
    "Account": ["Individual Donations", "Corporate Contributions", "In-Kind Donations", "In-Kind Product Donations"],
    "Amount": [96327.33, 188019.31, 0.00, 57248.54]
})

# Sidebar for filter options
st.sidebar.header("Dashboard Documentation")

# Balance Sheet: Pie Chart for Asset Distribution with red color scheme
st.subheader("Asset Distribution")
fig, ax = plt.subplots(figsize=(6, 6))
colors = ["#B22222", "#CD5C5C", "#FA8072"]
ax.pie(balance_sheet_data["Amount"], labels=balance_sheet_data["Category"], autopct="%1.1f%%", startangle=90, colors=colors)
ax.set_title("Asset Distribution", fontsize=14, color="#B22222")
st.pyplot(fig)

# Profit and Loss: Bar Chart for Income Sources with red color scheme
st.subheader("Income Sources")
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(profit_loss_data["Account"], profit_loss_data["Amount"], color="#B22222", edgecolor="black")
ax.set_title("Income Sources", fontsize=14, color="#B22222")
ax.set_xlabel("Account", fontsize=12, color="#B22222")
ax.set_ylabel("Amount ($)", fontsize=12, color="#B22222")
plt.xticks(rotation=45, color="#B22222")
plt.yticks(color="#B22222")
st.pyplot(fig)

# Summary Statistics with red-themed metrics
st.subheader("Summary Statistics")
total_assets = balance_sheet_data["Amount"].sum()
total_income = profit_loss_data["Amount"].sum()

col1, col2 = st.columns(2)
col1.metric("Total Assets", f"${total_assets:,.2f}", delta=None, delta_color="inverse")
col2.metric("Total Income", f"${total_income:,.2f}", delta=None, delta_color="inverse")

st.markdown("<h4 style='text-align: center; color: #B22222;'>About this Dashboard</h4>", unsafe_allow_html=True)
st.write("This dashboard is designed for Period, Inc. to automatically visualize relevant financial figures.")

# End of Streamlit app
