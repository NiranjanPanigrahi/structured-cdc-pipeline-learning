import random
from datetime import datetime, timedelta

ips = ["127.0.0.1", "192.168.1.5", "10.0.0.3", "172.16.0.9", "203.0.113.42"]
paths = ["/index.html", "/dashboard", "/api/login", "/api/data", "/missing", "/reports", "/upload"]
methods = ["GET", "POST", "PUT", "DELETE"]
statuses = [200, 200, 200, 201, 301, 400, 401, 403, 404, 500, 502]

start_time = datetime(2026, 8, 10, 14, 0, 0)
lines = []

for i in range(500):
    ip = random.choice(ips)
    ts = (start_time + timedelta(seconds=i * 2)).strftime("%d/%b/%Y:%H:%M:%S +0530")
    method = random.choice(methods)
    path = random.choice(paths)
    status = random.choice(statuses)
    size = random.randint(100, 5000)
    line = f'{ip} - - [{ts}] "{method} {path} HTTP/1.1" {status} {size}'
    lines.append(line)

# sprinkle in some malformed lines on purpose
for _ in range(15):
    pos = random.randint(0, len(lines) - 1)
    lines[pos] = "GARBAGE this line is broken and does not match"

with open("sample.log", "w") as f:
    f.write("\n".join(lines) + "\n")

print("sample.log written with", len(lines), "lines")
