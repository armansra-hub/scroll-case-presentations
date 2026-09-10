# Scroll-Driven Case Presentations

Two sales case studies rebuilt as **interactive websites instead of slide decks**, to be
presented live off a laptop. One is a 3D alpine descent rendered in Three.js; the other is
an 8-bit pixel RPG climb with branching paths. Each is a **single self-contained HTML file** —
no build step, no framework, no bundler.

**▶ Live demos:** https://armansra-hub.github.io/scroll-case-presentations/

| File | Scenario | Driven by |
| --- | --- | --- |
| [`summit-commerce-click.html`](summit-commerce-click.html) | 1 — Summit Commerce | **Next/Back buttons + clicker keys** (the presenter build) |
| [`summit-commerce.html`](summit-commerce.html) | 1 — Summit Commerce | Mouse wheel / virtual scroll |
| [`horizon-retail.html`](horizon-retail.html) | 2 — Horizon Retail Group | Mouse wheel, with click-driven branch choices |

---

## Why these exist

These were built for **live sales-case interviews**. The brief for each scenario arrived as
a PDF of prospect research and a recommended plan of attack — the kind of thing that
normally becomes a twelve-slide deck that the interviewer half-reads while you talk over it.

A deck has two problems in that room. It makes the argument *sequential but inert* — every
slide looks like every other slide, so nothing signals which beat matters. And it puts the
strongest evidence of how you think (the reasoning between the bullets) in your voice only,
where it evaporates.

So instead each scenario became a **journey you travel**. The case narrative maps onto
physical progress across a mountain — Scenario 1 descends from the summit to the first
draw, Scenario 2 climbs from the gate to sunrise. Each analytical beat is a *station* you
arrive at, the
popup text is the argument at that station, and the terrain between stations does the work
that transitions normally can't — it makes the sequence feel earned rather than clicked
through. Scenario 2 goes further and makes the prospect's decision points into **literal
forks in the path**, where the branch you choose changes the route you walk.

The point wasn't decoration. It was to make the structure of the argument legible at a
glance, and to demonstrate — without saying so — that I'll build the thing rather than
describe it.

---

## The hard constraint: text is verbatim

The case copy in every popup is **word-for-word from the source brief**. Formatting could
change; wording could not. That rule mattered enough to automate, because it is exactly the
kind of thing that quietly rots as you restyle a page for the fifth time.

`tools/` holds a re-runnable checker per scenario. Each one holds the source strings, pulls
the rendered text back out of the HTML, normalizes whitespace and typographic quotes, and
diffs. It exits loudly if a single word drifted:

```bash
python3 tools/verify_text.py                            # summit-commerce.html
python3 tools/verify_text.py summit-commerce-click.html # the presenter build
python3 tools/verify_text_horizon.py                    # horizon-retail.html
```

```
OK   [pos] 3 lines verified
OK   [draw] 39 lines verified
OK   [bubble] verified

ALL TEXT VERBATIM ✔
```

All three builds pass as committed.

---

## Scenario 1 — Summit Commerce

A dark, clinical, minimal aesthetic — midnight navy `#05070f`, a single cyan accent
`#5ee6ff`, thin hairlines, no ornament. A skier **descends** a Three.js mountain
(`three@0.161.0`, loaded via import map — there is no npm install anywhere in this repo),
stopping at each station where the corresponding argument appears. The framing is the deal
itself: *from approval email to first draw*, summit down to the base.

It ships in **two builds from the same scene**, because scrolling and presenting want
opposite things:

- **Scroll build** (`summit-commerce.html`) — the wheel drives a virtual scroll position.
  Stations are *magnetic*: uniform 180px ENTER/RELEASE/EXIT thresholds pull you onto a stop
  and hold you there until you deliberately push past, so you cannot accidentally fly by a
  beat mid-sentence. Motion is a lerp toward target (k ≈ 0.11) with a 3000 px/s velocity cap,
  which keeps a fast flick from turning into a jump cut.

- **Presenter build** (`summit-commerce-click.html`) — the one actually used live. Next/Back
  buttons plus keyboard and clicker keys tween between fixed stop points, so a remote clicker
  works and the pacing is deterministic in front of an audience. The wheel is demoted to
  scrolling *within* a long popup. `H` and `E` toggle presenter helpers.

Same content, same scene, two navigation models — kept as separate files on purpose so the
scroll version stays intact.

## Scenario 2 — Horizon Retail Group

Same scroll engine, completely different skin: an **8-bit pixel RPG** in the Undertale
register — `Press Start 2P` and `VT323`, hand-placed pixel sprites, chunky dialogue boxes,
and a dark-to-sunrise arc where the sun only breaks the horizon at the summit. Press **C**
to toggle CRT scanlines.

The structural addition here is **branching**. The journey runs gate → jungle → river
crossing → cliff climb → summit, and the jungle is a click-driven state machine with **four
virtual timelines** (main / fork / croc / oasis) swapped by the nav. Path 2 stays locked
until both of Path 1's outcomes have been fully read — the prospect's second option isn't
available until you've actually absorbed what the first one costs. Roughly 30 stations across
all timelines.

Beyond the shared `__step` / `__jump` hooks it exposes `__click('path1'|'path2'|'exact'|
'buffer'|'backfork'|'backent')`, `__tl()`, and `__state.flags`.

---

## Notes on the engineering

**Everything is one file.** Each build is 1,500–1,800 lines of HTML + CSS + JS with no
dependencies to install. That's a deliberate choice for the use case: the thing has to open
instantly off a laptop in a room with unreliable wifi, and it has to still open years later.

**Deterministic testability.** Animation loops are hostile to verification — a preview pane
that suspends `requestAnimationFrame` will happily show you a frozen frame and let you call
it correct. So every build exposes its state machine on `window`: `__state`, `__step(n)`,
`__jump(i)`, `__setTarget`, `__nudge`, `__segs`, plus `__next`/`__back`/`__stops` in the
presenter build. That makes it possible to drive frames by hand, land on an exact station,
and assert what's actually rendered — which is what the verbatim checkers do.

**Aesthetics are per-scenario, not shared.** There is no common stylesheet, and that's
intentional. Scenario 1 is clinical; Scenario 2 is a pixel game. Factoring out a shared
design system would have made both worse.

## Running locally

Open any `.html` file directly in a browser — that's the whole setup. The pages request
Three.js and Google Fonts from a CDN, so first load wants a network connection.

```bash
git clone https://github.com/armansra-hub/scroll-case-presentations.git
cd scroll-case-presentations
open summit-commerce-click.html   # macOS
```

Desktop browsers only; these are built for a laptop and a projector, not for phones.
