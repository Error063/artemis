from titles.mai2.index import Mai2Servlet
from titles.mai2.const import Mai2Constants
from titles.mai2.database import Mai2Data
from titles.mai2.read import Mai2Reader

index = Mai2Servlet
database = Mai2Data
reader = Mai2Reader
game_codes = [Mai2Constants.GAME_CODE]
current_schema_version = 5
