from typing import List, Dict, Optional

from titles.wacca.handlers.base import BaseRequest, BaseResponse
from titles.wacca.handlers.helpers import *

# ---user/status/get----
class UserStatusGetRequest(BaseRequest):
    aimeId: int = 0

    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.aimeId = int(data["params"][0])

class UserStatusGetV1Response(BaseResponse):
    def __init__(self) -> None:
        super().__init__()
        self.userStatus: UserStatusV1 = UserStatusV1()
        self.setTitleId: int = 0
        self.setIconId: int = 0
        self.profileStatus: ProfileStatus = ProfileStatus.ProfileGood
        self.versionStatus: PlayVersionStatus = PlayVersionStatus.VersionGood
        self.lastGameVersion: str = ""

    def make(self) -> Dict:
        self.params = [
            self.userStatus.make(),
            self.setTitleId,
            self.setIconId,
            self.profileStatus.value,
            [
                self.versionStatus.value,
                self.lastGameVersion
            ]
        ]
        
        return super().make()

class UserStatusGetV2Response(UserStatusGetV1Response):
    def __init__(self) -> None:
        super().__init__()
        self.userStatus: UserStatusV2 = UserStatusV2()
        self.unknownArr: List = []

    def make(self) -> Dict:
        super().make()

        self.params.append(self.unknownArr)

        return super(UserStatusGetV1Response, self).make()

# ---user/status/getDetail----
class UserStatusGetDetailRequest(BaseRequest):
    userId: int = 0

    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.userId = data["params"][0]

class UserStatusGetDetailResponseV1(BaseResponse):
    def __init__(self) -> None:
        super().__init__()
        self.userStatus: UserStatusV1 = UserStatusV1()
        self.options: List[UserOption] = []
        self.seasonalPlayModeCounts: List[PlayModeCounts] = []
        self.userItems: UserItemInfoV1 = UserItemInfoV1()
        self.scores: List[BestScoreDetailV1] = []
        self.songPlayStatus: List[int] = [0,0]
        self.seasonInfo: SeasonalInfoV1 = SeasonalInfoV1()
        self.playAreaList: List = [ [0],[0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0],[0,0,0,0],[0,0,0,0,0,0,0],[0] ]
        self.songUpdateTime: int = 0

    def make(self)-> Dict:
        opts = []
        play_modes = []
        scores = []

        for x in self.seasonalPlayModeCounts:
            play_modes.append(x.make())
        
        for x in self.scores:
            scores.append(x.make())
        
        for x in self.options:
            opts.append(x.make())

        self.params = [
            self.userStatus.make(),
            opts,
            play_modes,
            self.userItems.make(),
            scores,
            self.songPlayStatus,
            self.seasonInfo.make(),
            self.playAreaList,
            self.songUpdateTime
        ]

        return super().make()
    
    def find_score_idx(self, song_id: int, difficulty: int = 1, start_idx: int = 0, stop_idx: Optional[int] = None) -> Optional[int]:
        if stop_idx is None or stop_idx > len(self.scores):
            stop_idx = len(self.scores)

        for x in range(start_idx, stop_idx):
            if self.scores[x].songId == song_id and self.scores[x].difficulty == difficulty:
                return x
        
        return None

class UserStatusGetDetailResponseV2(UserStatusGetDetailResponseV1):
    def __init__(self) -> None:
        super().__init__()
        self.userStatus: UserStatusV2 = UserStatusV2()
        self.seasonInfo: SeasonalInfoV2 = SeasonalInfoV2()
        self.userItems: UserItemInfoV2 = UserItemInfoV2()
        self.favorites: List[int] = []
        self.stoppedSongIds: List[int] = []
        self.eventInfo: List[int] = []
        self.gateInfo: List[GateDetailV1] = []
        self.lastSongInfo: LastSongDetail = LastSongDetail()
        self.gateTutorialFlags: List[GateTutorialFlag] = []
        self.gatchaInfo: List[GachaInfo] = []
        self.friendList: List[FriendDetail] = []

    def make(self)-> Dict:
        super().make()
        gates = []
        friends = []
        tut_flg = []

        for x in self.gateInfo:
            gates.append(x.make())
        
        for x in self.friendList:
            friends.append(x.make())
        
        for x in self.gateTutorialFlags:
            tut_flg.append(x.make())
        
        while len(tut_flg) < 5:
            flag_id = len(tut_flg) + 1
            tut_flg.append([flag_id, 0])

        self.params.append(self.favorites)
        self.params.append(self.stoppedSongIds)
        self.params.append(self.eventInfo)
        self.params.append(gates)
        self.params.append(self.lastSongInfo.make())
        self.params.append(tut_flg)
        self.params.append(self.gatchaInfo)
        self.params.append(friends)

        return super(UserStatusGetDetailResponseV1, self).make()

