from titles.idac.index import IDACServlet
from titles.idac.const import IDACConstants
from titles.idac.database import IDACData
from titles.idac.read import IDACReader
from titles.idac.frontend import IDACFrontend

index = IDACServlet
database = IDACData
reader = IDACReader
frontend = IDACFrontend
game_codes = [IDACConstants.GAME_CODE]
current_schema_version = 1
