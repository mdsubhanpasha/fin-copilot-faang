import sqlite3, json
from http.server import BaseHTTPRequestHandler, HTTPServer

DB = "finance.db"
conn = sqlite3.connect(DB)
conn.execute("CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY, date TEXT, description TEXT, amount REAL)")
cur = conn.execute("SELECT COUNT(*) FROM transactions")
if cur.fetchone()[0] == 0:
    conn.executemany("INSERT INTO transactions (date, description, amount) VALUES (?,?,?)", [
        ("2026-10-01","Salary", 50000),
        ("2026-10-05","Rent", -15000),
        ("2026-11-01","Salary", 50000),
        ("2026-11-05","Groceries", -5000),
        ("2026-11-10","Freelance", 20000),
    ])
conn.commit(); conn.close()

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/summary":
            c = sqlite3.connect(DB); total = c.execute("SELECT SUM(amount) FROM transactions").fetchone()[0]; count = c.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]; c.close()
            self.send_json({"total": total, "count": count, "status": "Real DB Working"})
        elif self.path == "/api/chart":
            c = sqlite3.connect(DB); rows = c.execute("SELECT substr(date,1,7), SUM(amount) FROM transactions GROUP BY substr(date,1,7)").fetchall(); c.close()
            self.send_json({"labels": [r[0] for r in rows], "data": [float(r[1]) for r in rows]})
        else:
            with open("templates/index.html","rb") as f: data = f.read()
            self.send_response(200); self.send_header("Content-type","text/html"); self.end_headers(); self.wfile.write(data)
    def send_json(self, obj):
        data = json.dumps(obj).encode()
        self.send_response(200); self.send_header("Content-type","application/json"); self.end_headers(); self.wfile.write(data)
    def log_message(self, *a): pass

print("FIN-COPILOT Running on http://127.0.0.1:8000")
HTTPServer(("127.0.0.1", 8000), H).serve_forever()
