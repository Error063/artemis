from .index import SaoServlet
from .const import SaoConstants
from .database import SaoData
from .read import SaoReader

index = SaoServlet
database = SaoData
reader = SaoReader
game_codes = [SaoConstants.GAME_CODE]
