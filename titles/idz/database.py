from core.data import Data
from core.config import CoreConfig


class IDZData(Data):
    def __init__(self, cfg: CoreConfig) -> None:
        super().__init__(cfg)
