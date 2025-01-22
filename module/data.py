from dataclasses import dataclass, field
from enum import Enum

class Bonus(Enum):
    aka_dora = "赤ドラ"
    ura_dora = "裏ドラ"
    ippatsu = "一発"
    yiman = "役満"
    allstar = "オールスター"
    tobi = "トビ"

@dataclass
class Hule:
    to: str #支払い相手
    cnt: int #役達成回数
    zimo: bool #ツモならTrue, ロンならFalse
    bonus: Bonus #ご祝儀の題名
    yen: int = 0 #支払い金額

 
@dataclass
class User:
    seat: int #着順
    nickname: str #名前
    point: int = 0 #最終特典（ウマオカなし)
    score: float = 0 ##最終特典（ウマオカあり)
    score_yen: int = 0 #総合金額
    bonus_yen: int = 0 #獲得した祝儀の金額
    tobi: int = 0 #飛ばした回数
    ura_dora: int = 0 
    aka_dora: int = 0
    ippatsu: int = 0
    allstar: int = 0
    yiman: int = 0
    ura_dora_tumo: int = 0
    aka_dora_tumo: int = 0
    ippatsu_tumo: int = 0
    allstar_tumo: int = 0
    yiman_tumo: int = 0
    chip: int = 0
    transaction: list[Hule] = field(default_factory=list)

    def myless(self) -> int:
        total = 0
        for t in self.transaction:
            total += t.point
        return total
