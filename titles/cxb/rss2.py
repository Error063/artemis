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


class CxbRevSunriseS2(CxbBase):
    def __init__(self, cfg: CoreConfig, game_cfg: CxbConfig) -> None:
        super().__init__(cfg, game_cfg)
        self.version = CxbConstants.VER_CROSSBEATS_REV_SUNRISE_S2_OMNI

    def handle_data_path_list_request(self, data: Dict) -> Dict:
        return {"data": ""}

    @cached(lifetime=86400)
    def handle_data_music_list_request(self, data: Dict) -> Dict:
        ret_str = ""
        with open(r"titles/cxb/data/rss2/MusicArchiveList.csv") as music:
            lines = music.readlines()
            for line in lines:
                line_split = line.split(",")
                ret_str += f"{line_split[0]},{line_split[1]},{line_split[2]},{line_split[3]},{line_split[4]},{line_split[5]},{line_split[6]},{line_split[7]},{line_split[8]},{line_split[9]},{line_split[10]},{line_split[11]},{line_split[12]},{line_split[13]},{line_split[14]},\r\n"

        return {"data": ret_str}

    @cached(lifetime=86400)
    def handle_data_item_list_detail_request(self, data: Dict) -> Dict:
        # ItemListIcon load
        ret_str = "#ItemListIcon\r\n"
        with open(
            r"titles/cxb/data/rss2/Item/ItemList_Icon.csv", encoding="utf-8"
        ) as item:
            lines = item.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"

        # ItemListTitle load
        ret_str += "\r\n#ItemListTitle\r\n"
        with open(
            r"titles/cxb/data/rss2/Item/ItemList_Title.csv", encoding="utf-8"
        ) as item:
            lines = item.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"

        return {"data": ret_str}

    @cached(lifetime=86400)
    def handle_data_shop_list_detail_request(self, data: Dict) -> Dict:
        # ShopListIcon load
        ret_str = "#ShopListIcon\r\n"
        with open(
            r"titles/cxb/data/rss2/Shop/ShopList_Icon.csv", encoding="utf-8"
        ) as shop:
            lines = shop.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"

        # ShopListMusic load
        ret_str += "\r\n#ShopListMusic\r\n"
        with open(
            r"titles/cxb/data/rss2/Shop/ShopList_Music.csv", encoding="utf-8"
        ) as shop:
            lines = shop.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"

        # ShopListSale load
        ret_str += "\r\n#ShopListSale\r\n"
        with open(
            r"titles/cxb/data/rss2/Shop/ShopList_Sale.csv", encoding="shift-jis"
        ) as shop:
            lines = shop.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"

        # ShopListSkinBg load
        ret_str += "\r\n#ShopListSkinBg\r\n"
        with open(
            r"titles/cxb/data/rss2/Shop/ShopList_SkinBg.csv", encoding="shift-jis"
        ) as shop:
            lines = shop.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"

        # ShopListSkinEffect load
        ret_str += "\r\n#ShopListSkinEffect\r\n"
        with open(
            r"titles/cxb/data/rss2/Shop/ShopList_SkinEffect.csv", encoding="shift-jis"
        ) as shop:
            lines = shop.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"

        # ShopListSkinNotes load
        ret_str += "\r\n#ShopListSkinNotes\r\n"
        with open(
            r"titles/cxb/data/rss2/Shop/ShopList_SkinNotes.csv", encoding="shift-jis"
        ) as shop:
            lines = shop.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"

        # ShopListTitle load
        ret_str += "\r\n#ShopListTitle\r\n"
        with open(
            r"titles/cxb/data/rss2/Shop/ShopList_Title.csv", encoding="utf-8"
        ) as shop:
            lines = shop.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"
        return {"data": ret_str}

    def handle_data_extra_stage_list_request(self, data: Dict) -> Dict:
        ret_str=""
        with open(r"titles/cxb/data/rss2/ExtraStageList.csv") as extra:
            lines = extra.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"
        return({"data":ret_str})

    def handle_data_exxxxx_request(self, data: Dict) -> Dict:
        return {"data": ""}

    def handle_data_one_more_extra_list_request(self, data: Dict) -> Dict:
        return {"data": ""}

    def handle_data_bonus_list10100_request(self, data: Dict) -> Dict:
        return {"data": ""}

    def handle_data_oexxxx_request(self, data: Dict) -> Dict:
        return {"data": ""}

    def handle_data_free_coupon_request(self, data: Dict) -> Dict:
        return {"data": ""}

    @cached(lifetime=86400)
    def handle_data_news_list_request(self, data: Dict) -> Dict:
        ret_str = ""
        with open(r"titles/cxb/data/rss2/NewsList.csv", encoding="UTF-8") as news:
            lines = news.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"
        return {"data": ret_str}

    def handle_data_tips_request(self, data: Dict) -> Dict:
        return {"data": ""}

    def handle_data_release_info_list_request(self, data: Dict) -> Dict:
        return {"data": ""}

    @cached(lifetime=86400)
    def handle_data_random_music_list_request(self, data: Dict) -> Dict:
        ret_str = ""
        with open(r"titles/cxb/data/rss2/MusicArchiveList.csv") as music:
            lines = music.readlines()
            count = 0
            for line in lines:
                line_split = line.split(",")
                ret_str += (
                    str(count) + "," + line_split[0] + "," + line_split[0] + ",\r\n"
                )

        return {"data": ret_str}

    @cached(lifetime=86400)
    def handle_data_license_request(self, data: Dict) -> Dict:
        ret_str = ""
        with open(r"titles/cxb/data/rss2/License.csv", encoding="UTF-8") as licenses:
            lines = licenses.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"
        return {"data": ret_str}

    @cached(lifetime=86400)
    def handle_data_course_list_request(self, data: Dict) -> Dict:
        ret_str = ""
        with open(
            r"titles/cxb/data/rss2/Course/CourseList.csv", encoding="UTF-8"
        ) as course:
            lines = course.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"
        return {"data": ret_str}

    @cached(lifetime=86400)
    def handle_data_csxxxx_request(self, data: Dict) -> Dict:
        extra_num = int(data["dldate"]["filetype"][-4:])
        ret_str = ""
        with open(
            rf"titles/cxb/data/rss2/Course/Cs{extra_num}.csv", encoding="shift-jis"
        ) as course:
            lines = course.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"
        return {"data": ret_str}

    def handle_data_mission_list_request(self, data: Dict) -> Dict:
        return {"data": ""}

    def handle_data_mission_bonus_request(self, data: Dict) -> Dict:
        return {"data": ""}

    def handle_data_unlimited_mission_request(self, data: Dict) -> Dict:
        return {"data": ""}

    def handle_data_partner_list_request(self, data: Dict) -> Dict:
        ret_str = ""
        # Lord forgive me for the sins I am about to commit
        for i in range(0, 10):
            ret_str += f"80000{i},{i},{i},0,10000,,\r\n"
            ret_str += f"80000{i},{i},{i},1,10500,,\r\n"
            ret_str += f"80000{i},{i},{i},2,10500,,\r\n"
        for i in range(10, 13):
            ret_str += f"8000{i},{i},{i},0,10000,,\r\n"
            ret_str += f"8000{i},{i},{i},1,10500,,\r\n"
            ret_str += f"8000{i},{i},{i},2,10500,,\r\n"
        ret_str += "\r\n---\r\n0,150,100,100,100,100,\r\n"
        for i in range(1, 130):
            ret_str += f"{i},100,100,100,100,100,\r\n"

        ret_str += "---\r\n"
        return {"data": ret_str}

    @cached(lifetime=86400)
    def handle_data_partnerxxxx_request(self, data: Dict) -> Dict:
        partner_num = int(data["dldate"]["filetype"][-4:])
        ret_str = f"{partner_num},,{partner_num},1,10000,\r\n"
        with open(r"titles/cxb/data/rss2/Partner0000.csv") as partner:
            lines = partner.readlines()
            for line in lines:
                ret_str += f"{line[:-1]}\r\n"
        return {"data": ret_str}

    def handle_data_server_state_request(self, data: Dict) -> Dict:
        return {"data": True}

    def handle_data_settings_request(self, data: Dict) -> Dict:
        return {"data": "2,\r\n"}

    def handle_data_story_list_request(self, data: Dict) -> Dict:
        # story id, story name, game version, start time, end time, course arc, unlock flag, song mcode for menu
        ret_str = "\r\n"
        ret_str += (
            f"st0000,RISING PURPLE,10104,1464370990,4096483201,Cs1000,-1,purple,\r\n"
        )
        ret_str += (
            f"st0001,REBEL YELL,10104,1467999790,4096483201,Cs1000,-1,chaset,\r\n"
        )
        ret_str += f"st0002,REMNANT,10104,1502127790,4096483201,Cs1000,-1,overcl,\r\n"
        return {"data": ret_str}

    def handle_data_stxxxx_request(self, data: Dict) -> Dict:
        story_num = int(data["dldate"]["filetype"][-4:])
        ret_str = ""
        # Each stories appears to have 10 pieces based on the wiki but as on how they are set.... no clue
        for i in range(1, 11):
            ret_str += f"{i},st000{story_num}_{i-1},,,,,,,,,,,,,,,,1,,-1,1,\r\n"
        return {"data": ret_str}

    def handle_data_event_stamp_list_request(self, data: Dict) -> Dict:
        return {"data": "Cs1002,1,1,1,1,1,1,1,1,1,1,\r\n"}

    def handle_data_premium_list_request(self, data: Dict) -> Dict:
        return {"data": "1,,,,10,,,,,99,,,,,,,,,100,,\r\n"}

    def handle_data_event_list_request(self, data: Dict) -> Dict:
        return {
            "data": "Cs4001,0,10000,1601510400,1604188799,1,nv2006,1,\r\nCs4005,0,10000,1609459200,1615766399,1,nv2006,1,\r\n"
        }

    def handle_data_event_detail_list_request(self, data: Dict) -> Dict:
        event_id = data["dldate"]["filetype"].split("/")[2]
        if "Cs4001" in event_id:
            return {
                "data": "#EventMusicList\r\n1,zonzon2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,\r\n2,moonki,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,\r\n3,tricko,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,\r\n"
            }
        elif "Cs4005" in event_id:
            return {
                "data": "#EventMusicList\r\n2,firstl,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,\r\n2,valent,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,\r\n2,dazzli2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,\r\n"
            }
        elif "EventStampMapListCs1002" in event_id:
            return {"data": "1,2,1,1,2,3,9,5,6,7,8,9,10,\r\n"}
        elif "EventStampList" in event_id:
            return {"data": "Cs1002,1,1,1,1,1,1,1,1,1,1,\r\n"}
        else:
            return {"data": ""}

    def handle_data_event_stamp_map_list_csxxxx_request(self, data: Dict) -> Dict:
        event_id = data["dldate"]["filetype"].split("/")[2]
        if "EventStampMapListCs1002" in event_id:
            return {"data": "1,2,1,1,2,3,9,5,6,7,8,9,10,\r\n"}
        else:
            return {"data": ""}
