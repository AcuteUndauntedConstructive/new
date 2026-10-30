# Hop to Heal: New Website Blueprint (draft v1)

Based on the report, financial model, innovation deck and the search-indexed site.
Will be refined once the remaining data arrives.

---

## 1. Guiding principles (parent-friendly)

| Principle | What it means on the site |
|---|---|
| Mobile first | Most parents browse on a phone, often a budget Android on 4G. Pages must load in under 2.5 s. |
| Hindi + English | A language toggle at the top. Chatbot, booking and HopCheck work in both. |
| Plain words, no jargon | "Speech therapy: helps your child talk and understand" instead of "SLP intervention". |
| Reassure, never alarm | Tone: "Many children need a little help. You're in the right place." Screening is not diagnosis. |
| WhatsApp everywhere | A floating WhatsApp button. Confirmations, reminders and payment links arrive on WhatsApp. |
| Show real people | Therapist faces, qualifications, registration numbers, real centre photos. |
| Prices visible | No "call for price". Show the per-session fee, packages and sponsored-slot option. |
| Sensory-safe | A "Calm mode" toggle turns off animation and sound and softens colours. Many visiting children (and parents) are sensory-sensitive. Respect `prefers-reduced-motion`. |
| Accessible | WCAG 2.2 AA contrast, 48 px tap targets, readable 18 px body text. |

Brand tokens from the logo: mint `#F2F8EE` (background), sun `#FBA826`, blush `#F46A39`, ink `#352724`.

---

## 2. How many pages, and what each does

**Recommended: 11 main pages + 4 legal pages = 15.** Launch with the 8 marked MVP; add the rest in phase 2.

| # | Page | Purpose | MVP? |
|---|---|---|---|
| 1 | **Home** | Hero with the animated logo ("Hoppy" the sun). One line: what we do and for whom. Two buttons: *Book a first visit* and *Free 10-min HopCheck*. Trust strip: 5.0★ Google, 400+ children, open 7 days, founder credentials. Services grid, a "how it works" 4-step path, reviews and a map. | ✅ |
| 2 | **Services** (+ one sub-page per service) | Occupational therapy & sensory integration, speech therapy, early intervention, special education, behaviour & ABA, counselling, group therapy & school readiness, parent training. Each page answers: *signs your child may need this*, *what a session looks like*, *how long*, *price*, and gives a Book button. | ✅ |
| 3 | **HopCheck** (free screener) | A 10-minute questionnaire for parents, adding voice and camera tasks later. Ends with a traffic-light result (green/amber/red), an OT review promise and a booking button. Consent first. | ✅ (questionnaire only) |
| 4 | **Book a Visit** | The booking flow (section 4). | ✅ |
| 5 | **Pay** | The payment page (section 3). | ✅ |
| 6 | **Our Centres** | Hub-1 Mayur Vihar Ph-1 (address, landmark, map, hours, photos, parking). Hub-2 "Coming April 2027: join the waitlist". | ✅ |
| 7 | **Our Team** | Dr. Heena Gupta and the therapists: photo, qualifications, specialities, a short "why I do this" line. | ✅ |
| 8 | **Contact** | WhatsApp, call, email, map, hours, a callback-request form. | ✅ |
| 9 | **Parent Corner** | FAQs, a "What to expect on the first visit" guide, home activity ideas, blog and Instagram reels. Good for search traffic. | Phase 2 |
| 10 | **Stories & Reviews** | Parent testimonials (with consent), Google reviews and before/after milestones without identifying children. | Phase 2 |
| 11 | **Parent Portal** (login by WhatsApp OTP) | Upcoming sessions, reschedule, invoices, progress reports, home-activity plan and HopCheck history. | Phase 2 |
| 12–15 | **Privacy Policy, Terms, Refund & Cancellation, Child Safety & Consent** | Required by payment gateways (Razorpay/Cashfree check for these before activating your account) and by the DPDP Act 2023 for children's data. | ✅ |

Optional later: **For Schools** (book a screening camp, CSR partnerships), **Careers** (therapist hiring), **Hop Home Kit shop**.

---

## 3. Payment page: what it should include

**Goal: pay in under 30 seconds, from a WhatsApp link, without creating an account.**

### Layout (single screen on mobile)
1. **What are you paying for?** Big tappable cards:
   - First assessment (₹ to be set by the clinic)
   - Single session: **₹800**
   - Monthly package: 8 sessions (show the saving against single sessions)
   - Pay a pending invoice (enter the phone number and outstanding dues appear)
   - Hop Home Kit (phase 2)
