from typing import List, Dict

from titles.wacca.handlers.base import BaseRequest, BaseResponse
from titles.wacca.handlers.helpers import HousingInfo

# ---housing/get----
class HousingGetResponse(BaseResponse):
    def __init__(self, housingId: int) -> None:
        super().__init__()
        self.housingId: int = housingId
        self.regionId: int = 0

    def make(self) -> Dict:
        self.params = [self.housingId, self.regionId]
        return super().make()

# ---housing/start----
class HousingStartRequestV1(BaseRequest):
    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.unknown0: str = self.params[0]
        self.errorLog: str = self.params[1]
        self.info: List[HousingInfo] = []

        for info in self.params[2]:
            self.info.append(HousingInfo(info[0], info[1]))

class HousingStartRequestV2(HousingStartRequestV1):
    def __init__(self, data: Dict) -> None:
        super(HousingStartRequestV1, self).__init__(data)
        self.unknown0: str = self.params[0]
        self.errorLog: str = self.params[1]
        self.creditLog: str = self.params[2]
        self.info: List[HousingInfo] = []

        for info in self.params[3]:
            self.info.append(HousingInfo(info[0], info[1]))

class HousingStartResponseV1(BaseResponse):
    def __init__(self, regionId: int, songList: List[int]) -> None:
        super().__init__()
        self.regionId = regionId
        self.songList = songList

    def make(self) -> Dict:
        self.params = [self.regionId, self.songList]

        return super().make()
