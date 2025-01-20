import json
from dataclasses import dataclass, field
from enum import Enum


class Bonus(Enum):
    aka_dora = "赤ドラ"
    ura_dora = "裏ドラ"
    ippatsu = "一発"


@dataclass
class Hule:
    to: int
    cnt: int
    point: int
    bonus: Bonus


@dataclass
class User:
    seat: int
    nickname: str
    #level: str
    point: int = 0
    ura_dora: int = 0
    aka_dora: int = 0
    ippatsu: int = 0
    transaction: list[Hule] = field(default_factory=list)


class Jan:
    RATE = 500
    def __init__(self, paifu_path: str):
        raw_paifu = open(paifu_path, 'r')
        self.paifu = json.load(raw_paifu)
        self.users = self.get_users()

    def get_users(self) -> list[User]:
        users = []
        for u in self.paifu["head"]["accounts"]:
            user = User(seat=u["seat"], nickname=u["nickname"])
            for result in self.paifu["head"]["result"]["players"]:
                if result["seat"] == user.seat:
                    user.point = result["part_point_1"]
            users.append(user)
        return users
    
    def get_user_with_seat(self, seat: int) -> User:
        for u in self.users:
            if u.seat == seat:
                return u

    def get_recordHule(self) -> list:
        filtered_actions = [
            action for action in self.paifu["data"]["data"]["actions"]
            if action['type'] == 1 and action['result']['name'] == ".lq.RecordHule"
        ]
        return filtered_actions
 
    def calc_bonus(self):
        
        def count_ippatsu(hule: dict) -> int:
            return 1

        def count_ura_dora(hule: dict) -> int:
            if hule['liqi'] == False:
                return 0
            return 0
            
        def count_aka_dora(hule: dict) -> int:
            return 0
        
        def fangchong_user(delta_scores: list[int]) -> User:
            for i, score in enumerate(delta_scores):
                if score < 0:
                    return self.get_user_with_seat(i)

        def count(hule: dict, fangchong: User = None):
            winner = self.get_user_with_seat(hule['seat'])
            ippatsu = count_ippatsu(hule)
            ura_dora = count_ura_dora(hule)
            aka_dora = count_aka_dora(hule)

            if ippatsu + ura_dora + aka_dora == 0:
                return

            if fangchong is None: #ツモ
                for user in self.users:
                    if not user.seat == hule['seat']:
                        if ippatsu > 0:
                            user.transaction.append(Hule(to=hule['seat'], point=self.RATE*ippatsu, cnt=ippatsu, bonus=Bonus.ippatsu))
                            winner.ippatsu += 1
                        if ura_dora > 0:
                            user.transaction.append(Hule(to=hule['seat'], point=self.RATE*ura_dora, cnt=ura_dora, bonus=Bonus.ura_dora))
                            winner.ura_dora += 1
                        if aka_dora > 0:
                            user.transaction.append(Hule(to=hule['seat'], point=self.RATE*aka_dora, cnt=aka_dora, bonus=Bonus.aka_dora))
                            winner.aka_dora += 1
            else: #ロン
                if ippatsu > 0:
                    fangchong.transaction.append(Hule(to=hule['seat'], point=self.RATE*ippatsu, cnt=ippatsu, bonus=Bonus.ippatsu))
                    winner.ippatsu += 1
                if ura_dora > 0:
                    fangchong.transaction.append(Hule(to=hule['seat'], point=self.RATE*ura_dora, cnt=ura_dora, bonus=Bonus.ura_dora))
                    winner.ura_dora += 1
                if aka_dora > 0:
                    fangchong.transaction.append(Hule(to=hule['seat'], point=self.RATE*aka_dora, cnt=aka_dora, bonus=Bonus.aka_dora))
                    winner.aka_dora += 1

        recordHule = self.get_recordHule()
        for record in recordHule:
            for hule in record['result']['data']['hules']:
                user = None if hule['zimo'] == True else fangchong_user(['result']['data']['delta_scores'])
                count(hule, user)
                
        

    def _getValue(self, key, items):
        values = [x['Value'] for x in items if 'Key' in x and 'Value' in x and x['Key'] == key]
        return values[0] if values else None
        

j = Jan("./test.json")
j.calc_bonus()