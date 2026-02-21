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
