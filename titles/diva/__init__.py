from titles.diva.index import DivaServlet
from titles.diva.const import DivaConstants
from titles.diva.database import DivaData
from titles.diva.read import DivaReader

index = DivaServlet
database = DivaData
reader = DivaReader

use_default_title = True
include_protocol = True
title_secure = False
game_codes = [DivaConstants.GAME_CODE]
trailing_slash = True
use_default_host = False
host = ""

current_schema_version = 1