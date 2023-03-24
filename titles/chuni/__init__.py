from titles.chuni.index import ChuniServlet
from titles.chuni.const import ChuniConstants
from titles.chuni.database import ChuniData
from titles.chuni.read import ChuniReader

index = ChuniServlet
database = ChuniData
reader = ChuniReader
game_codes = [ChuniConstants.GAME_CODE, ChuniConstants.GAME_CODE_NEW]
current_schema_version = 3
