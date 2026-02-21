import argparse
import json
import os
import time
import urllib.request
import urllib.error

from utils import env_get, read_csv, write_csv, now_iso, is_valid_email
from render import render_template


def load_sequence(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_unsubscribes(path):
    items = set()
    for row in read_csv(path):
        email = row.get("email", "").lower().strip()
        if email:
            items.add(email)
    return items


def load_sent_log(path):
    sent = set()
    for row in read_csv(path):
        email = row.get("email", "").lower().strip()
        step = row.get("step", "").strip()
        if email and step:
            sent.add((email, step))
    return sent


def append_sent_log(path, rows):
    fieldnames = ["sent_at", "email", "step", "subject"]
    exists = os.path.exists(path)
    if exists:
        current = read_csv(path)
        current.extend(rows)
        write_csv(path, current, fieldnames)
    else:
        write_csv(path, rows, fieldnames)


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
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, ""
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", errors="ignore")
        except Exception:
            body = ""
        return e.code, body


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--leads", default="gtm/output/leads_clean.csv")
    parser.add_argument("--sequence", default="gtm/templates/sequence_es.json")
    parser.add_argument("--step", type=int, default=1)
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--sleep", type=float, default=0.4)
    parser.add_argument("--unsubscribe", default="gtm/output/unsubscribe.csv")
    parser.add_argument("--sent-log", default="gtm/logs/sent_log.csv")
    args = parser.parse_args()

    api_key = env_get("SENDGRID_API_KEY")
    from_email = env_get("FROM_EMAIL")
    agency_email = env_get("AGENCY_EMAIL")
    company_address = env_get("COMPANY_ADDRESS")

    if not api_key or not from_email:
        raise SystemExit("Missing SENDGRID_API_KEY or FROM_EMAIL in .env")

    seq = load_sequence(args.sequence)
    step_cfg = None
    for s in seq.get("steps", []):
        if int(s.get("step")) == args.step:
            step_cfg = s
            break
    if not step_cfg:
        raise SystemExit(f"Step {args.step} not found in sequence")

    leads = read_csv(args.leads)
    unsub = load_unsubscribes(args.unsubscribe)
    sent = load_sent_log(args.sent_log)

    send_rows = []
    sent_log_rows = []

    for row in leads:
        email = row.get("email", "").lower().strip()
        if not email:
            continue
        if email in unsub:
            continue
        if (email, str(args.step)) in sent:
            continue
        data = dict(row)
        data["company_address"] = company_address

        subject = render_template(step_cfg["subject"], data)
        body = render_template(step_cfg["body"], data)

        payload = {
            "personalizations": [{"to": [{"email": email}]}],
            "from": {"email": from_email, "name": seq.get("from_name", "Kultrip")},
            "subject": subject,
            "content": [{"type": "text/plain", "value": body}],
        }
        if agency_email and is_valid_email(agency_email.lower()):
            payload["reply_to"] = {"email": agency_email}

        send_rows.append((email, subject, payload))
        if len(send_rows) >= args.limit:
            break

    for email, subject, payload in send_rows:
        if args.dry_run:
            print(f"DRY RUN -> {email} :: {subject}")
        else:
            status, err = send_sendgrid(api_key, payload)
            if 200 <= int(status) < 300:
                print(f"SENT {status} -> {email}")
            else:
                print(f"ERROR {status} -> {email}")
                if err:
                    print(err)
                raise SystemExit(1)
            time.sleep(args.sleep)
        sent_log_rows.append({
            "sent_at": now_iso(),
            "email": email,
            "step": str(args.step),
            "subject": subject,
        })

    if sent_log_rows:
        append_sent_log(args.sent_log, sent_log_rows)
        print(f"logged {len(sent_log_rows)}")
    else:
        print("no leads to send")


if __name__ == "__main__":
    main()
