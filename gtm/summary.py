import argparse
import csv
import json
import os
from datetime import datetime, timedelta, timezone
import urllib.request

from utils import env_get


def read_sent_log(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_iso(ts):
    try:
        return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except Exception:
        return None


def send_sendgrid(api_key, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.sendgrid.com/v3/mail/send",
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return resp.status


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sent-log", default="gtm/logs/sent_log.csv")
    parser.add_argument("--hours", type=int, default=24)
    args = parser.parse_args()

    api_key = env_get("SENDGRID_API_KEY")
    from_email = env_get("FROM_EMAIL")
    to_email = env_get("SUMMARY_EMAIL") or env_get("AGENCY_EMAIL")

    if not api_key or not from_email or not to_email:
        raise SystemExit("Missing SENDGRID_API_KEY, FROM_EMAIL, or SUMMARY_EMAIL/AGENCY_EMAIL")

    now = datetime.now(timezone.utc)
    window_start = now - timedelta(hours=args.hours)

    rows = read_sent_log(args.sent_log)
    recent = []
    for r in rows:
        ts = parse_iso(r.get("sent_at", ""))
        if ts and ts >= window_start:
            recent.append(r)

    total = len(recent)
    by_step = {}
    for r in recent:
        step = r.get("step", "") or "?"
        by_step[step] = by_step.get(step, 0) + 1

    last_items = recent[-20:]

    lines = []
    lines.append(f"Kultrip daily summary (last {args.hours}h, UTC)")
    lines.append("")
    lines.append(f"Total sent: {total}")
    if by_step:
        lines.append("By step:")
        for step, count in sorted(by_step.items()):
            lines.append(f"- Step {step}: {count}")
    lines.append("")
    lines.append("Last sends:")
    if last_items:
        for r in last_items:
            lines.append(f"- {r.get('sent_at','')} | step {r.get('step','')} | {r.get('email','')} | {r.get('subject','')}")
    else:
        lines.append("- None")

    body = "\n".join(lines)

    payload = {
        "personalizations": [{"to": [{"email": to_email}]}],
        "from": {"email": from_email, "name": "Kultrip"},
        "subject": "Kultrip daily summary",
        "content": [{"type": "text/plain", "value": body}],
    }

    status = send_sendgrid(api_key, payload)
    print(f"SENT {status} -> {to_email}")


if __name__ == "__main__":
    main()
