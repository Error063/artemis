from typing import Dict, List
from titles.wacca.handlers.base import BaseRequest, BaseResponse
from titles.wacca.handlers.helpers import StageInfo, StageupClearType

# --user/trial/get--
class UserTrialGetRequest(BaseRequest):
    profileId: int = 0

    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.profileId = self.params[0]

class UserTrialGetResponse(BaseResponse):
    def __init__(self) -> None:
        super().__init__()
        
        self.stageList: List[StageInfo] = []

    def make(self) -> Dict:
        dans = []
        for x in self.stageList:
            dans.append(x.make())
        
        self.params = [dans]
        return super().make()

# --user/trial/update--
class UserTrialUpdateRequest(BaseRequest):
    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.profileId = self.params[0]
        self.stageId = self.params[1]
        self.stageLevel = self.params[2]
        self.clearType = StageupClearType(self.params[3])
        self.songScores = self.params[4]
        self.numSongsCleared = self.params[5]
        self.itemsObtained = self.params[6]
        self.unk7: List = []

        if len(self.params) == 8:
            self.unk7 = self.params[7]

class UserTrialUpdateResponse(BaseResponse):
    def __init__(self) -> None:
        super().__init__()
    
    def make(self) -> Dict:
        return super().make()