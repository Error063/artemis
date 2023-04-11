from .index import PokkenServlet
from .const import PokkenConstants
from .database import PokkenData
from .frontend import PokkenFrontend

index = PokkenServlet
database = PokkenData
game_codes = [PokkenConstants.GAME_CODE]
current_schema_version = 1
frontend = PokkenFrontend
