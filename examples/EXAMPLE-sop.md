---
type: sop
title: Approve an incoming invoice
created: 2026-01-15
tags: [finance, approval]
owner: office-management
status: stable
version: 1.2
valid_from: 2026-01-15
review_due: 2026-12-31
verified: {by: human:sam, at: 2026-01-15}
audience: [office-management, shift-lead, managing-director]
confidentiality: internal
---

<!-- DEMO CONTENT — style reference only, never copied into your vault.
     Company mode. The parts that make an SOP usable: numbered steps you
     could hand to a stand-in, a named exception path, and a change
     history. It is only binding because it has `status: stable` AND a
     `verified:` entry — a draft describes an intention, not the rule. -->

# Approve an incoming invoice

## Purpose
Every invoice is checked by someone who did NOT order the goods, so a
wrong or duplicated invoice is caught before it is paid. Without this
step we have twice paid the same delivery.

## Scope
All incoming supplier invoices, paper and email, any amount. Does NOT
cover: staff expense claims (own procedure), recurring direct debits
(reviewed once a year), and anything from a partner not yet listed in
`80-partners/` — those go to office management first.

## Roles
| Role | Does what |
|---|---|
| office-management | Receives, checks formally, books it |
| shift-lead | Confirms the goods actually arrived |
| managing-director | Approves anything above EUR 2,000 |

## Procedure
1. Scan or save the invoice into the finance drive, folder
   `incoming/<year>/<month>/`, file name `<supplier>-<invoice-no>.pdf`.
2. Check formally: supplier, invoice number, date, VAT number, our
   address, bank details. Bank details differ from last time? Stop —
   exception path below.
3. Match against the delivery note. No delivery note? Ask the shift-lead
   to confirm receipt in writing (email is enough) before going on.
4. Amount up to EUR 2,000: office management approves and books.
5. Amount above EUR 2,000: forward to the managing director with the
   delivery note attached; book only after written approval.
6. Enter the payment with the payment term from the invoice — never
   earlier, never on the day it arrives.
7. File the approval (email or signature) with the invoice PDF.

## Exceptions
- **Bank details changed** → do not pay. Call the supplier on the number
  in `80-partners/`, never on a number written in the invoice. This is
  the standard payment-diversion fraud pattern.
- **Invoice without an order** → office management clarifies with the
  requesting role before any approval.
- **Deadline pressure from the supplier** → never a reason to skip a
  step; the managing director decides on late-payment fees.
- Nothing fits? Stop and ask office management. Do not improvise in
  silence.

## Change history
| Version | Date | Change | By |
|---|---|---|---|
| 1.2 | 2026-01-15 | Bank-detail check made an explicit stop condition | sam |
| 1.1 | 2025-09-02 | Approval limit raised from EUR 1,000 to EUR 2,000 | sam |
| 1.0 | 2025-03-11 | First version | sam |
