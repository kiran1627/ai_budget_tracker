import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data
from models.anomaly_detection import detect_anomalies

# ✅ Set up Streamlit page config
st.set_page_config(page_title="Government Budget & Fraud Tracker", layout="wide")

# ✅ Sidebar Navigation
st.sidebar.title("📊 Budget & Fraud Analysis")
page = st.sidebar.radio("📌 Select Analysis", ["Expenditure", "Schemes", "Budget"])

# ✅ Load Data Button
if st.button("🔍 Load Data"):
    expenditure_df, schemes_df, budget_df = load_data()
    st.success("✅ Data loaded successfully!")

    # ✅ Detect Fraud in all datasets
    expenditure_df = detect_anomalies(expenditure_df, ["Budget 2023-2024 Total"])
    schemes_df = detect_anomalies(schemes_df, ["Budget Estimates 2023-2024"])
    budget_df = detect_anomalies(budget_df, ["2023-2024 Budget Estimates"])

    # ✅ Separate Fraud and Non-Fraud Data
    fraud_expenditure = expenditure_df[expenditure_df["Anomaly_Flag"] == "Fraud"]
    normal_expenditure = expenditure_df[expenditure_df["Anomaly_Flag"] == "Normal"]

    fraud_schemes = schemes_df[schemes_df["Anomaly_Flag"] == "Fraud"]
    normal_schemes = schemes_df[schemes_df["Anomaly_Flag"] == "Normal"]

    fraud_budget = budget_df[budget_df["Anomaly_Flag"] == "Fraud"]
    normal_budget = budget_df[budget_df["Anomaly_Flag"] == "Normal"]

    # ✅ Fraud Percentage Calculation Function
    def calculate_fraud_percentage(fraud_df, total_df):
        if total_df.empty:
            return 0
        return round((len(fraud_df) / len(total_df)) * 100, 2)

    # ✅ Fraud Percentages
    expenditure_fraud_pct = calculate_fraud_percentage(fraud_expenditure, expenditure_df)
    schemes_fraud_pct = calculate_fraud_percentage(fraud_schemes, schemes_df)
    budget_fraud_pct = calculate_fraud_percentage(fraud_budget, budget_df)

    # 📌 **Fraud Percentage Section**
    st.sidebar.header("🚨 Fraud Percentages")
    st.sidebar.metric("📌 Expenditure Fraud", f"{expenditure_fraud_pct}%")
    st.sidebar.metric("📌 Schemes Fraud", f"{schemes_fraud_pct}%")
    st.sidebar.metric("📌 Budget Fraud", f"{budget_fraud_pct}%")

    # ✅ **Expenditure Analysis**
    if page == "Expenditure":
        st.subheader("📊 Expenditure Analysis")

        # ✅ Show Data Tables
        with st.expander("📄 Normal Expenditure Data"):
            st.dataframe(normal_expenditure)

        with st.expander("🚨 Fraudulent Expenditure Data"):
            st.dataframe(fraud_expenditure)

        # ✅ **Normal Expenditure**
        st.markdown("### ✅ Normal Expenditure")
        fig_exp_normal = px.bar(
            normal_expenditure,
            x="Ministries/Departments",
            y="Budget 2023-2024 Total",
            title="📌 Normal Budget Allocation (by Department)",
            color="Ministries/Departments",
            text_auto=True
        )
        st.plotly_chart(fig_exp_normal, use_container_width=True)

        # ✅ **Fraudulent Expenditure**
        if not fraud_expenditure.empty:
            st.markdown("### 🚨 Fraudulent Expenditure")
            fig_exp_fraud = px.bar(
                fraud_expenditure,
                x="Ministries/Departments",
                y="Budget 2023-2024 Total",
                title="🚨 Fraudulent Budget Allocation (by Department)",
                color="Ministries/Departments",
                text_auto=True,
                color_discrete_sequence=["red"]
            )
            st.plotly_chart(fig_exp_fraud, use_container_width=True)

    # ✅ **Schemes Analysis**
    elif page == "Schemes":
        st.subheader("📜 Schemes Analysis")

        # ✅ Show Data Tables
        with st.expander("📄 Normal Schemes Data"):
            st.dataframe(normal_schemes)

        with st.expander("🚨 Fraudulent Schemes Data"):
            st.dataframe(fraud_schemes)

        # ✅ **Normal Schemes**
        st.markdown("### ✅ Normal Schemes Budget Allocation")
        fig_schemes_normal = px.pie(
            normal_schemes,
            names="Scheme Type",
            values="Budget Estimates 2023-2024",
            title="📌 Budget Allocation by Scheme Type"
        )
        st.plotly_chart(fig_schemes_normal)

        # ✅ **Fraudulent Schemes**
        if not fraud_schemes.empty:
            st.markdown("### 🚨 Fraudulent Schemes")
            fig_schemes_fraud = px.bar(
                fraud_schemes,
                x="Scheme Type",
                y="Budget Estimates 2023-2024",
                title="🚨 Fraudulent Budget Allocation by Scheme",
                color="Scheme Type",
                text_auto=True,
                color_discrete_sequence=["red"]
            )
            st.plotly_chart(fig_schemes_fraud)

    elif page == "Budget":
        st.subheader("📊 Budget Analysis")

        # ✅ Step 1: Check if budget data is loaded
        if "budget_df" not in locals() or budget_df is None or budget_df.empty:
            st.error("🚨 Error: Budget data is empty or failed to load!")
        else:
            # ✅ Step 2: Display raw data for debugging
            st.write("🛠️ **Raw Budget Data Preview:**")
            st.dataframe(budget_df.head())  # Show first few rows

           

            # ✅ Step 4: Rename columns if necessary
            if "Year" not in budget_df.columns:
                for col in budget_df.columns:
                    if "year" in col.lower():
                        budget_df.rename(columns={col: "Year"}, inplace=True)

            if "2023-2024 Budget Estimates" not in budget_df.columns:
                for col in budget_df.columns:
                    if "budget" in col.lower() and "estimate" in col.lower():
                        budget_df.rename(columns={col: "2023-2024 Budget Estimates"}, inplace=True)

            # ✅ Step 5: Check for required columns
            if "Year" not in budget_df.columns or "2023-2024 Budget Estimates" not in budget_df.columns:
                st.error("🚨 Error: Required columns ('Year', '2023-2024 Budget Estimates') are still missing!")
            else:
                # ✅ Step 6: Convert "Year" to numeric and remove NaN values
                budget_df["Year"] = pd.to_numeric(budget_df["Year"], errors="coerce")
                budget_df.dropna(subset=["Year", "2023-2024 Budget Estimates"], inplace=True)

                # ✅ Step 7: Separate fraud and normal budgets
                if "Anomaly_Flag" in budget_df.columns:
                    normal_budget = budget_df[budget_df["Anomaly_Flag"] == "Normal"]
                    fraud_budget = budget_df[budget_df["Anomaly_Flag"] == "Fraud"]
                else:
                    st.error("🚨 Error: 'Anomaly_Flag' column is missing! Cannot separate fraud data.")
                    normal_budget = pd.DataFrame()
                    fraud_budget = pd.DataFrame()

                # ✅ Step 8: Show Normal and Fraud Data
                if not normal_budget.empty:
                    with st.expander("📄 **Normal Budget Data**"):
                        st.dataframe(normal_budget)
                

              