import streamlit as st
import urllib.request
import json
import urllib.error
import time
import sqlite3

st.set_page_config(page_title="FIN-COPILOT-FAANG", layout="wide")
st.title("FIN-COPILOT-FAANG")
st.write("Ask in English. I will generate SQL, run it on real database, and show the answer.")

api_key = st.text_input("Enter Gemini API Key (from aistudio.google.com)", type="password")
question = st.text_input("Your Question: Ex - What are the top 5 products?")

def clean_sql(text):
    return text.replace("`sql", "").replace("`", "").strip()

def get_db():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE sales_table (product_name TEXT, sales INTEGER, region TEXT)")
    data = [
        ("Credit Card", 850000, "South"),
        ("Debit Card", 620000, "North"),
        ("Personal Loan", 540000, "South"),
        ("Home Loan", 480000, "West"),
        ("Savings Account", 390000, "East"),
        ("Credit Card", 250000, "North"),
        ("Debit Card", 180000, "South"),
        ("Home Loan", 320000, "South"),
    ]
    cur.executemany("INSERT INTO sales_table VALUES (?, ?, ?)", data)
    conn.commit()
    return conn

def call_gemini(api_key, question):
    models = ["gemini-2.5-flash-lite", "gemini-3.0-flash", "gemini-2.0-flash", "gemini-3.8-flash"]
    prompt = f"""You are a SQL expert. Table: sales_table(product_name TEXT, sales INTEGER, region TEXT).
    Rules:
    1. If user asks top products, use: SELECT product_name, SUM(sales) AS total_sales FROM sales_table GROUP BY product_name ORDER BY total_sales DESC LIMIT 5;
    2. If user asks top region, use: SELECT region, SUM(sales) AS total_sales FROM sales_table GROUP BY region ORDER BY total_sales DESC;
    3. Always include SUM(sales) when asking for totals. Never return only one column.
    4. Return only SQL query, no explanation, no markdown.
    User question: {question}"""
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    data = json.dumps(payload).encode("utf-8")
    last_error = ""
    for model in models:
        for attempt in range(2):
            try:
                url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={api_key}"
                req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=30) as resp:
                    result = json.loads(resp.read().decode("utf-8"))
                    sql = result["candidates"][0]["content"]["parts"][0]["text"].strip()
                    return clean_sql(sql), model
            except urllib.error.HTTPError as e:
                last_error = e.read().decode("utf-8")
                if "503" in last_error or "429" in last_error:
                    time.sleep(2)
                    continue
                break
            except Exception as e:
                last_error = str(e)
                break
    raise Exception(last_error)

if st.button("Run"):
    if not question.strip():
        st.warning("Please enter a question.")
    elif not api_key.strip():
        st.warning("Please enter Gemini API Key.")
    else:
        st.success(f"Your Question: {question}")
        try:
            sql, used_model = call_gemini(api_key.strip(), question)
            st.success(f"Gemini Connected - Live AI SQL using {used_model}")
        except Exception as e:
            st.error(f"All models busy: {e}")
            sql = "SELECT product_name, SUM(sales) AS total_sales FROM sales_table GROUP BY product_name ORDER BY total_sales DESC LIMIT 5;"
        st.subheader("Generated SQL")
        st.code(sql, language="sql")
        st.subheader("Real Result - From Database")
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]
            header = "| " + " | ".join(cols) + " |\n| " + " | ".join(["---"] * len(cols)) + " |"
            body = "\n".join(["| " + " | ".join([str(c) for c in r]) + " |" for r in rows])
            st.markdown(header + "\n" + body)
            if rows:
                st.success(f"Insight: Found {len(rows)} rows. Top result: {rows[0]}")
            conn.close()
        except Exception as e:
            st.error(f"SQL Run Error: {e}")
            st.warning("Gemini SQL lo chinna mistake undi, malli Run kottu.")
