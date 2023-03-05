from titles.ongeki.index import OngekiServlet
from titles.ongeki.const import OngekiConstants
from titles.ongeki.database import OngekiData
from titles.ongeki.read import OngekiReader

index = OngekiServlet
database = OngekiData
reader = OngekiReader

use_default_title = True
include_protocol = True
title_secure = False
game_codes = [OngekiConstants.GAME_CODE]
trailing_slash = True
use_default_host = False
host = ""

current_schema_version = 2
