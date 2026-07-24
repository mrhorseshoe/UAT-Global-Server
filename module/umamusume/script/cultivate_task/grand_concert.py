"""Our Grand Concert scenario-specific behaviour.

Kept out of cultivate.py deliberately: the existing `if scenario_type() ==
AOHARUHAI` pattern is working and earning ranks, so new logic lives here and
the shared scripts only reach in through the small helpers below.

Everything here was measured against docs/captures/grand_concert/; see
docs/GRAND_CONCERT_NOTES.md for the derivation of each number.
"""

from module.umamusume.asset.point import *
from module.umamusume.define import ScenarioType

import bot.base.log as logger
log = logger.get_logger(__name__)


# Shared point -> Grand Concert point. The bottom action row has four slots on
# this scenario (Infirmary / Recreation / Lessons / Races on a 164px pitch), so
# the shared coordinates land in gaps or on the wrong button; the career-end row
# gains a Lessons button and CULTIVATE_FINISH_CONFIRM would open the shop.
GRAND_CONCERT_POINTS = {
    CULTIVATE_MEDIC: GC_CULTIVATE_MEDIC,
    CULTIVATE_TRIP: GC_CULTIVATE_TRIP,
    CULTIVATE_RACE: GC_CULTIVATE_RACE,
    CULTIVATE_FINISH_LEARN_SKILL: GC_CULTIVATE_FINISH_LEARN_SKILL,
    CULTIVATE_FINISH_CONFIRM: GC_CULTIVATE_FINISH_CONFIRM,
}


def is_grand_concert(ctx) -> bool:
    try:
        return ctx.cultivate_detail.scenario.scenario_type() == ScenarioType.SCENARIO_TYPE_GRAND_CONCERT
    except Exception:
        return False


def gc_point(ctx, point):
    """Return the Grand Concert variant of `point`, or `point` unchanged on
    every other scenario."""
    if not is_grand_concert(ctx):
        return point
    return GRAND_CONCERT_POINTS.get(point, point)


def script_concert_bonuses_updated(ctx):
    """The post-concert "Bonuses Updated!" modal.

    Without this the screen matches no UI, every NOT_FOUND_UI heuristic misses,
    and the (719,1) fallback click cannot dismiss a modal - so the watchdog
    force-restarts the game roughly every 90s, straight back onto this popup.

    Close, not Confirm: Confirm opens "Active Concert Bonuses", whose only exit
    is a Close the generic INFO handler does not know how to press.
    """
    log.info("🎤 Post-concert bonuses popup - closing")
    ctx.ctrl.click_by_point(GC_CONCERT_BONUSES_CLOSE)


# Final confirmation screen: the career-mode tabs. The selected tab is green
# (B8 G208 R135), the unselected one near-white (B211 G215 R224). Single-pixel
# sampling can land on a letter glyph, so count green pixels over each band.
_TAB_BAND_Y = (205, 230)
_TAB_BAND_NORMAL_X = (30, 340)
_TAB_BAND_INDEPENDENT_X = (380, 690)
_TAB_SELECTED_BGR = (8, 208, 135)
_TAB_COLOUR_TOLERANCE = 30
# A band is only considered to carry a verdict once it holds this many pixels of
# the tab green; below that we are not looking at the tab row at all. The real
# tab fills ~6000 px of its band, and across the capture set no other screen
# puts more than 14 into either band, so this is a wide margin either way.
_TAB_MIN_GREEN_PIXELS = 500


def _count_tab_green(img) -> tuple[int, int]:
    """Counts of the selected-tab green in the (Normal Career, Independent
    Training) bands."""
    y1, y2 = _TAB_BAND_Y
    tb, tg, tr = _TAB_SELECTED_BGR
    tol = _TAB_COLOUR_TOLERANCE
    counts = []
    for x1, x2 in (_TAB_BAND_NORMAL_X, _TAB_BAND_INDEPENDENT_X):
        band = img[y1:y2, x1:x2]
        if band is None or getattr(band, 'size', 0) == 0:
            counts.append(0)
            continue
        band = band.astype(int)
        green = ((abs(band[:, :, 0] - tb) <= tol)
                 & (abs(band[:, :, 1] - tg) <= tol)
                 & (abs(band[:, :, 2] - tr) <= tol))
        counts.append(int(green.sum()))
    return counts[0], counts[1]


def ensure_normal_career_tab(ctx, img) -> bool:
    """Verify the Normal Career tab is selected on the final confirmation
    screen before the career is started.

    Returns True if it clicked the Normal Career tab, meaning the caller must
    not also click Start Career! this frame - script_info runs again on the
    next one and the check then passes.

    Returns False when Normal Career is already selected, and also when the
    screen carries no recognisable tab row (TITLE[33] is shared with the real
    Factor Confirmation dialog, which has no tabs). Not finding the tabs is not
    evidence of the wrong mode, so it must not block the click.
    """
    if not is_grand_concert(ctx) or img is None:
        return False
    try:
        normal_green, independent_green = _count_tab_green(img)
    except Exception as e:
        log.debug(f"Career-mode tab check failed: {e}")
        return False

    if max(normal_green, independent_green) < _TAB_MIN_GREEN_PIXELS:
        log.debug("No career-mode tab row on this screen - leaving it alone")
        return False

    log.info(f"Career-mode tabs - Normal: {normal_green} green px, Independent: {independent_green} green px")
    if normal_green >= independent_green:
        log.info("Normal Career is selected")
        return False

    log.warning("Independent Training is selected - switching to Normal Career")
    ctx.ctrl.click_by_point(GC_NORMAL_CAREER_TAB)
    return True


def dismiss_recreation_menu(ctx):
    """Close the Recreation menu after pal-stage detection.

    The shared code taps (5,5), an outside-the-dialog tap that is unverified on
    this scenario's menu. Cancel (360,918) was measured on the capture, so use
    it here.
    """
    if is_grand_concert(ctx):
        ctx.ctrl.click_by_point(GC_RECREATION_CANCEL)
    else:
        ctx.ctrl.click(5, 5)
