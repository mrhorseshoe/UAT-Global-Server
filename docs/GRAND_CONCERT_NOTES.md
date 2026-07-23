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

### Race-day menu (different layout — capture `49_predebut_race_menu.png`)

On a race turn the main menu is replaced by a three-button row and the mid
section shifts down ~65px.

| Button | Centre | Extent |
|--------|--------|--------|
| Skills | (122, 1085) | ~35-215 |
| **Race!** | (358, 1085) | ~235-480 |
| Lessons | (600, 1085) | ~505-695 |

A red "Race Day" banner sits above Race! at ~(291,986)-(470,1020).

**This works today, no change needed.** `REF_TRAIN_BTN` does not match
(0.573) so the screen is *not* `CULTIVATE_MAIN_MENU`; instead both
`CULTIVATE_GOAL_RACE` templates match (0.981 / 0.883), so
`script_cultivate_goal_race` runs and clicks
`CULTIVATE_GOAL_RACE_INTER_1` **(391,1081) — inside Race!** ✅

Consequences worth knowing:

- **PHASE 2 HAZARD: the Lessons button moves on race day.** The normal-menu
  Lessons point (443,1130) lands inside **Race!** here, and the race-day
  Lessons button is at (600,1085) instead. A lesson-buying routine that
  blind-clicks (443,1130) would start the debut race. Confirm the normal
  layout (or the absence of the Race Day banner) before clicking Lessons.
- `CULTIVATE_RACE` (564,1127) lands inside **Lessons** on this screen. Not
  reached today because the screen resolves to `CULTIVATE_GOAL_RACE`, but it
  means the normal-menu race point is actively wrong here.
- The stat row sits ~65px lower (values ~y 920-950, vs 855-885 normally).
  Nothing parses stats on this screen, so it is inert — but do not reuse the
  main-menu stat crops on race-day captures.
- The turn box reads **"GOAL"** instead of a number, so the pre-debut date
  branch OCRs no digits and falls back to `12 - (len(history)+1)`. The
  literal string `parse_date` looks for, "Race Day", is on the banner rather
  than in the turn box. The resulting date is imprecise but tolerable — on a
  race turn it only feeds tactic selection (`tactic_list[int((date-1)/24)]`,
  which still indexes 0). Revisit if a wrong date causes trouble; the
  existing `race_day_menu.png` template (matched 0.883 here) is a clean way
  to detect the state if a GC-specific shortcut is ever needed.

### BREAKING: career-end screen has a third button

Capture: `78_career_end.png`. The Complete Career screen gains a **Lessons**
button, so the row holds three buttons instead of two and everything shifted.
A "Remaining Performance Points" row sits above them (y ~880-925).

| Button | Grand Concert coord | Extent |
|--------|---------------------|--------|
| Skills (+ "Skill Pts N") | **(122, 1053)** | ~35-215 |
| **Complete Career** | **(360, 1053)** | ~228-490 |
| Lessons | (597, 1053) | ~505-690 |

**Both existing points are wrong here:**

