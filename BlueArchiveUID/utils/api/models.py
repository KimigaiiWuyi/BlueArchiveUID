from typing import Dict, List, TypedDict


class FriendData(TypedDict):
    server: int
    friendCode: str
    friendCount: int
    nickname: str
    representCharacterUniqueId: int
    clanName: str
    comment: str
    level: int
    db: str
    lastHardCampaignClearStageId: int
    lastNormalCampaignClearStageId: int
    updateTime: int
    maxFavorRank: int
    echelonType: int
    assistInfoList: List['AssistInfo']


class AssistInfo(TypedDict):
    baRank: dict[str, int]
    baGlobalRank: dict[str, int]
    type: int
    uniqueId: int
    bulletType: str
    tacticRole: str
    echelonType: int
    level: int
    slotIndex: int
    starGrade: int
    favorRank: int
    publicSkillLevel: int
    exSkillLevel: int
    passiveSkillLevel: int
    extraPassiveSkillLevel: int
    equipment: List['Equipment']
    weapon: str
    weaponUniqueId: int
    weaponType: int
    weaponLevel: int
    weaponStartGrade: int


class Equipment(TypedDict):
    Type: int
    ServerId: int
    UniqueId: int
    StackCount: int
    Level: int
    Tier: int
    BoundCharacterServerId: int
    isNew: bool
    IsLocked: bool


class RankAssistInfo(TypedDict):
    baRank: Dict[str, int]
    baGlobalRank: Dict[str, int]
    type: int
    uniqueId: int
    bulletType: str
    tacticRole: str
    echelonType: int
    level: int
    slotIndex: int
    starGrade: int
    favorRank: int
    publicSkillLevel: int
    exSkillLevel: int
    passiveSkillLevel: int
    extraPassiveSkillLevel: int
    equipment: List[Equipment]
    weapon: bool
    weaponUniqueId: int
    weaponType: int
    weaponLevel: int
    weaponStartGrade: int


class Record(TypedDict):
    server: int
    friendCode: str
    friendCount: int
    nickname: str
    representCharacterUniqueId: int
    clanName: str
    comment: str
    level: int
    db: bool
    lastHardCampaignClearStageId: int
    lastNormalCampaignClearStageId: int
    updateTime: int
    maxFavorRank: int
    echelonType: int
    assistInfoList: List[RankAssistInfo]


class RankResp(TypedDict):
    page: int
    size: int
    totalPages: int
    totalData: int
    records: List[Record]
    lastPage: bool


class LabelInfo(TypedDict):
    dataType: int
    tryNumber: int


class DataItem(TypedDict):
    rank: int
    bestRankingPoint: int
    hard: str
    battleTime: str
    labelInfo: List[LabelInfo]
