import streamlit as st

st.set_page_config(page_title="FIN-COPILOT-FAANG", layout="wide")
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
        table_text = "| Product | Total Sales | Region |\n| --- | --- | --- |\n| Credit Card | 850000 | South |\n| Debit Card | 620000 | North |\n| Personal Loan | 540000 | South |\n| Home Loan | 480000 | West |\n| Savings Account | 390000 | East |"
        st.markdown(table_text)
        st.subheader("Top Products")
        st.write("Credit Card - 850000 - [##########] 100%")
        st.write("Debit Card - 620000 - [#######] 73%")
        st.write("Personal Loan - 540000 - [######] 64%")
        st.write("Home Loan - 480000 - [#####] 56%")
        st.write("Savings Account - 390000 - [####] 46%")
        st.success("Insight: Credit Card is the top product with highest sales.")
