from core.data import Data
from core.config import CoreConfig
from titles.mai2.schema import (
    Mai2ItemData,
    Mai2ProfileData,
    Mai2StaticData,
    Mai2ScoreData,
)


class Mai2Data(Data):
    def __init__(self, cfg: CoreConfig) -> None:
        super().__init__(cfg)

        self.profile = Mai2ProfileData(self.config, self.session)
        self.item = Mai2ItemData(self.config, self.session)
        self.static = Mai2StaticData(self.config, self.session)
        self.score = Mai2ScoreData(self.config, self.session)
