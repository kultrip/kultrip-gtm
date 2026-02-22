# kultrip-gtm

Cold email GTM tooling for Kultrip.

## Quick start
1. Ensure `.env` has `SENDGRID_API_KEY`, `FROM_EMAIL`, `AGENCY_EMAIL` and optionally `COMPANY_ADDRESS`.
2. Build the cleaned lead list (Spain + LATAM by default):
   - `python gtm/build_leads.py`
3. Preview an email:
   - `python gtm/preview.py --step 1 --index 0`
4. Dry run send (no emails sent):
   - `python gtm/send.py --step 1 --limit 5 --dry-run`
5. Send a small batch:
   - `python gtm/send.py --step 1 --limit 20`

## Files
- `gtm/build_leads.py`: cleans and dedupes lead spreadsheets
- `gtm/preview.py`: renders templates for a given lead
- `gtm/send.py`: sends a sequence step with SendGrid
- `gtm/templates/sequence_es.json`: Spanish email sequence
- `gtm/output/unsubscribe.csv`: suppression list (do not send)

## Notes
- Only send to business addresses and honor opt-outs.
- Start with low volume and ramp up after confirming deliverability.

## GitHub Actions automation
There is a workflow at `.github/workflows/gtm-send.yml` that sends Step 1 six times per day.
It sends a fixed batch size of 16 each run (96/day total).

Required GitHub Secrets:
- `SENDGRID_API_KEY`
- `FROM_EMAIL`
- `AGENCY_EMAIL`
- `COMPANY_ADDRESS`
- `SUMMARY_EMAIL` (optional; defaults to `AGENCY_EMAIL`)

Note: GitHub Actions schedules are UTC. The workflow is set to 01:00, 05:00, 09:00,
13:00, 17:00, 21:00 UTC (10:00, 14:00, 18:00, 22:00, 02:00, 06:00 in Spain during
standard time). In daylight saving time it will run one hour later locally.

There is also a daily summary workflow at `.github/workflows/gtm-summary.yml` that
sends a 24h summary to `SUMMARY_EMAIL` or `AGENCY_EMAIL` at 05:00 UTC (06:00 Spain
standard time).
