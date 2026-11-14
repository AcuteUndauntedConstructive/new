# Mascot chatbot widget: spec for Claude Code

A floating website chatbot whose launcher is an animated mascot: an orange
egg-shaped character with three sun rays above its head, closed happy eyes,
pink cheeks and a small "w" mouth. It sways gently in the bottom-right corner,
reacts to hover, opens a chat panel on click, and answers questions about the
business's services.

Plain HTML, CSS and JavaScript. No framework, no build step, no dependencies.

## Files

| File | Role |
|---|---|
| `mascot.css` | All styles and every animation. Motion values are CSS custom properties (tokens) at the top of `.mb-root`. |
| `mascot.js` | Builds the widget DOM (including the mascot SVG), runs the state machine, answers questions. Exposes `window.MascotChat`. |
| `index.html` | Demo page showing how to include and configure the widget. |
| `CLAUDE.md` | This file. |

## Add it to a page

```html
<link rel="stylesheet" href="mascot.css">
<script src="mascot.js"></script>
<script>
  MascotChat.init({ name: "Sunny", topics: [ /* see Config */ ] });
</script>
```

Public API after `init`: `MascotChat.open()`, `MascotChat.close()`,
`MascotChat.ask("question text")`.

## Rules when editing

1. All class names start with `mb-` so the widget never clashes with the host site. Keep that prefix.
2. Change motion by editing the tokens in `mascot.css`, not by hard-coding numbers inside keyframes.
3. Visual state is driven only by `data-state` on `.mb-root`. JS calls `setState()`; CSS reacts. Do not toggle visibility classes on child elements from JS.
4. Never put user or bot text into the DOM with `innerHTML`. Use `textContent`.
5. Keep the `prefers-reduced-motion` block. It turns every animation off for users who ask for less motion.
6. Keep the three motion wrappers (`.mb-tilt > .mb-sway > .mb-bob`) separate. Merging them makes the animations overwrite each other's `transform`.

---

## 1. The mascot artwork

SVG, `viewBox="0 0 200 200"`. Built as a string in `mascot.js` (`MASCOT_SVG`).

| Part | Class | Shape | Colour |
|---|---|---|---|
| Left ray | `.mb-ray--left` | rounded rect 12×28, at (41,50), rotated −52° | `#F9A726` |
| Middle ray | `.mb-ray--middle` | rounded rect 12×32, at (100,24), upright | `#F9A726` |
| Right ray | `.mb-ray--right` | rounded rect 12×28, at (159,50), rotated +52° | `#F9A726` |
| Body | `.mb-body` | egg path: narrow rounded top at y=58, wider bottom at y=182, x from 51 to 149 | `#F9A726` |
| Cheeks | `.mb-cheek` | ellipses 17×10.4 at (72,119) and (128,119), 85% opacity | `#F4743B` |
| Closed eyes | `.mb-eyes-closed` | two downward arcs (smiling-closed) centred at x=82 and x=118, y=108 | stroke `#3B2314` |
| Open eyes | `.mb-eyes-open` > `.mb-eye` | two dark ovals with a small white highlight, same positions | `#3B2314` + white |
| Mouth | `.mb-mouth` | small "w" from (93,120) to (107,120) | stroke `#3B2314` |

Each ray has an outer `<g>` that positions and angles it, and an inner `<rect>`
that animates. That way the pulse scales along the ray's own length.

**Pivot point:** the bottom of the body is at y=182 of 200, so all body motion
pivots at `transform-origin: 50% 92%`. The mascot rocks as if standing on the
spot, rather than spinning around its middle.

## 2. Movement layers

Three nested wrappers inside the launcher button, each owning one kind of motion.
Their transforms multiply together.

```
.mb-launcher (button, 92×92 px; 76×76 on phones)
  └─ .mb-tilt   hover / press reaction    (CSS transition)
      └─ .mb-sway   side-to-side rocking  (infinite animation)
          └─ .mb-bob    float + squash    (infinite animation)
              └─ <svg>  rays pulse; eyes swap and blink (per-part animations)
```

