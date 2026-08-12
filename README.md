# UAT-Global-Server — mrhorseshoe's fork

Fork of [TomerGamerTV/UAT-Global-Server](https://github.com/TomerGamerTV/UAT-Global-Server).
All changes below were added on top of the upstream project.

## Game update fixes (July 2026 Global update)

1. **Scenario select fix** — the update rendered scenario key art ~5% larger, breaking template matching. Re-cropped both scenario templates and decoupled the carousel swipe count from the scenario enum (a third scenario card exists now).
2. **New dirt G1 races** — added Nambu Hai (Classic and Senior year), Kawasaki Kinen, Kashiwa Kinen, and Zen-Nippon Junior Yushun to the race database, Race Settings menu, and banner templates.
3. **Spark reroll screen option** — the update added an end-of-run offer to reroll sparks for 30 TP. A new tickbox (single-run Loop mode only) stops the bot on that screen so you can decide manually; otherwise the bot confirms without rerolling.
4. **Automated spark reroll** — an "Automate spark reroll" tickbox with a Spark Reroll Options popup: check the blue (stat) and pink (track/distance/style) sparks you want, each with its own minimum star count (1–3), and pick how the groups combine — OR keeps the roll when any desired spark hits its stars, AND requires both a desired blue and a desired pink spark (multiple checks within a group always mean "any of these", since an uma carries one of each). If the check fails the bot rerolls (30 TP). On the Spark Selection carousel it then compares the two sets: the rerolled set is kept if it satisfies the check; if neither set does, it keeps the one with more white sparks — read directly from the scroll bar length (a shorter thumb means more sparks below the fold), which is more reliable than scrolling each list. Ties fall back to total stars. Each step is captured to `screenshot/spark_reroll/` for troubleshooting.
   - **Insufficient TP** — an optional "Spend carats to restore TP" toggle lets the bot top up TP when a career ends with less than the 30 TP a reroll needs: it uses a non-chocolate TP recovery item if you have one, otherwise carats. Chocolate TP items are never spent. Left off, the bot keeps the original sparks instead of spending anything.

## Independent Training

The August 2026 Global update added Independent Training: you set a Training Focus and race Agenda, start the career, and the game plays it out on its own over about 50 real-time minutes for 15 TP, then hands you the usual end-of-career screens.

1. **Independent Training loop** — a tickbox in the General section (Loop mode, not compatible with Team Trials). The bot walks the normal preparation flow (scenario, trainee, legacy, borrowed support card), picks the **Independent Training** tab on the Final Confirmation dialog, starts the run, waits out the countdown, dismisses the training log when it finishes, and then buys skills and rerolls sparks exactly as it does for a normal career — before looping into the next run. Set the Training Focus, Agenda and Prioritized Skills yourself once; the game remembers them, so the bot only picks the tab and confirms.
2. **Career start dialog handled properly** — the Final Confirmation dialog had no handler on Global: its `CULTIVATE_FINAL_CHECK` template is the Chinese *最终确认* inherited from the upstream CN project and never matches, so the dialog fell through to the generic dialog handler, where "Final Confirmation" fuzzy-matched "Factor Confirmation" and landed on Start by coincidence. It is now matched by name, and the bot checks which of the two tabs is selected before starting. That matters because the game remembers the last tab used — without the check, a normal Career task would silently start Independent Training runs, or the reverse.
3. **The bot waits instead of clicking** — the in-progress screen has its own handler that deliberately clicks nothing. Left to the fallback handler, its blind corner clicks would trip the repetitive-click guard and restart the game roughly every eleven seconds for the whole 50-minute run. The screen animates, so the freeze watchdog stays satisfied on its own.
4. **Countdown in the web UI** — while a run is in progress the dashboard shows the remaining time, so a bot that is deliberately doing nothing for 50 minutes doesn't look stalled. It clears itself if the bot leaves that screen.
5. **Trackblazer and Grand Concert** — both scenarios are selectable, which is what Independent Training needs since the game plays the career itself. They are greyed out unless Independent Training is ticked: only the scenario picker is implemented for them, and a standard turn-by-turn career would need their own date, training and support-card parsing.

**TP budget matters.** A run costs 15 TP and regenerates only ~8 over its 50 minutes, so a loop ends each cycle poorer than it started, and a spark reroll costs 30 TP. Hunting sparks across a long loop therefore needs "Spend carats to restore TP" enabled (a separate setting from auto-recovering TP to start a career), or a banked TP bar.

## Unity Cup 2.0

1. **Renamed Aoharu Cup to Unity Cup** across the UI and removed the MANT scenario option.
2. **Extreme Spirit Burst (ESB) detection** — the bot recognizes the new ESB icon on training lanes (with a color gate so it can't be confused with the special-train arrow) and prioritizes those lanes.
3. **ESB top-priority training override** plus OCR of in-game stat caps so near-capped stats are handled correctly.
4. **Per-stat spirit burst exclusion** — checkboxes in the Unity Cup config to ignore bursts on chosen stats until Senior Year Late December.
5. **Clock retries for lost team races** — the Team Showdown handler reads the result banner and uses an alarm clock to retry losses, respecting the existing clock use limit.
6. **Training logic hole fixes** — lanes are always parsed so ESBs are never silently skipped, and projected stat gains feed the lane score so big multi-stat Unity Cup team lanes compete with card-stacked lanes.
7. **Dewloren flowchart mode** — optional toggle that replaces score-based training with Dewloren's community flowchart (point table plus tiered rest/infirmary/recreation/training decisions). Covered by unit tests.
8. **Widened Team Showdown title search box** so Unity Cup 2.0 screens are recognized.

## Web UI and run control

1. **Loop run limits** — Execution Mode consolidated to Loop and Team Trials; Loop takes a Number of Runs dropdown (infinite or 1–100). Run counts persist across the bot's post-run restarts (including a fix for counts never registering).
2. **Run count display** — task panels show "Run 3 of 10" (or "Run 3" for infinite loops).
3. **Stop After Run button** — finishes the current career cleanly instead of hard-stopping, and survives the post-run process restart. The status pill now live-updates (running / finishing / stopped) via a new bot status endpoint.
4. **Add Missing Skill form** — the skill picker loads the skill database from the server at runtime, and a webform adds new skills (with the Evolved rarity) without a restart.
5. **Add Missing Event form** — the event list is runtime-loaded and shows only your overrides by default (search or toggle for the full list), with a webform to add missing events.
6. **Race schedule presets** — the Race Options panel gained a preset dropdown with New / Override / Delete / Apply. Applying a preset replaces the current race selection. Four schedules ship with the repo — Triple Crown, Triple Tiara, Triple Crown Dirt and Triple Tiara Dirt — and your own presets are saved per-file under `userdata/umamusume/race_presets/`. A personal preset shadows a shipped one of the same name, and shipped presets can't be deleted; delete your copy and the shipped version reappears.
7. **Skill presets** — the same four actions in the Skills section, saved under `userdata/umamusume/skill_presets/`. A preset records the whole configuration: selected skills, which priority bucket each sits in (and how many buckets exist), the blacklist, "learn only user-provided skills", the skill-point threshold, "manual purchase at end" and "buy skills only post-career".
8. **Buy skills only post-career** — a toggle in Skill Settings that suppresses the mid-career skill-point trigger, so points accumulate untouched until the end-of-career skill sweep, which then buys down your priority list with the full stockpile. Combines with "manual purchase at end" if you want to spend them yourself.
9. **Borrowing Support Card menu rebuilt** — the picker is generated from the game's own master database (all 109 SSRs; R and SR cards are skipped since borrowing one is rare) instead of a hardcoded list that carried untranslated titles inherited from the upstream CN project (`队形: PARTY` is really *Party Formation*) and placeholders like "Event SSR". Card art is gone in favour of a text list of title and character, sortable by either, and the type tabs now include Friend and Group, so those cards are selectable for the first time. See [Maintenance scripts](#maintenance-scripts) for regenerating the list after a game update.

## Maintenance scripts

1. **`export_support_cards.py`** — regenerates `web/src/assets/support_cards.json`, the card list behind the Borrowing Support Card picker, from `master.mdb` (the SQLite master database the Global client stores its game data in, under `AppData\LocalLow\Cygames\Umamusume\master\`). Titles come straight from the game's own English text, which matters because the bot OCRs the card title on the borrow screen and fuzzy-matches it against the name saved in the task — a title that differs from the game's wording breaks card selection. Run it after a game update adds or renames cards, then rebuild the web UI:

   ```bash
   py -3.10 export_support_cards.py && cd web && npx vite build
   ```

   Use `--db` to read a copy of `master.mdb` from elsewhere (another PC, an emulator pull). The database is only ever opened read-only.

## Reliability and debugging

1. **Unknown events click the top choice** instead of stalling the run.
2. **File logging toggle** — `bot.log.file_enabled` in config.yaml writes one log file per bot start to `userdata/logs/`, capturing per-lane scoring and decision lines so finished runs can be audited.
3. **Disabled training lanes** — some uma have events that lock every training but one. Clicking a locked lane does nothing and the screen never changes, so the bot used to click its chosen lane until the repetitive-click guard restarted the game, landing right back on the same locked turn. A lane that hasn't responded after three visits to the training screen is now treated as disabled and the remaining lanes are tried in turn; if every lane refuses, the bot rests instead of looping.
4. **Screen recognition race fixed** — screen detection runs one worker per known screen and returns as soon as one matches, but the losing workers keep running and used to append their result to a list shared across frames. A late result could then be picked up on the *next* screenshot, running the previous screen's handler against the current screen and misclicking during transitions. Results are now per call.
5. **Cache purge on stop actually runs** — `Executor.stop()` called `purge_all` without importing it, so the template/OCR cache purge had never run; the resulting `NameError` was swallowed by a bare `except`.
6. **Startup race after the post-run restart** — the executor's "busy" flag defaulted to true and was only cleared by a path that a restored-active scheduler could skip, leaving the scheduler waiting forever on an executor that was never running. Since the bot soft-restarts after every career, that race was rolled every run.
7. **Scheduler survives a bad task** — the scheduling loop is wrapped so one task with, say, an invalid cron expression logs a traceback instead of silently killing the thread and leaving the web UI responsive but nothing ever scheduled.
8. **Tasks survive a crash** — `userdata/saved_tasks.json` was a one-shot handoff across the post-run restart: written only when a run ended, and deleted the moment it was read. Between runs the only copy of your task list lived in process memory, so any crash, kill or crash-loop lost the whole configuration. It is now written whenever a task is added or deleted, kept after loading, and written atomically so a crash mid-write can't truncate it.
9. **Partial spark reads are re-read** — rows on the sparks screen are skipped when their crop comes out undersized, which happens while the list is still rendering. A read missing the blue or pink spark turned a roll that satisfied your targets into a miss, buying an unnecessary 30 TP reroll. Every uma finishes with one blue and one pink spark, so a read missing either is now retried before the bot decides.