| Point | Coord | What is under it |
|-------|-------|------------------|
| `CULTIVATE_FINISH_LEARN_SKILL` | (215,1050) | the **gap** between Skills and Complete Career (samples B118 G76 R98 — the trainee's clothing) |
| `CULTIVATE_FINISH_CONFIRM` | (512,1050) | the **Lessons** button's left border (samples B239 G129 R238 magenta) |

So at career end the bot would fail to open Skills, and **would open the
Lessons shop instead of completing the career** — a stall, and one that parks
it on the screen where the `script_info` auto-buy hazard lives.

The UI itself is still detected correctly (`cultivate_finish.png` matches at
0.982), so only the two click points need scenario-specific values.

*Measurement note:* hue segmentation failed on this row too — the chibi
artwork and white button text break it. The extents above come from marker
overlay plus direct pixel sampling, which is the method that has held up on
every one of these button rows.

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
| Balances (header) | 98-150 | **98-168** | **221-291** | **344-414** | **467-537** | **590-660** |
| Cost (per card) | `y0+195..y0+238` | 248-302 | 340-394 | 430-484 | 528-582 | 624-678 |

Balance crops follow `x1 = 98 + 123*i`, `x2 = 168 + 123*i`. They are **wider
than the value looks like it needs** on purpose: balances are right-aligned,
so a 3-digit value grows leftward into the chip gap. Narrower crops (the
original 112-168 etc.) clip the leading digit — **Da 138 read as 38**. Caps
rise by 50 per concert from 200, so 3-digit balances are normal late in a
career and this would bite in every run. Verified 80/80 across 16 shop
captures including the 3-digit case.

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

### CONFIRMED STALL: the post-concert "Bonuses Updated!" popup

Capture: `60_post_concert_popup.png`. Appears after a concert. Modal card
reading **"Bonuses Updated!"** / "Concert bonuses updated!", with
**Close (202,834)** and **Confirm (517,834)**.

**This hangs the bot today.** Traced end to end:

1. No UI template matches → `NOT_FOUND_UI`.
2. `script_not_found_ui`'s heuristics all miss — its title probe
   (`img[200:400,100:620]`) OCRs to empty, and its middle probe
   (`img[800:1000,200:560]`) OCRs to `"confirnose"` (Confirm+Close mashed),
   hitting no result or goal keyword.
3. Falls through to `click(719, 1)`, which cannot dismiss a modal.
4. The screen never changes, so the watchdog force-restarts the game after
   ~90s — and the restart likely lands back on the same popup.

`btn/close.png` does match it (0.983 at (132,805)), but `BTN_CLOSE` gates no
UI, so that match goes unused.

**Fix (Phase 1, required):** template cut and validated at
`resource/umamusume/ui/concert_bonuses_updated.png` (292x32, from
`img[741:773, 213:505]` — the body text). Scores **1.000** on this screen and
at most **0.568** on all 60+ other captures, so it is safe to gate a UI on.
Wire it as a UI in `asset/ui.py` + `scan_ui_list`, add a handler in the script
dict, and click one of the two buttons.

**Click Close (202,834), not Confirm.** Resolved by observation: Confirm opens
a second modal, **"Active Concert Bonuses"** (`62_post_concert_detail.png`),
whose only exit is Close at (360,918). Taking Close on the first popup skips
that screen entirely.

That second screen would stall too if reached: it matches `info.png` at 1.000
so `script_info` runs, but "Active Concert Bonuses" matches no `TITLE` entry
(best 0.488), so it falls to the unknown-title branch and clicks `ESCAPE`
(5,715) — which lands *inside* this dialog's Active Songs strip and does
nothing. If the Close-on-first-popup handler ever misses, add a handler for
this screen too, clicking (360,918).

### The detail screen independently validates the song catalogue

"Active Concert Bonuses" showed **Friendship Training Effectiveness +5%,
Specialty Priority +10, Support Chain Event Frequency Lvl 1** against four
active songs (Make debut!, Believe in Miracles!, Full Speed Ahead! Umadol
Power, Zero Is Where the Center Stands!). Summing those songs' concert
bonuses from `grand_concert_lessons.json` predicts exactly those three totals,
including the +10 arising from two separate +5 sources.

Useful twice over: it confirms the catalogue's concert-bonus data, and it
means this screen can be used to **verify a purchase actually landed** if
lesson buying ever needs auditing.

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

## Light Hello (Pal card)

**Assume Light Hello is always in the deck for this scenario.** She is the
scenario-linked Pal; the guide credits her with energy/mood recovery, "See Ya
Later!" hints, and a 45% chance of +20 performance points of whichever
currency is scarcest — which interacts directly with the per-currency lesson
costs.

Practical consequences:
- The existing pal machinery (`pal_name`, `pal_thresholds`,
  `prioritize_recreation`, `pal_event_stage` detection) is in play, so the
  Grand Concert preset should ship with Light Hello configured rather than
  leaving recreation logic dormant.
- Her outing chain must actually be unlocked — see the event below.

### Recreation menu — existing pal stage detection works unchanged

Capture: `54_recreation_light_hello.png`. Opened from Recreation once her
outing chain is unlocked. Two rows: **Light Hello** (with a Friendship Gauge
and an Event Progress track of **5 chevron pips**) and **Silence Suzuka**
("Trainee Umamusume"). Cancel at **(360, 918)**.

The pal-stage sampling already in `script_cultivate_main_menu` lines up
**exactly**. Its 5-stage sample points read the empty-pip colour perfectly:

| Sample | Value | Empty test (`|b-223|,|g-227|,|r-231| <= 5`) |
|--------|-------|--------------------------------------------|
| (452,474) | B223 G227 R231 | pass |
| (503,474) | B223 G227 R231 | pass |
| (554,474) | B223 G227 R231 | pass |
| (605,474) | B223 G227 R231 | pass |

Five pips → the `num_stages == 5` branch → `4 - 4 + 1 = stage 1`, correct for
a fresh chain. So `pal_thresholds` should be configured with **5 stages** for
this scenario.

Two prerequisites before this can ever run:

1. **Recreation must actually open** — the detection is reached by clicking
   `CULTIVATE_TRIP`, which lands in a gap on this scenario. Fixing that point
   to (279,1130) is what makes pal detection work at all.
2. **Dismissal is unverified.** After sampling, the existing code closes the
   menu with `ctx.ctrl.click(5, 5)` — an outside-the-dialog tap. Whether that
   dismisses this dialog is untested; **Cancel (360,918)** is the reliable
   target if it does not.

### Event: "Embrace Those Emotions!" → always choice 1

Support Card Event, choices "I'd be glad to!" / "Sorry, I'm a little strapped
for time…". **Always take choice 1**: accepting unlocks recreation with her,
which is the main value of the card. Declining does not.

Was absent from `event_data.json`, so the bot fell through to its hardcoded
default of choice 2 — the wrong one. Now pinned in `event_map`
(`event/manifest.py`) as `"Embrace Those Emotions!": 1`, because it is a
strategic override rather than a stat calculation; that dict is checked before
the events database and survives any regeneration of it. (The Tutorial event
is forced the other way, via stuffed stats inside `event_data.json` — fragile
for exactly that reason.)

Verified: the name crop reads it cleanly, `find_similar_text` resolves it at
the 0.8 threshold even with the trailing "!" dropped, and the nearest of the
920 known event names is only 0.558 similar, so there is no hijack risk.

---

## Scenario skill event: "Closer Together" — needs a WebUI config option

Capture: `77_skill_choice_event.png`. A Main Scenario Event late in the career
(seen Senior Year Early Nov) offering **five** options, each granting a
different skill — the Grand Concert equivalent of Unity Cup's skill choice.
This is the one decision in the scenario that genuinely needs user
configuration, since the right pick depends on the trainee's build.

| # | On-screen text | Skill granted |
|---|----------------|---------------|
| 1 | "A song with some call-and-response"… | **Full Tilt** |
| 2 | "Gratitude towards the fans, without whom I would not be running"… | **Concentration** |
| 3 | "I'm home"… | **Trackblazer** |
| 4 | "The power to achieve a breakthrough"… | **All I've Got** |
| 5 | "Song brings us closer together"… | **Lane Legerdemain** |

Options 1-4 correspond to the scenario-linked characters (Smart Falcon,
Mihono Bourbon, Silence Suzuka, Agnes Tachyon); option 5 is the
character-independent choice. Per the guide, each option grants the
character's **gold** skill if that character is your trainee or their support
card is in the deck, and a **white** alternative otherwise — so the skill a
given option actually yields depends on the deck:

| Character | Gold | White alternative |
|-----------|------|-------------------|
| Smart Falcon | Full Speed! | Full Tilt |
| Mihono Bourbon | Concentration | Focus |
| Silence Suzuka | Trackblazer | Rosy Outlook |
| Agnes Tachyon | Come What May | All I've Got |
| (none) | — | Lane Legerdemain |

The mapping above was captured on a Silence Suzuka run, which is why options
3 and 2 showed gold names while 1 and 4 showed whites.

### Bot status and what is needed

- Event name crop reads **"Closer Together"** cleanly.
- All **5 selectors** are detected at (50, 369/501/633/765/897) — the
  `dialogue1..5` fallback handles the taller 5-option layout fine, and the ROI
  does not clip the fifth row.
- The event is **absent from `event_data.json`**, so the bot currently falls
  through to its hardcoded default of **choice 2** — arbitrary, not a choice.
- Do **not** pin this in `event_map`: unlike the Light Hello events, there is
  no single correct answer. It belongs in a `GrandConcertConfig` field
  (`scenario_skill_choice`, 1-5) exposed as a dropdown in the task setup UI,
  following the pattern of `UraConfig.skill_event_weight` and
  `AoharuConfig.preliminary_round_selections` in `scenario/configs.py`.
- Watch for the Unity Cup tutorial override, which fires on exactly 5
  selectors — it is gated on `event_name == "tutorial"`, so it does not
  trigger here, but any future 5-option handling should keep that gate intact.

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