| Layer | What it does | Keyframes | Default timing |
|---|---|---|---|
| Sway | Rotates from −5° to +5° and back | `mb-sway` | 3.4 s, ease-in-out, infinite |
| Bob | Rises 3 px, squashes slightly (scaleX .985, scaleY 1.02) | `mb-bob` | 1.7 s (two bobs per sway) |
| Rays | Each ray shrinks to 55% length and 70% opacity, then returns | `mb-ray` | 2.4 s; left, middle, right start .25 s apart, so the pulse travels across |
| Blink | Open eyes squash to 10% height for a moment | `mb-blink` | once every 4.5 s (only when open) |
| Hover / focus | Leans −9°, lifts 4 px, grows to 105% | transition | .35 s spring curve `cubic-bezier(.34,1.56,.64,1)` (slight overshoot) |
| Press | Shrinks to 94% | transition | same spring |

### Motion tokens (top of `mascot.css`)

| Token | Default | Effect |
|---|---|---|
| `--mb-sway-angle` | `5deg` | How far it swings each way |
| `--mb-sway-duration` | `3.4s` | Speed of one full swing |
| `--mb-bob-height` | `3px` | How high it floats |
| `--mb-bob-duration` | `1.7s` | Speed of the float |
| `--mb-ray-duration` | `2.4s` | Ray pulse cycle |
| `--mb-ray-stagger` | `.25s` | Gap between each ray's pulse |
| `--mb-ray-min-scale` | `.55` | How short a ray gets at its dip |
| `--mb-hover-tilt` | `-9deg` | Lean on hover |
| `--mb-hover-lift` | `4px` | Lift on hover |
| `--mb-hover-scale` | `1.05` | Grow on hover |
| `--mb-press-scale` | `.94` | Shrink on press |
| `--mb-open-sway-duration` | `5s` | Calmer sway while the chat is open |
| `--mb-blink-duration` | `4.5s` | Time between blinks |
| `--mb-think-ray-duration` | `.6s` | Fast ray flicker while thinking |
| `--mb-think-bob-duration` | `.5s` | Quick hops while thinking |

Examples: "make it swing more" → raise `--mb-sway-angle` to `8deg`.
"Make it calmer" → raise `--mb-sway-duration` to `5s` and lower `--mb-bob-height` to `2px`.

## 3. States

`mascot.js` sets `data-state` on `.mb-root`. The CSS reacts.

| State | When | Mascot | Panel |
|---|---|---|---|
| `closed` | Page load; after close | Idle sway 3.4 s, bob, ray pulse, eyes closed | Hidden |
| `open` | Mascot clicked | Eyes open and blink, sway slows to 5 s | Visible, input focused |
| `thinking` | A question was sent and the answer is pending | As open, plus rays flicker every .6 s and it hops every .5 s | Visible, typing dots shown |

```
           click mascot / MascotChat.open()
 closed ─────────────────────────────────────▶ open
   ▲                                           │  ▲
   │ click mascot / × / Esc                    │  │ answer arrives
   └───────────────────────────────────────────┘  │
                                   send question  ▼
                                               thinking
```

A second flag, `data-teaser="on" | "off"`, controls the speech bubble beside
the closed mascot: it turns on 2.2 s after load and off at 9 s, or as soon as
the chat opens.

## 4. Chat panel interface

```
┌──────────────────────────────────┐
│ [mini mascot] Sunny          [×] │  header, mint #EEF6EA
│               Ask about what…    │
├──────────────────────────────────┤
│ ┌───────────────────┐            │  bot bubble: mint, left,
│ │ Hi, I'm Sunny! …  │            │  tail bottom-left
│ └───────────────────┘            │
│            ┌──────────────────┐  │  user bubble: mango, right,
│            │ What we offer    │  │  tail bottom-right
│            └──────────────────┘  │
│ ┌─────┐                          │  typing: 3 bouncing dots
│ │ ••• │                          │
│ └─────┘                          │
├──────────────────────────────────┤
│ (What we offer) (Pricing)        │  topic chips: pill, mango outline
│ (Timings) (Contact us)           │
├──────────────────────────────────┤
│ ( Type your question       ) (➜) │  input pill + dark round send
└──────────────────────────────────┘
                              [mascot]
```

