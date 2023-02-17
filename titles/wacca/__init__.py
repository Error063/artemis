from titles.wacca.const import WaccaConstants
from titles.wacca.index import WaccaServlet
from titles.wacca.read import WaccaReader
from titles.wacca.database import WaccaData

index = WaccaServlet
database = WaccaData
reader = WaccaReader

use_default_title = True
include_protocol = True
title_secure = False
game_codes = [WaccaConstants.GAME_CODE]
trailing_slash = False
use_default_host = False
host = ""

current_schema_version = 3