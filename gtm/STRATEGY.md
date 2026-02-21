# Kultrip GTM System (Cold Email)

## Goal
Convert travel agencies and tour operators into demos / trial signups for Kultrip by using a short, story-led cold email sequence.

## Assumptions
- Primary market: Spain / Spanish‑speaking agencies.
- Channel: cold email to business addresses (B2B).
- CTA: quick demo or trial activation on kultrip.com/register.

If any of these are wrong, we will adjust the sequence and segmentation.

## Target ICP
- Small to mid-size travel agencies and niche tour operators.
- Pain: low website conversion and low‑quality leads.
- Desire: differentiated, premium, story-driven experience.

## Offer
- Free trial: first 10 leads.
- Widget installs like a contact form.
- Traveler gets a story‑inspired guide; agency gets the qualified lead.

## Sequence
1. Step 1 (Day 0): introduce Kultrip + outcome + offer.
2. Step 2 (Day 3): show example of guide + lead; ask preference for delivery.
3. Step 3 (Day 8): polite close + ask to resume later.

## Compliance & Deliverability
- Only send to business addresses.
- Include a clear opt-out (reply \"unsubscribe\"). 
- Use a stable sender identity (from @kultrip.com).
- Keep daily volume low at first (20–50/day), ramp gradually.
- Consider a separate subdomain for cold email if volume increases.
- Provide a physical business address if you have one.

## Metrics
- Open rate, reply rate, demo rate, trial conversion.
- Track through UTM params to `/register` or via reply.

## Tools In This Repo
- `gtm/build_leads.py`: clean + dedupe lead lists
- `gtm/preview.py`: render email from template
- `gtm/send.py`: send via SendGrid (step‑based)