- Size 340 × 460 px, capped at screen width − 24 px and screen height − 150 px.
- Corners 26 px, except bottom-right at 8 px, so the panel visually "points" at the mascot below it.
- **Open animation:** grows from the bottom-right corner, from 94% scale and 14 px lower, with a springy .28 s curve. Closing reverses it, then `visibility: hidden` takes it out of the tab order.
- **New message:** each bubble pops in (fade up 6 px, from 96% scale, .25 s).
- **Typing dots:** each dot jumps 5 px; the three are .15 s apart.
- Bot answers support line breaks: `\n` in an answer becomes a new line.

### Colour tokens

| Token | Hex | Used for |
|---|---|---|
| `--mb-mango` | `#F9A726` | Mascot, rays, user bubbles, chip outlines |
| `--mb-mango-deep` | `#E58E00` | Typing dots, input focus ring |
| `--mb-blush` | `#F4743B` | Cheeks |
| `--mb-ink` | `#3B2314` | Face lines, all text, send button |
| `--mb-mint` | `#EEF6EA` | Panel header, bot bubbles |
| `--mb-white` | `#FFFFFF` | Panel, chips, input |

Font: Baloo 2 (500, 700) from Google Fonts, falling back to Nunito, Trebuchet MS, system-ui.

## 5. Config (`MascotChat.init({...})`)

| Key | Type | Default | Meaning |
|---|---|---|---|
| `name` | string | `"Sunny"` | Shown in the panel header |
| `subtitle` | string | `"Ask about what we offer"` | Line under the name |
| `teaser` | string | `"Hi! Need a hand?"` | Bubble beside the closed mascot |
| `teaserShowAfterMs` / `teaserHideAfterMs` | number | `2200` / `9000` | Teaser timing |
| `greeting` | string | | First bot message when the chat first opens |
| `fallback` | string | | Reply when nothing matches |
| `thinkingMs` | number | `750` | Fake "thinking" delay for built-in answers |
| `topics` | array | 4 placeholders | `{ label, keywords[], answer }`. Each becomes a chip; typed text matching the label or any keyword returns `answer`. |
| `getReply` | function | `null` | Optional `(text, history) => Promise<string>` to plug in a real AI or backend. `history` is `[{ role: "user"|"bot", text }]`. Chip clicks still use the fixed `answer`. If it throws, the built-in matching is used. |

### Connecting a backend

Never put an API key in this front-end code. Call your own server endpoint:

```js
MascotChat.init({
  topics: [ /* ... */ ],
  getReply: async (text, history) => {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, history })
    });
    const data = await res.json();
    return data.reply;
  }
});
```

## 6. Accessibility and responsive

- The mascot is a real `<button>` with `aria-expanded` and `aria-controls`; its label switches between "Open chat" and "Close chat".
- The panel is `role="dialog"` with `aria-hidden` kept in sync; the message log is `aria-live="polite"` so screen readers announce replies.
- `Esc` closes the panel and returns focus to the mascot. All buttons show a visible focus outline.
- Under 480 px wide: mascot shrinks to 76 px and sits 12 px from the corner.
- `prefers-reduced-motion: reduce` switches off every animation and transition.

## 7. Ideas for later

- Wave a ray or tilt toward the cursor when it comes near (pointer tracking on `.mb-tilt`).
- A one-time "hello" hop on first load (a separate keyframe on `.mb-bob`, run once).
- Save the chat in `sessionStorage` so it survives page changes.
- Hide the teaser for returning visitors.
