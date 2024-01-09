from datetime import datetime, timedelta
import os
from random import choice
from typing import Any, Dict, List
import json
import logging

from core.config import CoreConfig
from titles.idac.const import IDACConstants
from titles.idac.config import IDACConfig
from titles.idac.base import IDACBase


class IDACSeason2(IDACBase):
    def __init__(self, core_cfg: CoreConfig, game_cfg: IDACConfig) -> None:
        super().__init__(core_cfg, game_cfg)
        self.version = IDACConstants.VER_IDAC_SEASON_2

        # load the play stamps and timetrial events into memory
        self.stamp_info = []
        if self.game_config.stamp.enable:
            for stamp in self.game_config.stamp.enabled_stamps:
                if not os.path.exists(f"./titles/idac/data/stamps/{stamp}.json"):
                    self.logger.warning(f"Stamp {stamp} is enabled but does not exist!")
                    continue

                with open(
                    f"./titles/idac/data/stamps/{stamp}.json", encoding="UTF-8"
                ) as f:
                    self.logger.debug(f"Loading stamp {stamp}")
                    self.stamp_info.append(self._fix_dates(json.load(f)))

        self.timetrial_event = {}
        self.timetrial_event_id = None
        if self.game_config.timetrial.enable:
            timetrial = self.game_config.timetrial.enabled_timetrial
            if timetrial is not None:
                if not os.path.exists(f"./titles/idac/data/timetrial/{timetrial}.json"):
                    self.logger.warning(
                        f"Timetrial {timetrial} is enabled but does not exist!"
                    )
                else:
                    self.logger.debug(f"Loading timetrial {timetrial}")
                    with open(
                        f"./titles/idac/data/timetrial/{timetrial}.json",
                        encoding="UTF-8",
                    ) as f:
                        self.timetrial_event = self._fix_dates(json.load(f))

                    # required for saving
                    self.timetrial_event_id = self.timetrial_event.get(
                        "timetrial_event_id"
                    )

    def handle_alive_get_request(self, data: Dict, headers: Dict):
        return {
            "status_code": "0",
            # 1 = success, 0 = failed
            "server_status": 1,
            "force_reboot_time": int(datetime.now().timestamp()) - 86400,
        }

    def _fix_dates(self, input: dict):
        """
        Fix "start_dt" and "end_dt" dates in a JSON file.
        """
        output = {}

        self.logger.debug(f"Fixing dates in {type(input)}")
        for key, value in input.items():
            if key in {"start_dt", "end_dt"}:
                if isinstance(value, str):
                    value = int(datetime.strptime(value, "%Y-%m-%d").timestamp())

            output[key] = value
        return output

    def handle_boot_getconfigdata_request(self, data: Dict, headers: Dict):
        """
        category:
        1  = D Coin
        3  = Car Dressup Token
        5  = Avatar Dressup Token
        6  = Tachometer
        7  = Aura
        8  = Aura Color
        9  = Avatar Face
        10 = Avatar Eye
        11 = Avatar Mouth
        12 = Avatar Hair
        13 = Avatar Glasses
        14 = Avatar Face accessories
        15 = Avatar Body
        18 = Avatar Background
        21 = Chat Stamp
        22 = Keychain
        24 = Title
        25 = FullTune Ticket
        26 = Paper Cup
        27 = BGM
        28 = Drifting Text
        31 = Start Menu BG
        32 = Car Color/Paint
        33 = Aura Level
        34 = FullTune Ticket Fragment
        35 = Underneon Lights
        """
        version = headers["device_version"]
        ver_str = version.replace(".", "")[:3]

        if self.core_cfg.server.is_develop:
            domain_api_game = f"http://{self.core_cfg.server.hostname}:{self.core_cfg.server.port}/{ver_str}/"
        else:
            domain_api_game = f"http://{self.core_cfg.server.hostname}/{ver_str}/"

        return {
            "status_code": "0",
            "free_continue_enable": 1,
            "free_continue_new": 1,
            "free_continue_play": 1,
            "difference_time_to_jp": 0,
            # has to match the game asset version to show theory of street
            "asset_version": "1",
            # option version? MV01?
            "optional_version": "1",
            "disconnect_offset": 0,
            "boost_balance_version": "0",
            "time_release_number": "0",
            "play_stamp_enable": 1,
            "play_stamp_bonus_coin": 1,
            "gacha_chara_needs": 1,
            "both_win_system_control": 1,
            "subcard_system_congrol": 1,
            "server_maintenance_start_hour": 0,
            "server_maintenance_start_minutes": 0,
            "server_maintenance_end_hour": 0,
            "server_maintenance_end_minutes": 0,
            "domain_api_game": domain_api_game,
            "domain_matching": f"{domain_api_game}initiald-matching/",
            "domain_echo1": f"{self.core_cfg.server.hostname}:{self.game_config.server.echo1}",
            "domain_echo2": f"{self.core_cfg.server.hostname}:{self.game_config.server.echo1}",
            "domain_ping": f"{self.core_cfg.server.hostname}",
            "battle_gift_event_master": [],
            "round_event": [
                {
                    "round_event_id": 30,
                    "round_event_nm": f"{self.core_cfg.server.name} Event",
                    "start_dt": int(
                        datetime.strptime("2023-01-01", "%Y-%m-%d").timestamp()
                    ),
                    "end_dt": int(
                        datetime.strptime("2029-01-01", "%Y-%m-%d").timestamp()
                    ),
                    "round_start_rank": 0,
                    "save_filename": "0",
                    # https://info-initialdac.sega.jp/1898/
                    "vscount": [
                        {
                            "reward_upper_limit": 10,
                            "reward_lower_limit": 10,
                            "reward": [{"reward_category": 21, "reward_type": 483}],
                        },
                        {
                            "reward_upper_limit": 40,
                            "reward_lower_limit": 40,
                            "reward": [{"reward_category": 21, "reward_type": 484}],
                        },
                        {
                            "reward_upper_limit": 80,
                            "reward_lower_limit": 80,
                            "reward": [{"reward_category": 22, "reward_type": 516}],
                        },
                        {
                            "reward_upper_limit": 120,
                            "reward_lower_limit": 120,
                            "reward": [{"reward_category": 21, "reward_type": 461}],
                        },
                        {
                            "reward_upper_limit": 180,
                            "reward_lower_limit": 180,
                            "reward": [{"reward_category": 21, "reward_type": 462}],
                        }
                    ],
                    "rank": [],
                    "point": [],
                    "playable_course_list": [
                        {"course_id": 4, "course_day": 0},
                        {"course_id": 4, "course_day": 1},
                        {"course_id": 6, "course_day": 0},
                        {"course_id": 6, "course_day": 1},
                        {"course_id": 8, "course_day": 0},
                        {"course_id": 8, "course_day": 1},
                        {"course_id": 10, "course_day": 0},
                        {"course_id": 10, "course_day": 1},
                        {"course_id": 12, "course_day": 0},
                        {"course_id": 12, "course_day": 1},
                        {"course_id": 14, "course_day": 0},
                        {"course_id": 14, "course_day": 1},
                        {"course_id": 16, "course_day": 0},
                        {"course_id": 16, "course_day": 1},
                        {"course_id": 18, "course_day": 0},
                        {"course_id": 18, "course_day": 1},
                        {"course_id": 20, "course_day": 0},
                        {"course_id": 20, "course_day": 1},
                        {"course_id": 22, "course_day": 0},
                        {"course_id": 22, "course_day": 1},
                        {"course_id": 24, "course_day": 0},
                        {"course_id": 24, "course_day": 1},
                        {"course_id": 26, "course_day": 0},
                        {"course_id": 26, "course_day": 1},
                        {"course_id": 36, "course_day": 0},
                        {"course_id": 36, "course_day": 1},
                        {"course_id": 38, "course_day": 0},
                        {"course_id": 38, "course_day": 1},
                        {"course_id": 40, "course_day": 0},
                        {"course_id": 40, "course_day": 1},
                        {"course_id": 42, "course_day": 0},
                        {"course_id": 42, "course_day": 1},
                        {"course_id": 44, "course_day": 0},
                        {"course_id": 44, "course_day": 1},
                        {"course_id": 46, "course_day": 0},
                        {"course_id": 46, "course_day": 1},
                        {"course_id": 48, "course_day": 0},
                        {"course_id": 48, "course_day": 1},
                        {"course_id": 50, "course_day": 0},
                        {"course_id": 50, "course_day": 1},
                        {"course_id": 52, "course_day": 0},
                        {"course_id": 52, "course_day": 1},
                        {"course_id": 54, "course_day": 0},
                        {"course_id": 54, "course_day": 1},
                        {"course_id": 56, "course_day": 0},
                        {"course_id": 56, "course_day": 1},
                        {"course_id": 58, "course_day": 0},
                        {"course_id": 58, "course_day": 1},
                        {"course_id": 68, "course_day": 0},
                        {"course_id": 68, "course_day": 1},
                        {"course_id": 70, "course_day": 0},
                        {"course_id": 70, "course_day": 1},
                    ],
                }
            ],
            "last_round_event": [],
            "last_round_event_ranking": [],
            "round_event_exp": [],
            "stamp_info": self.stamp_info,
            # 0 = use default data, 1+ = server version of timereleasedata response
            "timerelease_no": 3,
            # 0 = use default data, 1+ = server version of gachadata response
            "timerelease_avatar_gacha_no": 3,
            "takeover_reward": [],
            "subcard_judge": [
                {
                    "condition_id": 1,
                    "lower_rank": 0,
                    "higher_rank": 10,
                    "condition_start": 2,
                    "condition_end": 3,
                }
            ],
            "special_promote": [{"counter": 1, "online_rank_id": 1}],
            "matching_id": 1,
            "matching_group": [
                {
                    "group_id": 1,
                    "group_percent": 1,
                }
            ],
            "timetrial_disp_date": int(
                datetime.strptime("2023-10-01", "%Y-%m-%d").timestamp()
            ),
            # price for every car
            "buy_car_need_cash": 5000,
            # number of buyable shop/customization time limits
            "time_extension_limit": 1,
            "collabo_id": 0,
            "driver_debut_end_date": int(
                datetime.strptime("2029-01-01", "%Y-%m-%d").timestamp()
            ),
            "online_battle_param1": 1,
            "online_battle_param2": 1,
            "online_battle_param3": 1,
            "online_battle_param4": 1,
            "online_battle_param5": 1,
            "online_battle_param6": 1,
            "online_battle_param7": 1,
            "online_battle_param8": 1,
            "theory_open_version": "1.30",
            "theory_close_version": "1.50",
            "special_mode_data": {
                "start_dt": int(
                    datetime.strptime("2023-01-01", "%Y-%m-%d").timestamp()
                ),
                "end_dt": int(datetime.strptime("2029-01-01", "%Y-%m-%d").timestamp()),
                "story_type": 4,  # touhou special event
            },
            "timetrial_event_data": self.timetrial_event,
        }

    def handle_boot_bookkeep_request(self, data: Dict, headers: Dict):
        pass

    def handle_boot_getgachadata_request(self, data: Dict, headers: Dict):
        """
        Reward category types:
        9: Face
        10: Eye
        11: Mouth
        12: Hair
        13: Glasses
        14: Face accessories
        15: Body
        18: Background
        """

        with open("./titles/idac/data/avatarGacha.json", encoding="UTF-8") as f:
            avatar_gacha_data = json.load(f)

        # avatar_gacha_data = {
        #     "status_code": "0",
        #     "avatar_gacha_data": [
        #         {
        #             "avatar_gacha_id": 0,
        #             "avatar_gacha_nm": "Standard",
        #             "gacha_type": 0,
        #             "save_filename": "0",
        #             "use_ticket_cnt": 1,
        #             "start_dt": int(
        #                 datetime.strptime("2019-01-01", "%Y-%m-%d").timestamp()
        #             ),
        #             "end_dt": int(
        #                 datetime.strptime("2029-01-01", "%Y-%m-%d").timestamp()
        #             ),
        #             "gacha_reward": [
        #                 {
        #                     "reward_id": 117,
        #                     "reward_type": 118,
        #                     "reward_category": 18,
        #                     "rate": 1000,
        #                     "pickup_flag": 0,
        #                 },
        #             ],
        #         }
        #     ],
        # }

        self.logger.debug(
            f'Available avatar gacha items: {len(avatar_gacha_data["avatar_gacha_data"][0]["gacha_reward"])}'
        )

        return avatar_gacha_data

    def handle_boot_gettimereleasedata_request(self, data: Dict, headers: Dict):
        """
        timerelease chapter:
        1 = Story: 1, 2, 3, 4, 5, 6, 7, 8, 9, 19 (Chapter 10), (29 Chapter 11 lol?)
        2 = MF Ghost: 10, 11, 12, 13, 14, 15
        3 = Bunta: 15, 16, 17, 18, 19, 20, (21, 21, 22?)
        4 = Special Event: 23, 24, 25, 26, 27, 28 (Touhou Project)
        """
        path = "./titles/idac/data/"

        # 1.00.00 is default
        device_version_data = headers.get("device_version", "1.00.00")
        device_version = int(device_version_data.replace(".", "")[:-2])

        timerelease_filename = f"timeRelease_v{device_version:04d}"
        timerelease_path = f"{path}{timerelease_filename}.json"

        # if the file doesn't exist, try to find the next lowest version
        if not os.path.exists(timerelease_path):
            while device_version > 100:
                device_version -= 1
                timerelease_filename = f"timeRelease_v{device_version:04d}"
                timerelease_path = f"{path}{timerelease_filename}.json"

                # if the file exists, break out of the loop
                if os.path.exists(timerelease_path):
                    break

        self.logger.debug(f"Using time release file: {timerelease_filename}")
        # load the time release data
        with open(f"{path}{timerelease_filename}.json") as f:
            time_release_data = json.load(f)

        return time_release_data

    def handle_advertise_getrankingdata_request(self, data: Dict, headers: Dict):
        best_data = []
        for last_update in data.get("last_update_date"):
            course_id = last_update.get("course_id")

            ranking = self.data.item.get_time_trial_ranking_by_course(
                self.version, course_id
            )
            ranking_data = []
            for i, rank in enumerate(ranking):
                user_id = rank["user"]

                # get the username, country and store from the profile
                profile = self.data.profile.get_profile(user_id, self.version)
                arcade = self.data.arcade.get_arcade(profile["store"])

                if arcade is None:
                    arcade = {}
                    arcade["name"] = self.core_cfg.server.name

                # should never happen
                if profile is None:
                    continue

                ranking_data.append(
                    {
                        "course_id": course_id,
                        "rank": i + 1,
                        "username": profile["username"],
                        "value": rank["goal_time"],
                        # gat the store name from the profile
                        "store": arcade["name"],
                        # get the country id from the profile, 9 is JPN
                        "country": profile["country"],
                        "style_car_id": rank["style_car_id"],
                        # convert the datetime to a timestamp
                        "play_dt": int(rank["play_dt"].timestamp()),
                        "section_time_1": rank["section_time_1"],
                        "section_time_2": rank["section_time_2"],
                        "section_time_3": rank["section_time_3"],
                        "section_time_4": rank["section_time_4"],
                        "mission": rank["mission"],
                    }
                )

            best_data.append(
                {
                    "course_id": course_id,
                    "ranking_data": ranking_data,
                }
            )

        return {
            "status_code": "0",
            "national_best_data": best_data,
            "shop_best_data": best_data,
            "rank_management_flag": 0,
        }

    def handle_login_checklock_request(self, data: Dict, headers: Dict):
        user_id = data["id"]
        access_code = data["accesscode"]
        is_new_player = 0

        # check that the user_id from access_code matches the user_id
        if user_id == self.data.card.get_user_id_from_card(access_code):
            lock_result = 1

            # check if an IDAC profile already exists
            p = self.data.profile.get_profile(user_id, self.version)
            is_new_player = 1 if p is None else 0
        else:
            lock_result = 0
            user_id = ""

        # other: in use
        return {
            "status_code": "0",
            # 0 = already in use, 1 = good, 2 = too new
            "lock_result": lock_result,
            "lock_date": int(datetime.now().timestamp()),
            "daily_play": 1,
            "session": f"{user_id}",
            "shared_security_key": "a",
            "session_procseq": "a",
            "new_player": is_new_player,
            "server_status": 1,
        }

    def handle_login_unlock_request(self, data: Dict, headers: Dict):
        return {
            "status_code": "0",
            "lock_result": 1,
        }

    def handle_login_relock_request(self, data: Dict, headers: Dict):
        return {
            "status_code": "0",
            "lock_result": 1,
            "lock_date": int(datetime.now().timestamp()),
        }

    def handle_login_guestplay_request(self, data: Dict, headers: Dict):
        # TODO
        pass

    def _generate_story_data(self, user_id: int) -> Dict:
        stories = self.data.item.get_stories(user_id)

        story_data = []
        for s in stories:
            chapter_id = s["chapter"]
            episodes = self.data.item.get_story_episodes(user_id, chapter_id)

            episode_data = []
            for e in episodes:
                episode_id = e["episode"]
                difficulties = self.data.item.get_story_episode_difficulties(
                    user_id, episode_id
                )

                difficulty_data = []
                for d in difficulties:
                    difficulty_data.append(
                        {
                            "difficulty": d["difficulty"],
                            "play_count": d["play_count"],
                            "clear_count": d["clear_count"],
                            "play_status": d["play_status"],
                            "play_score": d["play_score"],
                        }
                    )

                episode_data.append(
                    {
                        "episode": e["episode"],
                        "play_status": e["play_status"],
                        "difficulty_data": difficulty_data,
                    }
                )

            story_data.append(
                {
                    "story_type": s["story_type"],
                    "chapter": s["chapter"],
                    "loop_count": s["loop_count"],
                    "episode_data": episode_data,
                }
            )

        return story_data

    def _generate_special_data(self, user_id: int) -> Dict:
        # 4 = special mode
        specials = self.data.item.get_best_challenges_by_vs_type(user_id, story_type=4)

        special_data = []
        for s in specials:
            special_data.append(
                {
                    "story_type": s["story_type"],
                    "vs_type": s["vs_type"],
                    "max_clear_lv": s["max_clear_lv"],
                    "last_play_lv": s["last_play_lv"],
                    # change to last_play_course_id?
                    "last_play_course_id": s["course_id"],
                }
            )

        return special_data

    def _generate_challenge_data(self, user_id: int) -> Dict:
        # challenge mode (Bunta challenge only right now)
        challenges = self.data.item.get_best_challenges_by_vs_type(
            user_id, story_type=3
        )

        challenge_data = []
        for c in challenges:
            challenge_data.append(
                {
                    "story_type": c["story_type"],
                    "vs_type": c["vs_type"],
                    "max_clear_lv": c["max_clear_lv"],
                    "last_play_lv": c["last_play_lv"],
                    # change to last_play_course_id?
                    "last_play_course_id": c["course_id"],
                    "play_count": c["play_count"],
                }
            )

        return challenge_data

    def _save_stock_data(self, user_id: int, stock_data: Dict):
        updated_stock_data = {}
        for k, v in stock_data.items():
            if v != "":
                updated_stock_data[k] = v

        if updated_stock_data:
            self.data.profile.put_profile_stock(
                user_id, self.version, updated_stock_data
            )

    def handle_user_getdata_request(self, data: Dict, headers: Dict):
        user_id = int(headers["session"])

        # get the user's profile, can never be None
        p = self.data.profile.get_profile(user_id, self.version)
        user_data = p._asdict()
        arcade = self.data.arcade.get_arcade(user_data["store"])

        del user_data["id"]
        del user_data["user"]
        del user_data["version"]
        user_data["id"] = user_id
        user_data["store_name"] = (
            self.core_cfg.server.name if arcade is None else arcade["name"]
        )
        user_data["last_play_date"] = int(user_data["last_play_date"].timestamp())
        user_data["create_date"] = int(user_data["create_date"].timestamp())

        # get the user's rank
        r = self.data.profile.get_profile_rank(user_id, self.version)
        rank_data = r._asdict()
        del rank_data["id"]
        del rank_data["user"]
        del rank_data["version"]

        # add the mode_rank_data to the user_data
        user_data["mode_rank_data"] = rank_data

        # get the user's avatar
        a = self.data.profile.get_profile_avatar(user_id)
        avatar_data = a._asdict()
        del avatar_data["id"]
        del avatar_data["user"]

        # get the user's stock
        s = self.data.profile.get_profile_stock(user_id, self.version)
        stock_data = s._asdict()
        del stock_data["id"]
        del stock_data["user"]
        del stock_data["version"]

        # get the user's config
        c = self.data.profile.get_profile_config(user_id)
        config_data = c._asdict()
        del config_data["id"]
        del config_data["user"]
        config_data["id"] = config_data.pop("config_id")

        # get the user's ticket
        tickets: list = self.data.item.get_tickets(user_id)

        """
        ticket_id:
        3 = Car Dressup Points
        5 = Avatar Dressup Points
        25 = Full Tune Tickets
        34 = Full Tune Fragments
        """

        ticket_data = []
        for ticket in tickets:
            ticket_data.append(
                {
                    "ticket_id": ticket["ticket_id"],
                    "ticket_cnt": ticket["ticket_cnt"],
                }
            )

        # get the user's course, required for the "course proeficiency"
        courses = self.data.item.get_courses(user_id)
        course_data = []
        for course in courses:
            course_data.append(
                {
                    "id": 0,  # no clue, always 0?
                    "course_id": course["course_id"],
                    "run_counts": course["run_counts"],
                    # "course proeficiency" in exp points
                    "skill_level_exp": course["skill_level_exp"],
                }
            )

        # get the profile theory data
        theory_data = {}
        theory = self.data.profile.get_profile_theory(user_id, self.version)
        if theory is not None:
            theory_data = theory._asdict()
            del theory_data["id"]
            del theory_data["user"]
            del theory_data["version"]

        # get the users theory course data
        theory_course_data = []
        theory_courses = self.data.item.get_theory_courses(user_id)
        for course in theory_courses:
            tmp = course._asdict()
            del tmp["id"]
            del tmp["user"]
            tmp["update_dt"] = int(tmp["update_dt"].timestamp())

            theory_course_data.append(tmp)

        # get the users theory partner data
        theory_partner_data = []
        theory_partners = self.data.item.get_theory_partners(user_id)
        for partner in theory_partners:
            tmp = partner._asdict()
            del tmp["id"]
            del tmp["user"]

            theory_partner_data.append(tmp)

        # get the users theory running pram data
        theory_running_pram_data = []
        theory_running = self.data.item.get_theory_running(user_id)
        for running in theory_running:
            tmp = running._asdict()
            del tmp["id"]
            del tmp["user"]

            theory_running_pram_data.append(tmp)

        # get the users vs info data
        vs_info_data = []
        vs_info = self.data.item.get_vs_infos(user_id)
        for vs in vs_info:
            vs_info_data.append(
                {
                    "battle_mode": 1,
                    "vs_cnt": 1,
                    "vs_win": vs["win_flg"],
                    "invalid": 0,
                    "str": 0,
                    "str_now": 0,
                    "lose_now": 0,
                    "vs_history": vs["vs_history"],
                    "course_select_priority": 0,
                    "vsinfo_course_data": [
                        {
                            "course_id": vs["course_id"],
                            "vs_cnt": 1,
                            "vs_win": vs["win_flg"],
                        }
                    ],
                }
            )

        # get the user's car
        cars = self.data.item.get_cars(self.version, user_id, only_pickup=True)
        fulltune_count = 0
        total_car_parts_count = 0
        car_data = []
        for car in cars:
            tmp = car._asdict()
            del tmp["id"]
            del tmp["user"]
            del tmp["version"]

            car_data.append(tmp)
            # tune_level of 16 means fully tuned, so add 1 to fulltune_count
            if car["tune_level"] >= 16:
                fulltune_count += 1

            # add the number of car parts to total_car_parts_count?
            # total_car_parts_count += tmp["total_car_parts_count"]

            car_data.append(tmp)

        # update user profile car count
        user_data["have_car_cnt"] = len(car_data)

        # get the user's play stamps
        stamps = self.data.item.get_stamps(user_id)
        stamp_event_data = []
        for stamp in stamps:
            tmp = stamp._asdict()
            del tmp["id"]
            del tmp["user"]

            now = datetime.now()

            # create timestamp for today at 1am
            this_day = now.replace(hour=1, minute=0, second=0, microsecond=0)

            # check if this_day is greater than or equal to create_date_daily
            if this_day >= tmp["create_date_daily"]:
                # reset the daily stamp
                tmp["create_date_daily"] = now
                tmp["daily_bonus"] = 0

            # create a timestamp for this monday at 1am
            this_monday = now - timedelta(days=now.weekday())
            this_monday = this_monday.replace(hour=1, minute=0, second=0, microsecond=0)

            # check if this_monday is greater than or equal to create_date_weekly
            if this_monday >= tmp["create_date_weekly"]:
                # reset the weekly stamp
                tmp["create_date_weekly"] = now
                tmp["weekly_bonus"] = 0

            # update the play stamp in the database
            self.data.item.put_stamp(user_id, tmp)

            del tmp["create_date_daily"]
            del tmp["create_date_weekly"]
            stamp_event_data.append(tmp)

        # get the user's timetrial event data
        timetrial_event_data = {}
        timetrial = self.data.item.get_timetrial_event(user_id, self.timetrial_event_id)
        if timetrial is not None:
            timetrial_event_data = {
                "timetrial_event_id": timetrial["timetrial_event_id"],
                "point": timetrial["point"],
            }

        return {
            "status_code": "0",
            "user_base_data": user_data,
            "avatar_data": avatar_data,
            "pick_up_car_data": car_data,
            "story_data": self._generate_story_data(user_id),
            "vsinfo_data": vs_info_data,
            "stock_data": stock_data,
            "mission_data": {
                "id": 0,
                "achieve_flag": 0,
                "received_flag": 0,
                "update_dt": int(datetime.now().timestamp() - 86400),
            },
            "weekly_mission_data": [],
            "course_data": course_data,
            "toppatu_event_data": {
                "id": 0,
                "event_id": 0,
                "count1": 0,
                "count2": 0,
                "count3": 0,
                "accept_flag": 0,
            },
            "event_data": {
                "id": 0,
                "active_event_id": 0,
                "dialog_show_date": int(datetime.now().timestamp() - 86400),
                "show_start_dialog_flag": 1,
                "show_progress_dialog_flag": 1,
                "show_end_dialog_flag": 1,
                "end_event_id": 0,
            },
            "rewards_data": {},
            "login_bonus_data": {
                "gacha_id": 0,
                "gacha_item_id": 0,
                "category": 0,
                "type": 0,
            },
            "frozen_data": {"frozen_status": 2},
            "penalty_data": {"penalty_flag": 0, "penalty_2_level": 0},
            "config_data": config_data,
            "battle_gift_data": [],
            "ticket_data": ticket_data,
            "round_event": [],
            "last_round_event": [],
            "past_round_event": [],
            "total_round_point": 0,
            "stamp_event_data": stamp_event_data,
            "avatar_gacha_lottery_data": {"avatar_gacha_id": 0},
            "fulltune_count": fulltune_count,
            "total_car_parts_count": total_car_parts_count,
            "car_layout_count": [],
            "car_style_count": [],
            "car_use_count": [],
            "maker_use_count": [],
            "story_course": [{"course_id": 0, "count": 1}],
            # TODO!
            # "driver_debut": {
            #     "play_count": 137,
            #     "daily_play": 5,
            #     "last_play_dt": 0,
            #     "use_start_date": 0,
            #     "use_end_date": 0,
            #     "use_dt": 0,
            #     "ticket_cnt": 0,
            #     "ticket_get_bit": 0,
            # },
            "theory_data": theory_data,
            "theory_course_data": theory_course_data,
            "theory_partner_data": theory_partner_data,
            "theory_running_pram_data": theory_running_pram_data,
            "special_mode_data": self._generate_special_data(user_id),
            "challenge_mode_data": self._generate_challenge_data(user_id),
            "season_rewards_data": [],
            "timetrial_event_data": timetrial_event_data,
            "special_mode_hint_data": {"story_type": 0, "hint_display_flag": 0},
        }

    def handle_timetrial_getbestrecordpreta_request(self, data: Dict, headers: Dict):
        user_id = headers["session"]

        for car_id in data["car_ids"]:
            pass

        course_mybest_data = []
        courses = self.data.item.get_time_trial_user_best_courses(self.version, user_id)
        for course in courses:
            course_mybest_data.append(
                {
                    "course_id": course["course_id"],
                    # local rank, store rank, worldwide rank?
                    "rank": 1,
                    # no clue
                    "member": 10000,
                    # goal_time in ms
                    "value": course["goal_time"],
                    # total number of entries per course?
                    "total": 10,
                    "store": self.core_cfg.server.name,
                    # use car_id from request?
                    "car_id": 0,
                    "style_car_id": course["style_car_id"],
                    "play_dt": course["play_dt"].timestamp(),
                    "section_time_1": course["section_time_1"],
                    "section_time_2": course["section_time_2"],
                    "section_time_3": course["section_time_3"],
                    "section_time_4": course["section_time_4"],
                    # no clue
                    "mission": course["mission"],
                }
            )

        course_pickup_car_best_data = []
        courses = self.data.item.get_time_trial_courses(self.version)
        for course in courses:
            car_list = []
            best_cars = self.data.item.get_time_trial_best_cars_by_course(
                self.version, course["course_id"], user_id
            )

            for i, car in enumerate(best_cars):
                car_list.append(
                    {
                        "rank": i + 1,
                        # no clue
                        "member": user_id,
                        "value": car["goal_time"],
                        "store": self.core_cfg.server.name,
                        # use car_id from request?
                        "car_id": 0,
                        "style_car_id": car["style_car_id"],
                        "play_dt": car["play_dt"].timestamp(),
                        "section_time_1": car["section_time_1"],
                        "section_time_2": car["section_time_2"],
                        "section_time_3": car["section_time_3"],
                        "section_time_4": car["section_time_4"],
                        "mission": car["mission"],
                    }
                )

            course_pickup_car_best_data.append(
                {
                    "course_id": course["course_id"],
                    "car_list": car_list,
                }
            )

        return {
            "status_code": "0",
            "course_mybest_data": course_mybest_data,
            "course_pickup_car_best_data": course_pickup_car_best_data,
        }

    def handle_timetrial_getbestrecordprerace_request(self, data: Dict, headers: Dict):
        user_id = headers["session"]

        course_id = data["course_id"]
        for car in data["car_ids"]:
            # TODO: get the best record for this car
            style_car_id = car["style_car_id"]

        # Not sure if this is actually correct
        ranking = self.data.item.get_time_trial_ranking_by_course(
            self.version, course_id
        )
        course_best_data = []
        for i, rank in enumerate(ranking):
            car_user_id = rank["user"]

            # get the username, country and store from the profile
            profile = self.data.profile.get_profile(car_user_id, self.version)
            arcade = self.data.arcade.get_arcade(profile["store"])

            if arcade is None:
                arcade = {}
                arcade["name"] = self.core_cfg.server.name

            # should never happen
            if profile is None:
                continue

            course_best_data.append(
                {
                    "course_id": course_id,
                    "rank": i + 1,
                    "member": car_user_id,
                    "value": rank["goal_time"],
                    "store": arcade["name"],
                    # use car_id from request?
                    "car_id": 0,
                    "style_car_id": rank["style_car_id"],
                    "play_dt": rank["play_dt"].timestamp(),
                    "section_time_1": rank["section_time_1"],
                    "section_time_2": rank["section_time_2"],
                    "section_time_3": rank["section_time_3"],
                    "section_time_4": rank["section_time_4"],
                    "mission": rank["mission"],
                }
            )

        best_cars = self.data.item.get_time_trial_best_cars_by_course(
            self.version, course_id
        )

        car_list = []
        for i, rank in enumerate(best_cars):
            car_user_id = rank["user"]
            # get the username, country and store from the profile
            profile = self.data.profile.get_profile(car_user_id, self.version)
            arcade = self.data.arcade.get_arcade(profile["store"])

            if arcade is None:
                arcade = {}
                arcade["name"] = self.core_cfg.server.name

            # should never happen
            if profile is None:
                continue

            car_list.append(
                {
                    "rank": i + 1,
                    # no clue
                    "member": car_user_id,
                    "value": rank["goal_time"],
                    "store": arcade["name"],
                    # use car_id from request?
                    "car_id": 0,
                    "style_car_id": rank["style_car_id"],
                    "play_dt": rank["play_dt"].timestamp(),
                    "section_time_1": rank["section_time_1"],
                    "section_time_2": rank["section_time_2"],
                    "section_time_3": rank["section_time_3"],
                    "section_time_4": rank["section_time_4"],
                    "mission": rank["mission"],
                }
            )

        return {
            "status_code": "0",
            "course_car_best_data": [{"course_id": course_id, "car_list": car_list}],
            "course_best_data": course_best_data,
        }

    def handle_user_createaccount_request(self, data: Dict, headers: Dict):
        user_id = headers["session"]

        car_data: Dict = data.pop("car_obj")
        parts_data: List = car_data.pop("parts_list")
        avatar_data: Dict = data.pop("avatar_obj")
        config_data: Dict = data.pop("config_obj")

        rank_data: Dict = data.pop("mode_rank_data")
        stock_data: Dict = data.pop("takeover_stock_obj")
        takeover_ticket_list: List = data.pop("takeover_ticket")

        # not required?
        use_ticket = data.pop("use_ticket")

        # save profile in database
        data["store"] = headers.get("a_store", 0)
        data["country"] = headers.get("a_country", 0)
        data["asset_version"] = headers.get("asset_version", 1)
        self.data.profile.put_profile(user_id, self.version, data)

        # save rank data in database
        self.data.profile.put_profile_rank(user_id, self.version, rank_data)

        # save stock data in database
        self._save_stock_data(user_id, stock_data)

        # save tickets in database
        for ticket in takeover_ticket_list:
            self.data.item.put_ticket(user_id, ticket)

        config_data["config_id"] = config_data.pop("id")
        self.data.profile.put_profile_config(user_id, config_data)
        self.data.profile.put_profile_avatar(user_id, avatar_data)

        # save car data and car parts in database
        car_data["parts_list"] = parts_data
        self.data.item.put_car(user_id, self.version, car_data)

        return {"status_code": "0"}

    def handle_user_updatelogin_request(self, data: Dict, headers: Dict):
        pass

    def handle_timetrial_getcarbest_request(self, data: Dict, headers: Dict):
        pass

    def handle_factory_avatargacharesult_request(self, data: Dict, headers: Dict):
        user_id = headers["session"]

        stock_data: Dict = data.pop("stock_obj")
        use_ticket_cnt = data["use_ticket_cnt"]

        # save stock data in database
        self._save_stock_data(user_id, stock_data)

        # get the user's ticket
        tickets: list = self.data.item.get_tickets(user_id)
        ticket_list = []
        for ticket in tickets:
            # avatar tickets
            if ticket["ticket_id"] == 5:
                ticket_data = {
                    "ticket_id": ticket["ticket_id"],
                    "ticket_cnt": ticket["ticket_cnt"] - use_ticket_cnt,
                }

                # update the ticket in the database
                self.data.item.put_ticket(user_id, ticket_data)
                ticket_list.append(ticket_data)

                continue

            ticket_list.append(
                {
                    "ticket_id": ticket["ticket_id"],
                    "ticket_cnt": ticket["ticket_cnt"],
                }
            )

        return {"status_code": "0", "ticket_data": ticket_list}

    def handle_factory_savefavoritecar_request(self, data: Dict, headers: Dict):
        user_id = headers["session"]

        # save favorite cars in database
        for car in data["pickup_on_car_ids"]:
            self.data.item.put_car(user_id, self.version, car)

        for car in data["pickup_off_car_ids"]:
            self.data.item.put_car(
                user_id,
                self.version,
                {"style_car_id": car["style_car_id"], "pickup_seq": 0},
            )

        return {"status_code": "0"}

    def handle_factory_updatemultiplecustomizeresult_request(
        self, data: Dict, headers: Dict
    ):
        user_id = headers["session"]

        car_list = data.pop("car_list")
        ticket_data: List = data.pop("ticket_data")

        # unused
        total_car_parts_count = data.pop("total_car_parts_count")

        # save tickets in database
        for ticket in ticket_data:
            self.data.item.put_ticket(user_id, ticket)

        for car in car_list:
            # save car data and car parts in database
            self.data.item.put_car(user_id, self.version, car)

        return {"status_code": "0"}

    def handle_factory_updatecustomizeresult_request(self, data: Dict, headers: Dict):
        user_id = headers["session"]

        parts_data: List = data.pop("parts_list")
        ticket_data: List = data.pop("ticket_data")

        # save tickets in database
        for ticket in ticket_data:
            self.data.item.put_ticket(user_id, ticket)

        # save car data in database
        data["parts_list"] = parts_data
        self.data.item.put_car(user_id, self.version, data)

        return {"status_code": "0"}

    def handle_factory_getcardata_request(self, data: Dict, headers: Dict):
        user_id = headers["session"]

        cars = self.data.item.get_cars(self.version, user_id)
        car_data = []
        for car in cars:
            tmp = car._asdict()
            del tmp["id"]
            del tmp["user"]
            del tmp["version"]

            car_data.append(tmp)

        return {
            "status_code": "0",
            "car_data": car_data,
        }

    def handle_factory_renamebefore_request(self, data: Dict, headers: Dict):
        pass

    def handle_factory_buycarresult_request(self, data: Dict, headers: Dict):
        user_id = headers["session"]

        parts_data: List = data.pop("parts_list")
        pickup_on_list: List = data.pop("pickup_on_car_ids")
        pickup_off_list: List = data.pop("pickup_off_car_ids")

        style_car_id = data.get("style_car_id")

        # get the pickup_seq for the new car
        pickup_seq = 0
        # save favorite cars in database
        for car in pickup_on_list:
            # if the new car is a favorite get the new pickup_seqn for later
            if car["style_car_id"] == style_car_id:
                pickup_seq = car["pickup_seq"]
            else:
                self.data.item.put_car(user_id, self.version, car)

        data["pickup_seq"] = pickup_seq

        cash = data.pop("cash")
        total_cash = data.pop("total_cash")

        # save the new cash in database
        self.data.profile.put_profile(
            user_id, self.version, {"total_cash": total_cash, "cash": cash}
        )

        # full tune ticket
        use_ticket = data.pop("use_ticket")
        if use_ticket:
            # get the user's tickets, full tune ticket id is 25
            ticket = self.data.item.get_ticket(user_id, ticket_id=25)

            # update the ticket in the database
            self.data.item.put_ticket(
                user_id,
                {
                    "ticket_id": ticket["ticket_id"],
                    "ticket_cnt": ticket["ticket_cnt"] - 1,
                },
            )

            # also set the tune_level to 16 (fully tuned)
            data["tune_level"] = 16

        # save car data and car parts in database
        data["parts_list"] = parts_data
        self.data.item.put_car(user_id, self.version, data)

        for car in pickup_off_list:
            self.data.item.put_car(
                user_id,
                self.version,
                {"style_car_id": car["style_car_id"], "pickup_seq": 0},
            )

        # get the user's car
        cars = self.data.item.get_cars(self.version, user_id)
        fulltune_count = 0
        total_car_parts_count = 0
        for car in cars:
            # tune_level of 16 means fully tuned, so add 1 to fulltune_count
            if car["tune_level"] >= 16:
                fulltune_count += 1

            # add the number of car parts to total_car_parts_count
            # total_car_parts_count += car["total_car_parts_count"]

        # get the user's ticket
        tickets = self.data.item.get_tickets(user_id)
        ticket_data = []
        for ticket in tickets:
            ticket_data.append(
                {
                    "ticket_id": ticket["ticket_id"],
                    "ticket_cnt": ticket["ticket_cnt"],
                }
            )

        return {
            "status_code": "0",
            "ticket_data": ticket_data,
            "fulltune_count": fulltune_count,
            "total_car_parts_count": total_car_parts_count,
            "car_layout_count": [],
            "car_style_count": [],
        }

    def handle_factory_renameresult_request(self, data: Dict, headers: Dict):
        user_id = headers["session"]

        new_username = data.get("username")

        # save new username in database
        if new_username:
            self.data.profile.put_profile(user_id, self.version, data)

        return {"status_code": "0"}

    def handle_factory_updatecustomizeavatar_request(self, data: Dict, headers: Dict):
        user_id = headers["session"]

        avatar_data: Dict = data.pop("avatar_obj")
        stock_data: Dict = data.pop("stock_obj")

        # update the stock data in database
        self._save_stock_data(user_id, stock_data)

        # save avatar data and avatar parts in database
        self.data.profile.put_profile_avatar(user_id, avatar_data)

        return {"status_code": "0"}

    def handle_factory_updatecustomizeuser_request(self, data: Dict, headers: Dict):
        user_id = headers["session"]

        stock_data: Dict = data.pop("stock_obj")

        # update the stock data in database
        self._save_stock_data(user_id, stock_data)

        # update profile data and config in database
        self.data.profile.put_profile(user_id, self.version, data)

        return {"status_code": "0"}

    def handle_user_updatestampinfo_request(self, data: Dict, headers: Dict):
        user_id = headers["session"]

        stamp_event_data = data.pop("stamp_event_data")
        for stamp in stamp_event_data:
            self.data.item.put_stamp(user_id, stamp)

        return {"status_code": "0"}

    def handle_user_updatetimetrialresult_request(self, data: Dict, headers: Dict):
        user_id = headers["session"]

        stock_data: Dict = data.pop("stock_obj")
        ticket_data: List = data.pop("ticket_data")
        reward_dist_data: Dict = data.pop("reward_dist_obj")
        driver_debut_data = data.pop("driver_debut_obj")
        rank_data: Dict = data.pop("mode_rank_obj")

        # time trial event points
        event_point = data.pop("event_point")

        # save stock data in database
        self._save_stock_data(user_id, stock_data)

        # save tickets in database
        for ticket in ticket_data:
            self.data.item.put_ticket(user_id, ticket)

        # save mode rank data in database
        rank_data.update(reward_dist_data)
        self.data.profile.put_profile_rank(user_id, self.version, rank_data)

        # get the profile data, update total_play and daily_play, and save it
        profile = self.data.profile.get_profile(user_id, self.version)
        total_play = profile["total_play"] + 1

        # update profile
        self.data.profile.put_profile(
            user_id,
            self.version,
            {
                "total_play": total_play,
                "last_play_date": datetime.now(),
                "aura_id": data.pop("aura_id"),
                "aura_color_id": data.pop("aura_color_id"),
                "aura_line_id": data.pop("aura_line_id"),
                "cash": data.pop("cash"),
                "total_cash": data.pop("total_cash"),
                "dressup_point": data.pop("dressup_point"),
                "avatar_point": data.pop("avatar_point"),
                "mileage": data.pop("mileage"),
            },
        )

        # get the use_count and story_use_count of the used car
        style_car_id = data.get("style_car_id")
        car_mileage = data.pop("car_mileage")
        used_car = self.data.item.get_car(user_id, self.version, style_car_id)._asdict()

        # increase the use_count and story_use_count of the used car
        used_car["use_count"] += 1
        used_car["timetrial_use_count"] += 1
        used_car["car_mileage"] = car_mileage

        # save the used car in database
        self.data.item.put_car(user_id, self.version, used_car)

        # skill_level_exp is the "course proeficiency" and is saved
        # in the course table
        course_id = data.get("course_id")
        run_counts = 1
        skill_level_exp = data.pop("skill_level_exp")

        # get the course data
        course = self.data.item.get_course(user_id, course_id)
        if course:
            # update run_counts
            run_counts = course["run_counts"] + 1

        self.data.item.put_course(
            user_id,
            {
                "course_id": course_id,
                "run_counts": run_counts,
                "skill_level_exp": skill_level_exp,
            },
        )

        goal_time = data.get("goal_time")
        # grab the ranking data and count the numbers of rows with a faster time
        # than the current goal_time
        course_rank = self.data.item.get_time_trial_ranking_by_course(
            self.version, course_id, limit=None
        )
        course_rank = len([r for r in course_rank if r["goal_time"] < goal_time]) + 1

        car_course_rank = self.data.item.get_time_trial_ranking_by_course(
            self.version, course_id, style_car_id, limit=None
        )
        car_course_rank = (
            len([r for r in car_course_rank if r["goal_time"] < goal_time]) + 1
        )

        # only update the time if its better than the best time and also not 0
        if data.get("goal_time") > 0:
            # get the current best goal time
            best_time_trial = (
                self.data.item.get_time_trial_user_best_time_by_course_car(
                    self.version, user_id, course_id, style_car_id
                )
            )

            if (
                best_time_trial is None
                or data.get("goal_time") < best_time_trial["goal_time"]
            ):
                # now finally save the time trial with updated timestamp
                data["play_dt"] = datetime.now()
                self.data.item.put_time_trial(self.version, user_id, data)

        # update the timetrial event points
        self.data.item.put_timetrial_event(
            user_id, self.timetrial_event_id, event_point
        )

        return {
            "status_code": "0",
            "course_rank": course_rank,
            "course_car_rank": car_course_rank,
            "location_course_store_rank": course_rank,
            "car_use_count": [],
            "maker_use_count": [],
            "timetrial_event_data": {
                "timetrial_event_id": self.timetrial_event_id,
                "point": event_point,
            },
        }

    def handle_user_updatestoryresult_request(self, data: Dict, headers: Dict):
        user_id = headers["session"]

        stock_data: Dict = data.pop("stock_obj")
        ticket_data: List = data.pop("ticket_data")
        reward_dist_data: Dict = data.pop("reward_dist_obj")
        driver_debut_data = data.pop("driver_debut_obj")
        rank_data: Dict = data.pop("mode_rank_obj")
        # stamp_event_data = data.pop("stamp_event_data")

        # save stock data in database
        self._save_stock_data(user_id, stock_data)

        # save tickets in database
        for ticket in ticket_data:
            self.data.item.put_ticket(user_id, ticket)

        # save mode rank data in database
        rank_data.update(reward_dist_data)
        self.data.profile.put_profile_rank(user_id, self.version, rank_data)

        # save the current story progress in database
        max_loop = data.get("chapter_loop_max")
        chapter_id = data.get("chapter")

        episode_id = data.get("episode")
        difficulty = data.get("difficulty")
        play_status = data.get("play_status")

        # get the current loop from the database
        story_data = self.data.item.get_story(user_id, chapter_id)
        # 1 = active, 2+ = cleared?
        loop_count = 1
        if story_data:
            loop_count = story_data["loop_count"]

        # if the played difficulty is smaller than loop_count you cannot clear
        # (play_status = 2) the episode otherwise the following difficulties
        # won't earn any EXP?
        if difficulty < loop_count:
            play_status = 1

        # if the episode has already been cleared, set the play_status to 2
        # so it won't be set to unplayed (play_status = 1)
        episode_data = self.data.item.get_story_episode(user_id, episode_id)
        if episode_data:
            if play_status < episode_data["play_status"]:
                play_status = 2

        # save the current episode progress in database
        self.data.item.put_story_episode(
            user_id,
            chapter_id,
            {
                "episode": episode_id,
                "play_status": play_status,
            },
        )

        if loop_count < max_loop and data.get("chapter_clear") == 1:
            # increase the loop count
            loop_count += 1

            # for the current chapter set all episode play_status back to 1
            self.data.item.put_story_episode_play_status(user_id, chapter_id, 1)

        self.data.item.put_story(
            user_id,
            {
                "story_type": data.get("story_type"),
                "chapter": chapter_id,
                "loop_count": loop_count,
            },
        )

        # save the current episode difficulty progress in database
        self.data.item.put_story_episode_difficulty(
            user_id,
            episode_id,
            {
                "difficulty": difficulty,
                "play_count": 1,  # no idea where this comes from
                "clear_count": 1,  # no idea where this comes from
                "play_status": data.get("play_status"),
                "play_score": data.get("play_score"),
            },
        )

        # get the use_count and story_use_count of the used car
        style_car_id = data.get("style_car_id")
        car_mileage = data.get("car_mileage")
        used_car = self.data.item.get_car(user_id, self.version, style_car_id)._asdict()

        # increase the use_count and story_use_count of the used car
        used_car["use_count"] += 1
        used_car["story_use_count"] += 1
        used_car["car_mileage"] = car_mileage

        # save the used car in database
        self.data.item.put_car(user_id, self.version, used_car)

        # get the profile data, update total_play and daily_play, and save it
        profile = self.data.profile.get_profile(user_id, self.version)
        total_play = profile["total_play"] + 1

        # save user profile in database
        self.data.profile.put_profile(
            user_id,
            self.version,
            {
                "total_play": total_play,
                "last_play_date": datetime.now(),
                "mileage": data.pop("mileage"),
                "cash": data.pop("cash"),
                "total_cash": data.pop("total_cash"),
                "dressup_point": data.pop("dressup_point"),
                "avatar_point": data.pop("avatar_point"),
                "aura_id": data.pop("aura_id"),
                "aura_color_id": data.pop("aura_color_id"),
                "aura_line_id": data.pop("aura_line_id"),
            },
        )

        return {
            "status_code": "0",
            "story_data": self._generate_story_data(user_id),
            "car_use_count": [],
            "maker_use_count": [],
        }

    def handle_user_updatespecialmoderesult_request(self, data: Dict, headers: Dict):
        user_id = headers["session"]

        stock_data: Dict = data.pop("stock_obj")
        ticket_data: List = data.pop("ticket_data")
        reward_dist_data: Dict = data.pop("reward_dist_obj")
        driver_debut_data = data.pop("driver_debut_obj")
        rank_data: Dict = data.pop("mode_rank_obj")

        # unused
        hint_display_flag: int = data.pop("hint_display_flag")

        # get the vs use count from database and update it
        style_car_id = data.pop("style_car_id")
        car_data = self.data.item.get_car(user_id, self.version, style_car_id)
        story_use_count = car_data["story_use_count"] + 1

        # save car data in database
        self.data.item.put_car(
            user_id,
            self.version,
            {
                "style_car_id": style_car_id,
                "car_mileage": data.pop("car_mileage"),
                "story_use_count": story_use_count,
            },
        )

        # get the profile data, update total_play and daily_play, and save it
        profile = self.data.profile.get_profile(user_id, self.version)
        total_play = profile["total_play"] + 1

        # save user profile in database
        self.data.profile.put_profile(
            user_id,
            self.version,
            {
                "total_play": total_play,
                "last_play_date": datetime.now(),
                "mileage": data.pop("mileage"),
                "cash": data.pop("cash"),
                "total_cash": data.pop("total_cash"),
                "dressup_point": data.pop("dressup_point"),
                "avatar_point": data.pop("avatar_point"),
                "aura_id": data.pop("aura_id"),
                "aura_color_id": data.pop("aura_color_id"),
                "aura_line_id": data.pop("aura_line_id"),
            },
        )

        # save stock data in database
        self._save_stock_data(user_id, stock_data)

        # save ticket data in database
        for ticket in ticket_data:
            self.data.item.put_ticket(user_id, ticket)

        # save mode_rank and reward_dist data in database
        rank_data.update(reward_dist_data)
        self.data.profile.put_profile_rank(user_id, self.version, rank_data)

        # finally save the special mode with story_type=4 in database
        self.data.item.put_challenge(user_id, data)

        return {
            "status_code": "0",
            "special_mode_data": self._generate_special_data(user_id),
            "car_use_count": [],
            "maker_use_count": [],
        }

    def handle_user_updatechallengemoderesult_request(self, data: Dict, headers: Dict):
        user_id = headers["session"]

        stock_data: Dict = data.pop("stock_obj")
        ticket_data: List = data.pop("ticket_data")
        reward_dist_data: Dict = data.pop("reward_dist_obj")
        driver_debut_data = data.pop("driver_debut_obj")
        rank_data: Dict = data.pop("mode_rank_obj")

        # get the vs use count from database and update it
        style_car_id = data.get("style_car_id")
        car_data = self.data.item.get_car(user_id, self.version, style_car_id)
        story_use_count = car_data["story_use_count"] + 1

        # save car data in database
        self.data.item.put_car(
            user_id,
            self.version,
            {
                "style_car_id": style_car_id,
                "car_mileage": data.pop("car_mileage"),
                "story_use_count": story_use_count,
            },
        )

        # get the profile data, update total_play and daily_play, and save it
        profile = self.data.profile.get_profile(user_id, self.version)
        total_play = profile["total_play"] + 1

        # save user profile in database
        self.data.profile.put_profile(
            user_id,
            self.version,
            {
                "total_play": total_play,
                "last_play_date": datetime.now(),
                "mileage": data.pop("mileage"),
                "cash": data.pop("cash"),
                "total_cash": data.pop("total_cash"),
                "dressup_point": data.pop("dressup_point"),
                "avatar_point": data.pop("avatar_point"),
                "aura_id": data.pop("aura_id"),
                "aura_color_id": data.pop("aura_color_id"),
                "aura_line_id": data.pop("aura_line_id"),
            },
        )

        # save stock data in database
        self._save_stock_data(user_id, stock_data)

        # save ticket data in database
        for ticket in ticket_data:
            self.data.item.put_ticket(user_id, ticket)

        # save mode_rank and reward_dist data in database
        rank_data.update(reward_dist_data)
        self.data.profile.put_profile_rank(user_id, self.version, rank_data)

        # get the challenge mode data from database
        challenge_data = self.data.item.get_challenge(
            user_id, data.get("vs_type"), data.get("play_difficulty")
        )

        if challenge_data:
            # update play count
            play_count = challenge_data["play_count"] + 1
            data["play_count"] = play_count

        # finally save the challenge mode with story_type=3 in database
        self.data.item.put_challenge(user_id, data)

        return {
            "status_code": "0",
            "challenge_mode_data": self._generate_challenge_data(user_id),
            "car_use_count": [],
            "maker_use_count": [],
        }

    def _generate_time_trial_data(self, season_id: int, user_id: int) -> List[Dict]:
        # get the season time trial data from database
        timetrial_data = []

        courses = self.data.item.get_courses(user_id)
        if courses is None or len(courses) == 0:
            return {"status_code": "0", "timetrial_data": timetrial_data}

        for course in courses:
            # grab the course id and course proeficiency
            course_id = course["course_id"]
            skill_level_exp = course["skill_level_exp"]

            # get the best time for the current course for the current user
            best_trial = self.data.item.get_time_trial_best_ranking_by_course(
                season_id, user_id, course_id
            )
            if not best_trial:
                continue

            goal_time = best_trial["goal_time"]
            # get the rank for the current course
            course_rank = self.data.item.get_time_trial_ranking_by_course(
                season_id, course_id, limit=None
            )
            course_rank = (
                len([r for r in course_rank if r["goal_time"] < goal_time]) + 1
            )

            timetrial_data.append(
                {
                    "style_car_id": best_trial["style_car_id"],
                    "course_id": course_id,
                    "skill_level_exp": skill_level_exp,
                    "goal_time": goal_time,
                    "rank": course_rank,
                    "rank_dt": int(best_trial["play_dt"].timestamp()),
                }
            )

        return timetrial_data

    def handle_user_getpastseasontadata_request(self, data: Dict, headers: Dict):
        user_id = headers["session"]
        season_id = data.get("season_id")

        # so to get the season 1 data just subtract 1 from the season id
        past_timetrial_data = self._generate_time_trial_data(season_id - 1, user_id)

        # TODO: get the current season timetrial data somehow, because after requesting
        # GetPastSeasonTAData the game will NOT request GetTAData?!
        return {
            "status_code": "0",
            "season_id": season_id,
            "past_season_timetrial_data": past_timetrial_data,
        }

    def handle_user_gettadata_request(self, data: Dict, headers: Dict):
        user_id = headers["session"]

        timetrial_data = self._generate_time_trial_data(self.version, user_id)

        # TODO: get the past season timetrial data somehow, because after requesting
        # GetTAData the game will NOT request GetPastSeasonTAData?!
        return {
            "status_code": "0",
            "timetrial_data": timetrial_data,
            # "past_season_timetrial_data": timetrial_data,
        }

    def handle_user_updatecartune_request(self, data: Dict, headers: Dict):
        user_id = headers["session"]

        # full tune ticket
        use_ticket = data.pop("use_ticket")
        if use_ticket:
            # get the user's tickets, full tune ticket id is 25
            ticket = self.data.item.get_ticket(user_id, ticket_id=25)

            # update the ticket in the database
            self.data.item.put_ticket(
                user_id,
                {
                    "ticket_id": ticket["ticket_id"],
                    "ticket_cnt": ticket["ticket_cnt"] - 1,
                },
            )

            # also set the tune_level to 16 (fully tuned)
            data["tune_level"] = 16

        self.data.item.put_car(user_id, self.version, data)

        return {
            "status_code": "0",
            "story_data": self._generate_story_data(user_id),
            "car_use_count": [],
            "maker_use_count": [],
        }

    def handle_log_saveplaylog_request(self, data: Dict, headers: Dict):
        pass

    def handle_log_saveendlog_request(self, data: Dict, headers: Dict):
        pass

    def handle_user_updatemoderesult_request(self, data: Dict, headers: Dict):
        user_id = headers["session"]

        config_data: Dict = data.pop("config_obj")
        stock_data: Dict = data.pop("stock_obj")
        ticket_data: List = data.pop("ticket_data")
        reward_dist_data: Dict = data.pop("reward_dist_obj")

        # not required?
        mode_id = data.pop("mode_id")
        standby_play_flag = data.pop("standby_play_flag")
        tips_list = data.pop("tips_list")

        # save stock data in database
        self._save_stock_data(user_id, stock_data)

        # save tickets in database
        for ticket in ticket_data:
            self.data.item.put_ticket(user_id, ticket)

        # save rank dist data in database
        self.data.profile.put_profile_rank(user_id, self.version, reward_dist_data)

        # update profile data and config in database
        self.data.profile.put_profile(user_id, self.version, data)
        config_data["config_id"] = config_data.pop("id")
        self.data.profile.put_profile_config(user_id, config_data)

        return {"status_code": "0", "server_status": 1}

    def _generate_theory_rival_data(
        self, user_list: list, course_id: int, req_user_id: int
    ) -> list:
        rival_data = []
        for user_id in user_list:
            # if not enough players are available just use the data from the req_user
            if user_id == -1:
                profile = self.data.profile.get_profile(req_user_id, self.version)
                profile = profile._asdict()
                # set the name to CPU
                profile["username"] = f"ＣＰＵ"
                # also reset stamps to default
                profile["country"] = 9
                profile["store"] = 0
                profile["stamp_key_assign_0"] = 0
                profile["stamp_key_assign_1"] = 1
                profile["stamp_key_assign_2"] = 2
                profile["stamp_key_assign_3"] = 3
                profile["mytitle_id"] = 0
            else:
                profile = self.data.profile.get_profile(user_id, self.version)

            rank = self.data.profile.get_profile_rank(profile["user"], self.version)

            avatars = [
                {
                    "sex": 0,
                    "face": 1,
                    "eye": 1,
                    "mouth": 1,
                    "hair": 1,
                    "glasses": 0,
                    "face_accessory": 0,
                    "body": 1,
                    "body_accessory": 0,
                    "behind": 0,
                    "bg": 1,
                    "effect": 0,
                    "special": 0,
                },
                {
                    "sex": 0,
                    "face": 1,
                    "eye": 1,
                    "mouth": 1,
                    "hair": 19,
                    "glasses": 0,
                    "face_accessory": 0,
                    "body": 2,
                    "body_accessory": 0,
                    "behind": 0,
                    "bg": 1,
                    "effect": 0,
                    "special": 0,
                },
                {
                    "sex": 1,
                    "face": 91,
                    "eye": 265,
                    "mouth": 13,
                    "hair": 369,
                    "glasses": 0,
                    "face_accessory": 0,
                    "body": 113,
                    "body_accessory": 0,
                    "behind": 0,
                    "bg": 1,
                    "effect": 0,
                    "special": 0,
                },
                {
                    "sex": 1,
                    "face": 91,
                    "eye": 265,
                    "mouth": 13,
                    "hair": 387,
                    "glasses": 0,
                    "face_accessory": 0,
                    "body": 114,
                    "body_accessory": 0,
                    "behind": 0,
                    "bg": 1,
                    "effect": 0,
                    "special": 0,
                },
            ]

            if user_id == -1:
                # get a random avatar from the list and some random car from all users
                avatar = choice(avatars)
                car = self.data.item.get_random_car(self.version)
            else:
                avatar = self.data.profile.get_profile_avatar(profile["user"])
                car = self.data.item.get_random_user_car(profile["user"], self.version)

            parts_list = []
            for part in car["parts_list"]:
                parts_list.append(part["parts"])

            course = self.data.item.get_theory_course(profile["user"], course_id)
            powerhose_lv = 0
            if course:
                powerhose_lv = course["powerhouse_lv"]

            theory_running = self.data.item.get_theory_running_by_course(
                profile["user"], course_id
            )

            # normally it's 127 after the first play so we set it to 128
            attack = 128
            defense = 128
            safety = 128
            runaway = 128
            trick_flag = 0
            if theory_running and user_id != -1:
                attack = theory_running["attack"]
                defense = theory_running["defense"]
                safety = theory_running["safety"]
                runaway = theory_running["runaway"]
                trick_flag = theory_running["trick_flag"]

            # get the time trial ranking medal
            eval_id = 0
            time_trial = self.data.item.get_time_trial_best_ranking_by_course(
                self.version, profile["user"], course_id
            )
            if time_trial:
                eval_id = time_trial["eval_id"]

            arcade = self.data.arcade.get_arcade(profile["store"])
            if arcade is None:
                arcade = {}
                arcade["name"] = self.core_cfg.server.name

            rival_data.append(
                {
                    "id": profile["user"],
                    "name": profile["username"],
                    "grade": rank["grade"],
                    # only needed for power match
                    "powerhouseLv": powerhose_lv,
                    "mytitleId": profile["mytitle_id"],
                    "country": profile["country"],
                    "auraId": profile["aura_id"],
                    "auraColor": profile["aura_color_id"],
                    "auraLine": profile["aura_line_id"],
                    # not sure?
                    "roundRanking": 0,
                    "storeName": arcade["name"],
                    "sex": avatar["sex"],
                    "face": avatar["face"],
                    "eye": avatar["eye"],
                    "mouth": avatar["mouth"],
                    "hair": avatar["hair"],
                    "glasses": avatar["glasses"],
                    "faceAccessory": avatar["face_accessory"],
                    "body": avatar["body"],
                    "bodyAccessory": avatar["body_accessory"],
                    "behind": avatar["behind"],
                    "bg": avatar["bg"],
                    "effect": avatar["effect"],
                    "special": avatar["special"],
                    "styleCarId": car["style_car_id"],
                    "color": car["color"],
                    "bureau": car["bureau"],
                    "kana": car["kana"],
                    "sNo": car["s_no"],
                    "lNo": car["l_no"],
                    "tuneLv": car["tune_level"],
                    "carFlag": car["car_flag"],
                    "tunePoint": car["tune_point"],
                    "infinityTune": car["infinity_tune"],
                    "tuneParts": car["tune_parts"],
                    "partsList": parts_list,
                    "partsCount": car["equip_parts_count"],
                    "stamp0": profile["stamp_key_assign_0"],
                    "stamp1": profile["stamp_key_assign_1"],
                    "stamp2": profile["stamp_key_assign_2"],
                    "stamp3": profile["stamp_key_assign_3"],
                    "attack": attack,
                    "defense": defense,
                    "safety": safety,
                    "runaway": runaway,
                    "trickFlg": trick_flag,
                    # time trial ranking medal
                    "taEval": eval_id,
                }
            )

        return rival_data

    def handle_theory_matching_request(self, data: Dict, headers: Dict):
        user_id = headers["session"]

        course_id = data.pop("course_id")
        # no idea why thats needed?
        grade = data.pop("grade")

        # number of auto_matches and power_matches, official values are:
        count_auto_match = 9
        count_power_match = 3

        # required for the power_match list?
        powerhose_lv = data.pop("powerhouse_lv")

        # get random profiles for auto match
        profiles = self.data.profile.get_different_random_profiles(
            user_id, self.version, count=count_auto_match
        )

        user_list = [profile["user"] for profile in profiles]
        # if user_list is not count_auto_match long, fill it up with -1
        while len(user_list) < count_auto_match:
            user_list.append(-1)

        auto_match = self._generate_theory_rival_data(user_list, course_id, user_id)

        # get profiles with the same powerhouse_lv for power match
        theory_courses = self.data.item.get_theory_course_by_powerhouse_lv(
            user_id, course_id, powerhose_lv, count=count_power_match
        )
        user_list = [course["user"] for course in theory_courses]

        # if user_list is not count_power_match long, fill it up with -1
        while len(user_list) < count_power_match:
            user_list.append(-1)

        power_match = self._generate_theory_rival_data(user_list, course_id, user_id)

        return {
            "status_code": "0",
            "server_status": 1,
            "rival_data": {
                "auto_match": auto_match,
                "power_match": power_match,
            },
        }

    def handle_user_updatetheoryresult_request(self, data: Dict, headers: Dict):
        user_id = headers["session"]

        stock_data: Dict = data.pop("stock_obj")
        ticket_data: List = data.pop("ticket_data")
        reward_dist_data: Dict = data.pop("reward_dist_obj")
        rank_data: Dict = data.pop("mode_rank_obj")
        driver_debut_data: Dict = data.pop("driver_debut_obj")

        # save stock data in database
        self._save_stock_data(user_id, stock_data)

        # save tickets in database
        for ticket in ticket_data:
            self.data.item.put_ticket(user_id, ticket)

        # save rank dist data in database
        rank_data.update(reward_dist_data)
        self.data.profile.put_profile_rank(user_id, self.version, rank_data)

        # save the profile theory data in database
        play_count = 1
        play_count_multi = 1
        win_count = 0
        win_count_multi = 0

        theory_data = self.data.profile.get_profile_theory(user_id, self.version)
        if theory_data:
            play_count = theory_data["play_count"] + 1
            play_count_multi = theory_data["play_count_multi"] + 1
            win_count = theory_data["win_count"]
            win_count_multi = theory_data["win_count_multi"]

        # check all advantages and see if one of them is larger than 0
        # if so, we won
        if (
            data.get("advantage_1") > 0
            or data.get("advantage_2") > 0
            or data.get("advantage_3") > 0
            or data.get("advantage_4") > 0
        ):
            win_count += 1
            win_count_multi += 1

        self.data.profile.put_profile_theory(
            user_id,
            self.version,
            {
                "play_count": play_count,
                "play_count_multi": play_count_multi,
                "partner_id": data.get("partner_id"),
                "partner_progress": data.get("partner_progress"),
                "partner_progress_score": data.get("partner_progress_score"),
                "practice_start_rank": data.get("practice_start_rank"),
                "general_flag": data.get("general_flag"),
                "vs_history": data.get("vs_history"),
                # no idea?
                "vs_history_multi": data.get("vs_history"),
                "win_count": win_count,
                "win_count_multi": win_count_multi,
            },
        )

        # save theory course in database
        self.data.item.put_theory_course(
            user_id,
            {
                "course_id": data.get("course_id"),
                "max_victory_grade": data.get("max_victory_grade"),
                # always add 1?
                "run_count": 1,
                "powerhouse_lv": data.get("powerhouse_lv"),
                "powerhouse_exp": data.get("powerhouse_exp"),
                # not sure if the played_powerhouse_lv is the same as powerhouse_lv
                "played_powerhouse_lv": data.get("powerhouse_lv"),
            },
        )

        # save the theory partner in database
        self.data.item.put_theory_partner(
            user_id,
            {
                "partner_id": data.get("partner_id"),
                "fellowship_lv": data.get("fellowship_lv"),
                "fellowship_exp": data.get("fellowship_exp"),
            },
        )

        # save the theory running in database?
        self.data.item.put_theory_running(
            user_id,
            {
                "course_id": data.get("course_id"),
                "attack": data.get("attack"),
                "defense": data.get("defense"),
                "safety": data.get("safety"),
                "runaway": data.get("runaway"),
                "trick_flag": data.get("trick_flag"),
            },
        )

        # get the use_count and theory_use_count of the used car
        style_car_id = data.get("style_car_id")
        car_mileage = data.get("car_mileage")
        used_car = self.data.item.get_car(user_id, self.version, style_car_id)._asdict()

        # increase the use_count and theory_use_count of the used car
        used_car["use_count"] += 1
        used_car["theory_use_count"] += 1
        used_car["car_mileage"] = car_mileage

        # save the used car in database
        self.data.item.put_car(user_id, self.version, used_car)

        # get the profile data, update total_play and daily_play, and save it
        profile = self.data.profile.get_profile(user_id, self.version)
        total_play = profile["total_play"] + 1

        # save the profile in database
        self.data.profile.put_profile(
            user_id,
            self.version,
            {
                "total_play": total_play,
                "last_play_date": datetime.now(),
                "mileage": data.get("mileage"),
                "aura_id": data.get("aura_id"),
                "aura_color_id": data.get("aura_color_id"),
                "aura_line_id": data.get("aura_line_id"),
                "cash": data.get("cash"),
                "total_cash": data.get("total_cash"),
                "dressup_point": data.get("dressup_point"),
                "avatar_point": data.get("avatar_point"),
            },
        )

        return {
            "status_code": "0",
            "played_powerhouse_lv": data.get("powerhouse_lv"),
            "car_use_count": [],
            "maker_use_count": [],
            "play_count": play_count,
            "play_count_multi": play_count_multi,
            "win_count": win_count,
            "win_count_multi": win_count_multi,
        }

    def handle_timetrial_getbestrecordprebattle_request(
        self, data: Dict, headers: Dict
    ):
        user_id = headers["session"]

        course_pickup_car_best_data = []
        courses = self.data.item.get_time_trial_courses(self.version)
        for course in courses:
            car_list = []
            best_cars = self.data.item.get_time_trial_best_cars_by_course(
                self.version, course["course_id"], user_id
            )

            for i, car in enumerate(best_cars):
                car_list.append(
                    {
                        "rank": i + 1,
                        # no clue
                        "member": user_id,
                        "value": car["goal_time"],
                        "store": self.core_cfg.server.name,
                        # use car_id from request?
                        "car_id": 0,
                        "style_car_id": car["style_car_id"],
                        "play_dt": car["play_dt"].timestamp(),
                        "section_time_1": car["section_time_1"],
                        "section_time_2": car["section_time_2"],
                        "section_time_3": car["section_time_3"],
                        "section_time_4": car["section_time_4"],
                        "mission": car["mission"],
                    }
                )

            course_pickup_car_best_data.append(
                {
                    "course_id": course["course_id"],
                    "car_list": car_list,
                }
            )

        return {
            "status_code": "0",
            "course_pickup_car_best_data": course_pickup_car_best_data,
        }

    def handle_user_updateonlinebattle_request(self, data: Dict, headers: Dict):
        return {
            "status_code": "0",
            "bothwin_penalty": 1,
        }

    def handle_user_updateonlinebattleresult_request(self, data: Dict, headers: Dict):
        user_id = headers["session"]

        stock_data: Dict = data.pop("stock_obj")
        # save stock data in database
        self._save_stock_data(user_id, stock_data)

        ticket_data: List = data.pop("ticket_data")
        for ticket in ticket_data:
            self.data.item.put_ticket(user_id, ticket)

        reward_dist_data: Dict = data.pop("reward_dist_obj")
        rank_data: Dict = data.pop("mode_rank_obj")

        # save rank dist data in database
        rank_data.update(reward_dist_data)
        self.data.profile.put_profile_rank(user_id, self.version, rank_data)

        driver_debut_data = data.pop("driver_debut_obj")

        # get the use_count and net_vs_use_count of the used car
        style_car_id = data.get("style_car_id")
        car_mileage = data.pop("car_mileage")
        used_car = self.data.item.get_car(user_id, self.version, style_car_id)._asdict()

        # increase the use_count and net_vs_use_count of the used car
        used_car["use_count"] += 1
        used_car["net_vs_use_count"] += 1
        used_car["car_mileage"] = car_mileage

        # save the used car in database
        self.data.item.put_car(user_id, self.version, used_car)

        # get the profile data, update total_play and daily_play, and save it
        profile = self.data.profile.get_profile(user_id, self.version)
        total_play = profile["total_play"] + 1

        # save the profile in database
        self.data.profile.put_profile(
            user_id,
            self.version,
            {
                "total_play": total_play,
                "last_play_date": datetime.now(),
                "mileage": data.pop("mileage"),
                "aura_id": data.pop("aura_id"),
                "aura_color_id": data.pop("aura_color_id"),
                "aura_line_id": data.pop("aura_line_id"),
                "cash": data.pop("cash"),
                "total_cash": data.pop("total_cash"),
                "dressup_point": data.pop("dressup_point"),
                "avatar_point": data.pop("avatar_point"),
            },
        )

        self.data.item.put_vs_info(user_id, data)

        vs_info = {
            "battle_mode": 0,
            "vs_cnt": 1,
            "vs_win": data.get("win_flg"),
            "invalid": 0,
            "str": 0,
            "str_now": 0,
            "lose_now": 0,
            "vs_history": data.get("vs_history"),
            "course_select_priority": data.get("course_select_priority"),
            "vsinfo_course_data": [
                {
                    "course_id": data.get("course_id"),
                    "vs_cnt": 1,
                    "vs_win": data.get("win_flg"),
                }
            ],
        }

        return {
            "status_code": "0",
            "vsinfo_data": vs_info,
            "round_event": [
                {
                    "count": 1,
                    "win": 1,
                    "rank": 1,
                    "point": 1,
                    "total_round_point": 1,
                }
            ],
            "car_use_count": [],
            "maker_use_count": [],
        }

    def handle_user_updatestorebattleresult_request(self, data: Dict, headers: Dict):
        user_id = headers["session"]

        stock_data: Dict = data.pop("stock_obj")
        ticket_data: List = data.pop("ticket_data")
        reward_dist_data: Dict = data.pop("reward_dist_obj")
        rank_data: Dict = data.pop("mode_rank_obj")
        driver_debut_data: Dict = data.pop("driver_debut_obj")

        # no idea?
        result = data.pop("result")
        battle_gift_event_id = data.pop("battle_gift_event_id")
        gift_id = data.pop("gift_id")

        # save stock data in database
        self._save_stock_data(user_id, stock_data)

        # save tickets in database
        for ticket in ticket_data:
            self.data.item.put_ticket(user_id, ticket)

        # save rank dist data in database
        rank_data.update(reward_dist_data)
        self.data.profile.put_profile_rank(user_id, self.version, rank_data)

        # get the use_count and net_vs_use_count of the used car
        style_car_id = data.get("style_car_id")
        car_mileage = data.pop("car_mileage")
        used_car = self.data.item.get_car(user_id, self.version, style_car_id)._asdict()

        # increase the use_count and net_vs_use_count of the used car
        used_car["use_count"] += 1
        used_car["vs_use_count"] += 1
        used_car["car_mileage"] = car_mileage

        # save the used car in database
        self.data.item.put_car(user_id, self.version, used_car)

        # get the profile data, update total_play and daily_play, and save it
        profile = self.data.profile.get_profile(user_id, self.version)
        total_play = profile["total_play"] + 1

        # save the profile in database
        self.data.profile.put_profile(
            user_id,
            self.version,
            {
                "total_play": total_play,
                "last_play_date": datetime.now(),
                "mileage": data.pop("mileage"),
                "aura_id": data.pop("aura_id"),
                "aura_color_id": data.pop("aura_color_id"),
                "aura_line_id": data.pop("aura_line_id"),
                "cash": data.pop("cash"),
                "total_cash": data.pop("total_cash"),
                "dressup_point": data.pop("dressup_point"),
                "avatar_point": data.pop("avatar_point"),
            },
        )

        # save vs_info in database
        self.data.item.put_vs_info(user_id, data)

        vs_info = {
            "battle_mode": 0,
            "vs_cnt": 1,
            "vs_win": data.get("win_flg"),
            "invalid": 0,
            "str": 0,
            "str_now": 0,
            "lose_now": 0,
            "vs_history": data.get("vs_history"),
            "course_select_priority": 0,
            "vsinfo_course_data": [
                {
                    "course_id": data.get("course_id"),
                    "vs_cnt": 1,
                    "vs_win": data.get("win_flg"),
                }
            ],
        }

        return {
            "status_code": "0",
            "vsinfo_data": vs_info,
            "car_use_count": [],
            "maker_use_count": [],
        }
