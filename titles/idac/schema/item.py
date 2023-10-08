from typing import Dict, Optional, List
from sqlalchemy import (
    Table,
    Column,
    UniqueConstraint,
    PrimaryKeyConstraint,
    and_,
    update,
)
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean, JSON
from sqlalchemy.schema import ForeignKey
from sqlalchemy.engine import Row
from sqlalchemy.sql import func, select
from sqlalchemy.dialects.mysql import insert

from core.data.schema import BaseData, metadata

car = Table(
    "idac_user_car",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("version", Integer, nullable=False),
    Column("car_id", Integer),
    Column("style_car_id", Integer),
    Column("color", Integer),
    Column("bureau", Integer),
    Column("kana", Integer),
    Column("s_no", Integer),
    Column("l_no", Integer),
    Column("car_flag", Integer),
    Column("tune_point", Integer),
    Column("tune_level", Integer, server_default="1"),
    Column("tune_parts", Integer),
    Column("infinity_tune", Integer, server_default="0"),
    Column("online_vs_win", Integer, server_default="0"),
    Column(
        "pickup_seq", Integer, server_default="1"
    ),  # the order in which the car was picked up
    Column(
        "purchase_seq", Integer, server_default="1"
    ),  # the order in which the car was purchased
    Column("color_stock_list", String(32)),
    Column("color_stock_new_list", String(32)),
    Column("parts_stock_list", String(48)),
    Column("parts_stock_new_list", String(48)),
    Column("parts_set_equip_list", String(48)),
    Column("parts_list", JSON),
    Column("equip_parts_count", Integer, server_default="0"),
    Column("total_car_parts_count", Integer, server_default="0"),
    Column("use_count", Integer, server_default="0"),
    Column("story_use_count", Integer, server_default="0"),
    Column("timetrial_use_count", Integer, server_default="0"),
    Column("vs_use_count", Integer, server_default="0"),
    Column("net_vs_use_count", Integer, server_default="0"),
    Column("theory_use_count", Integer, server_default="0"),
    Column("car_mileage", Integer, server_default="0"),
    UniqueConstraint("user", "version", "style_car_id", name="idac_user_car_uk"),
    mysql_charset="utf8mb4",
)

ticket = Table(
    "idac_user_ticket",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("ticket_id", Integer),
    Column("ticket_cnt", Integer),
    UniqueConstraint("user", "ticket_id", name="idac_user_ticket_uk"),
    mysql_charset="utf8mb4",
)

story = Table(
    "idac_user_story",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("story_type", Integer),
    Column("chapter", Integer),
    Column("loop_count", Integer, server_default="1"),
    UniqueConstraint("user", "chapter", name="idac_user_story_uk"),
    mysql_charset="utf8mb4",
)

episode = Table(
    "idac_user_story_episode",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("chapter", Integer),
    Column("episode", Integer),
    Column("play_status", Integer),
    UniqueConstraint("user", "chapter", "episode", name="idac_user_story_episode_uk"),
    mysql_charset="utf8mb4",
)

difficulty = Table(
    "idac_user_story_episode_difficulty",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("episode", Integer),
    Column("difficulty", Integer),
    Column("play_count", Integer),
    Column("clear_count", Integer),
    Column("play_status", Integer),
    Column("play_score", Integer),
    UniqueConstraint(
        "user", "episode", "difficulty", name="idac_user_story_episode_difficulty_uk"
    ),
    mysql_charset="utf8mb4",
)

course = Table(
    "idac_user_course",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("course_id", Integer),
    Column("run_counts", Integer, server_default="1"),
    Column("skill_level_exp", Integer, server_default="0"),
    UniqueConstraint("user", "course_id", name="idac_user_course_uk"),
    mysql_charset="utf8mb4",
)

