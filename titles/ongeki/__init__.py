from titles.ongeki.index import OngekiServlet
from titles.ongeki.const import OngekiConstants
from titles.ongeki.database import OngekiData
from titles.ongeki.read import OngekiReader

index = OngekiServlet
database = OngekiData
reader = OngekiReader
game_codes = [OngekiConstants.GAME_CODE]
current_schema_version = 5
