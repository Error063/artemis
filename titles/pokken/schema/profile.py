from typing import Optional, Dict, List, Union
from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_, case
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean, JSON
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func, select, update, delete
from sqlalchemy.engine import Row
from sqlalchemy.dialects.mysql import insert

from core.data.schema import BaseData, metadata
from ..const import PokkenConstants

# Some more of the repeated fields could probably be their own tables, for now I just did the ones that made sense to me
# Having the profile table be this massive kinda blows for updates but w/e, **kwargs to the rescue
profile = Table(
    "pokken_profile",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
        unique=True,
    ),
    Column("trainer_name", String(16)),  # optional
    Column("home_region_code", Integer),
    Column("home_loc_name", String(255)),
    Column("pref_code", Integer),
    Column("navi_newbie_flag", Boolean),
    Column("navi_enable_flag", Boolean),
    Column("pad_vibrate_flag", Boolean),
    Column("trainer_rank_point", Integer),
    Column("wallet", Integer),
    Column("fight_money", Integer),
    Column("score_point", Integer),
    Column("grade_max_num", Integer),
    Column("extra_counter", Integer),  # Optional
    Column("tutorial_progress_flag", JSON),  # Repeated, Integer
    Column("total_play_days", Integer),
    Column("play_date_time", Integer),
    Column("achievement_flag", JSON),  # Repeated, Integer
    Column("lucky_box_fail_num", Integer),
    Column("event_reward_get_flag", Integer),
    Column("rank_pvp_all", Integer),
    Column("rank_pvp_loc", Integer),
    Column("rank_cpu_all", Integer),
    Column("rank_cpu_loc", Integer),
    Column("rank_event", Integer),
    Column("awake_num", Integer),
    Column("use_support_num", Integer),
    Column("rankmatch_flag", Integer),
    Column("rankmatch_max", Integer),  # Optional
    Column("rankmatch_progress", JSON),  # Repeated, Integer
    Column("rankmatch_success", Integer),  # Optional
    Column("beat_num", Integer),  # Optional
    Column("title_text_id", Integer),
    Column("title_plate_id", Integer),
    Column("title_decoration_id", Integer),
    Column("support_pokemon_list", JSON),  # Repeated, Integer
    Column("support_set_1_1", Integer),  # Repeated, Integer
    Column("support_set_1_2", Integer),
    Column("support_set_2_1", Integer),  # Repeated, Integer
    Column("support_set_2_2", Integer),
    Column("support_set_3_1", Integer),  # Repeated, Integer
    Column("support_set_3_2", Integer),
    Column("navi_trainer", Integer),
    Column("navi_version_id", Integer),
    Column("aid_skill_list", JSON),  # Repeated, Integer
    Column("aid_skill", Integer),
    Column("comment_text_id", Integer),
    Column("comment_word_id", Integer),
    Column("latest_use_pokemon", Integer),
    Column("ex_ko_num", Integer),
    Column("wko_num", Integer),
    Column("timeup_win_num", Integer),
    Column("cool_ko_num", Integer),
    Column("perfect_ko_num", Integer),
    Column("record_flag", Integer),
    Column("continue_num", Integer),
    Column("avatar_body", Integer),  # Optional
    Column("avatar_gender", Integer),  # Optional
    Column("avatar_background", Integer),  # Optional
    Column("avatar_head", Integer),  # Optional
    Column("avatar_battleglass", Integer),  # Optional
    Column("avatar_face0", Integer),  # Optional
    Column("avatar_face1", Integer),  # Optional
    Column("avatar_face2", Integer),  # Optional
    Column("avatar_bodyall", Integer),  # Optional
    Column("avatar_wear", Integer),  # Optional
    Column("avatar_accessory", Integer),  # Optional
    Column("avatar_stamp", Integer),  # Optional
    Column("event_state", Integer),
    Column("event_id", Integer),
    Column("sp_bonus_category_id_1", Integer),
    Column("sp_bonus_key_value_1", Integer),
    Column("sp_bonus_category_id_2", Integer),
    Column("sp_bonus_key_value_2", Integer),
    Column("last_play_event_id", Integer),  # Optional
    Column("event_achievement_flag", JSON),  # Repeated, Integer
    Column("event_achievement_param", JSON),  # Repeated, Integer
    Column("battle_num_vs_wan", Integer),  # 4?
    Column("win_vs_wan", Integer),
    Column("battle_num_vs_lan", Integer),  # 3?
    Column("win_vs_lan", Integer),
    Column("battle_num_vs_cpu", Integer),  # 2
    Column("win_cpu", Integer),
    Column("battle_num_tutorial", Integer),  # 1?
    mysql_charset="utf8mb4",
)