trial = Table(
    "idac_user_time_trial",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("version", Integer, nullable=False),
    Column("style_car_id", Integer),
    Column("course_id", Integer),
    Column("eval_id", Integer, server_default="0"),
    Column("goal_time", Integer),
    Column("section_time_1", Integer),
    Column("section_time_2", Integer),
    Column("section_time_3", Integer),
    Column("section_time_4", Integer),
    Column("mission", Integer),
    Column("play_dt", TIMESTAMP, server_default=func.now()),
    UniqueConstraint(
        "user", "version", "course_id", "style_car_id", name="idac_user_time_trial_uk"
    ),
    mysql_charset="utf8mb4",
)

challenge = Table(
    "idac_user_challenge",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("vs_type", Integer),
    Column("play_difficulty", Integer),
    Column("cleared_difficulty", Integer),
    Column("story_type", Integer),
    Column("play_count", Integer, server_default="1"),
    Column("weak_difficulty", Integer, server_default="0"),
    Column("eval_id", Integer),
    Column("advantage", Integer),
    Column("sec1_advantage_avg", Integer),
    Column("sec2_advantage_avg", Integer),
    Column("sec3_advantage_avg", Integer),
    Column("sec4_advantage_avg", Integer),
    Column("nearby_advantage_rate", Integer),
    Column("win_flag", Integer),
    Column("result", Integer),
    Column("record", Integer),
    Column("course_id", Integer),
    Column("last_play_course_id", Integer),
    Column("style_car_id", Integer),
    Column("course_day", Integer),
    UniqueConstraint(
        "user", "vs_type", "play_difficulty", name="idac_user_challenge_uk"
    ),
    mysql_charset="utf8mb4",
)

theory_course = Table(
    "idac_user_theory_course",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("course_id", Integer),
    Column("max_victory_grade", Integer, server_default="0"),
    Column("run_count", Integer, server_default="1"),
    Column("powerhouse_lv", Integer),
    Column("powerhouse_exp", Integer),
    Column("played_powerhouse_lv", Integer),
    Column("update_dt", TIMESTAMP, server_default=func.now()),
    UniqueConstraint("user", "course_id", name="idac_user_theory_course_uk"),
    mysql_charset="utf8mb4",
)

theory_partner = Table(
    "idac_user_theory_partner",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("partner_id", Integer),
    Column("fellowship_lv", Integer),
    Column("fellowship_exp", Integer),
    UniqueConstraint("user", "partner_id", name="idac_user_theory_partner_uk"),
    mysql_charset="utf8mb4",
)

theory_running = Table(
    "idac_user_theory_running",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("course_id", Integer),
    Column("attack", Integer),
    Column("defense", Integer),
    Column("safety", Integer),
    Column("runaway", Integer),
    Column("trick_flag", Integer),
    UniqueConstraint("user", "course_id", name="idac_user_theory_running_uk"),
    mysql_charset="utf8mb4",
)

vs_info = Table(
    "idac_user_vs_info",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("group_key", String(25)),
    Column("win_flg", Integer),
    Column("style_car_id", Integer),
    Column("course_id", Integer),
    Column("course_day", Integer),
    Column("players_num", Integer),
    Column("winning", Integer),
    Column("advantage_1", Integer),
    Column("advantage_2", Integer),
    Column("advantage_3", Integer),
    Column("advantage_4", Integer),
    Column("select_course_id", Integer),
    Column("select_course_day", Integer),
    Column("select_course_random", Integer),
    Column("matching_success_sec", Integer),
    Column("boost_flag", Integer),
    Column("vs_history", Integer),
    Column("break_count", Integer),
    Column("break_penalty_flag", Integer),
    UniqueConstraint("user", "group_key", name="idac_user_vs_info_uk"),
    mysql_charset="utf8mb4",
)

