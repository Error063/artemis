from titles.pokken.index import PokkenServlet
from titles.pokken.const import PokkenConstants
from titles.pokken.database import PokkenData

index = PokkenServlet
database = PokkenData
game_codes = [PokkenConstants.GAME_CODE]
current_schema_version = 1