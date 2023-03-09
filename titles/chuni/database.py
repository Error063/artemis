from core.data import Data
from core.config import CoreConfig
from titles.chuni.schema import *


class ChuniData(Data):
    def __init__(self, cfg: CoreConfig) -> None:
        super().__init__(cfg)

        self.item = ChuniItemData(cfg, self.session)
        self.profile = ChuniProfileData(cfg, self.session)
        self.score = ChuniScoreData(cfg, self.session)
        self.static = ChuniStaticData(cfg, self.session)
