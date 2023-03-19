from core.data import Data
from core.config import CoreConfig
from titles.wacca.schema import *


class WaccaData(Data):
    def __init__(self, cfg: CoreConfig) -> None:
        super().__init__(cfg)

        self.profile = WaccaProfileData(self.config, self.session)
        self.score = WaccaScoreData(self.config, self.session)
        self.item = WaccaItemData(self.config, self.session)
        self.static = WaccaStaticData(self.config, self.session)
