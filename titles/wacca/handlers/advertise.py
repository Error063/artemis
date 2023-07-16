from typing import List, Dict

from titles.wacca.handlers.base import BaseResponse, BaseRequest
from titles.wacca.handlers.helpers import Notice


# ---advertise/GetNews---
class GetNewsResponseV1(BaseResponse):
    def __init__(self) -> None:
        super().__init__()
        self.notices: List[Notice] = []
        self.copywrightListings: List[str] = []
        self.stoppedSongs: List[int] = []
        self.stoppedJackets: List[int] = []
        self.stoppedMovies: List[int] = []
        self.stoppedIcons: List[int] = []

    def make(self) -> Dict:
        note = []

        for notice in self.notices:
            note.append(notice.make())

        self.params = [
            note,
            self.copywrightListings,
            self.stoppedSongs,
            self.stoppedJackets,
            self.stoppedMovies,
            self.stoppedIcons,
        ]

        return super().make()


class GetNewsResponseV2(GetNewsResponseV1):
    stoppedProducts: List[int] = []

    def make(self) -> Dict:
        super().make()
        self.params.append(self.stoppedProducts)

        return super(GetNewsResponseV1, self).make()


class GetNewsResponseV3(GetNewsResponseV2):
    stoppedNavs: List[int] = []
    stoppedNavVoices: List[int] = []

    def make(self) -> Dict:
        super().make()
        self.params.append(self.stoppedNavs)
        self.params.append(self.stoppedNavVoices)

        return super(GetNewsResponseV1, self).make()


# ---advertise/GetRanking---
class AdvertiseGetRankingRequest(BaseRequest):
    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.resourceVer: int = self.params[0]


class AdvertiseGetRankingResponse(BaseResponse):
    def __init__(self) -> None:
        super().__init__()

    def make(self) -> Dict:
        return super().make()
