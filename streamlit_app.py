import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def balanceTotals(csv_file):

    df = pd.read_csv(csv_file)

    # Rename columns
    df.rename(columns={'Period.,Inc.': 'Category', 'Unnamed: 1': 'Amount'}, inplace=True)

    # Drop rows with NaN
    df = df.dropna()

    #Cast to float vlaues
    df['Amount'] = df['Amount'].replace({',': '', '\$': '','-':' '}, regex=True).astype(float)

    #Getting totals
    getTotals = df[df['Category'].str.contains('Total', case=False, na=False)]

    #Splitting data
    totalAsset = getTotals.iloc[0:7]
    totalLiabilities = getTotals.iloc[7:] 


    return totalAsset['Category'], totalAsset['Amount'], totalLiabilities['Category'], totalLiabilities['Amount']

def PF_totals(csv_file):
    df = pd.read_csv(csv_file)
    df.rename(columns={'Period.,Inc.': 'Category', 'Unnamed: 1': 'Amount'}, inplace=True)

    # Drop NaN values
    df = df.dropna()

    #Cast to float
    df['Amount'] = df['Amount'].replace({',': '', '\$': '', '-': ' '}, regex=True).astype(float)

    #Look for Totals
    getTotals = df[df['Category'].str.contains('Total', case=False, na=False)]

    # Splitting data
    income = getTotals.iloc[0:4]
    expenses = getTotals.iloc[4:]


    net = df[df['Category'].str.contains('Net', case=False, na=False)]

    # Return the processed data
    return income['Category'], income['Amount'], expenses['Category'], expenses['Amount'], net['Category'], net['Amount']

# Set the password
PASSWORD = "periodpassword"

# Configure the page
st.set_page_config(page_title="DSS x Period Financial Dashboard", layout="wide")

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
            st.rerun()  # Refresh the page to display the dashboard
        else:
            st.error("Incorrect password. Please try again.")
else:
    # Set up styling and color scheme
    st.markdown("<h1 style='text-align: center; color: #B22222;'>DSS x Period Automated Dashboard</h1>", unsafe_allow_html=True)
    if st.button("Documentation"):
        st.write("Click [here](https://docs.google.com/document/d/1K6mAgw4I_pu06gdvjqOfTxXiHzgqGai3sHsZLqzYBk8/edit?usp=sharing) for the full documentation.")
        # or use st.markdown directly to open link in new tab:
        st.write("If you encounter issues with this app, please contact [DSS at Berkeley](https://dssberkeley.com/)")
    # Load cleaned data from preprocessed balance sheet and profit/loss
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    # Process the uploaded file
    if uploaded_file is not None:
        if "balance" in uploaded_file.name.lower():
            # Read the uploaded CSV file into a DataFrame
            assetcategory, assettotal, liabilitycategory, liabilitytotal = balanceTotals(uploaded_file)
            
            # Display the DataFrame
            st.subheader("Uploaded File Visualizations:")

            #show asset chart
            fig = px.pie(values=assettotal, names=assetcategory, title="Asset Distribution", hover_name=assetcategory)
            st.plotly_chart(fig, use_container_width=True)


            #show liability chart
            fig = px.pie(values=liabilitytotal, names=liabilitycategory, title="Liability Distribution", hover_name=liabilitycategory)
            st.plotly_chart(fig, use_container_width=True)

            #  # Summary Statistics with red-themed metrics
            # st.subheader("Summary Statistics")
            # total_assets = assettotal.sum()
            # total_income = profit_loss_data["Amount"].sum()

            # col1, col2 = st.columns(2)
            # col1.metric("Total Assets", f"${total_assets:,.2f}", delta=None, delta_color="inverse")
            # col2.metric("Total Income", f"${total_income:,.2f}", delta=None, delta_color="inverse")
        elif "profit" in uploaded_file.name.lower():
            incomecategory, incometotal, expensescategory, expensestotal, netcategory, nettotal = PF_totals(uploaded_file)
            st.subheader("Income Categories Distribution")
            # Create a DataFrame from the series
            data = pd.DataFrame({
                "Income Category": incomecategory,
                "Amount": incometotal
            })

            # Create an interactive bar chart using Plotly
            st.subheader("Income Categories Distribution")
            fig = px.bar(
                data,
                x="Income Category",
                y="Amount",
                text="Amount",
                title="Income Categories",
                labels={"Income Category": "Category", "Amount": "Income Amount ($)"},
                color="Income Category"
            )

            # Customize chart appearance
            fig.update_traces(texttemplate="$%{text:.2f}", textposition="outside")
            fig.update_layout(
                xaxis_title="Income Category",
                yaxis_title="Amount ($)",
                showlegend=False,
                template="plotly_white"
            )

            # Display the interactive chart in Streamlit
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Awaiting file upload. Please upload a CSV file.")
    balance_sheet_data = pd.DataFrame({
        "Category": ["Current Assets", "Fixed Assets", "Other Assets"],
        "Amount": [250448.58, 50000.00, 35000.00]
    })

    profit_loss_data = pd.DataFrame({
        "Account": ["Individual Donations", "Corporate Contributions", "In-Kind Donations", "In-Kind Product Donations"],
        "Amount": [96327.33, 188019.31, 0.00, 57248.54]
    })

    # Profit and Loss: Bar Chart for Income Sources with red color scheme
    # st.subheader("Income Sources")
    # fig, ax = plt.subplots(figsize=(10, 5))
    # ax.bar(profit_loss_data["Account"], profit_loss_data["Amount"], color="#B22222", edgecolor="black")
    # ax.set_title("Income Sources", fontsize=14, color="#B22222")
    # ax.set_xlabel("Account", fontsize=12, color="#B22222")
    # ax.set_ylabel("Amount ($)", fontsize=12, color="#B22222")
    # plt.xticks(rotation=45, color="#B22222")
    # plt.yticks(color="#B22222")
    # st.pyplot(fig)

    st.markdown("<h4 style='text-align: center; color: #B22222;'>About this Dashboard</h4>", unsafe_allow_html=True)
    st.write("This dashboard is designed for Period, Inc. to automatically visualize relevant financial figures.")

    # End of Streamlit app
