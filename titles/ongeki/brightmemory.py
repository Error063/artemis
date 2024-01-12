from datetime import date, datetime, timedelta
from typing import Any, Dict
import pytz
import json

from core.config import CoreConfig
from titles.ongeki.base import OngekiBase
from titles.ongeki.bright import OngekiBright
from titles.ongeki.const import OngekiConstants
from titles.ongeki.config import OngekiConfig


class OngekiBrightMemory(OngekiBright):
    def __init__(self, core_cfg: CoreConfig, game_cfg: OngekiConfig) -> None:
        super().__init__(core_cfg, game_cfg)
        self.version = OngekiConstants.VER_ONGEKI_BRIGHT_MEMORY

    async def handle_get_game_setting_api_request(self, data: Dict) -> Dict:
        ret = await super().handle_get_game_setting_api_request(data)
        ret["gameSetting"]["dataVersion"] = "1.35.00"
        ret["gameSetting"]["onlineDataVersion"] = "1.35.00"
        ret["gameSetting"]["maxCountCharacter"] = 50
        ret["gameSetting"]["maxCountCard"] = 300
        ret["gameSetting"]["maxCountItem"] = 300
        ret["gameSetting"]["maxCountMusic"] = 50
        ret["gameSetting"]["maxCountMusicItem"] = 300
        ret["gameSetting"]["maxCountRivalMusic"] = 300
        return ret

    async def handle_get_user_memory_chapter_api_request(self, data: Dict) -> Dict:
        memories = await self.data.item.get_memorychapters(data["userId"])
        if not memories:
            return {
                "userId": data["userId"],
                "length": 6,
                "userMemoryChapterList": [
                    {
                        "gaugeId": 0,
                        "isClear": False,
                        "gaugeNum": 0,
                        "chapterId": 70001,
                        "jewelCount": 0,
                        "isBossWatched": False,
                        "isStoryWatched": False,
                        "isDialogWatched": False,
                        "isEndingWatched": False,
                        "lastPlayMusicId": 0,
                        "lastPlayMusicLevel": 0,
                        "lastPlayMusicCategory": 0,
                    },
                    {
                        "gaugeId": 0,
                        "isClear": False,
                        "gaugeNum": 0,
                        "chapterId": 70002,
                        "jewelCount": 0,
                        "isBossWatched": False,
                        "isStoryWatched": False,
                        "isDialogWatched": False,
                        "isEndingWatched": False,
                        "lastPlayMusicId": 0,
                        "lastPlayMusicLevel": 0,
                        "lastPlayMusicCategory": 0,
                    },
                    {
                        "gaugeId": 0,
                        "isClear": False,
                        "gaugeNum": 0,
                        "chapterId": 70003,
                        "jewelCount": 0,
                        "isBossWatched": False,
                        "isStoryWatched": False,
                        "isDialogWatched": False,
                        "isEndingWatched": False,
                        "lastPlayMusicId": 0,
                        "lastPlayMusicLevel": 0,
                        "lastPlayMusicCategory": 0,
                    },
                    {
                        "gaugeId": 0,
                        "isClear": False,
                        "gaugeNum": 0,
                        "chapterId": 70004,
                        "jewelCount": 0,
                        "isBossWatched": False,
                        "isStoryWatched": False,
                        "isDialogWatched": False,
                        "isEndingWatched": False,
                        "lastPlayMusicId": 0,
                        "lastPlayMusicLevel": 0,
                        "lastPlayMusicCategory": 0,
                    },
                    {
                        "gaugeId": 0,
                        "isClear": False,
                        "gaugeNum": 0,
                        "chapterId": 70005,
                        "jewelCount": 0,
                        "isBossWatched": False,
                        "isStoryWatched": False,
                        "isDialogWatched": False,
                        "isEndingWatched": False,
                        "lastPlayMusicId": 0,
                        "lastPlayMusicLevel": 0,
                        "lastPlayMusicCategory": 0,
                    },
                    {
                        "gaugeId": 0,
                        "isClear": False,
                        "gaugeNum": 0,
                        "chapterId": 70099,
                        "jewelCount": 0,
                        "isBossWatched": False,
                        "isStoryWatched": False,
                        "isDialogWatched": False,
                        "isEndingWatched": False,
                        "lastPlayMusicId": 0,
                        "lastPlayMusicLevel": 0,
                        "lastPlayMusicCategory": 0,
                    },
                ],
            }

        memory_chp = []
        for chp in memories:
            tmp = chp._asdict()
            tmp.pop("id")
            tmp.pop("user")
            memory_chp.append(tmp)

        return {
            "userId": data["userId"],
            "length": len(memory_chp),
            "userMemoryChapterList": memory_chp,
        }

    async def handle_get_game_music_release_state_api_request(self, data: Dict) -> Dict:
        return {"techScore": 0, "cardNum": 0}
