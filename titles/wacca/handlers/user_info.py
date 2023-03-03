from typing import List, Dict

from titles.wacca.handlers.base import BaseRequest, BaseResponse
from titles.wacca.handlers.helpers import UserOption, DateUpdate

# ---user/info/update---
class UserInfoUpdateRequest(BaseRequest):
    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.profileId = int(self.params[0])
        self.optsUpdated: List[UserOption] = []
        self.unknown2: List = self.params[2]
        self.datesUpdated: List[DateUpdate] = []
        self.favoritesAdded: List[int] = self.params[4]
        self.favoritesRemoved: List[int] = self.params[5]

        for x in self.params[1]:
            self.optsUpdated.append(UserOption(x[0], x[1]))
        
        for x in self.params[3]:
            self.datesUpdated.append(DateUpdate[x[0], x[1]])

# ---user/info/getMyroom--- TODO: Understand this better
class UserInfogetMyroomRequest(BaseRequest):
    game_id = 0
    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.game_id = int(self.params[0])

class UserInfogetMyroomResponseV1(BaseResponse):
    def __init__(self) -> None:
        super().__init__()
        self.titleViewBadge = 0
        self.iconViewBadge = 0
        self.trophyViewBadge = 0
        self.noteColorViewBadge = 0
        self.noteSoundViewBadge = 0
        self.userViewingInfo = []

    def make(self) -> Dict:
        self.params = [
            self.titleViewBadge,
            self.iconViewBadge,
            self.trophyViewBadge,
            self.noteColorViewBadge,
            self.noteSoundViewBadge,
            self.userViewingInfo,
        ]

        return super().make()

class UserInfogetMyroomResponseV2(UserInfogetMyroomResponseV1):
    def __init__(self) -> None:
        super().__init__()

    def make(self) -> Dict:
        super().make()
        self.params += [0, 0, 0]
        return super(UserInfogetMyroomResponseV1, self).make()

# ---user/info/getRanking---
class UserInfogetRankingRequest(BaseRequest):
    game_id = 0
    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.game_id = int(self.params[0])
    
class UserInfogetRankingResponse(BaseResponse):
    def __init__(self) -> None:
        super().__init__()
        self.total_score_rank = 0
        self.high_score_by_song_rank = 0
        self.cumulative_score_rank = 0
        self.state_up_score_rank = 0
        self.other_score_ranking = 0
        self.wacca_points_ranking = 0

    def make(self) -> Dict:
        self.params = [
            self.total_score_rank,
            self.high_score_by_song_rank,
            self.cumulative_score_rank,
            self.state_up_score_rank,
            self.other_score_ranking,
            self.wacca_points_ranking,
        ]

        return super().make()