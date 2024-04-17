from typing import List, Optional, Any
from enum import Enum

from titles.wacca.const import WaccaConstants


class ShortVersion:
    def __init__(self, version: str = "", major=1, minor=0, patch=0) -> None:
        split = version.split(".")
        if len(split) >= 3:
            self.major = int(split[0])
            self.minor = int(split[1])
            self.patch = int(split[2])

        else:
            self.major = major
            self.minor = minor
            self.patch = patch

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def __int__(self) -> int:
        return (self.major * 10000) + (self.minor * 100) + self.patch

    def __eq__(self, other: "ShortVersion"):
        return (
            self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
        )

    def __gt__(self, other: "ShortVersion"):
        if self.major > other.major:
            return True
        elif self.major == other.major:
            if self.minor > other.minor:
                return True
            elif self.minor == other.minor:
                if self.patch > other.patch:
                    return True

        return False

    def __ge__(self, other: "ShortVersion"):
        if self.major > other.major:
            return True
        elif self.major == other.major:
            if self.minor > other.minor:
                return True
            elif self.minor == other.minor:
                if self.patch > other.patch or self.patch == other.patch:
                    return True

        return False

    def __lt__(self, other: "ShortVersion"):
        if self.major < other.major:
            return True
        elif self.major == other.major:
            if self.minor < other.minor:
                return True
            elif self.minor == other.minor:
                if self.patch < other.patch:
                    return True

        return False

    def __le__(self, other: "ShortVersion"):
        if self.major < other.major:
            return True
        elif self.major == other.major:
            if self.minor < other.minor:
                return True
            elif self.minor == other.minor:
                if self.patch < other.patch or self.patch == other.patch:
                    return True

        return False


class Version(ShortVersion):
    def __init__(
        self, version="", major=1, minor=0, patch=0, country="JPN", build=0, role="C"
    ) -> None:
        super().__init__(version, major, minor, patch)
        split = version.split(".")
        if len(split) >= 6:
            self.country: str = split[3]
            self.build = int(split[4])
            self.role: str = split[5]

        else:
            self.country = country
            self.build = build
            self.role = role

    def __str__(self) -> str:
        return f"{self.major}.{self.minor:02}.{self.patch:02}.{self.country}.{self.build:05}.{self.role}"


class HousingInfo:
    """
    1 is lan install role, 2 is country
    """

    id: int = 0
    val: str = ""

    def __init__(self, id: int = 0, val: str = "") -> None:
        self.id = id
        self.val = val

    def make(self) -> List:
        return [self.id, self.val]


class Notice:
    title: str = ""
    message: str = ""
    dialog: str = ""
    fullImage: str = ""
    messageImage: str = ""
    showTitleScreen: bool = True
    showWelcomeScreen: bool = True
    startTime: int = 0
    endTime: int = 0
    voiceLine: int = 0

    def __init__(
        self,
        title: str = "",
        message: str = "",
        dialog: str = "",
        start: int = 0,
        end: int = 0,
    ) -> None:
        self.title = title
        self.message = message
        self.dialog = dialog
        self.startTime = start
        self.endTime = end

    def make(self) -> List:
        return [
            self.title,
            self.message,
            self.dialog,
            self.fullImage,
            self.messageImage,
            int(self.showTitleScreen),
            int(self.showWelcomeScreen),
            self.startTime,
            self.endTime,
            self.voiceLine,
        ]


class UserOption:
    def __init__(self, opt_id: int = 0, opt_val: Any = 0) -> None:
        self.optId = opt_id
        self.optVal = opt_val

    def make(self) -> List:
        return [self.optId, self.optVal]


class UserStatusV1:
    def __init__(self) -> None:
        self.userId: int = 0
        self.username: str = ""
        self.userType: int = 1
        self.xp: int = 0
        self.danLevel: int = 0
        self.danType: int = 0
        self.wp: int = 0
        self.titlePartIds: List[int] = [0, 0, 0]
        self.useCount: int = 0

    def make(self) -> List:
        return [
            self.userId,
            self.username,
            self.userType,
            self.xp,
            self.danLevel,
            self.danType,
            self.wp,
            self.titlePartIds,
            self.useCount,
        ]