pokemon_data = Table(
    "pokken_pokemon_data",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("char_id", Integer, nullable=False),
    Column("illustration_book_no", Integer),
    Column("pokemon_exp", Integer),
    Column("battle_num_vs_wan", Integer),  # 4?
    Column("win_vs_wan", Integer),
    Column("battle_num_vs_lan", Integer),  # 3?
    Column("win_vs_lan", Integer),
    Column("battle_num_vs_cpu", Integer),  # 2
    Column("win_cpu", Integer),
    Column("battle_all_num_tutorial", Integer), # ???
    Column("battle_num_tutorial", Integer),  # 1?
    Column("bp_point_atk", Integer),
    Column("bp_point_res", Integer),
    Column("bp_point_def", Integer),
    Column("bp_point_sp", Integer),
    UniqueConstraint("user", "char_id", name="pokken_pokemon_data_uk"),
    mysql_charset="utf8mb4",
)


class PokkenProfileData(BaseData):
    def touch_profile(self, user_id: int) -> Optional[int]:
        sql = select([profile.c.id]).where(profile.c.user == user_id)
        
        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()['id']

    def create_profile(self, user_id: int) -> Optional[int]:
        sql = insert(profile).values(user=user_id)
        conflict = sql.on_duplicate_key_update(user=user_id)

        result = self.execute(conflict)
        if result is None:
            self.logger.error(f"Failed to create pokken profile for user {user_id}!")
            return None
        return result.lastrowid

    def set_profile_name(self, user_id: int, new_name: str, gender: Union[int, None] = None) -> None:
        sql = update(profile).where(profile.c.user == user_id).values(
            trainer_name=new_name,
            avatar_gender=gender if gender is not None else profile.c.avatar_gender
        )
        result = self.execute(sql)
        if result is None:
            self.logger.error(
                f"Failed to update pokken profile name for user {user_id}!"
            )

    def put_extra(
        self, 
        user_id: int, 
        extra_counter: int,
        evt_reward_get_flg: int,
        total_play_days: int,
        awake_num: int,
        use_support_ct: int,
        beat_num: int,
        aid_skill: int,
        last_evt: int
    ) -> None:
        sql = update(profile).where(profile.c.user == user_id).values(
            extra_counter=extra_counter,
            event_reward_get_flag=evt_reward_get_flg,
            total_play_days=total_play_days,
            awake_num=awake_num,
            use_support_num=use_support_ct,
            beat_num=beat_num,
            aid_skill=aid_skill,
            last_play_event_id=last_evt
        )

        result = self.execute(sql)
        if result is None:
            self.logger.error(f"Failed to put extra data for user {user_id}")

    def update_profile_tutorial_flags(self, user_id: int, tutorial_flags: List) -> None:
        sql = update(profile).where(profile.c.user == user_id).values(
            tutorial_progress_flag=tutorial_flags,
        )
        result = self.execute(sql)
        if result is None:
            self.logger.error(
                f"Failed to update pokken profile tutorial flags for user {user_id}!"
            )

    def update_profile_achievement_flags(self, user_id: int, achievement_flags: List) -> None:
        sql = update(profile).where(profile.c.user == user_id).values(
            achievement_flag=achievement_flags,
        )
        result = self.execute(sql)
        if result is None:
            self.logger.error(
                f"Failed to update pokken profile achievement flags for user {user_id}!"
            )

    def update_profile_event(self, user_id: int, event_state: List, event_flags: List[int], event_param: List[int], last_evt: int = None) -> None:
        sql = update(profile).where(profile.c.user == user_id).values(
            event_state=event_state,
            event_achievement_flag=event_flags,
            event_achievement_param=event_param,
            last_play_event_id=last_evt if last_evt is not None else profile.c.last_play_event_id,
        )
        result = self.execute(sql)
        if result is None:
            self.logger.error(
                f"Failed to update pokken profile event state for user {user_id}!"
            )

    def add_profile_points(
        self, user_id: int, rank_pts: int, money: int, score_pts: int, grade_max: int
    ) -> None:
        sql = update(profile).where(profile.c.user == user_id).values(
            trainer_rank_point = profile.c.trainer_rank_point + rank_pts,
            fight_money = profile.c.fight_money + money,
            score_point = profile.c.score_point + score_pts,
            grade_max_num = grade_max
        )

    def get_profile(self, user_id: int) -> Optional[Row]:
        sql = profile.select(profile.c.user == user_id)
        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def put_pokemon(
        self,
        user_id: int,
        pokemon_id: int,
        illust_no: int,
        atk: int,
        res: int,
        defe: int,
        sp: int
    ) -> Optional[int]:
        sql = insert(pokemon_data).values(
            user=user_id,
            char_id=pokemon_id,
            illustration_book_no=illust_no,
            pokemon_exp=0,
            battle_num_vs_wan=0,
            win_vs_wan=0,
            battle_num_vs_lan=0,
            win_vs_lan=0,
            battle_num_vs_cpu=0,
            win_cpu=0,
            battle_all_num_tutorial=0,
            battle_num_tutorial=0,
            bp_point_atk=1+atk,
            bp_point_res=1+res,
            bp_point_def=1+defe,
            bp_point_sp=1+sp,
        )

        conflict = sql.on_duplicate_key_update(
            illustration_book_no=illust_no,
            bp_point_atk=pokemon_data.c.bp_point_atk + atk,
            bp_point_res=pokemon_data.c.bp_point_res + res,
            bp_point_def=pokemon_data.c.bp_point_def + defe,
            bp_point_sp=pokemon_data.c.bp_point_sp + sp,
        )

        result = self.execute(conflict)
        if result is None:
            self.logger.warning(f"Failed to insert pokemon ID {pokemon_id} for user {user_id}")
            return None
        return result.lastrowid

    def add_pokemon_xp(
        self,
        user_id: int,
        pokemon_id: int,
        xp: int
    ) -> None:
        sql = update(pokemon_data).where(and_(pokemon_data.c.user==user_id, pokemon_data.c.char_id==pokemon_id)).values(
            pokemon_exp=pokemon_data.c.pokemon_exp + xp
        )

        result = self.execute(sql)
        if result is None:
            self.logger.warning(f"Failed to add {xp} XP to pokemon ID {pokemon_id} for user {user_id}")

    def get_pokemon_data(self, user_id: int, pokemon_id: int) -> Optional[Row]:
        pass

    def get_all_pokemon_data(self, user_id: int) -> Optional[List[Row]]:
        sql = pokemon_data.select(pokemon_data.c.user == user_id)
        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def put_pokemon_battle_result(
        self, user_id: int, pokemon_id: int, match_type: PokkenConstants.BATTLE_TYPE, match_result: PokkenConstants.BATTLE_RESULT
    ) -> None:
        """
        Records the match stats (type and win/loss) for the pokemon and profile
        """
        sql = update(pokemon_data).where(and_(pokemon_data.c.user==user_id, pokemon_data.c.char_id==pokemon_id)).values(
            battle_num_tutorial=pokemon_data.c.battle_num_tutorial + 1 if match_type==PokkenConstants.BATTLE_TYPE.TUTORIAL else pokemon_data.c.battle_num_tutorial,
            battle_all_num_tutorial=pokemon_data.c.battle_all_num_tutorial + 1 if match_type==PokkenConstants.BATTLE_TYPE.TUTORIAL else pokemon_data.c.battle_all_num_tutorial,

            battle_num_vs_cpu=pokemon_data.c.battle_num_vs_cpu + 1 if match_type==PokkenConstants.BATTLE_TYPE.AI else pokemon_data.c.battle_num_vs_cpu,
            win_cpu=pokemon_data.c.win_cpu + 1 if match_type==PokkenConstants.BATTLE_TYPE.AI and match_result==PokkenConstants.BATTLE_RESULT.WIN else pokemon_data.c.win_cpu,

            battle_num_vs_lan=pokemon_data.c.battle_num_vs_lan + 1 if match_type==PokkenConstants.BATTLE_TYPE.LAN else pokemon_data.c.battle_num_vs_lan,
            win_vs_lan=pokemon_data.c.win_vs_lan + 1 if match_type==PokkenConstants.BATTLE_TYPE.LAN and match_result==PokkenConstants.BATTLE_RESULT.WIN else pokemon_data.c.win_vs_lan,

            battle_num_vs_wan=pokemon_data.c.battle_num_vs_wan + 1 if match_type==PokkenConstants.BATTLE_TYPE.WAN else pokemon_data.c.battle_num_vs_wan,
            win_vs_wan=pokemon_data.c.win_vs_wan + 1 if match_type==PokkenConstants.BATTLE_TYPE.WAN and match_result==PokkenConstants.BATTLE_RESULT.WIN else pokemon_data.c.win_vs_wan,
        )

        result = self.execute(sql)
        if result is None:
            self.logger.warning(f"Failed to record match stats for user {user_id}'s pokemon {pokemon_id} (type {match_type.name} | result {match_result.name})")

    def put_stats(
        self,
        user_id: int,
        exkos: int,
        wkos: int,
        timeout_wins: int,
        cool_kos: int,
        perfects: int,
        continues: int,
    ) -> None:
        """
        Records profile stats
        """
        sql = update(profile).where(profile.c.user==user_id).values(
            ex_ko_num=profile.c.ex_ko_num + exkos,
            wko_num=profile.c.wko_num + wkos,
            timeup_win_num=profile.c.timeup_win_num + timeout_wins,
            cool_ko_num=profile.c.cool_ko_num + cool_kos,
            perfect_ko_num=profile.c.perfect_ko_num + perfects,
            continue_num=continues,
        )

        result = self.execute(sql)
        if result is None:
            self.logger.warning(f"Failed to update stats for user {user_id}")

    def update_support_team(self, user_id: int, support_id: int, support1: int = None, support2: int = None) -> None:
        if support1 == 4294967295:
            support1 = None
        if support2 == 4294967295:
            support2 = None
        sql = update(profile).where(profile.c.user==user_id).values(
            support_set_1_1=support1 if support_id == 1 else profile.c.support_set_1_1,
            support_set_1_2=support2 if support_id == 1 else profile.c.support_set_1_2,
            support_set_2_1=support1 if support_id == 2 else profile.c.support_set_2_1,
            support_set_2_2=support2 if support_id == 2 else profile.c.support_set_2_2,
            support_set_3_1=support1 if support_id == 3 else profile.c.support_set_3_1,
            support_set_3_2=support2 if support_id == 3 else profile.c.support_set_3_2,
        )

        result = self.execute(sql)
        if result is None:
            self.logger.warning(f"Failed to update support team {support_id} for user {user_id}")
