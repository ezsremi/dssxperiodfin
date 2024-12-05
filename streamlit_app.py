import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set the password
PASSWORD = "periodpassword"

# Configure the page
st.set_page_config(page_title="Secure Dashboard", layout="wide")

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Authentication Logic
if not st.session_state["authenticated"]:
    st.markdown("<h2 style='text-align: center;'>Secure Dashboard Login</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Please enter the password to access the dashboard.</p>", unsafe_allow_html=True)
    
    # Password input
    password_input = st.text_input("Password", type="password")
    
    # Button to submit the password
    if st.button("Login"):
        if password_input == PASSWORD:
            st.session_state["authenticated"] = True
            st.success("Login successful! Redirecting...")
            st.experimental_rerun()  # Refresh the page to display the dashboard
        else:
            st.error("Incorrect password. Please try again.")
else:
    # Set up styling and color scheme
    st.set_page_config(page_title="DSS x Period Financial Dashboard", layout="wide")
    st.markdown("<h1 style='text-align: center; color: #B22222;'>DSS x Period Automated Dashboard</h1>", unsafe_allow_html=True)
    if st.button("Documentation"):
        st.write("Click [here](https://docs.google.com/document/d/1K6mAgw4I_pu06gdvjqOfTxXiHzgqGai3sHsZLqzYBk8/edit?usp=sharing) for the full documentation.")
        # or use st.markdown directly to open link in new tab:
        st.write("If you encounter issues with this app, please contact [DSS at Berkeley](https://dssberkeley.com/)")
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
