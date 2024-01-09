import json
from typing import List
from starlette.routing import Route
from starlette.responses import Response, RedirectResponse
import yaml
import jinja2
from os import path
from starlette.requests import Request

from core.frontend import FE_Base, UserSession
from core.config import CoreConfig
from titles.idac.database import IDACData
from titles.idac.schema.profile import *
from titles.idac.schema.item import *
from titles.idac.config import IDACConfig
from titles.idac.const import IDACConstants


class IDACFrontend(FE_Base):
    def __init__(
        self, cfg: CoreConfig, environment: jinja2.Environment, cfg_dir: str
    ) -> None:
        super().__init__(cfg, environment)
        self.data = IDACData(cfg)
        self.game_cfg = IDACConfig()
        if path.exists(f"{cfg_dir}/{IDACConstants.CONFIG_NAME}"):
            self.game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{IDACConstants.CONFIG_NAME}"))
            )
        #self.nav_name = "頭文字D THE ARCADE"
        self.nav_name = "IDAC"
        # TODO: Add version list
        self.version = IDACConstants.VER_IDAC_SEASON_2

        self.ticket_names = {
            3: "car_dressup_points",
            5: "avatar_points",
            25: "full_tune_tickets",
            34: "full_tune_fragments",
        }
    
    def get_routes(self) -> List[Route]:
        return [
            Route("/", self.render_GET)
        ]

    async def generate_all_tables_json(self, user_id: int):
        json_export = {}

        idac_tables = {
            profile,
            config,
            avatar,
            rank,
            stock,
            theory,
            car,
            ticket,
            story,
            episode,
            difficulty,
            course,
            trial,
            challenge,
            theory_course,
            theory_partner,
            theory_running,
            vs_info,
            stamp,
            timetrial_event
        }

        for table in idac_tables:
            sql = select(table).where(
                table.c.user == user_id,
            )

            # check if the table has a version column
            if "version" in table.c:
                sql = sql.where(table.c.version == self.version)

            # lol use the profile connection for items, dirty hack
            result = await self.data.profile.execute(sql)
            data_list = result.fetchall()

            # add the list to the json export with the correct table name
            json_export[table.name] = []
            for data in data_list:
                tmp = data._asdict()
                tmp.pop("id")
                tmp.pop("user")
                json_export[table.name].append(tmp)

        return json.dumps(json_export, indent=4, default=str, ensure_ascii=False)

    async def render_GET(self, request: Request) -> bytes:
        uri: str = request.url.path

        template = self.environment.get_template(
            "titles/idac/templates/idac_index.jinja"
        )
        usr_sesh = self.validate_session(request)
        if not usr_sesh:
            usr_sesh = UserSession()
        user_id = usr_sesh.user_id
        # user_id = usr_sesh.user_id

        # profile export
        if uri.startswith("/game/idac/export"):
            if user_id == 0:
                return RedirectResponse(b"/game/idac", request)

            # set the file name, content type and size to download the json
            content = await self.generate_all_tables_json(user_id).encode("utf-8")

            self.logger.info(f"User {user_id} exported their IDAC data")
            return Response(
                content, 
                200, 
                {'content-disposition': 'attachment; filename=idac_profile.json'},
                "application/octet-stream"
            )

        profile_data, tickets, rank = None, None, None
        if user_id > 0:
            profile_data = await self.data.profile.get_profile(user_id, self.version)
            ticket_data = await self.data.item.get_tickets(user_id)
            rank = await self.data.profile.get_profile_rank(user_id, self.version)

            tickets = {
                self.ticket_names[ticket["ticket_id"]]: ticket["ticket_cnt"]
                for ticket in ticket_data
            }

        return Response(template.render(
            title=f"{self.core_config.server.name} | {self.nav_name}",
            game_list=self.environment.globals["game_list"],
            profile=profile_data,
            tickets=tickets,
            rank=rank,
            sesh=vars(usr_sesh),
            active_page="idac",
        ))