class UserStatusV2(UserStatusV1):
    def __init__(self) -> None:
        super().__init__()
        self.loginDays: int = 0
        self.loginConsecutive: int = 0
        self.loginConsecutiveDays: int = 0
        self.loginsToday: int = 0
        self.rating: int = 0
        self.vipExpireTime: int = 0

    def make(self) -> List:
        ret = super().make()

        ret.append(self.loginDays)
        ret.append(self.loginConsecutive)
        ret.append(self.loginConsecutiveDays)
        ret.append(self.vipExpireTime)
        ret.append(self.loginsToday)
        ret.append(self.rating)

        return ret


class ProfileStatus(Enum):
    ProfileGood = 0
    ProfileRegister = 1
    ProfileInUse = 2
    ProfileWrongRegion = 3


class PlayVersionStatus(Enum):
    VersionGood = 0
    VersionTooNew = 1
    VersionUpgrade = 2


class PlayModeCounts:
    seasonId: int = 0
    modeId: int = 0
    playNum: int = 0

    def __init__(self, seasonId: int, modeId: int, playNum: int) -> None:
        self.seasonId = seasonId
        self.modeId = modeId
        self.playNum = playNum

    def make(self) -> List:
        return [self.seasonId, self.modeId, self.playNum]


class SongUnlock:
    songId: int = 0
    difficulty: int = 0
    whenAppeared: int = 0
    whenUnlocked: int = 0

    def __init__(
        self,
        song_id: int = 0,
        difficulty: int = 1,
        whenAppered: int = 0,
        whenUnlocked: int = 0,
    ) -> None:
        self.songId = song_id
        self.difficulty = difficulty
        self.whenAppeared = whenAppered
        self.whenUnlocked = whenUnlocked

    def make(self) -> List:
        return [self.songId, self.difficulty, self.whenAppeared, self.whenUnlocked]


class GenericItemRecv:
    def __init__(self, item_type: int = 1, item_id: int = 1, quantity: int = 1) -> None:
        self.itemId = item_id
        self.itemType = item_type
        self.quantity = quantity

    def make(self) -> List:
        return [self.itemType, self.itemId, self.quantity]


class GenericItemSend:
    def __init__(self, itemId: int, itemType: int, whenAcquired: int) -> None:
        self.itemId = itemId
        self.itemType = itemType
        self.whenAcquired = whenAcquired

    def make(self) -> List:
        return [self.itemId, self.itemType, self.whenAcquired]


class IconItem(GenericItemSend):
    uses: int = 0

    def __init__(
        self, itemId: int, itemType: int, uses: int, whenAcquired: int
    ) -> None:
        super().__init__(itemId, itemType, whenAcquired)
        self.uses = uses

    def make(self) -> List:
        return [self.itemId, self.itemType, self.uses, self.whenAcquired]


class TrophyItem:
    trophyId: int = 0
    season: int = 1
    progress: int = 0
    badgeType: int = 0

    def __init__(
        self, trophyId: int, season: int, progress: int, badgeType: int
    ) -> None:
        self.trophyId = trophyId
        self.season = season
        self.progress = progress
        self.badgeType = badgeType

    def make(self) -> List:
        return [self.trophyId, self.season, self.progress, self.badgeType]


class TicketItem:
    userTicketId: int = 0
    ticketId: int = 0
    whenExpires: int = 0

    def __init__(self, userTicketId: int, ticketId: int, whenExpires: int) -> None:
        self.userTicketId = userTicketId
        self.ticketId = ticketId
        self.whenExpires = whenExpires

    def make(self) -> List:
        return [self.userTicketId, self.ticketId, self.whenExpires]


class NavigatorItem(IconItem):
    usesToday: int = 0

    def __init__(
        self, itemId: int, itemType: int, whenAcquired: int, uses: int, usesToday: int
    ) -> None:
        super().__init__(itemId, itemType, uses, whenAcquired)
        self.usesToday = usesToday

    def make(self) -> List:
        return [
            self.itemId,
            self.itemType,
            self.whenAcquired,
            self.uses,
            self.usesToday,
        ]


class SkillItem:
    skillType: int
    level: int
    flag: int
    badge: int

    def make(self) -> List:
        return [self.skillType, self.level, self.flag, self.badge]


class UserEventInfo:
    def __init__(self) -> None:
        self.eventId = 0
        self.conditionInfo: List[UserEventConditionInfo] = []

    def make(self) -> List:
        conditions = []
        for x in self.conditionInfo:
            conditions.append(x.make())

        return [self.eventId, conditions]


