from core.data import Data
from core.config import CoreConfig

from .schema import *

class PokkenData(Data):
    def __init__(self, cfg: CoreConfig) -> None:
        super().__init__(cfg)

        self.profile = PokkenProfileData(cfg, self.session)
        self.match = PokkenMatchData(cfg, self.session)
        self.item = PokkenItemData(cfg, self.session)
        self.static = PokkenStaticData(cfg, self.session)
