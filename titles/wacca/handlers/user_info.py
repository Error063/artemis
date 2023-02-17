from typing import List, Dict

from titles.wacca.handlers.base import BaseRequest, BaseResponse
from titles.wacca.handlers.helpers import UserOption

# ---user/info/update---
class UserInfoUpdateRequest(BaseRequest):
    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.profileId = int(self.params[0])
        self.optsUpdated: List[UserOption] = []
        self.datesUpdated: List = self.params[3]
        self.favoritesAdded: List[int] = self.params[4]
        self.favoritesRemoved: List[int] = self.params[5]

        for x in self.params[2]:
            self.optsUpdated.append(UserOption(x[0], x[1]))

# ---user/info/getMyroom--- TODO: Understand this better
class UserInfogetMyroomRequest(BaseRequest):
    game_id = 0
    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.game_id = int(self.params[0])

class UserInfogetMyroomResponse(BaseResponse):
    def make(self) -> Dict:
        self.params = [
            0,0,0,0,0,[],0,0,0
        ]

        return super().make()

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