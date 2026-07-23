# Our Grand Concert — scenario integration reference

Working reference for adding the "Our Grand Concert" scenario (Global, July
2026) to the bot. Condensed from a Phase 0 capture session; supersedes the
running log it replaced.

Mechanics guide used: https://uma.guide/guides/grand-concert (calls it Grand
Live). **The guide is wrong in places** — in-game text wins; disagreements are
flagged below.

---

## START HERE

**Status:** Phase 0 (capture/recon) largely complete. No bot code written yet.

**Artifacts:**
| Path | What |
|------|------|
| `docs/GRAND_CONCERT_NOTES.md` | this file |
| `resource/umamusume/data/grand_concert_lessons.json` | song catalogue + lesson rules |
| `resource/umamusume/scenario/scenario_grand_concert.png` | scenario-select template (done, validated) |
| `screenshot/grand_concert/` | ~62 reference captures, 27 MB, **untracked** — parser fixtures |

**Phased plan:** Phase 1 = plumbing + a career that completes buying nothing.
Phase 2 = lesson economy. Phase 3 = training-score integration. Phase 4 =
UI/polish. Ship Phase 1 separately so URA/Unity Cup stay usable.

**Next actions:**
1. Write the Phase 1 skeleton (checklist at the bottom of this file).
2. Still uncaptured: a concert (1st is Junior Late Dec), post-debut main menu
   with a normal month date, summer-camp main menu, race flow.

---

## Coordinates and crops (720x1280)

### Main menu — bottom action row has FOUR slots

A Lessons button sits between Recreation and Races. Everything shifted left.
Measured from the flat grey locked button pre-debut (x 366-520) → pitch 164.

| Slot | Button | Grand Concert coord |
|------|--------|---------------------|
| 1 | Infirmary | (115, 1130) |
| 2 | Recreation | (279, 1130) |
| 3 | **Lessons** | (443, 1130) |
| 4 | Races | (607, 1130) |

Against existing points: `CULTIVATE_TRIP` (355,1130) lands **in the gap —
outings will never register, must fix**. `CULTIVATE_MEDIC` (170,1120) is
inside Infirmary but ~20px from the edge. `CULTIVATE_RACE` (564,1127) is fine.

Summer-camp variants (`CULTIVATE_MEDIC_SUMMER`, `CULTIVATE_RACE_SUMMER`,
summer trip 68,991) are **unverified** — recapture during summer.

### Main menu — left rail (new, all clear of existing parse regions)

| Element | Crop | Notes |
|---------|------|-------|
| Turns left | `img[55:118, 15:150]` | |
| Concert countdown | `img[128:190, 12:152]` | "Concert in N turn(s)" |
| Hype panel | `img[190:315, 5:185]` | tier text + gauge |
| Hype gauge | row **y=297**, track **x 37-128** | see reading method below |
| Performance Points | `img[310:675, 5:145]` | 5 rows, value over `/cap` |

PP rows (full-screen y): Da 355-420, Pa 420-485, Vo 485-548, Vi 548-610,
Co 610-672. Value/cap are on separate lines; the coloured tag column
(x 10-70) is a stable row anchor.

Verified unaffected on this scenario: stat row, cap row, skill points,
`read_energy()` (53% on a ~55% bar), and the six availability probes.
`race_available`'s probe now lands in a gap and reads False forever — **the
flag is written and never read anywhere**, so it is harmless.

### Date crops — scenario-specific, required

URA's crops do not fit (the new left rail pushed the turns box up), and the
fallback returns a wrong turn (11 instead of 1).

| `BaseScenario` method | Grand Concert crop |
|-----------------------|--------------------|
| `get_date_img` | `img[40:66, 160:380]` |
| `get_turn_to_race_img` | `img[55:118, 15:150]` |

Validated pre-debut only ("Junior Year Pre-Debut" + "11 turn(s) left").
Re-verify on a normal month after the debut race.

### Lessons shop

Three offers, **no scrolling**. Cards on a **272px pitch**, header tops at
**y = 226, 498, 770**. For card header `y0`:

| Field | Region |
|-------|--------|
| "Learnable!" badge | `y0-16 .. y0+4`, x 540-695 |
| Name | `y0+8 .. y0+40`, x 55-500 |
| Type badge | `y0+10 .. y0+38`, x 505-675 |
| Mastery row | `y0+50 .. y0+112`, x 200-680 |
| Concert row | `y0+120 .. y0+182`, x 200-680 |
| Cost chips | `y0+195 .. y0+238`, x 195-680 |
| Tap target | (360, `y0+125`) → 351 / 623 / 895 |

