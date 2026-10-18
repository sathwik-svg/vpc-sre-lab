"""Check whether the VPC API health endpoint responds successfully."""

import json
import urllib.error
import urllib.request

URL = "http://127.0.0.1:8000/health"

try:
    with urllib.request.urlopen(URL, timeout=3) as response:
        if response.status != 200:
            raise SystemExit(1)

        payload = json.loads(response.read().decode("utf-8"))

        if payload.get("status") != "healthy":
            raise SystemExit(1)

except (urllib.error.URLError, TimeoutError, ValueError, OSError):
    raise SystemExit(1)

raise SystemExit(0)
