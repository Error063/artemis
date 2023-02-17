from typing import List, Dict

from titles.wacca.handlers.base import BaseResponse
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
    stoppedNavs: list[int] = []
    stoppedNavVoices: list[int] = []

    def make(self) -> Dict:
        super().make()
        self.params.append(self.stoppedProducts)
        self.params.append(self.stoppedNavs)
        self.params.append(self.stoppedNavVoices)
        
        return super(GetNewsResponseV1, self).make()
