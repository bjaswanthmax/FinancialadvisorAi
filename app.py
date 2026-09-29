import streamlit as st
import pandas as pd
from datetime import date

from src.ocr import extract_text_from_image
from src.expense_parser import parse_expense
from src.categorizer import categorize_expense

from src.database import (
    create_database,
    add_expense,
    get_expenses,
    delete_expense
)

from src.advisor import (
    get_financial_advice,
    generate_financial_advice,
    generate_indian_advice
)

from src.analytics import (
    expenses_to_dataframe,
    total_spending,
    average_expense,
    highest_expense,
    transaction_count,
    category_summary,
    merchant_summary,
    monthly_summary,
    source_summary
)

from src.budget import (
    budget_percentage,
    remaining_budget,
    budget_status
)

from src.csv_importer import prepare_csv

from src.reports import generate_report


st.set_page_config(
    page_title="Financial Advisor AI",
    page_icon="💰",
    layout="wide"
)

create_database()


st.title("💰 Financial Advisor AI")
st.caption(
    "AI-powered expense tracking and personal finance analysis"
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("⚙️ Settings")

monthly_budget = st.sidebar.number_input(
    "Monthly Budget",
    min_value=0.0,
    value=10000.0,
    step=500.0
)


st.sidebar.subheader("Category Budgets")

food_budget = st.sidebar.number_input(
    "Food Budget",
    min_value=0.0,
    value=3000.0,
    step=500.0
)

shopping_budget = st.sidebar.number_input(
    "Shopping Budget",
    min_value=0.0,
    value=3000.0,
    step=500.0
)

transport_budget = st.sidebar.number_input(
    "Transport Budget",
    min_value=0.0,
    value=2000.0,
    step=500.0
)

bills_budget = st.sidebar.number_input(
    "Bills Budget",
    min_value=0.0,
    value=2000.0,
    step=500.0
)


# =========================================================
# MANUAL EXPENSE
# =========================================================

st.subheader("➕ Add Expense Manually")

manual_col1, manual_col2, manual_col3 = st.columns(3)

with manual_col1:
    manual_merchant = st.text_input(
        "Merchant"
    )

with manual_col2:
    manual_amount = st.number_input(
        "Amount",
        min_value=0.0,
        step=10.0
    )

with manual_col3:
    manual_category = st.selectbox(
        "Category",
        [
            "Food",
            "Shopping",
            "Transport",
            "Bills",
            "Healthcare",
            "Education",
            "Entertainment",
            "Other"
        ]
    )

manual_date = st.date_input(
    "Expense Date",
    value=date.today()
)

if st.button(
    "Add Expense",
    type="primary"
):

    if manual_amount <= 0:
        st.error("Please enter a valid amount.")

    else:
        add_expense(
            manual_merchant if manual_merchant else "Unknown",
            manual_amount,
            manual_category,
            "",
            str(manual_date),
            "Manual"
        )

        st.success(
            "Expense added successfully."
        )

        st.rerun()


# =========================================================
# RECEIPT OCR
# =========================================================

st.subheader("📷 Upload Receipt")

uploaded_file = st.file_uploader(
    "Upload receipt image",
    type=[
        "png",
        "jpg",
        "jpeg"
    ]
)

if uploaded_file is not None:

    st.image(
        uploaded_file,
        caption="Uploaded Receipt",
        width=400
    )

    if st.button(
        "Extract Expense from Receipt"
    ):

        try:

            text = extract_text_from_image(
                uploaded_file
            )

            st.subheader(
                "🔍 Extracted Text"
            )

            st.text_area(
                "OCR Result",
                text,
                height=200
            )

            expense = parse_expense(
                text
            )

            merchant = expense[
                "merchant"
            ]

            amount = expense[
                "amount"
            ]

            category = categorize_expense(
                text
            )

            st.subheader(
                "💰 Expense Details"
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Merchant",
                    merchant
                )

            with col2:
                if amount is not None:
                    st.metric(
                        "Amount",
                        f"₹{amount:.2f}"
                    )
                else:
                    st.metric(
                        "Amount",
                        "Not detected"
                    )

            with col3:
                st.metric(
                    "Category",
                    category
                )

            if amount is not None:

                if st.button(
                    "Save Receipt Expense"
                ):

                    add_expense(
                        merchant,
                        amount,
                        category,
                        text,
                        str(date.today()),
                        "OCR Receipt"
                    )

                    st.success(
                        "Receipt expense saved."
                    )

                    st.rerun()

        except Exception as e:

            st.error(
                f"OCR processing failed: {e}"
            )


# =========================================================
# CSV IMPORT
# =========================================================

st.subheader("📄 Import Expenses from CSV")

csv_file = st.file_uploader(
    "Upload expense CSV",
    type=["csv"],
    key="csv_uploader"
)

if csv_file is not None:

    try:

        csv_df = prepare_csv(
            csv_file
        )

        st.write(
            "CSV Preview"
        )

        st.dataframe(
            csv_df,
            width="stretch"
        )

        if st.button(
            "Import CSV Expenses"
        ):

            imported_count = 0

            for _, row in csv_df.iterrows():

                amount = row.get(
                    "Amount"
                )

                merchant = row.get(
                    "Merchant",
                    "Unknown"
                )

                category = row.get(
                    "Category",
                    "Other"
                )

                expense_date = row.get(
                    "Date",
                    date.today()
                )

                if pd.isna(amount):
                    continue

                if pd.isna(merchant):
                    merchant = "Unknown"

                if pd.isna(category):
                    category = "Other"

                if pd.isna(expense_date):
                    expense_date = date.today()

                add_expense(
                    str(merchant),
                    float(amount),
                    str(category),
                    "",
                    str(expense_date),
                    "CSV"
                )

                imported_count += 1

            st.success(
                f"{imported_count} expenses imported successfully."
            )

            st.rerun()

    except Exception as e:

        st.error(
            f"Could not import CSV: {e}"
        )


# =========================================================
# LOAD DATABASE
# =========================================================

expenses = get_expenses()

df = expenses_to_dataframe(
    expenses
)


# =========================================================
# DASHBOARD
# =========================================================

st.header("📊 Dashboard")


if df.empty:

    st.info(
        "No expenses recorded yet. "
        "Add an expense or upload a receipt."
    )

    current_month_df = df.copy()

else:

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    today = pd.Timestamp.today()

    current_month_df = df[
        (df["Date"].dt.year == today.year)
        &
        (df["Date"].dt.month == today.month)
    ].copy()


# =========================================================
# MAIN METRICS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Spending",
        f"₹{total_spending(df):,.2f}"
    )

