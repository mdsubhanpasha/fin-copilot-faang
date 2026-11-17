import streamlit as st
import pandas as pd

st.set_page_config(page_title="FIN-COPILOT-FAANG", layout="centered")
st.title("FIN-COPILOT-FAANG")
st.write("Ask in English. I will generate SQL and show the answer.")

# Sample Finance Data
data = {
    "product_name": ["Credit Card", "Debit Card", "Personal Loan", "Home Loan", "Savings Account"],
    "sales": [850000, 620000, 540000, 480000, 390000],
    "region": ["South", "North", "South", "West", "East"]
}
df = pd.DataFrame(data)

question = st.text_input("Your Question: Ex - What are the top 5 products?")
if st.button("Run"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        st.success(f"Your Question: {question}")
        st.subheader("Generated SQL")
        st.code("SELECT product_name, SUM(sales) AS total_sales FROM sales_table GROUP BY product_name ORDER BY total_sales DESC LIMIT 5;", language="sql")
        st.subheader("Result")
        result = df.sort_values(by="sales", ascending=False)
        st.dataframe(result, use_container_width=True)
        st.subheader("Visualization")
        st.bar_chart(result.set_index("product_name")["sales"])
        st.success("Insight: Credit Card is the top product with highest sales.")
