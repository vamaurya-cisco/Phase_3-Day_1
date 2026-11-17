import sqlite3 
from alert_utils import get_alerts_by_source 

conn = sqlite3.connect("alerts_demo.db") 
conn.execute("DROP TABLE IF EXISTS alerts") 
conn.execute("CREATE TABLE alerts (id INTEGER PRIMARY KEY, source TEXT)") 
conn.executemany("INSERT INTO alerts (source) VALUES (?)", [("api-gateway",), 
("network-monitor",)]) 
conn.commit() 
conn.close() 

print("Normal lookup: ", get_alerts_by_source("alerts_demo.db", "api-gateway"))
print("Injection lookup:", get_alerts_by_source("alerts_demo.db", 
"nonexistent' OR '1'='1"))