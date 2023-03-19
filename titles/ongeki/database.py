from core.data import Data
from core.config import CoreConfig
from titles.ongeki.schema import OngekiItemData, OngekiProfileData, OngekiScoreData
from titles.ongeki.schema import OngekiStaticData, OngekiLogData


class OngekiData(Data):
    def __init__(self, cfg: CoreConfig) -> None:
        super().__init__(cfg)

        self.item = OngekiItemData(cfg, self.session)
        self.profile = OngekiProfileData(cfg, self.session)
        self.score = OngekiScoreData(cfg, self.session)
        self.static = OngekiStaticData(cfg, self.session)
        self.log = OngekiLogData(cfg, self.session)
