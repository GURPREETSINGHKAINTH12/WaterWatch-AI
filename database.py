import sqlite3, json, os
DB_PATH=os.path.join(os.path.dirname(os.path.dirname(__file__)),"waterwatch.db")
def init_db():
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS samples(
        id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        location TEXT, measurements TEXT, screening TEXT, anomaly INTEGER)""")
def save_sample(location, measurements, screening, anomaly):
    init_db()
    with sqlite3.connect(DB_PATH) as con:
        con.execute("INSERT INTO samples(location,measurements,screening,anomaly) VALUES(?,?,?,?)",
                    (location,json.dumps(measurements),json.dumps(screening),int(anomaly)))
def get_history():
    init_db()
    with sqlite3.connect(DB_PATH) as con:
        rows=con.execute("SELECT id,created_at,location,measurements,screening,anomaly FROM samples ORDER BY id DESC").fetchall()
    return rows
