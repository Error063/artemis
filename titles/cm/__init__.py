from titles.cm.index import CardMakerServlet
from titles.cm.const import CardMakerConstants
from titles.cm.read import CardMakerReader
from titles.cm.database import CardMakerData

index = CardMakerServlet
reader = CardMakerReader
database = CardMakerData

game_codes = [CardMakerConstants.GAME_CODE]

current_schema_version = 1
