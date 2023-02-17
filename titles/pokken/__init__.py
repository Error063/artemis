from titles.pokken.index import PokkenServlet
from titles.pokken.const import PokkenConstants

index = PokkenServlet

use_default_title = True
include_protocol = True
title_secure = True
game_codes = [PokkenConstants.GAME_CODE]
trailing_slash = True
use_default_host = False

include_port = True
uri="https://$h:$p/"
host="$h:$p/"

current_schema_version = 1