stamp = Table(
    "idac_user_stamp",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("m_stamp_event_id", Integer),
    Column("select_flag", Integer),
    Column("stamp_masu", Integer),
    Column("daily_bonus", Integer),
    Column("weekly_bonus", Integer),
    Column("weekday_bonus", Integer),
    Column("weekend_bonus", Integer),
    Column("total_bonus", Integer),
    Column("day_total_bonus", Integer),
    Column("store_battle_bonus", Integer),
    Column("story_bonus", Integer),
    Column("online_battle_bonus", Integer),
    Column("timetrial_bonus", Integer),
    Column("fasteststreetlegaltheory_bonus", Integer),
    Column("collaboration_bonus", Integer),
    Column("add_bonus_daily_flag_1", Integer),
    Column("add_bonus_daily_flag_2", Integer),
    Column("add_bonus_daily_flag_3", Integer),
    Column("create_date_daily", TIMESTAMP, server_default=func.now()),
    Column("create_date_weekly", TIMESTAMP, server_default=func.now()),
    UniqueConstraint("user", "m_stamp_event_id", name="idac_user_stamp_uk"),
    mysql_charset="utf8mb4",
)

timetrial_event = Table(
    "idac_user_timetrial_event",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("timetrial_event_id", Integer),
    Column("point", Integer),
    UniqueConstraint("user", "timetrial_event_id", name="idac_user_timetrial_event_uk"),
    mysql_charset="utf8mb4",
)


