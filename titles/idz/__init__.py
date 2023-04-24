from titles.idz.index import IDZServlet
from titles.idz.const import IDZConstants
from titles.idz.database import IDZData

index = IDZServlet
database = IDZData
game_codes = [IDZConstants.GAME_CODE]
current_schema_version = 1
