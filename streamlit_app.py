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
    income = getTotals.iloc[0:3]
    expenses = getTotals.iloc[4:-1]


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

    if "show_links" not in st.session_state:
        st.session_state["show_links"] = False

    # Function to toggle the visibility of links
    def toggle_links():
        st.session_state["show_links"] = not st.session_state["show_links"]

    # Button to toggle documentation links
    if st.button("Show/Hide Documentation", on_click=toggle_links):
        pass

    # Display clickable documentation links if toggled
    if st.session_state["show_links"]:
        st.markdown("<h4 style='text-align: center; color: #B22222;'>About this Dashboard</h4>", unsafe_allow_html=True)
        st.write("This dashboard is designed for Period, Inc. to automatically visualize relevant financial figures.")
        st.subheader("Helpful Documentation Links:")
        st.markdown("- [Dashboard Documentation](https://docs.google.com/document/d/1K6mAgw4I_pu06gdvjqOfTxXiHzgqGai3sHsZLqzYBk8/edit?usp=sharing)")
        st.markdown("- For Dashboard Maintenance or errors, [Contact DSS](https://dssberkeley.com/)")

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

        elif "profit" in uploaded_file.name.lower():
            incomecategory, incometotal, expensescategory, expensestotal, netcategory, nettotal = PF_totals(uploaded_file)
            st.subheader("Income Categories Distribution")
            # Create a DataFrame from the series
            data = pd.DataFrame({
                "Income Category": incomecategory,
                "Amount": incometotal
            })

            # Create an interactive bar chart using Plotly
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

            st.subheader("Expenses Categories Distribution")
            # Create a DataFrame from the series
            data1 = pd.DataFrame({
                "Expenses Category": expensescategory,
                "Amount": expensestotal
            })

            # Create an interactive bar chart using Plotly
            fig1 = px.bar(
                data1,
                x="Expenses Category",
                y="Amount",
                text="Amount",
                title="Expenses Categories",
                labels={"Expenses Category": "Category", "Amount": "Expenses Amount ($)"},
                color="Expenses Category"
            )

            # Customize chart appearance
            fig1.update_traces(texttemplate="$%{text:.2f}", textposition="outside")
            fig1.update_layout(
                xaxis_title="Expenses Category",
                yaxis_title="Amount ($)",
                showlegend=False,
                template="plotly_white"
            )

            # Display the interactive chart in Streamlit
            st.plotly_chart(fig1, use_container_width=True)

            st.subheader("Net Categories Distribution")
            # Create a DataFrame from the series
            data2 = pd.DataFrame({
                "Net Category": netcategory,
                "Amount": nettotal
            })

            # Create an interactive bar chart using Plotly
            fig2 = px.bar(
                data2,
                x="Net Category",
                y="Amount",
                text="Amount",
                title="Net Categories",
                labels={"Net Category": "Category", "Amount": "Net Amount ($)"},
                color="Net Category"
            )

            # Customize chart appearance
            fig2.update_traces(texttemplate="$%{text:.2f}", textposition="outside")
            fig2.update_layout(
                xaxis_title="Net Category",
                yaxis_title="Amount ($)",
                showlegend=False,
                template="plotly_white"
            )

            # Display the interactive chart in Streamlit
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Awaiting file upload. Please upload a CSV file.")

    # End of Streamlit app
