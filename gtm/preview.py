import argparse
import json

from render import render_template
from utils import read_csv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--leads", default="gtm/output/leads_clean.csv")
    parser.add_argument("--sequence", default="gtm/templates/sequence_es.json")
    parser.add_argument("--step", type=int, default=1)
    parser.add_argument("--index", type=int, default=0)
    args = parser.parse_args()

    leads = read_csv(args.leads)
    if not leads:
        raise SystemExit("no leads found; run build_leads.py first")
    row = leads[min(args.index, len(leads) - 1)]

    with open(args.sequence, "r", encoding="utf-8") as f:
        seq = json.load(f)
    step_cfg = None
    for s in seq.get("steps", []):
        if int(s.get("step")) == args.step:
            step_cfg = s
            break
    if not step_cfg:
        raise SystemExit(f"Step {args.step} not found")

    subject = render_template(step_cfg["subject"], row)
    body = render_template(step_cfg["body"], row)

    print("SUBJECT:")
    print(subject)
    print("\nBODY:\n")
    print(body)


if __name__ == "__main__":
    main()
