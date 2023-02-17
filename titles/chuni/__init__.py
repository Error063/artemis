from titles.chuni.index import ChuniServlet
from titles.chuni.const import ChuniConstants
from titles.chuni.database import ChuniData
from titles.chuni.read import ChuniReader

index = ChuniServlet
database = ChuniData
reader = ChuniReader

use_default_title = True
include_protocol = True
title_secure = False
game_codes = [ChuniConstants.GAME_CODE, ChuniConstants.GAME_CODE_NEW]
trailing_slash = True
use_default_host = False
host = ""

current_schema_version = 1
