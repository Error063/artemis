from typing import List, Dict

from titles.wacca.handlers.base import BaseRequest, BaseResponse
from titles.wacca.handlers.helpers import HousingInfo
from titles.wacca.const import WaccaConstants


# ---housing/get----
class HousingGetResponse(BaseResponse):
    def __init__(self, housingId: int) -> None:
        super().__init__()
        self.housingId: int = housingId
        self.isNewCab: bool = False

    def make(self) -> Dict:
        self.params = [self.housingId, int(self.isNewCab)]
        return super().make()


# ---housing/start----
class HousingStartRequestV1(BaseRequest):
    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        self.unknown0: str = self.params[0]
        self.errorLog: str = self.params[1]
        self.info: List[HousingInfo] = []

        for info in self.params[2]:
            self.info.append(HousingInfo(info[0], info[1]))


class HousingStartRequestV2(HousingStartRequestV1):
    def __init__(self, data: Dict) -> None:
        super(HousingStartRequestV1, self).__init__(data)
        self.unknown0: str = self.params[0]
        self.errorLog: str = self.params[1]
        self.creditLog: str = self.params[2]
        self.info: List[HousingInfo] = []

        for info in self.params[3]:
            self.info.append(HousingInfo(info[0], info[1]))


class HousingStartResponseV1(BaseResponse):
    def __init__(
        self,
        regionId: WaccaConstants.Region = WaccaConstants.Region.HOKKAIDO,
        songList: List[int] = [],
    ) -> None:
        super().__init__()
        self.regionId = regionId
        self.songList = songList  # Recomended songs

        if not self.songList:
            self.songList = [
                1269,
                1007,
                1270,
                1002,
                1020,
                1003,
                1008,
                1211,
                1018,
                1092,
                1056,
                32,
                1260,
                1230,
                1258,
                1251,
                2212,
                1264,
                1125,
                1037,
                2001,
                1272,
                1126,
                1119,
                1104,
                1070,
                1047,
                1044,
                1027,
                1004,
                1001,
                24,
                2068,
                2062,
                2021,
                1275,
                1249,
                1207,
                1203,
                1107,
                1021,
                1009,
                9,
                4,
                3,
                23,
                22,
                2014,
                13,
                1276,
                1247,
                1240,
                1237,
                1128,
                1114,
                1110,
                1109,
                1102,
                1045,
                1043,
                1036,
                1035,
                1030,
                1023,
                1015,
            ]

    def make(self) -> Dict:
        self.params = [self.regionId.value, self.songList]

        return super().make()
