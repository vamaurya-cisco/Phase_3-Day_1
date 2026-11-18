# test_alert_utils.py 
  
import sqlite3 
import pytest 
  
from alert_utils import format_alert_message, get_alerts_by_source 
  
  
def test_critical_message_matches_before_behavior(): 
    msg = format_alert_message("CRITICAL", "CPU spike", "api-gateway", 
"cpu_utilization", 96.5, 85.0) 
    assert msg == ( 
        "CRITICAL ALERT: CPU spike from api-gateway. " 
        "cpu_utilization reached 96.5, threshold is 85.0." 
    ) 
  
  
def test_unknown_level_raises_value_error(): 
    with pytest.raises(ValueError, match="Unknown alert level"): 
        format_alert_message("EMERGENCY", "x", "y", "z", 1, 1) 
  
  
def test_sql_injection_payload_is_treated_as_literal_value(tmp_path): 
    """A classic ' OR '1'='1 payload must match zero rows, not the whole 
table.""" 
    db_path = str(tmp_path / "alerts.db") 
    conn = sqlite3.connect(db_path) 
    conn.execute("CREATE TABLE alerts (id INTEGER PRIMARY KEY, source TEXT)") 
    conn.executemany(
        "INSERT INTO alerts (source) VALUES (?)",
        [("api-gateway",), ("network-monitor",)],
    )
    conn.commit() 
    conn.close() 
  
    rows = get_alerts_by_source(db_path, "api-gateway") 
    assert len(rows) == 1 
  
    injection_payload = "nonexistent' OR '1'='1" 
    rows = get_alerts_by_source(db_path, injection_payload) 
    assert rows == [] 
  
  
def test_empty_source_name_is_rejected(): 
    with pytest.raises(ValueError, match="non-empty string"): 
        get_alerts_by_source("irrelevant.db", "") 