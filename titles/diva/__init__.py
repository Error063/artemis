from titles.diva.index import DivaServlet
from titles.diva.const import DivaConstants
from titles.diva.database import DivaData
from titles.diva.read import DivaReader

index = DivaServlet
database = DivaData
reader = DivaReader
game_codes = [DivaConstants.GAME_CODE]