class UserStatusGetDetailResponseV3(UserStatusGetDetailResponseV2):
    def __init__(self) -> None:
        super().__init__()
        self.gateInfo: List[GateDetailV2] = []

class UserStatusGetDetailResponseV4(UserStatusGetDetailResponseV3):
    def __init__(self) -> None:
        super().__init__()
        self.userItems: UserItemInfoV3 = UserItemInfoV3()
        self.bingoStatus: BingoDetail = BingoDetail(0)
        self.scores: List[BestScoreDetailV2] = []

    def make(self)-> Dict:
        super().make()
        self.params.append(self.bingoStatus.make())

        return super(UserStatusGetDetailResponseV1, self).make()

# ---user/status/login----
class UserStatusLoginRequest(BaseRequest):
    userId: int = 0

    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.userId = data["params"][0]

class UserStatusLoginResponseV1(BaseResponse):
    def __init__(self, is_first_login_daily: bool = False, last_login_date: int = 0) -> None:
        super().__init__()
        self.dailyBonus: List[LoginBonusInfo] = []
        self.consecBonus: List[LoginBonusInfo] = []
        self.otherBonus: List[LoginBonusInfo] = []  
        self.firstLoginDaily = is_first_login_daily
        self.lastLoginDate = last_login_date

    def make(self)-> Dict:
        super().make()
        daily = []
        consec = []
        other = []

        for bonus in self.dailyBonus:
            daily.append(bonus.make())

        for bonus in self.consecBonus:
            consec.append(bonus.make())

        for bonus in self.otherBonus:
            other.append(bonus.make())

        self.params = [ daily, consec, other, int(self.firstLoginDaily)]
        return super().make()

class UserStatusLoginResponseV2(UserStatusLoginResponseV1):
    def __init__(self, is_first_login_daily: bool = False, last_login_date: int = 0) -> None:
        super().__init__(is_first_login_daily)
        self.lastLoginDate = last_login_date

        self.vipInfo = VipInfo()
    
    def make(self)-> Dict:
        super().make()
        self.params.append(self.vipInfo.make())
        self.params.append(self.lastLoginDate)
        return super(UserStatusLoginResponseV1, self).make()

class UserStatusLoginResponseV3(UserStatusLoginResponseV2):
    def __init__(self, is_first_login_daily: bool = False, last_login_date: int = 0) -> None:
        super().__init__(is_first_login_daily, last_login_date)
        self.unk: List = []

    def make(self)-> Dict:
        super().make()
        self.params.append(self.unk)
        return super(UserStatusLoginResponseV1, self).make()

# ---user/status/create---
class UserStatusCreateRequest(BaseRequest):
    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.aimeId = data["params"][0]
        self.username = data["params"][1]

class UserStatusCreateResponseV1(BaseResponse):
    def __init__(self, userId: int, username: str) -> None:
        super().__init__()
        self.userStatus = UserStatusV1()
        self.userStatus.userId = userId
        self.userStatus.username = username
    
    def make(self)-> Dict:
        self.params = [
            self.userStatus.make()
        ]
        return super().make()

class UserStatusCreateResponseV2(UserStatusCreateResponseV1):
    def __init__(self, userId: int, username: str) -> None:
        super().__init__(userId, username)
        self.userStatus: UserStatusV2 = UserStatusV2()        
        self.userStatus.userId = userId
        self.userStatus.username = username

# ---user/status/logout---
class UserStatusLogoutRequest(BaseRequest):
    userId: int

    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.userId = data["params"][0]

# ---user/status/update---
class UserStatusUpdateRequestV1(BaseRequest):
    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.profileId: int = data["params"][0]
        self.playType: PlayType = PlayType(data["params"][1])
        self.itemsRecieved: List[GenericItemRecv] = []

        for itm in data["params"][2]:
            self.itemsRecieved.append(GenericItemRecv(itm[0], itm[1], itm[2]))

class UserStatusUpdateRequestV2(UserStatusUpdateRequestV1):
    isContinue = False
    isFirstPlayFree = False
    itemsUsed = []
    lastSongInfo: LastSongDetail

    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.isContinue = bool(data["params"][3])
        self.isFirstPlayFree = bool(data["params"][4])
        self.itemsUsed = data["params"][5]
        self.lastSongInfo = LastSongDetail(data["params"][6][0], data["params"][6][1], 
            data["params"][6][2], data["params"][6][3], data["params"][6][4])
