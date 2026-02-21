import csv
import os
import re
from datetime import datetime

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def load_dotenv(path=".env"):
    env = {}
    if not os.path.exists(path):
        return env
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            env[key.strip()] = value.strip()
    return env


def env_get(key, default="", dotenv_path=".env"):
    if key in os.environ:
        return os.environ.get(key, default)
    env = load_dotenv(dotenv_path)
    return env.get(key, default)


def normalize_cell(value):
    if value is None:
        return ""
    if isinstance(value, str):
        v = value.strip()
        if v.upper() == "[BLANK]":
            return ""
        return v
    return str(value).strip()


def normalize_email(email):
    return normalize_cell(email).lower()


def is_valid_email(email):
    if not email:
        return False
    return EMAIL_RE.match(email) is not None


def write_csv(path, rows, fieldnames):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def now_iso():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
