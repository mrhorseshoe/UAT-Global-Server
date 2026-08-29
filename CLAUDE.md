# CLAUDE.md

Guidance for Claude Code working in this repo. See `README.md` for the feature
list and `CHANGELOG.md` for history; this file covers how the thing is built and
the traps that are not obvious from reading the code.

## What this is

A screenshot-driven bot that plays Umamusume: Pretty Derby (Global) on an
Android emulator, plus a Vue web UI to configure and drive it. There is no game
API: everything is OpenCV template matching and PaddleOCR over screenshots, with
taps sent through uiautomator2 over ADB.

## Layout

- `main.py` — device health checks and ADB recovery, restores saved state, starts
  the scheduler thread, then serves the FastAPI app on **127.0.0.1:8071**.
- `bot/` — game-agnostic engine.
  - `engine/scheduler.py` — task list loop, one tick per second.
  - `engine/executor.py` — the perception-action loop: screenshot → match against
    every known UI in a thread pool → dispatch to that screen's handler → sleep.
    Also the 30 s screen watchdog that restarts the game when the screen freezes.
  - `conn/u2_ctrl.py` — taps/swipes/screenshots, click randomization, and the
    repetitive-click guard (11 identical clicks → app restart).
  - `recog/` — `image_matcher.py` (template match + LRU cache), `ocr.py` (PaddleOCR).
- `module/umamusume/` — everything game-specific.
  - `asset/` — UI definitions, click points, templates (PNGs in `resource/`), race DB.
  - `manifest.py` — the dispatch table mapping each UI screen to its handler.
  - `script/cultivate_task/` — the handlers. `parse.py` reads the screen into a
    `TurnInfo`; `ai.py` `get_operation()` decides the turn; `cultivate.py` holds
    the per-screen scripts.
- `web/` — Vue 3 + Vite source. `public/` — the **built** output, committed.

## Working on it

**Python is `py -3.10`.** The bot's packages live in system Python 3.10's
site-packages, not in `venv/`. Bare `python` / `pip` hits the wrong interpreter.

**Web changes need a rebuild, and the build output is committed:**

```bash
cd web && node clean-assets.js && npx vite build
```

That writes hashed assets into `public/`, which the FastAPI app serves. Commit
`public/` along with `web/src/` or the UI ships stale. (`npm run build` invokes
`bun` in prebuild; calling `node clean-assets.js` then `npx vite build` avoids
needing bun.)

**Changes reach the running bot only after it restarts.** The process
soft-restarts itself after every career run, so it picks changes up on its own
within a run or two.

**Verifying UI work.** There is no tracked test suite. For Python logic, write a
throwaway simulation script in the scratchpad that imports the real functions and
drives them with fakes — that is how the training-lane failsafe and the spark
matcher were checked. For the web UI, serving `public/` on another port and
driving the page with the browser tools works for rendering and interaction, but
`web/src/util/axiosConf.js` hardcodes `baseURL` to `http://127.0.0.1:8071`, so
the page's API calls still hit whatever bot is running there.

The pattern that works best for screen handlers: capture real screens over ADB
(`deps/adb/adb.exe -s emulator-5554 exec-out screencap -p > shot.png`), then run
the actual handler against the saved PNG with a fake controller exposing
`get_screen`, `click_by_point` and `click`, and assert on the clicks it records.
That catches a wrong click point without touching the game. **Such scripts must
`os.chdir` to the repo root** — `Template` resolves `resource/...` relative to
the working directory, and templates that fail to load silently make every
screen look unrecognised.

## Traps

**State must survive the soft restart.** Because the process restarts after every
career, anything needing continuity (loop counts, stop-after-run, scheduler
active flag, runtime thresholds) is serialized to `userdata/` by
`bot/base/purge.py` and reloaded at boot. A feature that only keeps state in
memory will silently reset every run.

**Adding a task setting** touches four places: the payload in
`web/src/components/TaskEditModal.vue`, `build_task()` in
`module/umamusume/task.py`, the copy into `CultivateContextDetail` in
`module/umamusume/context.py`, then the script that reads it. Use
`attachment_data.get(key, default)` and `getattr(detail, key, default)` — tasks
saved before your change are restored from disk without the new field.

**Theme quirk: `btn-outline-primary` renders accent-on-accent (invisible text)
inside input groups in the task modal.** Use `btn-outline-success` there, as the
race and skill preset buttons do. Check computed colors after adding buttons.

**`TaskEditModal.vue` has two `watch:` keys** — a populated one and an empty one
declared later, which wins, so every watcher in that component is dead code. Use
`@change` handlers instead, or fix the duplicate first (and re-check what
reviving the dormant watchers does, since they have never run).

