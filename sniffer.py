
from scapy.all import sniff, IP, TCP, UDP
import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("traffic.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS traffic (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            protocol TEXT,
            src_ip TEXT,
            dst_ip TEXT,
            dst_port INTEGER
        )
    """)
    conn.commit()
    conn.close()

def store_packet(packet):
    conn = sqlite3.connect("traffic.db")
    c = conn.cursor()
    now = datetime.now().isoformat(timespec='seconds')

    proto = packet.__class__.__name__
    src_ip = packet[IP].src if IP in packet else None
    dst_ip = packet[IP].dst if IP in packet else None
    dst_port = None

    if TCP in packet:
        dst_port = packet[TCP].dport
    elif UDP in packet:
        dst_port = packet[UDP].dport

    c.execute("INSERT INTO traffic (timestamp, protocol, src_ip, dst_ip, dst_port) VALUES (?, ?, ?, ?, ?)",
              (now, proto, src_ip, dst_ip, dst_port))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    sniff(prn=store_packet, store=False)
