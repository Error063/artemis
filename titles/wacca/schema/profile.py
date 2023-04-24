from typing import Optional, Dict, List
from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean, JSON
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func, select
from sqlalchemy.engine import Row
from sqlalchemy.dialects.mysql import insert

from core.data.schema import BaseData, metadata
from ..handlers.helpers import PlayType

profile = Table(
    "wacca_profile",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("version", Integer),
    Column("username", String(8), nullable=False),
    Column("xp", Integer, server_default="0"),
    Column("wp", Integer, server_default="0"),
    Column("wp_total", Integer, server_default="0"),
    Column("wp_spent", Integer, server_default="0"),
    Column("dan_type", Integer, server_default="0"),
    Column("dan_level", Integer, server_default="0"),
    Column("title_0", Integer, server_default="0"),
    Column("title_1", Integer, server_default="0"),
    Column("title_2", Integer, server_default="0"),
    Column("rating", Integer, server_default="0"),
    Column("vip_expire_time", TIMESTAMP),
    Column("always_vip", Boolean, server_default="0"),
    Column("login_count", Integer, server_default="0"),
    Column("login_count_consec", Integer, server_default="0"),
    Column("login_count_days", Integer, server_default="0"),
    Column("login_count_days_consec", Integer, server_default="0"),
    Column("login_count_today", Integer, server_default="0"),
    Column("playcount_single", Integer, server_default="0"),
    Column("playcount_multi_vs", Integer, server_default="0"),
    Column("playcount_multi_coop", Integer, server_default="0"),
    Column("playcount_stageup", Integer, server_default="0"),
    Column("playcount_time_free", Integer, server_default="0"),
    Column("friend_view_1", Integer),
    Column("friend_view_2", Integer),
    Column("friend_view_3", Integer),
    Column("last_game_ver", String(50)),
    Column("last_song_id", Integer, server_default="0"),
    Column("last_song_difficulty", Integer, server_default="0"),
    Column("last_folder_order", Integer, server_default="0"),
    Column("last_folder_id", Integer, server_default="0"),
    Column("last_song_order", Integer, server_default="0"),
    Column("last_login_date", TIMESTAMP, server_default=func.now()),
    Column("gate_tutorial_flags", JSON),
    UniqueConstraint("user", "version", name="wacca_profile_uk"),
    mysql_charset="utf8mb4",
)

option = Table(
    "wacca_option",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("opt_id", Integer, nullable=False),
    Column("value", Integer, nullable=False),
    UniqueConstraint("user", "opt_id", name="wacca_option_uk"),
)

bingo = Table(
    "wacca_bingo",
    metadata,
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        primary_key=True,
        nullable=False,
    ),
    Column("page_number", Integer, nullable=False),
    Column("page_progress", JSON, nullable=False),
    UniqueConstraint("user", "page_number", name="wacca_bingo_uk"),
    mysql_charset="utf8mb4",
)

