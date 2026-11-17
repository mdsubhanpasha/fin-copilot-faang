import streamlit as st
st.title("FIN-COPILOT-FAANG")
st.write("Adugu bro, nenu SQL rasi answer istha")
question = st.text_input("Nee Question: Ex - Top 5 products enti?")
if st.button("Run"):
    st.success(f"Nee Question: {question}")
    st.code("SELECT product_name, SUM(sales) as total_sales FROM sales_table GROUP BY product_name ORDER BY total_sales DESC LIMIT 5;", language="sql")
    st.info("Next Step: Ee SQL ni BigQuery ki connect chestham")
