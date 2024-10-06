from log2pg.log_processor import parse_log_line
from datetime import datetime

def test_parse_log_line():
    log_line = "2024-05-01 12:34:56 cust_1 /api/v1/resource1 200 0.123"
    parsed = parse_log_line(log_line)
    
    assert parsed["timestamp"] == datetime(2024, 5, 1, 12, 34, 56)
    assert parsed["customer_id"] == "cust_1"
    assert parsed["request_path"] == "/api/v1/resource1"
    assert parsed["status_code"] == 200
    assert parsed["duration"] == 0.123