class UserEventConditionInfo:
    def __init__(self) -> None:
        self.achievementCondition = 0
        self.progress = 0

    def make(self) -> List:
        return [self.achievementCondition, self.progress]


class UserItemInfoV1:
    def __init__(self) -> None:
        self.songUnlocks: List[SongUnlock] = []
        self.titles: List[GenericItemSend] = []
        self.icons: List[IconItem] = []
        self.trophies: List[TrophyItem] = []
        self.skills: List[SkillItem] = []
        self.tickets: List[TicketItem] = []
        self.noteColors: List[GenericItemSend] = []
        self.noteSounds: List[GenericItemSend] = []

    def make(self) -> List:
        unlocks = []
        titles = []
        icons = []
        trophies = []
        skills = []
        tickets = []
        colors = []
        sounds = []

        for x in self.songUnlocks:
            unlocks.append(x.make())
        for x in self.titles:
            titles.append(x.make())
        for x in self.icons:
            icons.append(x.make())
        for x in self.trophies:
            trophies.append(x.make())
        for x in self.skills:
            skills.append(x.make())
        for x in self.tickets:
            tickets.append(x.make())
        for x in self.noteColors:
            colors.append(x.make())
        for x in self.noteSounds:
            sounds.append(x.make())

        return [
            unlocks,
            titles,
            icons,
            trophies,
            skills,
            tickets,
            colors,
            sounds,
        ]


class UserItemInfoV2(UserItemInfoV1):
    def __init__(self) -> None:
        super().__init__()
        self.navigators: List[NavigatorItem] = []
        self.plates: List[GenericItemSend] = []

    def make(self) -> List:
        ret = super().make()
        plates = []
        navs = []

        for x in self.navigators:
            navs.append(x.make())
        for x in self.plates:
            plates.append(x.make())

        ret.append(navs)
        ret.append(plates)
        return ret


class UserItemInfoV3(UserItemInfoV2):
    def __init__(self) -> None:
        super().__init__()
        self.touchEffect: List[GenericItemSend] = []

    def make(self) -> List:
        ret = super().make()
        effect = []

        for x in self.touchEffect:
            effect.append(x.make())

        ret.append(effect)
        return ret


class SongDetailClearCounts:
    def __init__(
        self,
        playCt: int = 0,
        clearCt: int = 0,
        mlCt: int = 0,
        fcCt: int = 0,
        amCt: int = 0,
        counts: Optional[List[int]] = None,
    ) -> None:
        if counts is None:
            self.playCt = playCt
            self.clearCt = clearCt
            self.misslessCt = mlCt
            self.fullComboCt = fcCt
            self.allMarvelousCt = amCt

        else:
            self.playCt = counts[0]
            self.clearCt = counts[1]
            self.misslessCt = counts[2]
            self.fullComboCt = counts[3]
            self.allMarvelousCt = counts[4]

    def make(self) -> List:
        return [
            self.playCt,
            self.clearCt,
            self.misslessCt,
            self.fullComboCt,
            self.allMarvelousCt,
        ]


class SongDetailGradeCountsV1:
    dCt: int
    cCt: int
    bCt: int
    aCt: int
    aaCt: int
    aaaCt: int
    sCt: int
    ssCt: int
    sssCt: int
    masterCt: int

    def __init__(
        self,
        d: int = 0,
        c: int = 0,
        b: int = 0,
        a: int = 0,
        aa: int = 0,
        aaa: int = 0,
        s: int = 0,
        ss: int = 0,
        sss: int = 0,
        master: int = 0,
        counts: Optional[List[int]] = None,
    ) -> None:
        if counts is None:
            self.dCt = d
            self.cCt = c
            self.bCt = b
            self.aCt = a
            self.aaCt = aa
            self.aaaCt = aaa
            self.sCt = s
            self.ssCt = ss
            self.sssCt = sss
            self.masterCt = master

        else:
            self.dCt = counts[0]
            self.cCt = counts[1]
            self.bCt = counts[2]
            self.aCt = counts[3]
            self.aaCt = counts[4]
            self.aaaCt = counts[5]
            self.sCt = counts[6]
            self.ssCt = counts[7]
            self.sssCt = counts[8]
            self.masterCt = counts[9]

    def make(self) -> List:
        return [
            self.dCt,
            self.cCt,
            self.bCt,
            self.aCt,
            self.aaCt,
            self.aaaCt,
            self.sCt,
            self.ssCt,
            self.sssCt,
            self.masterCt,
        ]