Numeric fields:

| Field | y | Da | Pa | Vo | Vi | Co |
|-------|---|----|----|----|----|-----|
| Balances (header) | 98-150 | 112-168 | 238-294 | 364-420 | 490-546 | 614-670 |
| Cost (per card) | `y0+195..y0+238` | 248-302 | 340-394 | 430-484 | 528-582 | 624-678 |

Other controls: Concert Info (618,1083), Full Stats (472,1083),
Back (82,1231).

### Concert Info screen

Opened from the shop; Close (360,1182). Best single status source.

| Field | Crop |
|-------|------|
| Which concert is next | `[120:180, 200:520]` ("1st Concert") |
| Hype tier text | `[203:245, 265:450]` ("Mild Hype") |
| Hype gauge | row y 218-227, track x 495-645 |
| Total Songs Learned | `[258:298, 425:485]` |
| Concert bonus 1/2/3 | `[455:505, 25:250]` / `[455:505, 252:470]` / `[455:505, 476:696]` |

Set List strip of learned song jackets below (first at x 32-155, y 565-720).

### Final confirmation screen

Start Career! (518,1182) — existing `CULTIVATE_FINAL_CHECK_START` (500,1185)
also lands inside it. Cancel (200,1182).

**New "Independent Training" tab:** Normal Career (188,216) vs Independent
Training (530,216). Selected tab is green (B8 G208 R135), unselected
near-white (B211 G215 R224). Single-pixel sampling can hit a letter glyph —
count green pixels over each tab band (y 205-230; left x 30-340, right
x 380-690) and take the larger. **Phase 1 must verify Normal Career is
selected before starting**, or a run could silently start the wrong mode.

---

## Mechanics

### Hype Level → Great Success

In-game (i) popup: *"Each time you learn a song, your Hype Level will
increase, and if the gauge is filled to the maximum, your next concert will be
a Great Success. Since the Hype Level is reset each time a concert is held,
you should learn new songs in preparation for each concert!"*

- Only **songs** raise it. Verified: learning a technique left it at 32%.
- Resets at every concert.
- 1 song ≈ 32% of the gauge, consistent with the guide's "3 songs = Great
  Success (+10 all stats), fewer = +3" — **for the 1st concert**.

**Read the gauge, don't count songs.** If the requirement differs at later
concerts the gauge absorbs it. Also note "Total Songs Learned" counts
*awarded* songs ("Make debut!" is granted a few turns in), so it must never be
derived from purchase history.

Reading method: classify pixels along the row — strongly coloured
(max-min > 55) = filled, flat mid-grey = empty. **Anchor on the longest grey
run and walk left through the contiguous fill.** Both ♪ endcaps are rainbow
and a naive first-to-last-coloured scan counts them as fill (returns 46%
instead of 32%). Cross-validated: main menu and Concert Info both read 32%.

### Lessons

Two types. **Techniques**: Mastery bonus only, immediate. **Songs**: Mastery
bonus (a persistent training bonus) *plus* a Concert bonus that activates
after the next concert and lasts to end of career. Concert bonuses are
**levelled and cumulative** (Lvl 0 → Lvl 1).

Costs are **per-currency** (Da/Pa/Vo/Vi/Co), so affordability is a five-way
comparison.

**Rotation (fully characterised):**
- A set is static until a purchase — verified pixel-identical across a turn
  boundary. Waiting never rotates it.
- Any purchase (technique *or* song) immediately replaces the set and reopens
  the shop on the new one.
- Passed-over lessons return later, so declining costs nothing permanent.
- Sets can be homogeneous — all techniques or all songs.
- **Therefore buying is the only way to roll a set.** When a set holds no
  song worth taking, buying a technique is the mechanism for rolling toward
  one.

The dialog's exclusivity warning ("your trainee won't be able to learn the
other 2 options") means the current *set* is consumed, not that lessons are
destroyed. Because sets refresh on purchase, **greedy buying is safe** — a
bad pick costs only the value difference within one set.

Learning one technique unlocked the first song tier; set 4→5 went techniques
→ songs, so availability tracks cumulative technique count (guide's
1-2-3-4-4-2-3 progression) rather than a one-time unlock.

### Affordability detection

**Use cost-row mean brightness** (`y0+195..y0+238`, x 195-680): **~226-231
affordable vs ~161-162 unaffordable**, threshold 195. Correct on all 12+ card
observations.

