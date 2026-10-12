"""Issue a local development token.

Usage: python scripts/make_token.py --sub researcher@example.org --studies ONC-101
"""

import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.auth import SECRET_KEY  # noqa: E402

parser = argparse.ArgumentParser()
parser.add_argument("--sub", required=True)
parser.add_argument("--studies", nargs="*", default=[])
args = parser.parse_args()

payload = {
    "sub": args.sub,
    "studies": args.studies,
    "exp": datetime.now(timezone.utc) + timedelta(hours=8),
}
print(jwt.encode(payload, SECRET_KEY, algorithm="HS256"))
