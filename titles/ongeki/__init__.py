from titles.ongeki.index import OngekiServlet
from titles.ongeki.const import OngekiConstants
from titles.ongeki.database import OngekiData
from titles.ongeki.read import OngekiReader
from titles.ongeki.frontend import OngekiFrontend

index = OngekiServlet
database = OngekiData
reader = OngekiReader
frontend = OngekiFrontend
game_codes = [OngekiConstants.GAME_CODE]
current_schema_version = 5