**Do NOT use the "Learnable!" badge.** By template match it gave a false
negative (0.799 on a genuinely affordable card, and 0.827 on another) — the
badge has soft edges over an animated stage background and slot 2 is
consistently weak. By region brightness the ranges overlap outright.

### OCR recipe — upscale 2x

Resize each numeric crop **2x (INTER_CUBIC)**, then pad 12px white, then
`ocr_digits`. Validated 35/35 balances and 21/21 cost rows across 7 shop
captures, including greyed-out unaffordable rows.

At 1x, a Composure balance of **11 read as 1** — not clipping (ink was inside
the crop); two narrow `1` glyphs with a wide gap confuse the detector, and
crop widening was erratic. The failure is silent and plausible, so the parser
should log every value and sanity-check balances against the previous turn
(they only move by training income or a known purchase).

---

## Hazards

### The INFO handler will auto-buy a lesson

The lesson confirmation dialog's title bar is **"Confirmation"**. `info.png`
matches it at 1.000, so `script_info` fires, OCRs "Confirmation", hits
`TITLE[9]` on an exact match, and clicks `CULTIVATE_LEARN_SKILL_CONFIRM_AGAIN`
at **(516,1185)** — which is the **Learn** button (517,1182).

So landing on that dialog buys the lesson with no logic involved. On an
unaffordable lesson the same click lands on **Schedule** instead (the green
button changes label, same position), committing to a scheduled lesson.

Phase 1 risk is low: nothing currently clicks (443,1130), and the broken
`CULTIVATE_TRIP` lands in a gap rather than on Lessons. **Phase 2 must
intercept this dialog before the generic title dispatch** — same pattern the
spark-reroll flow already uses in `script_info`.

The bot never needs Schedule: sets don't expire and points only accumulate.
Avoiding it is the requirement.

### Existing screen-detection collisions (mostly pre-existing)

| Screen | Detected as | Consequence |
|--------|-------------|-------------|
| Final confirmation | `INFO` | "Final Confirmation" fuzzy-matches "Factor Confirmation" `TITLE[33]` at 0.811; its Fujikiseki cutoff (2025-07-13) has expired so the `else` branch clicks (525,1185) = **Start Career!**. Works entirely by coincidence, but identical for this scenario. |
| Final confirmation | also `CULTIVATE_RESULT_2` (0.954, "Support Cards" header) and `FACTOR_RECEIVE` (0.863, "Sparks") | `detect_ui` races; the losing click lands in the dead gap between Cancel and Start Career. Pre-existing on all scenarios. |
| Lessons shop | no UI matches → `NOT_FOUND_UI` | heuristics then the (719,1) fallback click. Harmless. |
| Concert Info | `INFO` | title matches nothing at 0.8 (best 0.500) → unknown-title branch → ESCAPE, which closes it. Benign. |

`UI_CULTIVATE_FINAL_CHECK` is the Chinese 最终确认 and **never matches on
Global** (0.494); `script_cultivate_final_check` is dead code there.
`REF_SELECTOR` is likewise dead on Global (0.601) — all events run through the
`dialogue1..5` fallback.

---

## Training select — existing parsers all work

Layout *looks* different (circular portraits, narrower column) but is on the
**same 115px pitch as Aoharu**. All four parsers validated unchanged:

| Parser | Result |
|--------|--------|
| `parse_train_type` (`img[210:275, 0:210]`) | Speed 0.972, Stamina 0.957; others <0.76 |
| support card type icons (ROI x 550-695, `base_y` 177, `inc` 115) | Speed **0.999** @ (600,198), Wit **0.955** @ (600,313) |
| favor colour (`roi_rgb[106,56]`) | lands exactly on the bond bar: RGB (42,192,255) = pixel-perfect `FAVOR_LEVEL_1` |
| `parse_training_result` (`img[800:830]`) | gains in the right x-ranges on both lanes |
| `parse_failure_rates` (`img[916:981]`) | the single "Failure 0%" badge sits above the *selected* lane, so it falls in that lane's x range |

So `GrandConcertScenario` can reuse the Aoharu parsing methods nearly
verbatim, minus the spirit-burst/ESB block.

Caveat: a card with no bond bar (an NPC) samples RGB (79,203,157) → favor
UNKNOWN → skipped rather than scored as NPC. Minor scoring loss.

A single tap **previews** a lane; the two-click confirm pattern still applies.
Lane points (235/360/490/620 @ y1085) are correct. The selected lane is
raised ~50px, but the bot only clicks unselected lanes.

### New elements on this screen

- **Facility level printed in the lane header** — "Speed Lvl 1" / "Turf"
  (`img[200:280]`). No need to count trainings.