class SongDetailGradeCountsV2(SongDetailGradeCountsV1):
    spCt: int
    sspCt: int
    ssspCt: int

    def __init__(
        self,
        d: int = 0,
        c: int = 0,
        b: int = 0,
        a: int = 0,
        aa: int = 0,
        aaa: int = 0,
        s: int = 0,
        ss: int = 0,
        sss: int = 0,
        master: int = 0,
        sp: int = 0,
        ssp: int = 0,
        sssp: int = 0,
        counts: Optional[List[int]] = None,
    ) -> None:
        super().__init__(d, c, b, a, aa, aaa, s, ss, sss, master, counts)
        if counts is None:
            self.spCt = sp
            self.sspCt = ssp
            self.ssspCt = sssp

        else:
            self.spCt = counts[10]
            self.sspCt = counts[11]
            self.ssspCt = counts[12]

    def make(self) -> List:
        return [
            self.dCt,
            self.cCt,
            self.bCt,
            self.aCt,
            self.aaCt,
            self.aaaCt,
            self.sCt,
            self.spCt,
            self.ssCt,
            self.sspCt,
            self.sssCt,
            self.ssspCt,
            self.masterCt,
        ]


class BestScoreDetailV1:
    songId: int = 0
    difficulty: int = 1
    clearCounts: SongDetailClearCounts = SongDetailClearCounts()
    clearCountsSeason: SongDetailClearCounts = SongDetailClearCounts()
    gradeCounts: SongDetailGradeCountsV1 = SongDetailGradeCountsV1()
    score: int = 0
    bestCombo: int = 0
    lowestMissCtMaybe: int = 0
    isUnlock: int = 1
    rating: int = 0

    def __init__(self, song_id: int, difficulty: int = 1) -> None:
        self.songId = song_id
        self.difficulty = difficulty

    def make(self) -> List:
        return [
            self.songId,
            self.difficulty,
            self.clearCounts.make(),
            self.clearCountsSeason.make(),
            self.gradeCounts.make(),
            self.score,
            self.bestCombo,
            self.lowestMissCtMaybe,
            self.isUnlock,
            self.rating,
        ]


class BestScoreDetailV2(BestScoreDetailV1):
    gradeCounts: SongDetailGradeCountsV2 = SongDetailGradeCountsV2()


class SongUpdateJudgementCounts:
    marvCt: int
    greatCt: int
    goodCt: int
    missCt: int

    def __init__(
        self, marvs: int = 0, greats: int = 0, goods: int = 0, misses: int = 0
    ) -> None:
        self.marvCt = marvs
        self.greatCt = greats
        self.goodCt = goods
        self.missCt = misses

    def make(self) -> List:
        return [self.marvCt, self.greatCt, self.goodCt, self.missCt]


class SongUpdateDetailV1:
    def __init__(self, data: List) -> None:
        if data is not None:
            self.songId = data[0]
            self.difficulty = data[1]
            self.level = data[2]
            self.score = data[3]

            self.judgements = SongUpdateJudgementCounts(
                data[4][0], data[4][1], data[4][2], data[4][3]
            )
            self.maxCombo = data[5]
            self.grade = WaccaConstants.GRADES(
                data[6]
            )  # .value to get number, .name to get letter

            self.flagCleared = False if data[7] == 0 else True
            self.flagMissless = False if data[8] == 0 else True
            self.flagFullcombo = False if data[9] == 0 else True
            self.flagAllMarvelous = False if data[10] == 0 else True
            self.flagGiveUp = False if data[11] == 0 else True
            self.skillPt = data[12]
            self.fastCt = 0
            self.slowCt = 0
            self.flagNewRecord = False


class SongUpdateDetailV2(SongUpdateDetailV1):
    def __init__(self, data: List) -> None:
        super().__init__(data)
        if data is not None:
            self.fastCt = data[13]
            self.slowCt = data[14]
            self.flagNewRecord = False if data[15] == 0 else True


