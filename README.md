# UAT-Global-Server — mrhorseshoe's fork

Fork of [TomerGamerTV/UAT-Global-Server](https://github.com/TomerGamerTV/UAT-Global-Server).
All changes below were added on top of the upstream project.

## Game update fixes (July 2026 Global update)

1. **Scenario select fix** — the update rendered scenario key art ~5% larger, breaking template matching. Re-cropped both scenario templates and decoupled the carousel swipe count from the scenario enum (a third scenario card exists now).
2. **New dirt G1 races** — added Nambu Hai (Classic and Senior year), Kawasaki Kinen, Kashiwa Kinen, and Zen-Nippon Junior Yushun to the race database, Race Settings menu, and banner templates.
3. **Spark reroll screen option** — the update added an end-of-run offer to reroll sparks for 30 TP. A new tickbox (single-run Loop mode only) stops the bot on that screen so you can decide manually; otherwise the bot confirms without rerolling.
4. **Automated spark reroll** — an "Automate spark reroll" tickbox with a Spark Reroll Options popup: check the blue (stat) and pink (track/distance/style) sparks you want, each with its own minimum star count (1–3), and pick how the groups combine — OR keeps the roll when any desired spark hits its stars, AND requires both a desired blue and a desired pink spark (multiple checks within a group always mean "any of these", since an uma carries one of each). If the check fails the bot rerolls (30 TP). On the Spark Selection carousel it then compares the two sets: the rerolled set is kept if it satisfies the check; if neither set does, it keeps the one with more white sparks — read directly from the scroll bar length (a shorter thumb means more sparks below the fold), which is more reliable than scrolling each list. Ties fall back to total stars. Each step is captured to `screenshot/spark_reroll/` for troubleshooting.
   - **Insufficient TP** — an optional "Spend carats to restore TP" toggle lets the bot top up TP when a career ends with less than the 30 TP a reroll needs: it uses a non-chocolate TP recovery item if you have one, otherwise carats. Chocolate TP items are never spent. Left off, the bot keeps the original sparks instead of spending anything.

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
9. **Borrowing Support Card menu rebuilt** — the picker is generated from the game's own master database (all 109 SSRs; R and SR cards are skipped since borrowing one is rare) instead of a hardcoded list that carried untranslated titles inherited from the upstream CN project (`队形: PARTY` is really *Party Formation*) and placeholders like "Event SSR". Card art is gone in favour of a text list showing rarity, title and character, and the type tabs now include Friend and Group, so those cards are selectable for the first time. See [Maintenance scripts](#maintenance-scripts) for regenerating the list after a game update.

## Maintenance scripts

1. **`export_support_cards.py`** — regenerates `web/src/assets/support_cards.json`, the card list behind the Borrowing Support Card picker, from `master.mdb` (the SQLite master database the Global client stores its game data in, under `AppData\LocalLow\Cygames\Umamusume\master\`). Titles come straight from the game's own English text, which matters because the bot OCRs the card title on the borrow screen and fuzzy-matches it against the name saved in the task — a title that differs from the game's wording breaks card selection. Run it after a game update adds or renames cards, then rebuild the web UI:

   ```bash
   py -3.10 export_support_cards.py && cd web && npx vite build
   ```

   Use `--db` to read a copy of `master.mdb` from elsewhere (another PC, an emulator pull). The database is only ever opened read-only.

## Reliability and debugging

1. **Unknown events click the top choice** instead of stalling the run.
2. **File logging toggle** — `bot.log.file_enabled` in config.yaml writes one log file per bot start to `userdata/logs/`, capturing per-lane scoring and decision lines so finished runs can be audited.
3. **Screen recognition race fixed** — screen detection runs one worker per known screen and returns as soon as one matches, but the losing workers keep running and used to append their result to a list shared across frames. A late result could then be picked up on the *next* screenshot, running the previous screen's handler against the current screen and misclicking during transitions. Results are now per call.
4. **Cache purge on stop actually runs** — `Executor.stop()` called `purge_all` without importing it, so the template/OCR cache purge had never run; the resulting `NameError` was swallowed by a bare `except`.
5. **Startup race after the post-run restart** — the executor's "busy" flag defaulted to true and was only cleared by a path that a restored-active scheduler could skip, leaving the scheduler waiting forever on an executor that was never running. Since the bot soft-restarts after every career, that race was rolled every run.
6. **Scheduler survives a bad task** — the scheduling loop is wrapped so one task with, say, an invalid cron expression logs a traceback instead of silently killing the thread and leaving the web UI responsive but nothing ever scheduled.
