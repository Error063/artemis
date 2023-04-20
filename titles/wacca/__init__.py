from titles.wacca.const import WaccaConstants
from titles.wacca.index import WaccaServlet
from titles.wacca.read import WaccaReader
from titles.wacca.database import WaccaData
from titles.wacca.frontend import WaccaFrontend

index = WaccaServlet
database = WaccaData
reader = WaccaReader
frontend = WaccaFrontend
game_codes = [WaccaConstants.GAME_CODE]
current_schema_version = 5
