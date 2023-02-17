from core.data import Data
from core.config import CoreConfig
from titles.diva.schema import DivaProfileData, DivaScoreData, DivaItemData, DivaStaticData

class DivaData(Data):
    def __init__(self, cfg: CoreConfig) -> None:
        super().__init__(cfg)

        self.profile = DivaProfileData(self.config, self.session)
        self.score = DivaScoreData(self.config, self.session)
        self.item = DivaItemData(self.config, self.session)
        self.static = DivaStaticData(self.config, self.session)
