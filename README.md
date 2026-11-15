# Hop to Heal website

The website for Hop to Heal, a child development and counselling centre in Mayur Vihar Phase 1, Delhi.

**Status: preview.** All 16 pages work in the browser with example data. Sign-in, saved accounts and payments are not connected to a real service yet (see "Going live" below). Every page shows a "Preview site" bar and is hidden from search engines until launch.

Public link, once GitHub Pages is turned on: **https://acuteundauntedconstructive.github.io/new/**

## Folders

| Folder | What it is |
| --- | --- |
| `docs/` | **The website.** One `.html` file per page, plus `assets/` (shared code, styles, images). GitHub Pages publishes this folder. |
| `tools/build_site.py` | Re-imports the pages from the design boards. It overwrites `docs/*.html`, so only run it if the designs changed. |
| `hoptoheal/website-designs-2.0/` | The design boards the site was made from. |
| `hoptoheal/` | Business info, logo, photos, research paper and earlier designs. |

Pages: `index` (home), `services`, `counselling`, `hopcheck`, `hopcheck-parent`, `hopcheck-child`, `hopcheck-result`, `sign-in`, `book`, `pay`, `portal` (parent), `child`, `therapist`, `therapist-update`. Team-only pages: `question-bank`, `test-plan`.

## Turn on the public link (one time)

1. On GitHub open this repository, then **Settings → Pages**.
2. Under **Build and deployment**, set **Source** to **Deploy from a branch**.
3. Choose branch **`hoptoheal-website-research`** and folder **`/docs`**, then **Save**.
4. Wait about a minute and open the link above. Every later push to that branch updates the site by itself.

## Work on it in VS Code

1. Install [VS Code](https://code.visualstudio.com/) and [Git](https://git-scm.com/downloads).
2. In VS Code press `Ctrl+Shift+P`, choose **Git: Clone**, and paste `https://github.com/AcuteUndauntedConstructive/new.git`. Open the folder when asked.
3. Bottom-left of the window, click the branch name and pick `hoptoheal-website-research`.
4. Install the **Live Server** extension. Right-click `docs/index.html` → **Open with Live Server** to see the site on your computer. It reloads when you save.
5. To publish a change: **Source Control** panel (`Ctrl+Shift+G`) → type a message → **Commit** → **Sync Changes**.

## How a page is put together

Each page in `docs/` has three parts:

- `<style>` in the head: the look of that page.
- `<template id="view">`: the HTML. `{{name}}` is filled in from the script; `<sc-if>` shows a block only when a value is true; `<sc-for>` repeats a block for each item in a list.
- `<script>` at the bottom: a `Component` class. `renderVals()` returns the values the template uses, and `this.setState({...})` changes data and redraws the page.

`docs/assets/app.js` is the small engine that makes this work (about 200 lines, no other libraries). `docs/assets/site.css` holds shared and phone styles.

To change text, edit it in the template. To change prices, search for `800`, `9,600`, `500` and `8,400` across `docs/`.

## Going live with real accounts

The pages are ready; what is missing is the service behind them. Nothing below should be skipped before real families use the site, because it holds children's health information.

| Need | What for | Who sets it up |
| --- | --- | --- |
| Database + sign-in service (recommended: Supabase, Mumbai region) | Stores parents, children, sessions, progress, notes, reports and payments, and lets each parent see only their own family | Centre creates the project; project URL and public key go in the site code |
| Google sign-in | "Continue with Google" | A Google Cloud OAuth client, entered in the sign-in service's dashboard |
| Email + password sign-in | For parents without Google | Built into the sign-in service; needs a sender email address |
| Payment gateway (Razorpay) | UPI, cards and net banking, receipts, refunds | Centre's Razorpay account (needs business KYC). The secret key goes only in the server settings, never in this repository |
| WhatsApp / SMS provider (optional at first) | Reminders, Meet link 5 minutes before, phone OTP | An approved WhatsApp Business or SMS account |
| Legal pages | Privacy, Terms, Refund, Child safety, and parental consent wording | Centre, checked by a lawyer |
| Content still in [brackets] | Counsellor's name and registration, adult service prices, GST line, no-show rule | Centre |

Never put passwords or secret keys in this repository or in a chat. Public keys (the Supabase "anon" key, the Razorpay key ID) are safe in the site code; secret keys belong in the service dashboards.
