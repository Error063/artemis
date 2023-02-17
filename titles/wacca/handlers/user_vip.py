from typing import Dict, List
from titles.wacca.handlers.base import BaseRequest, BaseResponse
from titles.wacca.handlers.helpers import VipLoginBonus

# --user/vip/get--
class UserVipGetRequest(BaseRequest):
    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.profileId = self.params[0]

class UserVipGetResponse(BaseResponse):
    def __init__(self) -> None:
        super().__init__()
        self.vipDays: int = 0
        self.unknown1: int = 1
        self.unknown2: int = 1
        self.presents: List[VipLoginBonus] = []
    
    def make(self) -> Dict:
        pres = []
        for x in self.presents:
            pres.append(x.make())

        self.params = [
            self.vipDays,
            [
                self.unknown1,
                self.unknown2,
                pres
            ]
        ]
        return super().make()

# --user/vip/start--
class UserVipStartRequest(BaseRequest):
    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.profileId = self.params[0]
        self.cost = self.params[1]
        self.days = self.params[2]

class UserVipStartResponse(BaseResponse):
    def __init__(self, expires: int = 0) -> None:
        super().__init__()
        self.whenExpires: int = expires
        self.presents = []

    def make(self) -> Dict:
        self.params = [
            self.whenExpires,
            self.presents
        ]

        return super().make()