class SeasonalInfoV1:
    def __init__(self) -> None:
        self.level: int = 0
        self.wpObtained: int = 0
        self.wpSpent: int = 0
        self.cumulativeScore: int = 0
        self.titlesObtained: int = 0
        self.iconsObtained: int = 0
        self.skillPts: int = 0
        self.noteColorsObtained: int = 0
        self.noteSoundsObtained: int = 0

    def make(self) -> List:
        return [
            self.level,
            self.wpObtained,
            self.wpSpent,
            self.cumulativeScore,
            self.titlesObtained,
            self.iconsObtained,
            self.skillPts,
            self.noteColorsObtained,
            self.noteSoundsObtained,
        ]


class SeasonalInfoV2(SeasonalInfoV1):
    def __init__(self) -> None:
        super().__init__()
        self.platesObtained: int = 0
        self.cumulativeGatePts: int = 0

    def make(self) -> List:
        return super().make() + [self.platesObtained, self.cumulativeGatePts]


class BingoPageStatus:
    id = 0
    location = 1
    progress = 0

    def __init__(self, id: int = 0, location: int = 1, progress: int = 0) -> None:
        self.id = id
        self.location = location
        self.progress = progress

    def make(self) -> List:
        return [self.id, self.location, self.progress]


class BingoDetail:
    def __init__(self, pageNumber: int) -> None:
        self.pageNumber = pageNumber
        self.pageStatus: List[BingoPageStatus] = []

    def make(self) -> List:
        status = []
        for x in self.pageStatus:
            status.append(x.make())

        return [self.pageNumber, status]


class GateDetailV1:
    def __init__(
        self,
        gate_id: int = 1,
        page: int = 1,
        progress: int = 0,
        loops: int = 0,
        last_used: int = 0,
        mission_flg=0,
    ) -> None:
        self.id = gate_id
        self.page = page
        self.progress = progress
        self.loops = loops
        self.lastUsed = last_used
        self.missionFlg = mission_flg

    def make(self) -> List:
        return [self.id, 1, self.page, self.progress, self.loops, self.lastUsed]


class GateDetailV2(GateDetailV1):
    def make(self) -> List:
        return super().make() + [self.missionFlg]


class GachaInfo:
    def __init__(self, gacha_id: int = 0, gacha_roll_ct: int = 0) -> None:
        self.gachaId = gacha_id
        self.rollCt = gacha_roll_ct

    def make(self) -> List:
        return [self.gachaId, self.rollCt]


class LastSongDetail:
    lastSongId = 90
    lastSongDiff = 1
    lastFolderOrd = 1
    lastFolderId = 1
    lastSongOrd = 1

    def __init__(
        self,
        last_song: int = 90,
        last_diff: int = 1,
        last_folder_ord: int = 1,
        last_folder_id: int = 1,
        last_song_ord: int = 1,
    ) -> None:
        self.lastSongId = last_song
        self.lastSongDiff = last_diff
        self.lastFolderOrd = last_folder_ord
        self.lastFolderId = last_folder_id
        self.lastSongOrd = last_song_ord

    def make(self) -> List:
        return [
            self.lastSongId,
            self.lastSongDiff,
            self.lastFolderOrd,
            self.lastFolderId,
            self.lastSongOrd,
        ]


class FriendScoreDetail:
    def __init__(
        self, song_id: int = 0, difficulty: int = 1, best_score: int = 0
    ) -> None:
        self.songId = song_id
        self.difficulty = difficulty
        self.bestScore = best_score

    def make(self) -> List:
        return [self.songId, self.difficulty, self.bestScore]


class FriendDetail:
    def __init__(self, user_id: int = 0, username: str = "") -> None:
        self.friendId = user_id
        self.friendUsername = username
        self.friendUserType = 1
        self.friendScoreDetail: List[FriendScoreDetail] = []

    def make(self) -> List:
        scores = []

        for x in self.friendScoreDetail:
            scores.append(x.make())

        return [self.friendId, self.friendUsername, self.friendUserType, scores]


class LoginBonusInfo:
    def __init__(self) -> None:
        self.tickets: List[TicketItem] = []
        self.items: List[GenericItemRecv] = []
        self.message: str = ""

    def make(self) -> List:
        tks = []
        itms = []

        for ticket in self.tickets:
            tks.append(ticket.make())

        for item in self.items:
            itms.append(item.make())

        return [tks, itms, self.message]


