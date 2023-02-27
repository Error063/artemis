from typing import List, Dict

from titles.wacca.handlers.base import BaseResponse, BaseRequest
from titles.wacca.handlers.helpers import Notice

# ---advertise/GetNews---
class GetNewsResponseV1(BaseResponse):
    def __init__(self) -> None:
        super().__init__()
        self.notices: list[Notice] = []
        self.copywrightListings: list[str] = []
        self.stoppedSongs: list[int] = []
        self.stoppedJackets: list[int] = []
        self.stoppedMovies: list[int] = []
        self.stoppedIcons: list[int] = []

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
            self.stoppedIcons 
        ]

        return super().make()

class GetNewsResponseV2(GetNewsResponseV1):    
    stoppedProducts: list[int] = []

    def make(self) -> Dict:
        super().make()
        self.params.append(self.stoppedProducts)
        
        return super(GetNewsResponseV1, self).make()

class GetNewsResponseV3(GetNewsResponseV2):
    stoppedNavs: list[int] = []
    stoppedNavVoices: list[int] = []

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