from core.data import Data
from core.config import CoreConfig

from .schema import *


class SaoData(Data):
    def __init__(self, cfg: CoreConfig) -> None:
        super().__init__(cfg)

        self.item = SaoItemData(cfg, self.session)
        self.profile = SaoProfileData(cfg, self.session)
        self.static = SaoStaticData(cfg, self.session)