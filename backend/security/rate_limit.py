import time

REQUEST_LOG = {}
MAX_REQUESTS = 10
WINDOW = 60  # seconds

def is_rate_limited(ip: str):
    now = time.time()
    REQUEST_LOG.setdefault(ip, [])
    REQUEST_LOG[ip] = [t for t in REQUEST_LOG[ip] if now - t < WINDOW]

    if len(REQUEST_LOG[ip]) >= MAX_REQUESTS:
        return True

    REQUEST_LOG[ip].append(now)
    return False
