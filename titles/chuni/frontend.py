from typing import List
from starlette.routing import Route, Mount
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from os import path
import yaml
import jinja2

from core.frontend import FE_Base, UserSession
from core.config import CoreConfig
from .database import ChuniData
from .config import ChuniConfig
from .const import ChuniConstants


class ChuniFrontend(FE_Base):
    def __init__(
        self, cfg: CoreConfig, environment: jinja2.Environment, cfg_dir: str
    ) -> None:
        super().__init__(cfg, environment)
        self.data = ChuniData(cfg)
        self.game_cfg = ChuniConfig()
        if path.exists(f"{cfg_dir}/{ChuniConstants.CONFIG_NAME}"):
            self.game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{ChuniConstants.CONFIG_NAME}"))
            )
        self.nav_name = "Chunithm"

    def get_routes(self) -> List[Route]:
        return [
            Route("/", self.render_GET, methods=['GET']),
            Route("/rating", self.render_GET_rating, methods=['GET']),
            Mount("/playlog", routes=[
                Route("/", self.render_GET_playlog, methods=['GET']),
                Route("/{index}", self.render_GET_playlog, methods=['GET']),
            ]),
            Route("/update.name", self.update_name, methods=['POST']),
            Route("/version.change", self.version_change, methods=['POST']),
        ]

    async def render_GET(self, request: Request) -> bytes:
        template = self.environment.get_template(
            "titles/chuni/templates/chuni_index.jinja"
        )
        usr_sesh = self.validate_session(request)
        if not usr_sesh:
            usr_sesh = UserSession()

        if usr_sesh.user_id > 0:
            versions = await self.data.profile.get_all_profile_versions(usr_sesh.user_id)
            profile = []
            if versions:
                # chunithm_version is -1 means it is not initialized yet, select a default version from existing.
                if usr_sesh.chunithm_version < 0:
                    usr_sesh.chunithm_version = versions[0]
                profile = await self.data.profile.get_profile_data(usr_sesh.user_id, usr_sesh.chunithm_version)

            resp = Response(template.render(
                title=f"{self.core_config.server.name} | {self.nav_name}",
                game_list=self.environment.globals["game_list"],
                sesh=vars(usr_sesh),
                user_id=usr_sesh.user_id,
                profile=profile,
                version_list=ChuniConstants.VERSION_NAMES,
                versions=versions,
                cur_version=usr_sesh.chunithm_version
            ), media_type="text/html; charset=utf-8")

            if usr_sesh.chunithm_version >= 0:
                encoded_sesh = self.encode_session(usr_sesh)
                resp.set_cookie("DIANA_SESH", encoded_sesh)
            return resp

        else:
            return RedirectResponse("/gate/", 303)

    async def render_GET_rating(self, request: Request) -> bytes:
        template = self.environment.get_template(
            "titles/chuni/templates/chuni_rating.jinja"
        )
        usr_sesh = self.validate_session(request)
        if not usr_sesh:
            usr_sesh = UserSession()

        if usr_sesh.user_id > 0:
            if usr_sesh.chunithm_version < 0:
                return RedirectResponse("/game/chuni/", 303)
            profile = await self.data.profile.get_profile_data(usr_sesh.user_id, usr_sesh.chunithm_version)
            rating = await self.data.profile.get_profile_rating(usr_sesh.user_id, usr_sesh.chunithm_version)
            hot_list=[]
            base_list=[]
            if profile and rating:
                song_records = []
                for song in rating:
                    music_chart = await self.data.static.get_music_chart(usr_sesh.chunithm_version, song.musicId, song.difficultId)
                    if music_chart:
                        if (song.score < 800000):
                            song_rating = 0
                        elif (song.score >= 800000 and song.score < 900000):
                            song_rating = music_chart.level / 2 - 5
                        elif (song.score >= 900000 and song.score < 925000):
                            song_rating = music_chart.level - 5
                        elif (song.score >= 925000 and song.score < 975000):
                            song_rating = music_chart.level - 3
                        elif (song.score >= 975000 and song.score < 1000000):
                            song_rating = (song.score - 975000) / 2500 * 0.1 + music_chart.level
                        elif (song.score >= 1000000 and song.score < 1005000):
                            song_rating = (song.score - 1000000) / 1000 * 0.1 + 1 + music_chart.level
                        elif (song.score >= 1005000 and song.score < 1007500):
                            song_rating = (song.score - 1005000) / 500 * 0.1 + 1.5 + music_chart.level
                        elif (song.score >= 1007500 and song.score < 1009000):
                            song_rating = (song.score - 1007500) / 100 * 0.01 + 2 + music_chart.level
                        elif (song.score >= 1009000):
                            song_rating = 2.15 + music_chart.level
                        song_rating = int(song_rating * 10 ** 2) / 10 ** 2
                        song_records.append({
                            "difficultId": song.difficultId,
                            "musicId": song.musicId,
                            "title": music_chart.title,
                            "level": music_chart.level,
                            "score": song.score,
                            "type": song.type,
                            "song_rating": song_rating,
                        })
                hot_list = [obj for obj in song_records if obj["type"] == "userRatingBaseHotList"]
                base_list = [obj for obj in song_records if obj["type"] == "userRatingBaseList"]
            return Response(template.render(
                title=f"{self.core_config.server.name} | {self.nav_name}",
                game_list=self.environment.globals["game_list"],
                sesh=vars(usr_sesh),
                profile=profile,
                hot_list=hot_list,
                base_list=base_list,
            ), media_type="text/html; charset=utf-8")
        else:
            return RedirectResponse("/gate/", 303)

    async def render_GET_playlog(self, request: Request) -> bytes:
        template = self.environment.get_template(
            "titles/chuni/templates/chuni_playlog.jinja"
        )
        usr_sesh = self.validate_session(request)
        if not usr_sesh:
            usr_sesh = UserSession()

        if usr_sesh.user_id > 0:
            if usr_sesh.chunithm_version < 0:
                return RedirectResponse("/game/chuni/", 303)
            path_index = request.path_params.get('index')
            if not path_index or int(path_index) < 1:
                index = 0
            else:
                index = int(path_index) - 1 # 0 and 1 are 1st page
            user_id = usr_sesh.user_id
            playlog_count = await self.data.score.get_user_playlogs_count(user_id)
            if playlog_count < index * 20 :
                return Response(template.render(
                    title=f"{self.core_config.server.name} | {self.nav_name}",
                    game_list=self.environment.globals["game_list"],
                    sesh=vars(usr_sesh),
                    playlog_count=0
                ), media_type="text/html; charset=utf-8")
            playlog = await self.data.score.get_playlogs_limited(user_id, index, 20)
            playlog_with_title = []
            for record in playlog:
                music_chart = await self.data.static.get_music_chart(usr_sesh.chunithm_version, record.musicId, record.level)
                if music_chart:
                    difficultyNum=music_chart.level
                    artist=music_chart.artist
                    title=music_chart.title
                else:
                    difficultyNum=0
                    artist="unknown"
                    title="musicid: " + str(record.musicId)
                playlog_with_title.append({
                    "raw": record,
                    "title": title,
                    "difficultyNum": difficultyNum,
                    "artist": artist,
                })
            return Response(template.render(
                title=f"{self.core_config.server.name} | {self.nav_name}",
                game_list=self.environment.globals["game_list"],
                sesh=vars(usr_sesh),
                user_id=usr_sesh.user_id,
                playlog=playlog_with_title,
                playlog_count=playlog_count
            ), media_type="text/html; charset=utf-8")
        else:
            return RedirectResponse("/gate/", 303)

    async def update_name(self, request: Request) -> bytes:
        usr_sesh = self.validate_session(request)
        if not usr_sesh:
            return RedirectResponse("/gate/", 303)

        form_data = await request.form()
        new_name: str  = form_data.get("new_name")
        new_name_full = ""

        if not new_name:
            return RedirectResponse("/gate/?e=4", 303)

        if len(new_name) > 8:
            return RedirectResponse("/gate/?e=8", 303)

        for x in new_name: # FIXME: This will let some invalid characters through atm
            o = ord(x)
            try:
                if o == 0x20:
                    new_name_full += chr(0x3000)
                elif o < 0x7F and o > 0x20:
                    new_name_full += chr(o + 0xFEE0)
                elif o <= 0x7F:
                    self.logger.warn(f"Invalid ascii character {o:02X}")
                    return RedirectResponse("/gate/?e=4", 303)
                else:
                    new_name_full += x

            except Exception as e:
                self.logger.error(f"Something went wrong parsing character {o:04X} - {e}")
                return RedirectResponse("/gate/?e=4", 303)

        if not await self.data.profile.update_name(usr_sesh.user_id, new_name_full):
            return RedirectResponse("/gate/?e=999", 303)

        return RedirectResponse("/game/chuni/?s=1", 303)

    async def version_change(self, request: Request):
        usr_sesh = self.validate_session(request)
        if not usr_sesh:
            usr_sesh = UserSession()

        if usr_sesh.user_id > 0:
            form_data = await request.form()
            chunithm_version = form_data.get("version")
            self.logger.info(f"version change to: {chunithm_version}")
            if(chunithm_version.isdigit()):
                usr_sesh.chunithm_version=int(chunithm_version)
                encoded_sesh = self.encode_session(usr_sesh)
                self.logger.info(f"Created session with JWT {encoded_sesh}")
                resp = RedirectResponse("/game/chuni/", 303)
                resp.set_cookie("DIANA_SESH", encoded_sesh)
            return resp
        else:
            return RedirectResponse("/gate/", 303)