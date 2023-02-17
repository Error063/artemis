from titles.cxb.index import CxbServlet
from titles.cxb.const import CxbConstants
from titles.cxb.database import CxbData
from titles.cxb.read import CxbReader

index = CxbServlet
database = CxbData
reader = CxbReader

use_default_title = False
include_protocol = True
title_secure = True
game_codes = [CxbConstants.GAME_CODE]
trailing_slash = True
use_default_host = False

include_port = True
uri = "http://$h:$p/" # If you care about the allnet response you're probably running with no SSL
host = ""

current_schema_version = 1