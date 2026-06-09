import time, os, re
from prometheus_client import start_http_server, Counter

errors = Counter('log_errors_total', 'HTTP 500 errors')
security = Counter('log_security_total', 'Auth failures 401/403')
suspicious = Counter('log_suspicious_total', 'SQLi/XSS attempts')
ddos = Counter('log_ddos_total', '429 rate limit hits')

PATTERNS = {
    'error': re.compile(r'" 5\d\d '),
    'security': re.compile(r'" 40[13] '),
    'suspicious': re.compile(r'(union.*select|<script|\.\.\/)', re.I),
    'ddos': re.compile(r'" 429 '),
}

def classify(line):
    if PATTERNS['suspicious'].search(line): suspicious.inc()
    if PATTERNS['error'].search(line): errors.inc()
    if PATTERNS['security'].search(line): security.inc()
    if PATTERNS['ddos'].search(line): ddos.inc()

start_http_server(8000)
print("Classifier running on :8000")

log_path = '/logs/access.log'
while not os.path.exists(log_path):
    print("Waiting for access.log...")
    time.sleep(2)

with open(log_path, 'r') as f:
    f.seek(0, 2)
    while True:
        line = f.readline()
        if line:
            classify(line)
        else:
            time.sleep(0.5)