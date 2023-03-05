from titles.cm.index import CardMakerServlet
from titles.cm.const import CardMakerConstants
from titles.cm.read import CardMakerReader

index = CardMakerServlet
reader = CardMakerReader

use_default_title = True
include_protocol = True
title_secure = False
game_codes = [CardMakerConstants.GAME_CODE]
trailing_slash = True
use_default_host = False
host = ""

current_schema_version = 1