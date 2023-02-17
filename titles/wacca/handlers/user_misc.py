from typing import List, Dict

from titles.wacca.handlers.base import BaseRequest, BaseResponse
from titles.wacca.handlers.helpers import PurchaseType, GenericItemRecv
from titles.wacca.handlers.helpers import TicketItem, SongRatingUpdate, BingoDetail
from titles.wacca.handlers.helpers import BingoPageStatus, GateTutorialFlag

# ---user/goods/purchase---
class UserGoodsPurchaseRequest(BaseRequest):
    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.profileId = int(self.params[0])
        self.purchaseId = int(self.params[1])
        self.purchaseCount = int(self.params[2])
        self.purchaseType = PurchaseType(self.params[3])
        self.cost = int(self.params[4])
        self.itemObtained: GenericItemRecv = GenericItemRecv(self.params[5][0], self.params[5][1], self.params[5][2])

class UserGoodsPurchaseResponse(BaseResponse):
    def __init__(self, wp: int = 0, tickets: List = []) -> None:
        super().__init__()
        self.currentWp = wp
        self.tickets: List[TicketItem] = []
        
        for ticket in tickets:
            self.tickets.append(TicketItem(ticket[0], ticket[1], ticket[2]))

    def make(self) -> List:
        tix = []
        for ticket in self.tickets:
            tix.append(ticket.make())

        self.params = [self.currentWp, tix]

        return super().make()

# ---user/sugaroku/update---
class UserSugarokuUpdateRequestV1(BaseRequest):
    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.profileId = int(self.params[0])
        self.gateId = int(self.params[1])
        self.page = int(self.params[2])
        self.progress = int(self.params[3])
        self.loops = int(self.params[4])
        self.boostsUsed = self.params[5]
        self.totalPts = int(self.params[7])        
        self.itemsObtainted: List[GenericItemRecv] = []

        for item in self.params[6]:
            self.itemsObtainted.append(GenericItemRecv(item[0], item[1], item[2]))

class UserSugarokuUpdateRequestV2(UserSugarokuUpdateRequestV1):
    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.mission_flag = int(self.params[8])

# ---user/rating/update---
class UserRatingUpdateRequest(BaseRequest):
    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.profileId = self.params[0]
        self.totalRating = self.params[1]
        self.songs: List[SongRatingUpdate] = []

        for x in self.params[2]:
            self.songs.append(SongRatingUpdate(x[0], x[1], x[2]))

# ---user/mission/update---
class UserMissionUpdateRequest(BaseRequest):    
    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.profileId = self.params[0]
        self.bingoDetail = BingoDetail(self.params[1][0])
        self.itemsObtained: List[GenericItemRecv] = []
        self.gateTutorialFlags: List[GateTutorialFlag] = []

        for x in self.params[1][1]:
            self.bingoDetail.pageStatus.append(BingoPageStatus(x[0], x[1], x[2]))

        for x in self.params[2]:
            self.itemsObtained.append(GenericItemRecv(x[0], x[1], x[2]))

        for x in self.params[3]:
            self.gateTutorialFlags.append(GateTutorialFlag(x[0], x[1]))
