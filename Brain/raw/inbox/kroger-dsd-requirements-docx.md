---
date: 2026-04-22
type: raw
source: /Users/gclyle/secure/Kroger DSD requirements.docx
tags: [secure, secure, loss-prevention, retail]
project: secure
status: unprocessed
---

# Kroger DSD requirements.docx

## Source
File: `/Users/gclyle/secure/Kroger DSD requirements.docx`
Size: 1,835 bytes

## Raw content
| DSD ID | DSD Integration Requirement | Priority  (H,M,L) | Business Comments |
| --- | --- | --- | --- |
| DSD1 | * Duplicate Invoice Payments   + Data lives in VPS   + By Vendor   + Should look for similar invoice #s by vendor   + Should look for repayments on same invoice # | H |  |
| DSD2 | * Product Cost Errors (Paying wrong cost)   + Data starts in DSD Host, flows to Chain Track   + Short Pays (leads to repayment request)   + Chaintrack Vendor Cost vs. Kroger Cost   + Receiver scan pulls in only Kroger cost, not necessarily the lower cost | H |  |
| DSD3 | * Vendor Over-Delivered/ Under-Delivered Analysis   + Data lives in Chaintrack, IPI, KCMS   + Min/Max varies by vendor and product type | H |  |
| DSD4 | * Vendor Missing/Zero Credits   + Data lives in Chaintrack   + Frequency varies by vendor and product type (Weekly/Monthly) | H |  |
| DSD5 | * Credits as a % of Sales   + Data lives in Chaintrack | H |  |
| DSD6 | * Promo Allowance (Product delivered outside of promo window)   + Data lives in Chaintrack and DSD Host   + Large deliveries before and after promotion | H |  |
| DSD7 | * Vendor Violations   + Data lives in Chaintrack     - Dependent on store receiver input   + Rodney Tarleton has a list of violations | H |  |
| DSD8 | * The system shall contain 9 consecutive Kroger fiscal quarters of DSD data.   + All DSD Vendors   + All DSD Items   + Required for Year over Year comparison   + Could be a weekly feed   + Not much value with real time | H |  |
| DSD9 | * Credits ran as deliveries   + Data lives in Chaintrack   + Kroger paying for items that should be a credit back to Kroger | H |  |
| DSD10 | * Inventory Results   + Data lives in IRS   + Physical inventory for DSD items/ vendors | H |  |
| DSD11 | * Receiver Information   + Data lives in Chaintrack   + Receiver Name/ User ID | H |  |

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
