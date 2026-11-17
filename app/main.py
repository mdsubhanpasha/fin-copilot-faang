import streamlit as st

st.set_page_config(page_title="FIN-COPILOT-FAANG", layout="centered")
st.title("FIN-COPILOT-FAANG")
st.write("Ask in English. I will generate SQL and show the answer.")

question = st.text_input("Your Question: Ex - What are the top 5 products?")
if st.button("Run"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        st.success(f"Your Question: {question}")
        st.subheader("Generated SQL")
        st.code("SELECT product_name, SUM(sales) AS total_sales FROM sales_table GROUP BY product_name ORDER BY total_sales DESC LIMIT 5;", language="sql")
        st.subheader("Result")
        st.info("Next Step: Connect this SQL to BigQuery to fetch live data.")
