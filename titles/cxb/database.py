from core.data import Data
from core.config import CoreConfig
from titles.cxb.schema import CxbProfileData, CxbScoreData, CxbItemData, CxbStaticData


class CxbData(Data):
    def __init__(self, cfg: CoreConfig) -> None:
        super().__init__(cfg)

        self.profile = CxbProfileData(self.config, self.session)
        self.score = CxbScoreData(self.config, self.session)
        self.item = CxbItemData(self.config, self.session)
        self.static = CxbStaticData(self.config, self.session)
