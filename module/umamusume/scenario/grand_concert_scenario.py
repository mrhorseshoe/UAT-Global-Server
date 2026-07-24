import re
import cv2

from .base_scenario import BaseScenario
from module.umamusume.asset import *
from module.umamusume.define import ScenarioType, SupportCardFavorLevel, SupportCardType
from module.umamusume.types import SupportCardInfo
from bot.recog.image_matcher import image_match, compare_color_equal
from module.umamusume.asset.template import *
from bot.recog.ocr import ocr_digits

import bot.base.log as logger
log = logger.get_logger(__name__)


class GrandConcertScenario(BaseScenario):
    """Our Grand Concert (Global, July 2026).

    The training-select screen looks different from Aoharu's (circular
    portraits, narrower column) but sits on the same 115px pitch, and both
    Aoharu parsers were validated unchanged against the Phase 0 captures. They
    are reused here minus the spirit-burst / extreme-spirit-burst detection,
    which has no equivalent on this scenario.

    The main menu does differ: a left rail pushed the turns box up, so the date
    crops below are scenario-specific.
    """

    def __init__(self):
        super().__init__()

    def scenario_type(self) -> ScenarioType:
        return ScenarioType.SCENARIO_TYPE_GRAND_CONCERT

    def scenario_name(self) -> str:
        return "Our Grand Concert"

    def get_date_img(self, img: any) -> any:
        return img[40:66, 160:380]

    def get_turn_to_race_img(self, img: any) -> any:
        return img[55:118, 15:150]

    def parse_training_result(self, img: any) -> list[int]:
        # Digit OCR, same regions as Aoharu: verified the gains land in the
        # expected x ranges on both lanes.
        sub_img_speed_incr = img[800:830, 30:140]
        sub_img_speed_incr = cv2.copyMakeBorder(sub_img_speed_incr, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=(255, 255, 255))
        speed_incr_text = ocr_digits(sub_img_speed_incr)
        speed_incr_text = re.sub("\\D", "", speed_incr_text)

        sub_img_speed_incr_extra = img[760:800, 30:140]
        sub_img_speed_incr_extra = cv2.copyMakeBorder(sub_img_speed_incr_extra, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=(255, 255, 255))
        speed_incr_extra_text = ocr_digits(sub_img_speed_incr_extra)
        speed_incr_extra_text = re.sub("\\D", "", speed_incr_extra_text)

        sub_img_stamina_incr = img[800:830, 140:250]
        sub_img_stamina_incr = cv2.copyMakeBorder(sub_img_stamina_incr, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=(255, 255, 255))
        stamina_incr_text = ocr_digits(sub_img_stamina_incr)
        stamina_incr_text = re.sub("\\D", "", stamina_incr_text)

        sub_img_stamina_incr_extra = img[760:800, 140:250]
        sub_img_stamina_incr_extra = cv2.copyMakeBorder(sub_img_stamina_incr_extra, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=(255, 255, 255))
        stamina_incr_extra_text = ocr_digits(sub_img_stamina_incr_extra)
        stamina_incr_extra_text = re.sub("\\D", "", stamina_incr_extra_text)

        sub_img_power_incr = img[800:830, 250:360]
        sub_img_power_incr = cv2.copyMakeBorder(sub_img_power_incr, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=(255, 255, 255))
        power_incr_text = ocr_digits(sub_img_power_incr)
        power_incr_text = re.sub("\\D", "", power_incr_text)

        sub_img_power_incr_extra = img[760:800, 250:360]
        sub_img_power_incr_extra = cv2.copyMakeBorder(sub_img_power_incr_extra, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=(255, 255, 255))
        power_incr_extra_text = ocr_digits(sub_img_power_incr_extra)
        power_incr_extra_text = re.sub("\\D", "", power_incr_extra_text)

        sub_img_will_incr = img[800:830, 360:470]
        sub_img_will_incr = cv2.copyMakeBorder(sub_img_will_incr, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=(255, 255, 255))
        will_incr_text = ocr_digits(sub_img_will_incr)
        will_incr_text = re.sub("\\D", "", will_incr_text)

        sub_img_will_incr_extra = img[760:800, 360:470]
        sub_img_will_incr_extra = cv2.copyMakeBorder(sub_img_will_incr_extra, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=(255, 255, 255))
        will_incr_extra_text = ocr_digits(sub_img_will_incr_extra)
        will_incr_extra_text = re.sub("\\D", "", will_incr_extra_text)

        sub_img_intelligence_incr = img[800:830, 470:580]
        sub_img_intelligence_incr = cv2.copyMakeBorder(sub_img_intelligence_incr, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=(255, 255, 255))
        intelligence_incr_text = ocr_digits(sub_img_intelligence_incr)
        intelligence_incr_text = re.sub("\\D", "", intelligence_incr_text)

        sub_img_intelligence_incr_extra = img[760:800, 470:580]
        sub_img_intelligence_incr_extra = cv2.copyMakeBorder(sub_img_intelligence_incr_extra, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=(255, 255, 255))
        intelligence_incr_extra_text = ocr_digits(sub_img_intelligence_incr_extra)
        intelligence_incr_extra_text = re.sub("\\D", "", intelligence_incr_extra_text)

        sub_img_skill_point_incr = img[800:830, 588:695]
        sub_img_skill_point_incr = cv2.copyMakeBorder(sub_img_skill_point_incr, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=(255, 255, 255))
        skill_point_incr_text = ocr_digits(sub_img_skill_point_incr)
        skill_point_incr_text = re.sub("\\D", "", skill_point_incr_text)

        sub_img_skill_point_incr_extra = img[760:800, 588:695]
        sub_img_skill_point_incr_extra = cv2.copyMakeBorder(sub_img_skill_point_incr_extra, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=(255, 255, 255))
        skill_point_incr_extra_text = ocr_digits(sub_img_skill_point_incr_extra)
        skill_point_incr_extra_text = re.sub("\\D", "", skill_point_incr_extra_text)

        speed_icr = (0 if speed_incr_text == "" else int(speed_incr_text)) + (0 if speed_incr_extra_text == "" else int(speed_incr_extra_text))
        stamina_incr = (0 if stamina_incr_text == "" else int(stamina_incr_text)) + (0 if stamina_incr_extra_text == "" else int(stamina_incr_extra_text))
        power_incr = (0 if power_incr_text == "" else int(power_incr_text)) + (0 if power_incr_extra_text == "" else int(power_incr_extra_text))
        will_incr = (0 if will_incr_text == "" else int(will_incr_text)) + (0 if will_incr_extra_text == "" else int(will_incr_extra_text))
        intelligence_incr = (0 if intelligence_incr_text == "" else int(intelligence_incr_text)) + (0 if intelligence_incr_extra_text == "" else int(intelligence_incr_extra_text))
        skill_point_incr = (0 if skill_point_incr_text == "" else int(skill_point_incr_text)) + (0 if skill_point_incr_extra_text == "" else int(skill_point_incr_extra_text))

        return [speed_icr, stamina_incr, power_incr, will_incr, intelligence_incr, skill_point_incr]

    def parse_training_support_card(self, img: any) -> list[SupportCardInfo]:
        base_x = 550
        base_y = 177
        inc = 115
        support_card_list_info_result: list[SupportCardInfo] = []

        for i in range(5):
            roi = img[base_y:base_y + inc, base_x: base_x + 145]
            if roi is None or getattr(roi, 'size', 0) == 0:
                base_y += inc
                continue

            roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

            # Favor detection (color). The sample lands exactly on the bond bar
            # on this layout. A card with no bond bar (an NPC) reads a colour
            # that matches no level, so it stays UNKNOWN and is skipped.
            roi_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
            favor_process_check_list = [roi_rgb[106, 56], roi_rgb[106, 60]]
            support_card_favor_process = SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_UNKNOWN
            for pix in favor_process_check_list:
                if compare_color_equal(pix, [255, 235, 120]):
                    support_card_favor_process = SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_4
                elif compare_color_equal(pix, [255, 173, 30]):
                    support_card_favor_process = SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_3
                elif compare_color_equal(pix, [162, 230, 30]):
                    support_card_favor_process = SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_2
                elif (compare_color_equal(pix, [42, 192, 255]) or compare_color_equal(pix, [109, 108, 117])):
                    support_card_favor_process = SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_1
                if support_card_favor_process != SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_UNKNOWN:
                    break

            # Support card type (template match for type icon only)
            support_card_type = SupportCardType.SUPPORT_CARD_TYPE_UNKNOWN
            match_center = None
            for ref, t in (
                (REF_SUPPORT_CARD_TYPE_SPEED, SupportCardType.SUPPORT_CARD_TYPE_SPEED),
                (REF_SUPPORT_CARD_TYPE_STAMINA, SupportCardType.SUPPORT_CARD_TYPE_STAMINA),
                (REF_SUPPORT_CARD_TYPE_POWER, SupportCardType.SUPPORT_CARD_TYPE_POWER),
                (REF_SUPPORT_CARD_TYPE_WILL, SupportCardType.SUPPORT_CARD_TYPE_WILL),
                (REF_SUPPORT_CARD_TYPE_INTELLIGENCE, SupportCardType.SUPPORT_CARD_TYPE_INTELLIGENCE),
                (REF_SUPPORT_CARD_TYPE_FRIEND, SupportCardType.SUPPORT_CARD_TYPE_FRIEND),
            ):
                r = image_match(roi_gray, ref)
                if r.find_match:
                    support_card_type = t
                    match_center = r.center_point
                    break

            if support_card_type == SupportCardType.SUPPORT_CARD_TYPE_UNKNOWN and support_card_favor_process != SupportCardFavorLevel.SUPPORT_CARD_FAVOR_LEVEL_UNKNOWN:
                support_card_type = SupportCardType.SUPPORT_CARD_TYPE_NPC

            h_local, w_local = roi.shape[:2]
            cx = base_x + (w_local // 2)
            cy = base_y + (h_local // 2)
            if isinstance(match_center, (tuple, list)) and len(match_center) >= 2:
                cx = base_x + int(match_center[0])
                cy = base_y + int(match_center[1])

            name_map = {
                SupportCardType.SUPPORT_CARD_TYPE_SPEED: "support_card_type_speed",
                SupportCardType.SUPPORT_CARD_TYPE_STAMINA: "support_card_type_stamina",
                SupportCardType.SUPPORT_CARD_TYPE_POWER: "support_card_type_power",
                SupportCardType.SUPPORT_CARD_TYPE_WILL: "support_card_type_will",
                SupportCardType.SUPPORT_CARD_TYPE_INTELLIGENCE: "support_card_type_intelligence",
                SupportCardType.SUPPORT_CARD_TYPE_FRIEND: "support_card_type_friend",
            }
            info = SupportCardInfo(
                name=name_map.get(support_card_type, "support_card"),
                card_type=support_card_type,
                favor=support_card_favor_process,
                can_incr_special_training=False,
                spirit_explosion=False,
                extreme_spirit_explosion=False
            )
            info.center = (cx, cy)
            support_card_list_info_result.append(info)

            base_y += inc

        return support_card_list_info_result