**Several UI templates are crops of buttons, so they match wherever that button
appears** — and button art is not stable. `MAIN_MENU` used to be a crop of the
CAREER button, which also sits on event hub pages, so the bot matched a hub as
Home and looped on a hardcoded coordinate. Worse, that button's art rotates
with in-game events (one chibi and dumbbells, then two Champions Meeting
characters), and the lettering moves with it: no single crop matches two
rotations, and twice in one week the bot could not find Home at all. `MAIN_MENU`
is now a crop of the **bottom nav Home tab**, which does not change (0.96+ on
both rotations, under 0.55 elsewhere), and `script_main_menu` locates CAREER by
colour with `find_green_button`. Prefer a stable anchor plus a colour or
position search over a template of decorated art.

**Trainer events (a few times a year) rewrite the career start path.** While one
runs, a "Choose Career Mode" dialog appears between the scenario and trainee
pickers with the event option preselected, and the Scenario Select screen grows
an event banner. `_choose_career_mode` in `info.py` picks Normal Mode, verifies
the switch took, and only then confirms — Confirm is the one-way door, and
confirming the wrong option starts an event run. Expect a new event to add
dialogs: check the logs for `Unknown option box - OCR: '...'` and add each exact
title to `TITLE`.

**The in-game master database is the source of truth for names.** It is SQLite at
`%USERPROFILE%\AppData\LocalLow\Cygames\Umamusume\master\master.mdb`; entity
tables carry ids, and `text_data` carries localized strings keyed by
`(category, "index")`. Reach for it rather than a wiki when a name is wrong.
`export_support_cards.py` regenerates the support card picker from it. Card
titles must match the game exactly — the bot OCRs the title on the borrow screen
and fuzzy-matches it against the name saved in the task.

**Race banner templates must be cropped starting at x ≥ 60**, or the
icon-anchored search region in `find_race` cannot contain them.

**`scripts/` is gitignored.** Put committed tooling at the repo root next to
`scrape.py` and `export_support_cards.py`.

**Screens are matched by templates that must and must not be present**, so a
handler firing on the wrong screen usually means a template needs re-cropping
after a game update, not that the handler logic is wrong.

**Dialogs are dispatched by their OCR'd title, not by a UI template.** Anything
with the green diagonal header matches `INFO`, and `script_info` fuzzy-matches
the title against the `TITLE` list at 0.8, taking the *best* match. Some
templates inherited from the CN project never match on Global at all
(`CULTIVATE_FINAL_CHECK` is the Chinese 最终确认), so a screen can appear handled
while actually being cleared by a coincidental title match against an unrelated
entry — that is how the career start dialog worked before it was given a real
entry. When adding a dialog, add its exact title to `TITLE` and check what it
previously fuzzy-matched.

**A handler that waits must click nothing.** `NOT_FOUND_UI` falls back to a
blind corner click under a fixed name, and 11 identical consecutive clicks trip
the repetitive-click guard into restarting the game. Any screen the bot sits on
for a while (the Independent Training countdown) needs its own handler that
clicks nothing. The other half of the trap is the 30 s watchdog in
`executor.py`, which restarts the game when the downscaled frame stops changing
— animated screens pass it, static ones need thought. Measure before assuming:
the idle Home screen scores 5-25 against a threshold of 1.0.

**Restarting the bot process used to lose the task list.** `saved_tasks.json` is
now the durable store (written on add/delete, kept after loading), but the state
that still only reaches disk when a run *ends* — run counts, scheduler flags —
is lost if you kill the process mid-run. Prefer `POST /action/bot/stop` and let
it finish, and remember that code changes only reach the bot after a process
restart, so a long-running career is running whatever code it started with.

## Conventions

- Presets live per-file under `userdata/umamusume/{race,skill}_presets/`; race
  presets shipped with the repo are in `resource/umamusume/race_presets/` and are
  shadowed by a user preset of the same name.
- `userdata/` is gitignored — anything a user should receive has to live in
  `resource/` or `web/src/assets/`.
- Match the surrounding code; much of it is inherited from an upstream CN project
  and still has Chinese comments.

## Where things stand (Aug 2026)

`origin` is the owner's fork (`mrhorseshoe/UAT-Global-Server`) and is the only
place to push; `upstream` is the original project, which is abandoned and
rejects pushes.

The current line of work is the branch **`feat/independent-training`** (pushed,
not merged into `main`): the Independent Training loop, the two new scenarios,
durable task storage, the spark partial-read retry, and the trainer-event
failsafe. It has run unattended for a dozen careers in a row, so treat it as
working and be suspicious of regressions rather than rebuilding it.

Two deliberate limits, in case they look like bugs:

- The bot always declines the event career and picks Normal Mode; running an
  event career would need a task setting that does not exist yet.
- Trackblazer and Grand Concert are selectable only — their scenario classes
  inherit URA's parsing — so they are greyed out unless Independent Training is
  ticked. A standard career there would need its own date/training parsing.

`'Career Complete'` (the end-of-career "Return to the home screen?" prompt) now
has its own `TITLE` entry and always clicks Cancel. It used to ride the 0.6
fuzzy fallback onto `'Training Complete'`, which happened to click the same
point; the trainer event reuses the dialog with the green button relabelled
"Event Home", so the choice had to stop being a coincidence.
