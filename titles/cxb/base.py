import logging
import json
from decimal import Decimal
from base64 import b64encode
from typing import Any, Dict, List
from hashlib import md5
from datetime import datetime

from core.config import CoreConfig
from titles.cxb.config import CxbConfig
from titles.cxb.const import CxbConstants
from titles.cxb.database import CxbData

from threading import Thread

class CxbBase:
    def __init__(self, cfg: CoreConfig, game_cfg: CxbConfig) -> None:
        self.config = cfg  # Config file
        self.game_config = game_cfg
        self.data = CxbData(cfg)  # Database
        self.game = CxbConstants.GAME_CODE
        self.logger = logging.getLogger("cxb")
        self.version = CxbConstants.VER_CROSSBEATS_REV

    def handle_action_rpreq_request(self, data: Dict) -> Dict:
        return {}

    def handle_action_hitreq_request(self, data: Dict) -> Dict:
        return {"data": []}

    def handle_auth_usercheck_request(self, data: Dict) -> Dict:
        profile = self.data.profile.get_profile_index(
            0, data["usercheck"]["authid"], self.version
        )
        if profile is not None:
            self.logger.info(f"User {data['usercheck']['authid']} has CXB profile")
            return {"exist": "true", "logout": "true"}

        self.logger.info(f"No profile for aime id {data['usercheck']['authid']}")
        return {"exist": "false", "logout": "true"}

    def handle_auth_entry_request(self, data: Dict) -> Dict:
        self.logger.info(f"New profile for {data['entry']['authid']}")
        return {"token": data["entry"]["authid"], "uid": data["entry"]["authid"]}

    def handle_auth_login_request(self, data: Dict) -> Dict:
        profile = self.data.profile.get_profile_index(
            0, data["login"]["authid"], self.version
        )

        if profile is not None:
            self.logger.info(f"Login user {data['login']['authid']}")
            return {"token": data["login"]["authid"], "uid": data["login"]["authid"]}

        self.logger.warning(f"User {data['login']['authid']} does not have a profile")
        return {}

    def task_generateCoupon(index, data1):
        # Coupons
        for i in range(500, 510):
            index.append(str(i))
            couponid = int(i) - 500
            dataValue = [
                {
                    "couponId": str(couponid),
                    "couponNum": "1",
                    "couponLog": [],
                }
            ]
            data1.append(
                b64encode(
                    bytes(json.dumps(dataValue[0], separators=(",", ":")), "utf-8")
                ).decode("utf-8")
            )

    def task_generateShopListTitle(index, data1):
        # ShopList_Title
        for i in range(200000, 201451):
            index.append(str(i))
            shopid = int(i) - 200000
            dataValue = [
                {
                    "shopId": shopid,
                    "shopState": "2",
                    "isDisable": "t",
                    "isDeleted": "f",
                    "isSpecialFlag": "f",
                }
            ]
            data1.append(
                b64encode(
                    bytes(json.dumps(dataValue[0], separators=(",", ":")), "utf-8")
                ).decode("utf-8")
            )

    def task_generateShopListIcon(index, data1):
        # ShopList_Icon
        for i in range(202000, 202264):
            index.append(str(i))
            shopid = int(i) - 200000
            dataValue = [
                {
                    "shopId": shopid,
                    "shopState": "2",
                    "isDisable": "t",
                    "isDeleted": "f",
                    "isSpecialFlag": "f",
                }
            ]
            data1.append(
                b64encode(
                    bytes(json.dumps(dataValue[0], separators=(",", ":")), "utf-8")
                ).decode("utf-8")
            )

    def task_generateStories(index, data1):
        # Stories
        for i in range(900000, 900003):
            index.append(str(i))
            storyid = int(i) - 900000
            dataValue = [
                {
                    "storyId": storyid,
                    "unlockState1": ["t"] * 10,
                    "unlockState2": ["t"] * 10,
                    "unlockState3": ["t"] * 10,
                    "unlockState4": ["t"] * 10,
                    "unlockState5": ["t"] * 10,
                    "unlockState6": ["t"] * 10,
                    "unlockState7": ["t"] * 10,
                    "unlockState8": ["t"] * 10,
                    "unlockState9": ["t"] * 10,
                    "unlockState10": ["t"] * 10,
                    "unlockState11": ["t"] * 10,
                    "unlockState12": ["t"] * 10,
                    "unlockState13": ["t"] * 10,
                    "unlockState14": ["t"] * 10,
                    "unlockState15": ["t"] * 10,
                    "unlockState16": ["t"] * 10,
                }
            ]
            data1.append(
                b64encode(
                    bytes(json.dumps(dataValue[0], separators=(",", ":")), "utf-8")
                ).decode("utf-8")
            )

    def task_generateScoreData(song, index, data1):
        song_data = song["data"]
        songCode = []

        songCode.append(
            {
                "mcode": song_data["mcode"],
                "musicState": song_data["musicState"],
                "playCount": song_data["playCount"],
                "totalScore": song_data["totalScore"],
                "highScore": song_data["highScore"],
                "everHighScore": song_data["everHighScore"]
                if "everHighScore" in song_data
                else ["0", "0", "0", "0", "0"],
                "clearRate": song_data["clearRate"],
                "rankPoint": song_data["rankPoint"],
                "normalCR": song_data["normalCR"]
                if "normalCR" in song_data
                else ["0", "0", "0", "0", "0"],
                "survivalCR": song_data["survivalCR"]
                if "survivalCR" in song_data
                else ["0", "0", "0", "0", "0"],
                "ultimateCR": song_data["ultimateCR"]
                if "ultimateCR" in song_data
                else ["0", "0", "0", "0", "0"],
                "nohopeCR": song_data["nohopeCR"]
                if "nohopeCR" in song_data
                else ["0", "0", "0", "0", "0"],
                "combo": song_data["combo"],
                "coupleUserId": song_data["coupleUserId"],
                "difficulty": song_data["difficulty"],
                "isFullCombo": song_data["isFullCombo"],
                "clearGaugeType": song_data["clearGaugeType"],
                "fieldType": song_data["fieldType"],
                "gameType": song_data["gameType"],
                "grade": song_data["grade"],
                "unlockState": song_data["unlockState"],
                "extraState": song_data["extraState"],
            }
        )
        index.append(song_data["index"])
        data1.append(
            b64encode(
                bytes(json.dumps(songCode[0], separators=(",", ":")), "utf-8")
            ).decode("utf-8")
        )

    def task_generateIndexData(versionindex):
        try:
            v_profile = self.data.profile.get_profile_index(0, uid, self.version)
            v_profile_data = v_profile["data"]
            versionindex.append(int(v_profile_data["appVersion"]))
        except Exception:
            versionindex.append("10400")

    def handle_action_loadrange_request(self, data: Dict) -> Dict:
        range_start = data["loadrange"]["range"][0]
        range_end = data["loadrange"]["range"][1]
        uid = data["loadrange"]["uid"]

        self.logger.info(f"Load data for {uid}")
        profile = self.data.profile.get_profile(uid, self.version)
        songs = self.data.score.get_best_scores(uid)

        data1 = []
        index = []
        versionindex = []

        for profile_index in profile:
            profile_data = profile_index["data"]

            if int(range_start) == 800000:
                return {"index": range_start, "data": [], "version": 10400}

            if not (int(range_start) <= int(profile_index[3]) <= int(range_end)):
                continue
            # Prevent loading of the coupons within the profile to use the force unlock instead
            elif 500 <= int(profile_index[3]) <= 510:
                continue
            # Prevent loading of songs saved in the profile
            elif 100000 <= int(profile_index[3]) <= 110000:
                continue
            # Prevent loading of the shop list / unlocked titles & icons saved in the profile
            elif 200000 <= int(profile_index[3]) <= 210000:
                continue
            # Prevent loading of stories in the profile
            elif 900000 <= int(profile_index[3]) <= 900200:
                continue
            else:
                index.append(profile_index[3])
                data1.append(
                    b64encode(
                        bytes(json.dumps(profile_data, separators=(",", ":")), "utf-8")
                    ).decode("utf-8")
                )

        """
        100000 = Songs
        200000 = Shop
        300000 = Courses
        400000 = Events
        500000 = Challenges
        600000 = Bonuses
        700000 = rcLog
        800000 = Partners
        900000 = Stories
        """

        # Async threads to generate the response
        thread_Coupon = Thread(target=CxbBase.task_generateCoupon(index, data1))
        thread_ShopListTitle = Thread(target=CxbBase.task_generateShopListTitle(index, data1))
        thread_ShopListIcon = Thread(target=CxbBase.task_generateShopListIcon(index, data1))
        thread_Stories = Thread(target=CxbBase.task_generateStories(index, data1))

        thread_Coupon.start()
        thread_ShopListTitle.start()
        thread_ShopListIcon.start()
        thread_Stories.start()

        thread_Coupon.join()
        thread_ShopListTitle.join()
        thread_ShopListIcon.join()
        thread_Stories.join()

        for song in songs:
            thread_ScoreData = Thread(target=CxbBase.task_generateScoreData(song, index, data1))
            thread_ScoreData.start()

        for v in index:
            thread_IndexData = Thread(target=CxbBase.task_generateIndexData(versionindex))
            thread_IndexData.start()

        return {"index": index, "data": data1, "version": versionindex}

    def handle_action_saveindex_request(self, data: Dict) -> Dict:
        save_data = data["saveindex"]

        try:
            # REV Omnimix Version Fetcher
            gameversion = data["saveindex"]["data"][0][2]
            self.logger.warning(f"Game Version is {gameversion}")
        except Exception:
            pass

        if "10205" in gameversion:
            self.logger.info(
                f"Saving CrossBeats REV profile for {data['saveindex']['uid']}"
            )
            # Alright.... time to bring the jank code

            for value in data["saveindex"]["data"]:
                if "playedUserId" in value[1]:
                    self.data.profile.put_profile(
                        data["saveindex"]["uid"], self.version, value[0], value[1]
                    )
                if "mcode" not in value[1]:
                    self.data.profile.put_profile(
                        data["saveindex"]["uid"], self.version, value[0], value[1]
                    )
                if "shopId" in value:
                    continue
                if "mcode" in value[1] and "musicState" in value[1]:
                    song_json = json.loads(value[1])

                    songCode = []
                    songCode.append(
                        {
                            "mcode": song_json["mcode"],
                            "musicState": song_json["musicState"],
                            "playCount": song_json["playCount"],
                            "totalScore": song_json["totalScore"],
                            "highScore": song_json["highScore"],
                            "clearRate": song_json["clearRate"],
                            "rankPoint": song_json["rankPoint"],
                            "combo": song_json["combo"],
                            "coupleUserId": song_json["coupleUserId"],
                            "difficulty": song_json["difficulty"],
                            "isFullCombo": song_json["isFullCombo"],
                            "clearGaugeType": song_json["clearGaugeType"],
                            "fieldType": song_json["fieldType"],
                            "gameType": song_json["gameType"],
                            "grade": song_json["grade"],
                            "unlockState": song_json["unlockState"],
                            "extraState": song_json["extraState"],
                            "index": value[0],
                        }
                    )
                    self.data.score.put_best_score(
                        data["saveindex"]["uid"],
                        song_json["mcode"],
                        self.version,
                        value[0],
                        songCode[0],
                    )
            return {}
        else:
            self.logger.info(
                f"Saving CrossBeats REV Sunrise profile for {data['saveindex']['uid']}"
            )

        # Sunrise
        try:
            profileIndex = save_data["index"].index("0")
        except Exception:
            return {"data": ""}  # Maybe

        profile = json.loads(save_data["data"][profileIndex])
        aimeId = profile["aimeId"]
        i = 0

        for index, value in enumerate(data["saveindex"]["data"]):
            if int(data["saveindex"]["index"][index]) == 101:
                self.data.profile.put_profile(
                    aimeId, self.version, data["saveindex"]["index"][index], value
                )
            if (
                int(data["saveindex"]["index"][index]) >= 700000
                and int(data["saveindex"]["index"][index]) <= 701000
            ):
                self.data.profile.put_profile(
                    aimeId, self.version, data["saveindex"]["index"][index], value
                )
            if (
                int(data["saveindex"]["index"][index]) >= 500
                and int(data["saveindex"]["index"][index]) <= 510
            ):
                self.data.profile.put_profile(
                    aimeId, self.version, data["saveindex"]["index"][index], value
                )
            if "playedUserId" in value:
                self.data.profile.put_profile(
                    aimeId,
                    self.version,
                    data["saveindex"]["index"][index],
                    json.loads(value),
                )
            if "mcode" not in value and "normalCR" not in value:
                self.data.profile.put_profile(
                    aimeId,
                    self.version,
                    data["saveindex"]["index"][index],
                    json.loads(value),
                )
            if "shopId" in value:
                continue

        # MusicList Index for the profile
        indexSongList = []
        for value in data["saveindex"]["index"]:
            if int(value) in range(100000, 110000):
                indexSongList.append(value)

        for index, value in enumerate(data["saveindex"]["data"]):
            if "mcode" not in value:
                continue
            if "playedUserId" in value:
                continue

            data1 = json.loads(value)

            songCode = []
            songCode.append(
                {
                    "mcode": data1["mcode"],
                    "musicState": data1["musicState"],
                    "playCount": data1["playCount"],
                    "totalScore": data1["totalScore"],
                    "highScore": data1["highScore"],
                    "everHighScore": data1["everHighScore"],
                    "clearRate": data1["clearRate"],
                    "rankPoint": data1["rankPoint"],
                    "normalCR": data1["normalCR"],
                    "survivalCR": data1["survivalCR"],
                    "ultimateCR": data1["ultimateCR"],
                    "nohopeCR": data1["nohopeCR"],
                    "combo": data1["combo"],
                    "coupleUserId": data1["coupleUserId"],
                    "difficulty": data1["difficulty"],
                    "isFullCombo": data1["isFullCombo"],
                    "clearGaugeType": data1["clearGaugeType"],
                    "fieldType": data1["fieldType"],
                    "gameType": data1["gameType"],
                    "grade": data1["grade"],
                    "unlockState": data1["unlockState"],
                    "extraState": data1["extraState"],
                    "index": indexSongList[i],
                }
            )

            self.data.score.put_best_score(
                aimeId, data1["mcode"], self.version, indexSongList[i], songCode[0]
            )
            i += 1
        return {}

    def handle_action_sprankreq_request(self, data: Dict) -> Dict:
        uid = data["sprankreq"]["uid"]
        self.logger.info(f"Get best rankings for {uid}")
        p = self.data.score.get_best_rankings(uid)

        rankList: List[Dict[str, Any]] = []

        for rank in p:
            if rank["song_id"] is not None:
                rankList.append(
                    {
                        "sc": [rank["score"], rank["song_id"]],
                        "rid": rank["rev_id"],
                        "clear": rank["clear"],
                    }
                )
            else:
                rankList.append(
                    {
                        "sc": [rank["score"]],
                        "rid": rank["rev_id"],
                        "clear": rank["clear"],
                    }
                )

        return {
            "uid": data["sprankreq"]["uid"],
            "aid": data["sprankreq"]["aid"],
            "rank": rankList,
            "rankx": [1, 1, 1],
        }

    def handle_action_getadv_request(self, data: Dict) -> Dict:
        return {"data": [{"r": "1", "i": "100300", "c": "20"}]}

    def handle_action_getmsg_request(self, data: Dict) -> Dict:
        return {"msgs": []}

    def handle_auth_logout_request(self, data: Dict) -> Dict:
        return {"auth": True}

    def handle_action_rankreg_request(self, data: Dict) -> Dict:
        uid = data["rankreg"]["uid"]
        self.logger.info(f"Put {len(data['rankreg']['data'])} rankings for {uid}")

        for rid in data["rankreg"]["data"]:
            # REV S2
            if "clear" in rid:
                try:
                    self.data.score.put_ranking(
                        user_id=uid,
                        rev_id=int(rid["rid"]),
                        song_id=int(rid["sc"][1]),
                        score=int(rid["sc"][0]),
                        clear=rid["clear"],
                    )
                except Exception:
                    self.data.score.put_ranking(
                        user_id=uid,
                        rev_id=int(rid["rid"]),
                        song_id=0,
                        score=int(rid["sc"][0]),
                        clear=rid["clear"],
                    )
            # REV
            else:
                try:
                    self.data.score.put_ranking(
                        user_id=uid,
                        rev_id=int(rid["rid"]),
                        song_id=int(rid["sc"][1]),
                        score=int(rid["sc"][0]),
                        clear=0,
                    )
                except Exception:
                    self.data.score.put_ranking(
                        user_id=uid,
                        rev_id=int(rid["rid"]),
                        song_id=0,
                        score=int(rid["sc"][0]),
                        clear=0,
                    )
        return {}

    def handle_action_addenergy_request(self, data: Dict) -> Dict:
        uid = data["addenergy"]["uid"]
        self.logger.info(f"Add energy to user {uid}")
        profile = self.data.profile.get_profile_index(0, uid, self.version)
        data1 = profile["data"]
        p = self.data.item.get_energy(uid)
        energy = p["energy"]

        if not p:
            self.data.item.put_energy(uid, 5)

            return {
                "class": data1["myClass"],
                "granted": "5",
                "total": "5",
                "threshold": "1000",
            }

        array = []

        newenergy = int(energy) + 5
        self.data.item.put_energy(uid, newenergy)

        if int(energy) <= 995:
            array.append(
                {
                    "class": data1["myClass"],
                    "granted": "5",
                    "total": str(energy),
                    "threshold": "1000",
                }
            )
        else:
            array.append(
                {
                    "class": data1["myClass"],
                    "granted": "0",
                    "total": str(energy),
                    "threshold": "1000",
                }
            )
        return array[0]

    def handle_action_eventreq_request(self, data: Dict) -> Dict:
        self.logger.info(data)
        return {"eventreq": ""}

    def handle_action_stampreq_request(self, data: Dict) -> Dict:
        self.logger.info(data)
        return {"stampreq": ""}