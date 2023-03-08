from titles.cm.index import CardMakerServlet
from titles.cm.const import CardMakerConstants
from titles.cm.read import CardMakerReader

index = CardMakerServlet
reader = CardMakerReader

game_codes = [CardMakerConstants.GAME_CODE]

current_schema_version = 1
