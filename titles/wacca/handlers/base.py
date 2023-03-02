from typing import Dict, List
from titles.wacca.handlers.helpers import Version
from datetime import datetime

class BaseRequest():
    def __init__(self, data: Dict) -> None:
        self.requestNo: int = data["requestNo"]
        self.appVersion: Version = Version(data["appVersion"])
        self.boardId: str = data["boardId"]
        self.chipId: str = data["chipId"]
        self.params: List = data["params"]

class BaseResponse():
    def __init__(self) -> None:
        self.status: int = 0
        self.message: str = ""
        self.serverTime: int = int(datetime.now().timestamp())
        self.maintNoticeTime: int = 0
        self.maintNotPlayableTime: int = 0
        self.maintStartTime: int = 0
        self.params: List = []

    def make(self) -> Dict:
        return {
            "status": self.status,
            "message": self.message,
            "serverTime": self.serverTime,
            "maintNoticeTime": self.maintNoticeTime,
            "maintNotPlayableTime": self.maintNotPlayableTime,
            "maintStartTime": self.maintStartTime,
            "params": self.params
        }
