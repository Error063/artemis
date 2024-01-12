from .index import ChuniServlet
from .const import ChuniConstants
from .database import ChuniData
from .read import ChuniReader
from .frontend import ChuniFrontend

index = ChuniServlet
database = ChuniData
reader = ChuniReader
frontend = ChuniFrontend
game_codes = [ChuniConstants.GAME_CODE, ChuniConstants.GAME_CODE_NEW, ChuniConstants.GAME_CODE_INT]