2. **Child & parent:** child's first name, parent's WhatsApp number. These fields are pre-filled when the parent arrives from a booking or WhatsApp link.
3. **Centre:** Mayur Vihar Ph-1 or Hub-2.
4. **Amount summary:** a clear total, with no hidden fees. Ask your CA whether GST applies; health-care services by clinical establishments are often exempt. Add a coupon or sponsored-slot code field.
5. **Pay with:** **UPI first** (GPay, PhonePe or Paytm opens directly on mobile; a QR code on desktop), then cards, net-banking and wallets.
6. **Pay at centre** option for the first visit, so new families aren't scared off.
7. Trust row: secure-payment badge, refund policy link and a "Questions? WhatsApp us" link.

### After payment
- A success screen where Hoppy celebrates
- An instant **WhatsApp and email receipt** with a PDF invoice
- An "Add to calendar" button and a "What to bring" checklist
- A reschedule link

### Behind the scenes
- Gateway: **Cashfree** (assumed in the report: 1.95% + GST) or Razorpay. Both support UPI, payment links and **UPI Autopay** for monthly packages.
- Webhook updates the CRM and marks the booking paid. Failed payments trigger a retry link on WhatsApp.
- Sponsored slots: CSR-funded codes that zero the amount, for low-income families (planned in the report).

---

## 4. Onboarding / booking flow (friendly for parent and child)

One question per screen, with big buttons and Hoppy hopping along a progress path. It takes about 2 minutes.