- **PP gain preview** — an orange `+N` beside the row that lane feeds
  (Speed → `+17` on Da; Stamina → `+13` on Pa). Scan x ~138-200 across the
  five row bands to get currency and amount in one read. Verified accurate:
  a Speed training yielded exactly +17 Da.
- **Per-lane currency badges** (top-left of each lane button) read
  Da/Pa/Co/Vi/Pa — **two lanes showed "Pa"**, so this is *not* the fixed
  lane→currency mapping (which is proven elsewhere: see the lessons JSON).
  Meaning unresolved; prefer the `+N` preview.

---

## Events

Header "Main Scenario Event"; name below it. Earlier scenario events had no
choices and skip mode cleared them.

**"Tutorial" (first decision event) already resolves correctly** to choice 2
("No, I think I'm okay") — traced end to end: name crop reads "Tutorial",
`REF_SELECTOR` finds 0, `dialogue1..5` collapses to exactly 2 selectors
((50,765) and (50,897)), the Unity Cup tutorial override needs exactly 5 so it
does not fire, and `get_event_choice` returns 2 → clicks (50,897).

That 2 comes from `event_data.json`, where "Tutorial" has all-zero stats on
every choice **except** choice 2, which carries deliberately enormous fake
values. It is pinned by data, not logic — if that entry is ever regenerated
from a scraper it silently reverts to choice 1 (all-zero tie, scorer keeps the
first key) and the bot would enter the tutorial.

Watch: a later tutorial screen whose bubble says "ask about" or "are you sure"
would be intercepted by the committed Unity Cup handler and click its
hardcoded (360,893)/(360,762). On this layout those coincide with the same two
choices, so it would still be right — but by coincidence.

---

## Method gotchas (mistakes already made — don't repeat)

1. **Don't colour-segment the main-menu button row.** The striped skirt behind
   the buttons defeats saturation thresholds; it produced nonsense extents
   twice. Measure from a flat element (the grey locked button) and confirm by
   overlaying markers on a zoomed crop.
2. **Don't eyeball pitch on circular art.** A ruler estimate put the support
   card pitch at 105px; template matching proved 115px. Template match wins.
3. **Prefer large flat regions over small stylised art** for state detection.
   Cost-row brightness beat the "Learnable!" badge; both failures above were
   the same mistake in different clothes.
4. **Upscale 2x before OCR** — see the recipe above.
5. **Treat the guide as a hypothesis.** It was wrong that offers "don't
   expire" in the sense implied, and it omits Hype Level entirely.

---

## Phase 1 checklist (career completes, buys nothing)

- [ ] `SCENARIO_TYPE_GRAND_CONCERT = 3` in `define.py`
- [ ] `GrandConcertScenario(BaseScenario)` — copy Aoharu's parsing methods
      minus spirit-burst/ESB; override `get_date_img` /
      `get_turn_to_race_img` with the crops above
- [ ] Wire-up: `context.py` match arm, `task.py`, a (initially empty)
      `GrandConcertConfig` in `configs.py`, web UI dropdown option
- [ ] Scenario template is already cut and validated (1.000 vs ≤0.254 on the
      other three cards); `script_scenario_select`'s 6-swipe loop covers 4
      cards unchanged
- [ ] **Grand Concert bottom-row click points** — at minimum fix Recreation;
      Infirmary is marginal
- [ ] Verify the **Normal Career** tab before Start Career!
- [ ] Concert screens: click-through handlers + any new `INFO` titles
- [ ] Shakedown run with `bot.log.file_enabled: true`

Deliberate non-goals for Phase 1: no lesson buying (so the INFO auto-buy
hazard cannot fire), no PP-aware scoring. Concerts still fire with <3 songs
(+3 stats instead of +10), so a career completes without touching the shop.

**Do not refactor the scenario abstraction yet.** The
`if scenario_type() == AOHARUHAI` pattern in `hook.py`/`cultivate.py` is
working and earning SS ranks; new logic goes in its own module instead.

---

## Open questions

- What do the per-lane currency badges mean? (Not the lane→currency mapping.)
- Does a scheduled lesson auto-learn when affordable, or is it only a tracker?
- Does the Lessons "!" badge mean "affordable" or just "unlocked"? Decisive
  test: capture the main menu while nothing is affordable.
- Do song costs stay stable across appearances? ("Go This Way" repeated
  identically; every repeated *technique* changed currency.)
- Guide claims races give zero performance points — unverified.
- Concert screens, summer-camp layout, post-debut month parsing: uncaptured.
