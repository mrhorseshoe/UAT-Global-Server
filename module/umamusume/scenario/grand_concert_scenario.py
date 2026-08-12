from .ura_scenario import URAScenario
from module.umamusume.define import ScenarioType

import bot.base.log as logger
log = logger.get_logger(__name__)


class GrandConcertScenario(URAScenario):
    """Our Grand Concert - "Brighter Together".

    Only scenario *selection* is implemented: the bot can find and pick this
    scenario in the carousel, which is all Independent Training needs, since
    the game plays the career itself. The screen parsing is inherited from URA
    and has not been checked against this scenario's own career UI, so a
    normal turn-by-turn career here is not supported yet.
    """

    def scenario_type(self) -> ScenarioType:
        return ScenarioType.SCENARIO_TYPE_GRAND_CONCERT

    def scenario_name(self) -> str:
        return "Our Grand Concert"