with col2:

    st.metric(
        "Transactions",
        transaction_count(df)
    )

with col3:

    st.metric(
        "Average Expense",
        f"₹{average_expense(df):,.2f}"
    )

with col4:

    st.metric(
        "Highest Expense",
        f"₹{highest_expense(df):,.2f}"
    )


# =========================================================
# CURRENT MONTH
# =========================================================

st.subheader(
    "📅 Current Month"
)

current_month_spending = total_spending(
    current_month_df
)

remaining = remaining_budget(
    current_month_spending,
    monthly_budget
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Current Month Spending",
        f"₹{current_month_spending:,.2f}"
    )

with col2:

    st.metric(
        "Monthly Budget",
        f"₹{monthly_budget:,.2f}"
    )

with col3:

    st.metric(
        "Remaining Budget",
        f"₹{remaining:,.2f}"
    )


# =========================================================
# FILTERS
# =========================================================

st.subheader(
    "🔎 Expense Filters"
)

if not df.empty:

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()

    with filter_col1:

        selected_dates = st.date_input(
            "Date Range",
            value=(
                min_date,
                max_date
            )
        )

    with filter_col2:

        categories = [
            "All"
        ] + sorted(
            df["Category"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_category = st.selectbox(
            "Category",
            categories
        )

    with filter_col3:

        merchants = [
            "All"
        ] + sorted(
            df["Merchant"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_merchant = st.selectbox(
            "Merchant",
            merchants
        )

    filtered_df = df.copy()

    if (
        isinstance(
            selected_dates,
            tuple
        )
        and len(selected_dates) == 2
    ):

        start_date = pd.Timestamp(
            selected_dates[0]
        )

        end_date = pd.Timestamp(
            selected_dates[1]
        )

        filtered_df = filtered_df[
            (filtered_df["Date"] >= start_date)
            &
            (filtered_df["Date"] <= end_date)
        ]

    if selected_category != "All":

        filtered_df = filtered_df[
            filtered_df["Category"]
            == selected_category
        ]

    if selected_merchant != "All":

        filtered_df = filtered_df[
            filtered_df["Merchant"]
            == selected_merchant
        ]

else:

    filtered_df = df.copy()


# =========================================================
# EXPENSE HISTORY
# =========================================================

st.subheader(
    "📋 Expense History"
)

if filtered_df.empty:

    st.info(
        "No expenses match the selected filters."
    )

else:

    display_df = filtered_df.copy()

    display_df["Date"] = (
        display_df["Date"]
        .dt.strftime("%Y-%m-%d")
    )

    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True
    )


# =========================================================
# CSV EXPORT
# =========================================================

if not filtered_df.empty:

    export_df = filtered_df.copy()

    export_df["Date"] = (
        export_df["Date"]
        .dt.strftime("%Y-%m-%d")
    )

    csv_data = export_df.to_csv(
        index=False
    )

    st.download_button(
        "⬇️ Download Expenses CSV",
        data=csv_data,
        file_name="expenses.csv",
        mime="text/csv"
    )


# =========================================================
# DELETE EXPENSE
# =========================================================

st.subheader(
    "🗑️ Delete Expense"
)

if not df.empty:

    expense_options = {}

    for _, row in df.iterrows():

        label = (
            f"{int(row['ID'])} - "
            f"{row['Merchant']} - "
            f"₹{row['Amount']:.2f}"
        )

        expense_options[label] = int(
            row["ID"]
        )

    selected_expense = st.selectbox(
        "Select expense to delete",
        list(expense_options.keys())
    )

    if st.button(
        "Delete Selected Expense"
    ):

        expense_id = expense_options[
            selected_expense
        ]

        delete_expense(
            expense_id
        )

        st.success(
            "Expense deleted successfully."
        )

        st.rerun()


# =========================================================
# SPENDING BY CATEGORY
# =========================================================

st.subheader(
    "📊 Spending by Category"
)

if not df.empty:

    category_df = category_summary(
        df
    )

    if not category_df.empty:

        st.bar_chart(
            category_df.set_index(
                "Category"
            )["Amount"]
        )

        st.dataframe(
            category_df,
            width="stretch",
            hide_index=True
        )

    else:

        st.info(
            "No category data available."
        )


# =========================================================
# SPENDING BY MERCHANT
# =========================================================

st.subheader(
    "🏪 Spending by Merchant"
)

if not df.empty:

    merchant_df = merchant_summary(
        df
    )

    if not merchant_df.empty:

        st.bar_chart(
            merchant_df.set_index(
                "Merchant"
            )["Amount"]
        )


# =========================================================
# MONTHLY SPENDING
# =========================================================

st.subheader(
    "📅 Monthly Spending"
)

if not df.empty:

    monthly_df = monthly_summary(
        df
    )

    if not monthly_df.empty:

        st.line_chart(
            monthly_df.set_index(
                "Month"
            )["Amount"]
        )


# =========================================================
# SOURCE ANALYSIS
# =========================================================

st.subheader(
    "📥 Expense Sources"
)

if not df.empty:

    source_df = source_summary(
        df
    )

    if not source_df.empty:

        st.dataframe(
            source_df,
            width="stretch",
            hide_index=True
        )


# =========================================================
# SPENDING INSIGHTS
# =========================================================

st.subheader(
    "💡 Spending Insights"
)

if not df.empty:

    highest_category = (
        category_summary(df)
    )

    highest_merchant = (
        merchant_summary(df)
    )

    if not highest_category.empty:

        top_category = (
            highest_category.iloc[0]
        )

        st.info(
            f"Highest spending category: "
            f"{top_category['Category']} "
            f"₹{top_category['Amount']:.2f}"
        )

    if not highest_merchant.empty:

        top_merchant = (
            highest_merchant.iloc[0]
        )

        st.info(
            f"Highest spending merchant: "
            f"{top_merchant['Merchant']} "
            f"₹{top_merchant['Amount']:.2f}"
        )


# =========================================================
# CATEGORY BUDGET ANALYSIS
# =========================================================

st.subheader(
    "🎯 Category Budget Analysis"
)

category_budgets = {
    "Food": food_budget,
    "Shopping": shopping_budget,
    "Transport": transport_budget,
    "Bills": bills_budget
}

for category, budget in category_budgets.items():

    if df.empty:

        spending = 0.0

    else:

        spending = df.loc[
            df["Category"] == category,
            "Amount"
        ].sum()

    percentage = budget_percentage(
        spending,
        budget
    )

    remaining_category = (
        remaining_budget(
            spending,
            budget
        )
    )

    status = budget_status(
        spending,
        budget
    )

    st.write(
        f"**{category}**"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Spent",
            f"₹{spending:.2f}"
        )

    with col2:

        st.metric(
            "Budget",
            f"₹{budget:.2f}"
        )

    with col3:

        st.metric(
            "Remaining",
            f"₹{remaining_category:.2f}"
        )

    with col4:

        st.metric(
            "Status",
            status
        )

    st.progress(
        min(
            max(
                percentage / 100,
                0.0
            ),
            1.0
        )
    )


# =========================================================
# FINANCIAL HEALTH
# =========================================================

st.subheader(
    "❤️ Financial Health Summary"
)

budget_used = budget_percentage(
    current_month_spending,
    monthly_budget
)

if monthly_budget > 0:

    if budget_used <= 50:

        health_message = (
            "Your current spending is below "
            "half of the monthly budget."
        )

    elif budget_used <= 80:

        health_message = (
            "Your spending is using a moderate "
            "portion of the monthly budget."
        )

    elif budget_used <= 100:

        health_message = (
            "Your spending is approaching the "
            "monthly budget limit."
        )

    else:

        health_message = (
            "Your current spending is above "
            "the monthly budget."
        )

    st.info(
        health_message
    )

    st.progress(
        min(
            max(
                budget_used / 100,
                0.0
            ),
            1.0
        )
    )


# =========================================================
# FINANCIAL ADVISOR
# =========================================================

st.subheader(
    "🤖 Financial Advisor"
)

advisor_budget = st.number_input(
    "Advisor Monthly Budget",
    min_value=0.0,
    value=10000.0,
    step=500.0,
    key="advisor_budget"
)

if not current_month_df.empty:

    advice_list = generate_financial_advice(
        current_month_df,
        advisor_budget
    )

    for advice in advice_list:

        st.info(
            advice
        )

else:

    st.info(
        "Add expenses to receive financial insights."
    )


# =========================================================
# INDIAN FINANCE ADVISOR
# =========================================================

st.subheader(
    "🇮🇳 Indian Personal Finance Advisor"
)

income = st.number_input(
    "Monthly Income",
    min_value=0.0,
    value=30000.0,
    step=1000.0,
    key="indian_income"
)

indian_expenses = st.number_input(
    "Monthly Expenses",
    min_value=0.0,
    value=float(
        current_month_spending
    ),
    step=500.0,
    key="indian_expenses"
)

savings_goal = st.number_input(
    "Monthly Savings Goal",
    min_value=0.0,
    value=5000.0,
    step=500.0,
    key="savings_goal"
)

if st.button(
    "Generate Indian Finance Advice"
):

    try:

        indian_advice = generate_indian_advice(
            income,
            indian_expenses,
            savings_goal
        )

        if isinstance(
            indian_advice,
            list
        ):

            for advice in indian_advice:

                st.info(
                    advice
                )

        else:

            st.info(
                indian_advice
            )

    except Exception as e:

        st.error(
            f"Could not generate Indian finance advice: {e}"
        )


# =========================================================
# FINANCIAL REPORT
# =========================================================

st.subheader(
    "📑 Financial Report"
)

if not df.empty:

    if st.button(
        "Generate Financial Report"
    ):

        try:

            report = generate_report(
                df
            )

            if isinstance(
                report,
                str
            ):

                st.text_area(
                    "Financial Report",
                    report,
                    height=400
                )

            else:

                st.write(
                    report
                )

        except Exception as e:

            st.error(
                f"Could not generate report: {e}"
            )

else:

    st.info(
        "Add expenses to generate a financial report."
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Financial Advisor AI | "
    "Educational financial analysis only. "
    "Not professional financial advice."
)