class IDACItemData(BaseData):
    def get_random_user_car(self, aime_id: int, version: int) -> Optional[List[Row]]:
        sql = (
            select(car)
            .where(and_(car.c.user == aime_id, car.c.version == version))
            .order_by(func.rand())
            .limit(1)
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_random_car(self, version: int) -> Optional[List[Row]]:
        sql = select(car).where(car.c.version == version).order_by(func.rand()).limit(1)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_car(
        self, aime_id: int, version: int, style_car_id: int
    ) -> Optional[List[Row]]:
        sql = select(car).where(
            and_(
                car.c.user == aime_id,
                car.c.version == version,
                car.c.style_car_id == style_car_id,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_cars(
        self, version: int, aime_id: int, only_pickup: bool = False
    ) -> Optional[List[Row]]:
        if only_pickup:
            sql = select(car).where(
                and_(
                    car.c.user == aime_id,
                    car.c.version == version,
                    car.c.pickup_seq != 0,
                )
            )
        else:
            sql = select(car).where(
                and_(car.c.user == aime_id, car.c.version == version)
            )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_ticket(self, aime_id: int, ticket_id: int) -> Optional[Row]:
        sql = select(ticket).where(
            ticket.c.user == aime_id, ticket.c.ticket_id == ticket_id
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_tickets(self, aime_id: int) -> Optional[List[Row]]:
        sql = select(ticket).where(ticket.c.user == aime_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_story(self, aime_id: int, chapter_id: int) -> Optional[Row]:
        sql = select(story).where(
            and_(story.c.user == aime_id, story.c.chapter == chapter_id)
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_stories(self, aime_id: int) -> Optional[List[Row]]:
        sql = select(story).where(story.c.user == aime_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_story_episodes(self, aime_id: int, chapter_id: int) -> Optional[List[Row]]:
        sql = select(episode).where(
            and_(episode.c.user == aime_id, episode.c.chapter == chapter_id)
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_story_episode(self, aime_id: int, episode_id: int) -> Optional[Row]:
        sql = select(episode).where(
            and_(episode.c.user == aime_id, episode.c.episode == episode_id)
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_story_episode_difficulties(
        self, aime_id: int, episode_id: int
    ) -> Optional[List[Row]]:
        sql = select(difficulty).where(
            and_(difficulty.c.user == aime_id, difficulty.c.episode == episode_id)
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_courses(self, aime_id: int) -> Optional[List[Row]]:
        sql = select(course).where(course.c.user == aime_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_course(self, aime_id: int, course_id: int) -> Optional[Row]:
        sql = select(course).where(
            and_(course.c.user == aime_id, course.c.course_id == course_id)
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_time_trial_courses(self, version: int) -> Optional[List[Row]]:
        sql = select(trial.c.course_id).where(trial.c.version == version).distinct()

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_time_trial_user_best_time_by_course_car(
        self, version: int, aime_id: int, course_id: int, style_car_id: int
    ) -> Optional[Row]:
        sql = select(trial).where(
            and_(
                trial.c.user == aime_id,
                trial.c.version == version,
                trial.c.course_id == course_id,
                trial.c.style_car_id == style_car_id,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_time_trial_user_best_courses(
        self, version: int, aime_id: int
    ) -> Optional[List[Row]]:
        # get for a given aime_id the best time for each course
        subquery = (
            select(
                trial.c.version,
                func.min(trial.c.goal_time).label("min_goal_time"),
                trial.c.course_id,
            )
            .where(and_(trial.c.version == version, trial.c.user == aime_id))
            .group_by(trial.c.course_id)
            .subquery()
        )

        # now get the full row for each best time
        sql = select(trial).where(
            and_(
                trial.c.version == subquery.c.version,
                trial.c.goal_time == subquery.c.min_goal_time,
                trial.c.course_id == subquery.c.course_id,
                trial.c.user == aime_id,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_time_trial_best_cars_by_course(
        self, version: int, aime_id: int, course_id: int
    ) -> Optional[List[Row]]:
        subquery = (
            select(
                trial.c.version,
                func.min(trial.c.goal_time).label("min_goal_time"),
                trial.c.style_car_id,
            )
            .where(
                and_(
                    trial.c.version == version,
                    trial.c.user == aime_id,
                    trial.c.course_id == course_id,
                )
            )
            .group_by(trial.c.style_car_id)
            .subquery()
        )

        sql = select(trial).where(
            and_(
                trial.c.version == subquery.c.version,
                trial.c.goal_time == subquery.c.min_goal_time,
                trial.c.style_car_id == subquery.c.style_car_id,
                trial.c.course_id == course_id,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_time_trial_ranking_by_course(
        self,
        version: int,
        course_id: int,
        style_car_id: Optional[int] = None,
        limit: Optional[int] = 10,
    ) -> Optional[List[Row]]:
        # get the top 10 ranking by goal_time for a given course which is grouped by user
        subquery = select(
            trial.c.version,
            trial.c.user,
            func.min(trial.c.goal_time).label("min_goal_time"),
        ).where(and_(trial.c.version == version, trial.c.course_id == course_id))

        # if wantd filter only by style_car_id
        if style_car_id is not None:
            subquery = subquery.where(trial.c.style_car_id == style_car_id)

        subquery = subquery.group_by(trial.c.user).subquery()

        sql = (
            select(trial)
            .where(
                and_(
                    trial.c.version == subquery.c.version,
                    trial.c.user == subquery.c.user,
                    trial.c.goal_time == subquery.c.min_goal_time,
                ),
            )
            .order_by(trial.c.goal_time)
        )

        # limit the result if needed
        if limit is not None:
            sql = sql.limit(limit)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_time_trial_best_ranking_by_course(
        self, version: int, aime_id: int, course_id: int
    ) -> Optional[Row]:
        sql = (
            select(trial)
            .where(
                and_(
                    trial.c.version == version,
                    trial.c.user == aime_id,
                    trial.c.course_id == course_id,
                ),
            )
            .order_by(trial.c.goal_time)
            .limit(1)
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_challenge(
        self, aime_id: int, vs_type: int, play_difficulty: int
    ) -> Optional[Row]:
        sql = select(challenge).where(
            and_(
                challenge.c.user == aime_id,
                challenge.c.vs_type == vs_type,
                challenge.c.play_difficulty == play_difficulty,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_challenges(self, aime_id: int) -> Optional[List[Row]]:
        sql = select(challenge).where(challenge.c.user == aime_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_best_challenges_by_vs_type(
        self, aime_id: int, story_type: int = 4
    ) -> Optional[List[Row]]:
        subquery = (
            select(
                challenge.c.story_type,
                challenge.c.user,
                challenge.c.vs_type,
                func.max(challenge.c.play_difficulty).label("last_play_lv"),
            )
            .where(
                and_(challenge.c.user == aime_id, challenge.c.story_type == story_type)
            )
            .group_by(challenge.c.vs_type)
        )

        sql = (
            select(
                challenge.c.story_type,
                challenge.c.vs_type,
                challenge.c.cleared_difficulty.label("max_clear_lv"),
                challenge.c.play_difficulty.label("last_play_lv"),
                challenge.c.course_id,
                challenge.c.play_count,
            )
            .where(
                and_(
                    challenge.c.user == subquery.c.user,
                    challenge.c.vs_type == subquery.c.vs_type,
                    challenge.c.play_difficulty == subquery.c.last_play_lv,
                ),
            )
            .order_by(challenge.c.vs_type)
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_theory_courses(self, aime_id: int) -> Optional[List[Row]]:
        sql = select(theory_course).where(theory_course.c.user == aime_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_theory_course_by_powerhouse_lv(
        self, aime_id: int, course_id: int, powerhouse_lv: int, count: int = 3
    ) -> Optional[List[Row]]:
        sql = (
            select(theory_course)
            .where(
                and_(
                    theory_course.c.user != aime_id,
                    theory_course.c.course_id == course_id,
                    theory_course.c.powerhouse_lv == powerhouse_lv,
                )
            )
            .order_by(func.rand())
            .limit(count)
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_theory_course(self, aime_id: int, course_id: int) -> Optional[List[Row]]:
        sql = select(theory_course).where(
            and_(
                theory_course.c.user == aime_id, theory_course.c.course_id == course_id
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_theory_partners(self, aime_id: int) -> Optional[List[Row]]:
        sql = select(theory_partner).where(theory_partner.c.user == aime_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_theory_running(self, aime_id: int) -> Optional[List[Row]]:
        sql = select(theory_running).where(theory_running.c.user == aime_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_theory_running_by_course(
        self, aime_id: int, course_id: int
    ) -> Optional[Row]:
        sql = select(theory_running).where(
            and_(
                theory_running.c.user == aime_id,
                theory_running.c.course_id == course_id,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_vs_infos(self, aime_id: int) -> Optional[List[Row]]:
        sql = select(vs_info).where(vs_info.c.user == aime_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_stamps(self, aime_id: int) -> Optional[List[Row]]:
        sql = select(stamp).where(
            and_(
                stamp.c.user == aime_id,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_timetrial_event(self, aime_id: int, timetrial_event_id: int) -> Optional[Row]:
        sql = select(timetrial_event).where(
            and_(
                timetrial_event.c.user == aime_id,
                timetrial_event.c.timetrial_event_id == timetrial_event_id,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def put_car(self, aime_id: int, version: int, car_data: Dict) -> Optional[int]:
        car_data["user"] = aime_id
        car_data["version"] = version

        sql = insert(car).values(**car_data)
        conflict = sql.on_duplicate_key_update(**car_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_car: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    def put_ticket(self, aime_id: int, ticket_data: Dict) -> Optional[int]:
        ticket_data["user"] = aime_id

        sql = insert(ticket).values(**ticket_data)
        conflict = sql.on_duplicate_key_update(**ticket_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_ticket: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    def put_story(self, aime_id: int, story_data: Dict) -> Optional[int]:
        story_data["user"] = aime_id

        sql = insert(story).values(**story_data)
        conflict = sql.on_duplicate_key_update(**story_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_story: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    def put_story_episode_play_status(
        self, aime_id: int, chapter_id: int, play_status: int = 1
    ) -> Optional[int]:
        sql = (
            update(episode)
            .where(and_(episode.c.user == aime_id, episode.c.chapter == chapter_id))
            .values(play_status=play_status)
        )

        result = self.execute(sql)
        if result is None:
            self.logger.warn(
                f"put_story_episode_play_status: Failed to update! aime_id: {aime_id}"
            )
            return None
        return result.lastrowid

    def put_story_episode(
        self, aime_id: int, chapter_id: int, episode_data: Dict
    ) -> Optional[int]:
        episode_data["user"] = aime_id
        episode_data["chapter"] = chapter_id

        sql = insert(episode).values(**episode_data)
        conflict = sql.on_duplicate_key_update(**episode_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_story_episode: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    def put_story_episode_difficulty(
        self, aime_id: int, episode_id: int, difficulty_data: Dict
    ) -> Optional[int]:
        difficulty_data["user"] = aime_id
        difficulty_data["episode"] = episode_id

        sql = insert(difficulty).values(**difficulty_data)
        conflict = sql.on_duplicate_key_update(**difficulty_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(
                f"put_story_episode_difficulty: Failed to update! aime_id: {aime_id}"
            )
            return None
        return result.lastrowid

    def put_course(self, aime_id: int, course_data: Dict) -> Optional[int]:
        course_data["user"] = aime_id

        sql = insert(course).values(**course_data)
        conflict = sql.on_duplicate_key_update(**course_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_course: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    def put_time_trial(
        self, version: int, aime_id: int, time_trial_data: Dict
    ) -> Optional[int]:
        time_trial_data["user"] = aime_id
        time_trial_data["version"] = version

        sql = insert(trial).values(**time_trial_data)
        conflict = sql.on_duplicate_key_update(**time_trial_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_time_trial: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    def put_challenge(self, aime_id: int, challenge_data: Dict) -> Optional[int]:
        challenge_data["user"] = aime_id

        sql = insert(challenge).values(**challenge_data)
        conflict = sql.on_duplicate_key_update(**challenge_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_challenge: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    def put_theory_course(
        self, aime_id: int, theory_course_data: Dict
    ) -> Optional[int]:
        theory_course_data["user"] = aime_id

        sql = insert(theory_course).values(**theory_course_data)
        conflict = sql.on_duplicate_key_update(**theory_course_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_theory_course: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    def put_theory_partner(
        self, aime_id: int, theory_partner_data: Dict
    ) -> Optional[int]:
        theory_partner_data["user"] = aime_id

        sql = insert(theory_partner).values(**theory_partner_data)
        conflict = sql.on_duplicate_key_update(**theory_partner_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(
                f"put_theory_partner: Failed to update! aime_id: {aime_id}"
            )
            return None
        return result.lastrowid

    def put_theory_running(
        self, aime_id: int, theory_running_data: Dict
    ) -> Optional[int]:
        theory_running_data["user"] = aime_id

        sql = insert(theory_running).values(**theory_running_data)
        conflict = sql.on_duplicate_key_update(**theory_running_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(
                f"put_theory_running: Failed to update! aime_id: {aime_id}"
            )
            return None
        return result.lastrowid

    def put_vs_info(self, aime_id: int, vs_info_data: Dict) -> Optional[int]:
        vs_info_data["user"] = aime_id

        sql = insert(vs_info).values(**vs_info_data)
        conflict = sql.on_duplicate_key_update(**vs_info_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_vs_info: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    def put_stamp(
        self, aime_id: int, stamp_data: Dict
    ) -> Optional[int]:
        stamp_data["user"] = aime_id

        sql = insert(stamp).values(**stamp_data)
        conflict = sql.on_duplicate_key_update(**stamp_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(
                f"putstamp: Failed to update! aime_id: {aime_id}"
            )
            return None
        return result.lastrowid

    def put_timetrial_event(
        self, aime_id: int, time_trial_event_id: int, point: int
    ) -> Optional[int]:
        timetrial_event_data = {
            "user": aime_id,
            "timetrial_event_id": time_trial_event_id,
            "point": point,
        }

        sql = insert(timetrial_event).values(**timetrial_event_data)
        conflict = sql.on_duplicate_key_update(**timetrial_event_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(
                f"put_timetrial_event: Failed to update! aime_id: {aime_id}"
            )
            return None
        return result.lastrowid
