import json
from decimal import Decimal
from base64 import b64encode
from typing import Any, Dict
from hashlib import md5
from datetime import datetime

from core.config import CoreConfig
from core.data import Data, cached
from .config import CxbConfig
from .base import CxbBase
from .const import CxbConstants


class CxbRev(CxbBase):
    def __init__(self, cfg: CoreConfig, game_cfg: CxbConfig) -> None:
        super().__init__(cfg, game_cfg)
        self.version = CxbConstants.VER_CROSSBEATS_REV

    async def handle_data_path_list_request(self, data: Dict) -> Dict:
        return {"data": ""}

    async def handle_data_putlog_request(self, data: Dict) -> Dict:
        if data["putlog"]["type"] == "ResultLog":
            score_data = json.loads(data["putlog"]["data"])
            userid = score_data["usid"]

            await self.data.score.put_playlog(
                userid,
                score_data["mcode"],
                score_data["difficulty"],
                score_data["score"],
                int(Decimal(score_data["clearrate"]) * 100),
                score_data["flawless"],
                score_data["super"],
                score_data["cool"],
                score_data["fast"],
                score_data["fast2"],
                score_data["slow"],
                score_data["slow2"],
                score_data["fail"],
                score_data["combo"],
            )
            return {"data": True}
        return {"data": True}

    @cached(lifetime=86400)
    async def handle_data_music_list_request(self, data: Dict) -> Dict:
        ret_str = ""
        with open(r"titles/cxb/data/rss/MusicArchiveList.csv") as music:
            lines = music.readlines()
            for line in lines:
                line_split = line.split(",")
                ret_str += f"{line_split[0]},{line_split[1]},{line_split[2]},{line_split[3]},{line_split[4]},{line_split[5]},{line_split[6]},{line_split[7]},{line_split[8]},{line_split[9]},{line_split[10]},{line_split[11]},{line_split[12]},{line_split[13]},{line_split[14]},\r\n"

        return {"data": ret_str}

    @cached(lifetime=86400)
    async def handle_data_item_list_icon_request(self, data: Dict) -> Dict:
        ret_str = "\r\n#ItemListIcon\r\n"
        with open(
            r"titles/cxb/data/rss/Item/ItemArchiveList_Icon.csv", encoding="utf-8"
        ) as item:
            lines = item.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"
        return {"data": ret_str}

    @cached(lifetime=86400)
    async def handle_data_item_list_skin_notes_request(self, data: Dict) -> Dict:
        ret_str = "\r\n#ItemListSkinNotes\r\n"
        with open(
            r"titles/cxb/data/rss/Item/ItemArchiveList_SkinNotes.csv", encoding="utf-8"
        ) as item:
            lines = item.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"
        return {"data": ret_str}

    @cached(lifetime=86400)
    async def handle_data_item_list_skin_effect_request(self, data: Dict) -> Dict:
        ret_str = "\r\n#ItemListSkinEffect\r\n"
        with open(
            r"titles/cxb/data/rss/Item/ItemArchiveList_SkinEffect.csv", encoding="utf-8"
        ) as item:
            lines = item.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"
        return {"data": ret_str}

    @cached(lifetime=86400)
    async def handle_data_item_list_skin_bg_request(self, data: Dict) -> Dict:
        ret_str = "\r\n#ItemListSkinBg\r\n"
        with open(
            r"titles/cxb/data/rss/Item/ItemArchiveList_SkinBg.csv", encoding="utf-8"
        ) as item:
            lines = item.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"
        return {"data": ret_str}

    @cached(lifetime=86400)
    async def handle_data_item_list_title_request(self, data: Dict) -> Dict:
        ret_str = "\r\n#ItemListTitle\r\n"
        with open(
            r"titles/cxb/data/rss/Item/ItemList_Title.csv", encoding="shift-jis"
        ) as item:
            lines = item.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"
        return {"data": ret_str}

    @cached(lifetime=86400)
    async def handle_data_shop_list_music_request(self, data: Dict) -> Dict:
        ret_str = "\r\n#ShopListMusic\r\n"
        with open(
            r"titles/cxb/data/rss/Shop/ShopList_Music.csv", encoding="shift-jis"
        ) as shop:
            lines = shop.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"
        return {"data": ret_str}

    @cached(lifetime=86400)
    async def handle_data_shop_list_icon_request(self, data: Dict) -> Dict:
        ret_str = "\r\n#ShopListIcon\r\n"
        with open(
            r"titles/cxb/data/rss/Shop/ShopList_Icon.csv", encoding="shift-jis"
        ) as shop:
            lines = shop.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"
        return {"data": ret_str}

    @cached(lifetime=86400)
    async def handle_data_shop_list_title_request(self, data: Dict) -> Dict:
        ret_str = "\r\n#ShopListTitle\r\n"
        with open(
            r"titles/cxb/data/rss/Shop/ShopList_Title.csv", encoding="shift-jis"
        ) as shop:
            lines = shop.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"
        return {"data": ret_str}

    async def handle_data_shop_list_skin_hud_request(self, data: Dict) -> Dict:
        return {"data": ""}

    async def handle_data_shop_list_skin_arrow_request(self, data: Dict) -> Dict:
        return {"data": ""}

    async def handle_data_shop_list_skin_hit_request(self, data: Dict) -> Dict:
        return {"data": ""}

    @cached(lifetime=86400)
    async def handle_data_shop_list_sale_request(self, data: Dict) -> Dict:
        ret_str = "\r\n#ShopListSale\r\n"
        with open(
            r"titles/cxb/data/rss/Shop/ShopList_Sale.csv", encoding="shift-jis"
        ) as shop:
            lines = shop.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"
        return {"data": ret_str}

    async def handle_data_extra_stage_list_request(self, data: Dict) -> Dict:
        return {"data": ""}

    @cached(lifetime=86400)
    async def handle_data_exxxxx_request(self, data: Dict) -> Dict:
        extra_num = int(data["dldate"]["filetype"][-4:])
        ret_str = ""
        with open(
            rf"titles/cxb/data/rss/Ex000{extra_num}.csv", encoding="shift-jis"
        ) as stage:
            lines = stage.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"
        return {"data": ret_str}

    async def handle_data_bonus_list10100_request(self, data: Dict) -> Dict:
        return {"data": ""}

    async def handle_data_free_coupon_request(self, data: Dict) -> Dict:
        return {"data": ""}

    @cached(lifetime=86400)
    async def handle_data_news_list_request(self, data: Dict) -> Dict:
        ret_str = ""
        with open(r"titles/cxb/data/rss/NewsList.csv", encoding="UTF-8") as news:
            lines = news.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"
        return {"data": ret_str}

    async def handle_data_tips_request(self, data: Dict) -> Dict:
        return {"data": ""}

    @cached(lifetime=86400)
    async def handle_data_license_request(self, data: Dict) -> Dict:
        ret_str = ""
        with open(r"titles/cxb/data/rss/License_Offline.csv", encoding="UTF-8") as lic:
            lines = lic.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"
        return {"data": ret_str}

    @cached(lifetime=86400)
    async def handle_data_course_list_request(self, data: Dict) -> Dict:
        ret_str = ""
        with open(
            r"titles/cxb/data/rss/Course/CourseList.csv", encoding="UTF-8"
        ) as course:
            lines = course.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"
        return {"data": ret_str}

    @cached(lifetime=86400)
    async def handle_data_csxxxx_request(self, data: Dict) -> Dict:
        # Removed the CSVs since the format isnt quite right
        extra_num = int(data["dldate"]["filetype"][-4:])
        ret_str = ""
        with open(
            rf"titles/cxb/data/rss/Course/Cs000{extra_num}.csv", encoding="shift-jis"
        ) as course:
            lines = course.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"
        return {"data": ret_str}

    @cached(lifetime=86400)
    async def handle_data_mission_list_request(self, data: Dict) -> Dict:
        ret_str = ""
        with open(
            r"titles/cxb/data/rss/MissionList.csv", encoding="shift-jis"
        ) as mission:
            lines = mission.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"
        return {"data": ret_str}

    async def handle_data_mission_bonus_request(self, data: Dict) -> Dict:
        return {"data": ""}

    async def handle_data_unlimited_mission_request(self, data: Dict) -> Dict:
        return {"data": ""}

    @cached(lifetime=86400)
    async def handle_data_event_list_request(self, data: Dict) -> Dict:
        ret_str = ""
        with open(
            r"titles/cxb/data/rss/Event/EventArchiveList.csv", encoding="shift-jis"
        ) as mission:
            lines = mission.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"
        return {"data": ret_str}

    async def handle_data_event_music_list_request(self, data: Dict) -> Dict:
        return {"data": ""}

    async def handle_data_event_mission_list_request(self, data: Dict) -> Dict:
        return {"data": ""}

    async def handle_data_event_achievement_single_high_score_list_request(
        self, data: Dict
    ) -> Dict:
        return {"data": ""}

    async def handle_data_event_achievement_single_accumulation_request(
        self, data: Dict
    ) -> Dict:
        return {"data": ""}

    async def handle_data_event_ranking_high_score_list_request(self, data: Dict) -> Dict:
        return {"data": ""}

    async def handle_data_event_ranking_accumulation_list_request(self, data: Dict) -> Dict:
        return {"data": ""}

    async def handle_data_event_ranking_stamp_list_request(self, data: Dict) -> Dict:
        return {"data": ""}

    async def handle_data_event_ranking_store_list_request(self, data: Dict) -> Dict:
        return {"data": ""}

    async def handle_data_event_ranking_area_list_request(self, data: Dict) -> Dict:
        return {"data": ""}

    @cached(lifetime=86400)
    async def handle_data_event_stamp_list_request(self, data: Dict) -> Dict:
        ret_str = ""
        with open(
            r"titles/cxb/data/rss/Event/EventStampList.csv", encoding="shift-jis"
        ) as event:
            lines = event.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"
        return {"data": ret_str}

    async def handle_data_event_stamp_map_list_csxxxx_request(self, data: Dict) -> Dict:
        return {"data": "1,2,1,1,2,3,9,5,6,7,8,9,10,\r\n"}

    async def handle_data_server_state_request(self, data: Dict) -> Dict:
        return {"data": True}
