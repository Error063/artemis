from typing import List, Dict

from titles.wacca.handlers.base import BaseRequest, BaseResponse
from titles.wacca.handlers.helpers import GenericItemRecv, SongUpdateDetail, TicketItem
from titles.wacca.handlers.helpers import MusicUpdateDetailV1, MusicUpdateDetailV2
from titles.wacca.handlers.helpers import SeasonalInfoV2, SeasonalInfoV1

# ---user/music/update---
class UserMusicUpdateRequest(BaseRequest):
    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.profileId: int = self.params[0]
        self.songNumber: int = self.params[1]
        self.songDetail = SongUpdateDetail(self.params[2])
        self.itemsObtained: List[GenericItemRecv] = []

        for itm in data["params"][3]:
            self.itemsObtained.append(GenericItemRecv(itm[0], itm[1], itm[2]))

class UserMusicUpdateResponseV1(BaseResponse):
    def __init__(self) -> None:
        super().__init__()
        self.songDetail = MusicUpdateDetailV1()
        self.seasonInfo = SeasonalInfoV1()
        self.rankingInfo: List[List[int]] = []
    
    def make(self) -> Dict:
        self.params = [
            self.songDetail.make(),
            [self.songDetail.songId, self.songDetail.clearCounts.playCt],
            self.seasonInfo.make(),
            self.rankingInfo
        ]

        return super().make()

class UserMusicUpdateResponseV2(UserMusicUpdateResponseV1):
    def __init__(self) -> None:
        super().__init__()
        self.seasonInfo = SeasonalInfoV2()

class UserMusicUpdateResponseV3(UserMusicUpdateResponseV2):
    def __init__(self) -> None:
        super().__init__()
        self.songDetail = MusicUpdateDetailV2()

# ---user/music/updateCoop---
class UserMusicUpdateCoopRequest(UserMusicUpdateRequest):
    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.coopData = self.params[4]

# ---user/music/updateVs---
class UserMusicUpdateVsRequest(UserMusicUpdateRequest):
    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.vsData = self.params[4]

# ---user/music/unlock---
class UserMusicUnlockRequest(BaseRequest):
    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.profileId = self.params[0]
        self.songId = self.params[1]
        self.difficulty = self.params[2]        
        self.itemsUsed: List[GenericItemRecv] = []

        for itm in self.params[3]:
            self.itemsUsed.append(GenericItemRecv(itm[0], itm[1], itm[2]))

class UserMusicUnlockResponse(BaseResponse):
    def __init__(self, current_wp: int = 0, tickets_remaining: List = []) -> None:
        super().__init__()
        self.wp = current_wp        
        self.tickets: List[TicketItem] = []

        for ticket in tickets_remaining:
            self.tickets.append(TicketItem(ticket[0], ticket[1], ticket[2]))
    
    def make(self) -> List:
        tickets = []

        for ticket in self.tickets:
            tickets.append(ticket.make())

        self.params = [
            self.wp,
            tickets
        ]

        return super().make()