| Step | Screen | Notes |
|---|---|---|
| 1 | **"Who are we helping today?"** Child's first name + age (tap an age bubble: 1, 2, 3 … 12) | The rest of the flow uses the child's name: "Let's find the right help for Aarav." |
| 2 | **"What have you noticed?"** Tap any: *not talking much yet · doesn't respond to name · clumsy / falls often · upset by noise or touch · hard to sit still · tantrums · handwriting / school trouble · picky eating · not sure, just want a check-up* | Plain-language chips that never name a diagnosis. Answers pre-fill the therapist's intake. |
| 3 | **Recommendation:** "We suggest a First Assessment with an occupational therapist" (or the free HopCheck if they're unsure) | Explain what happens and how long it takes. |
| 4 | **Pick a centre, day and time.** Slot calendar with weekend slots highlighted, since the centre is open 7 days. Show the therapist's photo. | Shows only real free slots from the clinic calendar. |
| 5 | **Parent details:** name, WhatsApp number (OTP verify), preferred language | Ask for nothing else yet. |
| 6 | **Consent:** two simple checkboxes (data use for therapy; WhatsApp updates) | DPDP verifiable parental consent. |
| 7 | **Pay now or pay at the centre** | Goes to the Pay page with everything pre-filled. |
| 8 | **Done!** Hoppy celebrates. WhatsApp confirmation sent. | Includes the items below. |

**What happens after booking (this is where children benefit most):**
- **"My visit to Hop to Heal" picture story.** A 6-panel visual story (the building, the door, the play room, the therapist's smiling photo, the swing, going home with a sticker) for parents to show the child beforehand. This kind of picture story eases anxiety for autistic and sensory-sensitive children.
- A **map + landmark** ("near Mother Dairy & Safal outlet"), plus parking and lift info.
- **Reminders:** WhatsApp 24 h and 2 h before, with one-tap reschedule.
- After the first visit: an assessment summary, therapy plan, package offer and home activities.
- **Hop Passport** for the child: one sticker or badge per session in the portal, with a printable sticker sheet at the centre. Hoppy "hops" one step further on the child's path each week.

---

## 5. How the website interacts with customers

| Channel | Role |
|---|---|
| **Hoppy chatbot** (the animated "o") | Answers FAQs (fees, timings, location, what OT is), guides booking, runs the HopCheck intake and collects callback requests. Bilingual. Hands over to a human on WhatsApp when unsure. |
| **WhatsApp Business API** (e.g., Interakt, WATI or Meta Cloud API) | Booking confirmations, reminders, payment links, receipts, monthly progress summaries and re-screen nudges every 3 months. |
| **CRM** | Every lead (chatbot, HopCheck, form, call) becomes a record with a status: new → screened → booked → in therapy → renewed. Therapists see the intake before the first visit. |
| **Parent Portal** | Self-service for rescheduling, invoices, reports and home activities. Cuts calls to the coordinator. |
| **Review loop** | After the 3rd session, a WhatsApp message asks happy parents for a Google review. This builds on the 5.0★ rating. |
| **Instagram feed** | Embedded reels on Home and Parent Corner, with a "Follow for daily activity ideas" prompt. |

**Chatbot guardrails (must have):**
- Never diagnoses. Always says "screening, not diagnosis; a therapist will review".
- Escalates immediately for safety concerns, regression or medical red flags ("please consult your paediatrician / call us").
- Answers only from approved clinic content (FAQ, services, prices, policies).
- Stores no child data without consent. Shows a privacy note in the first message.
- Offers a "Talk to a person" button at all times.

Suggested build: an LLM (e.g., a fast, low-cost Claude model) restricted to the clinic's FAQ and policy documents, with booking and slot lookup exposed as tools.

---

## 6. Hoppy: animating the "o" in "Hop"

**Concept:** On page load, the logo sits in the hero. The sun-"o" opens its eyes, blinks, and its rays twinkle. When the parent scrolls, Hoppy **hops out of the word "Hop"** (leaving a soft outline behind), bounces down to the bottom-right corner and becomes the chat button. Tap it and Hoppy greets the parent: "Hi! I'm Hoppy. How can I help your little one today?"

**Recommended tech: Rive** (a 2D, vector, state-machine animation tool for the web)
- Tiny files (~50–150 KB), smooth at 60 fps on budget phones, and it matches the flat logo style.
- Its state machine maps directly to chatbot states.
- A **3D anime model** (three.js + VRM) is possible but costs 5–20 MB, drains batteries on low-end phones and clashes with the flat logo. Keep 3D for a later campaign if wanted.
- Lottie works for one-off animations but is weaker for interactive states.

**Hoppy's animation states (looping idle + triggered reactions):**

| State | Trigger | Motion |
|---|---|---|
| Idle loop | Always | Gentle breathing squash-and-stretch, rays slowly pulse, a blink every 3–6 s |
| Look | Cursor or finger moves | Eyes follow the pointer |
| Hop | Hover, scroll or tap | A little bounce with a squash on landing |
| Wave / greet | Chat opens | Ray "arm" waves, cheeks glow |
| Listening | Parent is typing | Leans in, eyes open wide |
| Thinking | Bot is replying | Rays rotate slowly like a loader |
| Talking | Bot message appears | Mouth opens and closes in sync with the text |
| Celebrate | Booking or payment success | Big hop + confetti of tiny suns |
| Sleepy | Outside 10 am–7 pm | Eyes droop, a "Zzz": "We're closed; leave a message and we'll reply at 10 am!" |
| Oops | Error | Tilts head, small "?" |
| Calm mode | Toggle / reduced-motion | Static, smiling, no motion |

Deliverables for the animator: the logo as SVG with the sun-"o" as separate layers (face, eyes, mouth, cheeks, 3 rays). The current file is a flat PNG on a mint background, so it needs vectorising first.

---

## 7. Which animations are worth it

**Worth it (adds meaning or guides action):**
- Hoppy mascot: brand recognition and the chatbot entry point
- Hoppy hopping along the booking progress bar, which makes a form feel like a game
- Celebrate on booking/payment success, a moment of relief for parents
- Soft "hop" bounce on primary buttons (small, about 150 ms)
- Count-up stats (400+ children, 5.0★) when scrolled into view
- The 6-step HopCheck journey path drawing itself on scroll
- Gentle fade-up of service cards

**Not worth it (slows the site, hurts sensory-sensitive visitors, hurts SEO):**
- Auto-rotating carousels and sliders
- Heavy parallax and scroll-jacking
- Auto-playing video with sound
- Intro/splash loading animations
- Flashing, fast-moving or high-contrast blinking effects
- 3D scenes on every page

Rule of thumb: every animation either **guides the next action**, **gives feedback**, or **is Hoppy**. Anything else gets cut.

---

## 8. Suggested tech stack

| Layer | Choice |
|---|---|
| Framework | Next.js + Tailwind CSS (fast, SEO-friendly, easy Hindi/English routing) |
| Mascot | Rive (`@rive-app/react-canvas`) |
| Booking | Cal.com (open source; supports multiple therapists, centres and WhatsApp reminders) or custom with Supabase |
| Payments | Cashfree or Razorpay (UPI, payment links, UPI Autopay) |
| WhatsApp | Interakt / WATI / Meta Cloud API |
| CRM | Zoho CRM or HubSpot free tier, or a Supabase dashboard for the MVP |
| Chatbot | LLM with retrieval over approved FAQ content, plus booking tools |
| Hosting | Vercel (Mumbai edge) |
| Analytics | GA4 + Microsoft Clarity (privacy-respecting configuration) |

Fits the ₹3,00,000 digital-front-door budget and the ~8-week build window in the report.
