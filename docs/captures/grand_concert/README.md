# Grand Concert reference captures

Curated fixtures from the Phase 0 capture run (Global, July 2026). Every
coordinate, crop and OCR claim in `docs/GRAND_CONCERT_NOTES.md` was measured
against these, and they double as regression fixtures for the parsers Phase 1
and Phase 2 will build - the shop set in particular already caught two OCR
bugs that only appear with real gameplay values.

All are 720x1280, straight from `adb exec-out screencap`, losslessly
recompressed and verified pixel-identical to the originals. **Do not crop,
rescale or re-encode them** - the measurements are pixel-exact.

23 files, ~13 MB. This is a subset of a ~40 MB capture run; the rest
(intermediate shop sets, zoomed crops, annotated overlays and working images)
stayed local, since they duplicate what these cover.

## Scenario select

- **`02_grand_concert_f2.png`** — Grand Concert carousel card; source of scenario_grand_concert.png
- **`01_scenario_select_a.png`** — URA Finale card; negative sample for the scenario template

## Career start and end

- **`04_final_check.png`** — Final Confirmation; Independent Training tab, Start Career coords
- **`78_career_end.png`** — Career end; 3-button row that breaks both FINISH click points

## Main menu variants

- **`05_main_menu_predebut.png`** — Pre-debut menu; the flat grey locked button that gave the 4-slot pitch
- **`13_main_menu_active.png`** — Active menu; PP panel, Hype gauge, Lessons button, energy bar
- **`49_predebut_race_menu.png`** — Race-day menu; 3-button layout, GOAL turn box

## Training and recreation

- **`35_training_select.png`** — Training select (Speed); support-card column, gain row, failure badge
- **`36_training_stamina_1click.png`** — Training select (Stamina) after one tap; proves tap-to-preview
- **`54_recreation_light_hello.png`** — Recreation menu; 5 pal pips at the existing sample coords

## Lesson shop (OCR / affordability regression suite)

- **`22_lesson_shop.png`** — Shop: 3 techniques, ALL affordable (bright cost rows ~230)
- **`33_after_learn.png`** — Shop: 3 songs, ALL unaffordable (grey cost rows ~161)
- **`43_shop_mixed_affordability.png`** — Shop: MIXED affordability; the A/B that killed badge matching
- **`47_shop_set5.png`** — Shop: balance 11 - the case that fails OCR without 2x upscale
- **`64_shop_energy_technique.png`** — Shop: energy technique (blue icon) beside stat/dual techniques
- **`72_shop_set13.png`** — Shop: balance 138 - the 3-digit case that clipped the old crop

## Lesson confirmation dialogs

- **`29_lesson_detail_learnable.png`** — Lesson confirm (technique); Learn button under the INFO auto-buy hazard
- **`44_song_confirm.png`** — Lesson confirm (song); Training/Concert bonus rows, Hype preview

## Concert screens

- **`27_concert_info.png`** — Concert Info; hype gauge, songs learned, concert bonus totals
- **`60_post_concert_popup.png`** — Bonuses Updated popup; the stall, source of the detection template
- **`62_post_concert_detail.png`** — Active Concert Bonuses; the second modal reached via Confirm

## Events

- **`09_event_tutorial_prompt.png`** — Event with 2 choices; REF_SELECTOR fails, dialogue1..5 fallback works
- **`77_skill_choice_event.png`** — Closer Together; 5-option scenario skill event

## Notes

- `43_shop_mixed_affordability.png` is the most valuable single fixture: it is
  the only capture with affordable and unaffordable cards side by side, which
  is what proved cost-row brightness works and the "Learnable!" badge does not.
- `47_shop_set5.png` (balance 11) and `72_shop_set13.png` (balance 138) are kept
  specifically because each breaks a naive OCR implementation. Any change to the
  balance reader should be tested against both.
- `36_training_stamina_1click.png` was taken one tap after `35_training_select.png`;
  together they prove a single tap previews a lane rather than committing it.