class VipLoginBonus:
    id = 1
    unknown = 0
    item: GenericItemRecv

    def __init__(
        self,
        id: int = 1,
        unk: int = 0,
        item_type: int = 1,
        item_id: int = 1,
        item_qt: int = 1,
    ) -> None:
        self.id = id
        self.unknown = unk
        self.item = GenericItemRecv(item_type, item_id, item_qt)

    def make(self) -> List:
        return [self.id, self.unknown, self.item.make()]


class VipInfo:
    def __init__(
        self, year: int = 2019, month: int = 1, day: int = 1, num_item: int = 1
    ) -> None:
        self.pageYear = year
        self.pageMonth = month
        self.pageDay = day
        self.numItem = num_item
        self.presentInfo: List[LoginBonusInfo] = []
        self.vipLoginBonus: List[VipLoginBonus] = []

    def make(self) -> List:
        pres = []
        vipBonus = []

        for present in self.presentInfo:
            pres.append(present.make())

        for b in self.vipLoginBonus:
            vipBonus.append(b.make())

        return [
            self.pageYear,
            self.pageMonth,
            self.pageDay,
            self.numItem,
            pres,
            vipBonus,
        ]


class PurchaseType(Enum):
    PurchaseTypeCredit = 1
    PurchaseTypeWP = 2


class PlayType(Enum):
    PlayTypeSingle = 1
    PlayTypeVs = 2
    PlayTypeCoop = 3
    PlayTypeStageup = 4
    PlayTypeTimeFree = 5


class StageInfo:
    danId: int = 0
    danLevel: int = 0
    clearStatus: int = 0
    numSongCleared: int = 0
    song1BestScore: int = 0
    song2BestScore: int = 0
    song3BestScore: int = 0
    unk5: int = 1

    def __init__(self, dan_id: int = 0, dan_level: int = 0) -> None:
        self.danId = dan_id
        self.danLevel = dan_level

    def make(self) -> List:
        return [
            self.danId,
            self.danLevel,
            self.clearStatus,
            self.numSongCleared,
            [
                self.song1BestScore,
                self.song2BestScore,
                self.song3BestScore,
            ],
            self.unk5,
        ]


class StageupClearType(Enum):
    FAIL = 0
    CLEAR_BLUE = 1
    CLEAR_SILVER = 2
    CLEAR_GOLD = 3


class MusicUpdateDetailV1:
    def __init__(self) -> None:
        self.songId = 0
        self.difficulty = 1
        self.clearCounts: SongDetailClearCounts = SongDetailClearCounts()
        self.clearCountsSeason: SongDetailClearCounts = SongDetailClearCounts()
        self.grades: SongDetailGradeCountsV1 = SongDetailGradeCountsV1()
        self.score = 0
        self.lowestMissCount = 0
        self.maxSkillPts = 0
        self.lockState = 0

    def make(self) -> List:
        return [
            self.songId,
            self.difficulty,
            self.clearCounts.make(),
            self.clearCountsSeason.make(),
            self.grades.make(),
            self.score,
            self.lowestMissCount,
            self.maxSkillPts,
            self.lockState,
        ]


class MusicUpdateDetailV2(MusicUpdateDetailV1):
    def __init__(self) -> None:
        super().__init__()
        self.rating = 0

    def make(self) -> List:
        return super().make() + [self.rating]


class MusicUpdateDetailV3(MusicUpdateDetailV2):
    def __init__(self) -> None:
        super().__init__()
        self.grades = SongDetailGradeCountsV2()


class SongRatingUpdate:
    def __init__(
        self, song_id: int = 0, difficulty: int = 1, new_rating: int = 0
    ) -> None:
        self.songId = song_id
        self.difficulty = difficulty
        self.rating = new_rating

    def make(self) -> List:
        return [
            self.songId,
            self.difficulty,
            self.rating,
        ]


class GateTutorialFlag:
    def __init__(self, tutorial_id: int = 1, flg_watched: bool = False) -> None:
        self.tutorialId = tutorial_id
        self.flagWatched = flg_watched

    def make(self) -> List:
        return [self.tutorialId, int(self.flagWatched)]


class DateUpdate:
    def __init__(self, date_id: int = 0, timestamp: int = 0) -> None:
        self.id = date_id
        self.timestamp = timestamp

    def make(self) -> List:
        return [self.id, self.timestamp]
