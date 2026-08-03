# kvc_theme — KaliVibeCoding CRM for Odoo 18

> KVC Neon-Noir design system applied to Odoo 18 backend, portal, and website.
> Programs · Cohorts · Students · GHL sync · Stripe billing · Cloudflare storage.

![KVC Logo](https://cdn.abacus.ai/images/134ce4b7-b0d1-4ba8-8655-3afd323fb646.png)

---

## What this addon does

Drops the KVC brand into every layer of Odoo 18:

**Design**
- Dark background `#1E1E24`, cards `#25252D`, pink `#FF69B4`, blue `#87CEEB`, gold `#FFD700`
- Lobster headings, Montserrat body, Fira Code for all code fields
- Custom scrollbars, selection highlight, focus rings, kanban stage color-coding

**Models**
- `kvc.program` — training program with NAICS, WIOA funding, pricing, GHL pipeline
- `kvc.cohort` — scheduled run of a program with seat management and status workflow
- `kvc.student` — enrollment record: progress, payment status, certificate, GHL/Stripe IDs

**Views**
- List, form, and kanban for programs, cohorts, and students
- Top-level "KVC CRM" menu item with sub-menus

**Portal**
- `/kvc/portal/dashboard` — student-facing enrollment dashboard with progress bars
- `/kvc/portal/enrollment/<id>` — per-enrollment detail with tech stack chips and meeting link

**Website**
- Hero section with Lobster gradient headline
- Programs grid page matching KVC Neon-Noir

**Integrations**
- `POST /kvc/webhook/ghl` — GoHighLevel contact sync (HMAC-verified)
- Stripe customer ID stored per student
- Cloudflare Account ID in `ir.config_parameter`

---

## Installation

```bash
# Place addon in your Odoo addons path
cp -r addons/kvc_theme /path/to/odoo/addons/

# Restart Odoo server
./odoo-bin -u kvc_theme -d your_database
```

## Config parameters (set in Technical → Parameters → System Parameters)

| Key | Value |
|-----|-------|
| `kvc.ghl_webhook_secret` | Your GHL webhook signing secret |
| `kvc.stripe_webhook_secret` | Your Stripe webhook secret |
| `kvc.cloudflare_account_id` | `9a3c0d0f1bc8bb5c83574905b6e13680` |

## Environment

Tested on Odoo 18.0 Community and Enterprise.

---

**RJ Business Solutions · KaliVibeCoding · kalivibecoding.com**