friend = Table(
    "wacca_friend",
    metadata,
    Column(
        "profile_sender",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column(
        "profile_reciever",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("is_accepted", Boolean, server_default="0"),
    PrimaryKeyConstraint("profile_sender", "profile_reciever", name="arcade_owner_pk"),
    mysql_charset="utf8mb4",
)

favorite = Table(
    "wacca_favorite_song",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("song_id", Integer, nullable=False),
    UniqueConstraint("user", "song_id", name="wacca_favorite_song_uk"),
    mysql_charset="utf8mb4",
)

gate = Table(
    "wacca_gate",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("gate_id", Integer, nullable=False),
    Column("page", Integer, nullable=False, server_default="0"),
    Column("progress", Integer, nullable=False, server_default="0"),
    Column("loops", Integer, nullable=False, server_default="0"),
    Column("last_used", TIMESTAMP, nullable=False, server_default=func.now()),
    Column("mission_flag", Integer, nullable=False, server_default="0"),
    Column("total_points", Integer, nullable=False, server_default="0"),
    UniqueConstraint("user", "gate_id", name="wacca_gate_uk"),
)


class WaccaProfileData(BaseData):
    def create_profile(
        self, aime_id: int, username: str, version: int
    ) -> Optional[int]:
        """
        Given a game version, aime id, and username, create a profile and return it's ID
        """
        sql = insert(profile).values(user=aime_id, username=username, version=version)

        conflict = sql.on_duplicate_key_update(username=sql.inserted.username)

        result = self.execute(conflict)
        if result is None:
            self.logger.error(
                f"{__name__} Failed to insert wacca profile! aime id: {aime_id} username: {username}"
            )
            return None
        return result.lastrowid

    def update_profile_playtype(
        self, profile_id: int, play_type: int, game_version: str
    ) -> None:
        sql = profile.update(profile.c.id == profile_id).values(
            playcount_single=profile.c.playcount_single + 1
            if play_type == PlayType.PlayTypeSingle.value
            else profile.c.playcount_single,
            playcount_multi_vs=profile.c.playcount_multi_vs + 1
            if play_type == PlayType.PlayTypeVs.value
            else profile.c.playcount_multi_vs,
            playcount_multi_coop=profile.c.playcount_multi_coop + 1
            if play_type == PlayType.PlayTypeCoop.value
            else profile.c.playcount_multi_coop,
            playcount_stageup=profile.c.playcount_stageup + 1
            if play_type == PlayType.PlayTypeStageup.value
            else profile.c.playcount_stageup,
            playcount_time_free=profile.c.playcount_time_free + 1
            if play_type == PlayType.PlayTypeTimeFree.value
            else profile.c.playcount_time_free,
            last_game_ver=game_version,
        )

        result = self.execute(sql)
        if result is None:
            self.logger.error(
                f"update_profile: failed to update profile! profile: {profile_id}"
            )
        return None

    def update_profile_lastplayed(
        self,
        profile_id: int,
        last_song_id: int,
        last_song_difficulty: int,
        last_folder_order: int,
        last_folder_id: int,
        last_song_order: int,
    ) -> None:
        sql = profile.update(profile.c.id == profile_id).values(
            last_song_id=last_song_id,
            last_song_difficulty=last_song_difficulty,
            last_folder_order=last_folder_order,
            last_folder_id=last_folder_id,
            last_song_order=last_song_order,
        )
        result = self.execute(sql)
        if result is None:
            self.logger.error(
                f"update_profile_lastplayed: failed to update profile! profile: {profile_id}"
            )
        return None

    def update_profile_dan(
        self, profile_id: int, dan_level: int, dan_type: int
    ) -> Optional[int]:
        sql = profile.update(profile.c.id == profile_id).values(
            dan_level=dan_level, dan_type=dan_type
        )

        result = self.execute(sql)
        if result is None:
            self.logger.warn(
                f"update_profile_dan: Failed to update! profile {profile_id}"
            )
            return None
        return result.lastrowid

    def get_profile(self, profile_id: int = 0, aime_id: int = None) -> Optional[Row]:
        """
        Given a game version and either a profile or aime id, return the profile
        """
        if aime_id is not None:
            sql = profile.select(profile.c.user == aime_id)
        elif profile_id > 0:
            sql = profile.select(profile.c.id == profile_id)
        else:
            self.logger.error(
                f"get_profile: Bad arguments!! profile_id {profile_id} aime_id {aime_id}"
            )
            return None

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_options(self, user_id: int, option_id: int = None) -> Optional[List[Row]]:
        """
        Get a specific user option for a profile, or all of them if none specified
        """
        sql = option.select(
            and_(
                option.c.user == user_id,
                option.c.opt_id == option_id if option_id is not None else True,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        if option_id is not None:
            return result.fetchone()
        else:
            return result.fetchall()

    def update_option(self, user_id: int, option_id: int, value: int) -> Optional[int]:
        sql = insert(option).values(user=user_id, opt_id=option_id, value=value)

        conflict = sql.on_duplicate_key_update(value=value)

        result = self.execute(conflict)
        if result is None:
            self.logger.error(
                f"{__name__} failed to insert option! profile: {user_id}, option: {option_id}, value: {value}"
            )
            return None

        return result.lastrowid

    def add_favorite_song(self, user_id: int, song_id: int) -> Optional[int]:
        sql = favorite.insert().values(user=user_id, song_id=song_id)

        result = self.execute(sql)
        if result is None:
            self.logger.error(
                f"{__name__} failed to insert favorite! profile: {user_id}, song_id: {song_id}"
            )
            return None
        return result.lastrowid

    def remove_favorite_song(self, user_id: int, song_id: int) -> None:
        sql = favorite.delete(
            and_(favorite.c.user == user_id, favorite.c.song_id == song_id)
        )

        result = self.execute(sql)
        if result is None:
            self.logger.error(
                f"{__name__} failed to remove favorite! profile: {user_id}, song_id: {song_id}"
            )
        return None

    def get_favorite_songs(self, user_id: int) -> Optional[List[Row]]:
        sql = favorite.select(favorite.c.user == user_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_gates(self, user_id: int) -> Optional[List[Row]]:
        sql = select(gate).where(gate.c.user == user_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def update_gate(
        self,
        user_id: int,
        gate_id: int,
        page: int,
        progress: int,
        loop: int,
        mission_flag: int,
        total_points: int,
    ) -> Optional[int]:
        sql = insert(gate).values(
            user=user_id,
            gate_id=gate_id,
            page=page,
            progress=progress,
            loops=loop,
            mission_flag=mission_flag,
            total_points=total_points,
        )

        conflict = sql.on_duplicate_key_update(
            page=sql.inserted.page,
            progress=sql.inserted.progress,
            loops=sql.inserted.loops,
            mission_flag=sql.inserted.mission_flag,
            total_points=sql.inserted.total_points,
        )

        result = self.execute(conflict)
        if result is None:
            self.logger.error(
                f"{__name__} failed to update gate! user: {user_id}, gate_id: {gate_id}"
            )
            return None
        return result.lastrowid

    def get_friends(self, user_id: int) -> Optional[List[Row]]:
        sql = friend.select(friend.c.profile_sender == user_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def profile_to_aime_user(self, profile_id: int) -> Optional[int]:
        sql = select(profile.c.user).where(profile.c.id == profile_id)

        result = self.execute(sql)
        if result is None:
            self.logger.info(
                f"profile_to_aime_user: No user found for profile {profile_id}"
            )
            return None

        this_profile = result.fetchone()
        if this_profile is None:
            self.logger.info(
                f"profile_to_aime_user: No user found for profile {profile_id}"
            )
            return None

        return this_profile["user"]

    def session_login(
        self, profile_id: int, is_new_day: bool, is_consec_day: bool
    ) -> None:
        # TODO: Reset consec days counter
        sql = profile.update(profile.c.id == profile_id).values(
            login_count=profile.c.login_count + 1,
            login_count_consec=profile.c.login_count_consec + 1,
            login_count_days=profile.c.login_count_days + 1
            if is_new_day
            else profile.c.login_count_days,
            login_count_days_consec=profile.c.login_count_days_consec + 1
            if is_new_day and is_consec_day
            else profile.c.login_count_days_consec,
            login_count_today=1 if is_new_day else profile.c.login_count_today + 1,
            last_login_date=func.now(),
        )

        result = self.execute(sql)
        if result is None:
            self.logger.error(
                f"session_login: failed to update profile! profile: {profile_id}"
            )
        return None

    def session_logout(self, profile_id: int) -> None:
        sql = profile.update(profile.c.id == id).values(login_count_consec=0)

        result = self.execute(sql)
        if result is None:
            self.logger.error(
                f"{__name__} failed to update profile! profile: {profile_id}"
            )
        return None

    def add_xp(self, profile_id: int, xp: int) -> None:
        sql = profile.update(profile.c.id == profile_id).values(xp=profile.c.xp + xp)

        result = self.execute(sql)
        if result is None:
            self.logger.error(
                f"add_xp: Failed to update profile! profile_id {profile_id} xp {xp}"
            )
        return None

    def add_wp(self, profile_id: int, wp: int) -> None:
        sql = profile.update(profile.c.id == profile_id).values(
            wp=profile.c.wp + wp,
            wp_total=profile.c.wp_total + wp,
        )

        result = self.execute(sql)
        if result is None:
            self.logger.error(
                f"add_wp: Failed to update profile! profile_id {profile_id} wp {wp}"
            )
        return None

    def spend_wp(self, profile_id: int, wp: int) -> None:
        sql = profile.update(profile.c.id == profile_id).values(
            wp=profile.c.wp - wp,
            wp_spent=profile.c.wp_spent + wp,
        )

        result = self.execute(sql)
        if result is None:
            self.logger.error(
                f"spend_wp: Failed to update profile! profile_id {profile_id} wp {wp}"
            )
        return None

    def activate_vip(self, profile_id: int, expire_time) -> None:
        sql = profile.update(profile.c.id == profile_id).values(
            vip_expire_time=expire_time
        )

        result = self.execute(sql)
        if result is None:
            self.logger.error(
                f"activate_vip: Failed to update profile! profile_id {profile_id} expire_time {expire_time}"
            )
        return None

    def update_user_rating(self, profile_id: int, new_rating: int) -> None:
        sql = profile.update(profile.c.id == profile_id).values(rating=new_rating)

        result = self.execute(sql)
        if result is None:
            self.logger.error(
                f"update_user_rating: Failed to update profile! profile_id {profile_id} new_rating {new_rating}"
            )
        return None

    def update_bingo(self, aime_id: int, page: int, progress: int) -> Optional[int]:
        sql = insert(bingo).values(
            user=aime_id, page_number=page, page_progress=progress
        )

        conflict = sql.on_duplicate_key_update(page_number=page, page_progress=progress)

        result = self.execute(conflict)
        if result is None:
            self.logger.error(f"put_bingo: failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    def get_bingo(self, aime_id: int) -> Optional[List[Row]]:
        sql = select(bingo).where(bingo.c.user == aime_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_bingo_page(self, aime_id: int, page: Dict) -> Optional[List[Row]]:
        sql = select(bingo).where(
            and_(bingo.c.user == aime_id, bingo.c.page_number == page)
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def update_vip_time(self, profile_id: int, time_left) -> None:
        sql = profile.update(profile.c.id == profile_id).values(
            vip_expire_time=time_left
        )

        result = self.execute(sql)
        if result is None:
            self.logger.error(f"Failed to update VIP time for profile {profile_id}")

    def update_tutorial_flags(self, profile_id: int, flags: Dict) -> None:
        sql = profile.update(profile.c.id == profile_id).values(
            gate_tutorial_flags=flags
        )

        result = self.execute(sql)
        if result is None:
            self.logger.error(
                f"Failed to update tutorial flags for profile {profile_id}"
            )
