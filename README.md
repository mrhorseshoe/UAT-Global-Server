# UAT-Global-Server — mrhorseshoe's fork

Fork of [TomerGamerTV/UAT-Global-Server](https://github.com/TomerGamerTV/UAT-Global-Server).
All changes below were added on top of the upstream project.

## Game update fixes (July 2026 Global update)

1. **Scenario select fix** — the update rendered scenario key art ~5% larger, breaking template matching. Re-cropped both scenario templates and decoupled the carousel swipe count from the scenario enum (a third scenario card exists now).
2. **New dirt G1 races** — added Nambu Hai (Classic and Senior year), Kawasaki Kinen, Kashiwa Kinen, and Zen-Nippon Junior Yushun to the race database, Race Settings menu, and banner templates.
3. **Spark reroll screen option** — the update added an end-of-run offer to reroll sparks for 30 TP. A new tickbox (single-run Loop mode only) stops the bot on that screen so you can decide manually; otherwise the bot confirms without rerolling.
4. **Automated spark reroll** — an "Automate spark reroll" tickbox with a Spark Reroll Options popup: check the blue (stat) and pink (track/distance/style) sparks you want and a minimum star count (1–3). At the spark screen the bot keeps the roll if any desired spark is present at that star level, otherwise it rerolls (30 TP). On the Spark Selection carousel it then compares the two sets: the rerolled set is kept if it satisfies the check; if neither set does, it keeps the one with more white sparks — read directly from the scroll bar length (a shorter thumb means more sparks below the fold), which is more reliable than scrolling each list. Ties fall back to total stars. Each step is captured to `screenshot/spark_reroll/` for troubleshooting.
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

## Reliability and debugging

1. **Unknown events click the top choice** instead of stalling the run.
2. **File logging toggle** — `bot.log.file_enabled` in config.yaml writes one log file per bot start to `userdata/logs/`, capturing per-lane scoring and decision lines so finished runs can be audited.
