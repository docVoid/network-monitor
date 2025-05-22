
from flask import Flask, render_template, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def fetch_query(query):
    conn = sqlite3.connect("traffic.db")
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/protocols')
def protocols():
    query = "SELECT protocol, COUNT(*) FROM traffic GROUP BY protocol"
    data = fetch_query(query)
    return jsonify({row[0]: row[1] for row in data})

@app.route('/toptalkers')
def toptalkers():
    query = "SELECT src_ip, COUNT(*) as cnt FROM traffic GROUP BY src_ip ORDER BY cnt DESC LIMIT 10"
    data = fetch_query(query)
    return jsonify(data)

@app.route('/connections')
def connections():
    query = "SELECT src_ip, dst_ip, COUNT(*) FROM traffic GROUP BY src_ip, dst_ip ORDER BY COUNT(*) DESC LIMIT 10"
    data = fetch_query(query)
    return jsonify(data)

@app.route('/ports')
def ports():
    query = "SELECT dst_port, COUNT(*) as cnt FROM traffic WHERE dst_port IS NOT NULL GROUP BY dst_port ORDER BY cnt DESC LIMIT 10"
    data = fetch_query(query)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
