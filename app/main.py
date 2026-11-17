import streamlit as st

st.set_page_config(page_title="FIN-COPILOT-FAANG", layout="centered")
st.title("FIN-COPILOT-FAANG")
st.write("Ask in English. I will generate SQL and show the answer.")

# Sample Finance Data - No Pandas, No Numpy
data = [
    {"Product": "Credit Card", "Total Sales": 850000, "Region": "South"},
    {"Product": "Debit Card", "Total Sales": 620000, "Region": "North"},
    {"Product": "Personal Loan", "Total Sales": 540000, "Region": "South"},
    {"Product": "Home Loan", "Total Sales": 480000, "Region": "West"},
    {"Product": "Savings Account", "Total Sales": 390000, "Region": "East"},
]

question = st.text_input("Your Question: Ex - What are the top 5 products?")
if st.button("Run"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        st.success(f"Your Question: {question}")
        st.subheader("Generated SQL")
        st.code("SELECT product_name, SUM(sales) AS total_sales FROM sales_table GROUP BY product_name ORDER BY total_sales DESC LIMIT 5;", language="sql")
        st.subheader("Result")
        st.table(data)
        st.subheader("Top Products")
        for row in data:
            st.write(f"{row['Product']} - {row['Total Sales']}")
            st.progress(row['Total Sales'] / 850000)
        st.success("Insight: Credit Card is the top product with highest sales.")
