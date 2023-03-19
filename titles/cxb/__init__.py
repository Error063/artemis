from titles.cxb.index import CxbServlet
from titles.cxb.const import CxbConstants
from titles.cxb.database import CxbData
from titles.cxb.read import CxbReader

index = CxbServlet
database = CxbData
reader = CxbReader
game_codes = [CxbConstants.GAME_CODE]
current_schema_version = 1
