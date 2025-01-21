import json
from dataclasses import dataclass, field
from enum import Enum
from rich import print
from rich.table import Table
from rich.console import Console
from rich.text import Text
class Bonus(Enum):
    aka_dora = "赤ドラ"
    ura_dora = "裏ドラ"
    ippatsu = "一発"


@dataclass
class Hule:
    to: str
    cnt: int
    point: int
    zimo: bool
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
    ura_dora_tumo: int = 0
    aka_dora_tumo: int = 0
    ippatsu_tumo: int = 0
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
            for fans in hule['fans']:
                if fans['id'] == 30:
                    return fans['val']
            return 0
                
        def count_aka_dora(hule: dict) -> int:
            for fans in hule['fans']:
                if fans['id'] == 32:
                    return fans['val']
            return 0
                
        def count_ura_dora(hule: dict) -> int:
            for fans in hule['fans']:
                if fans['id'] == 33:
                    return fans['val']
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
                            user.transaction.append(Hule(to=winner.nickname, point=self.RATE*ippatsu, cnt=ippatsu, bonus=Bonus.ippatsu, zimo=True))
                            winner.ippatsu_tumo += ippatsu
                        if ura_dora > 0:
                            user.transaction.append(Hule(to=winner.nickname, point=self.RATE*ura_dora, cnt=ura_dora, bonus=Bonus.ura_dora, zimo=True))
                            winner.ura_dora_tumo += ura_dora
                        if aka_dora > 0:
                            user.transaction.append(Hule(to=winner.nickname, point=self.RATE*aka_dora, cnt=aka_dora, bonus=Bonus.aka_dora, zimo=True))
                            winner.aka_dora_tumo += aka_dora
            else: #ロン
                if ippatsu > 0:
                    fangchong.transaction.append(Hule(to=winner.nickname, point=self.RATE*ippatsu, cnt=ippatsu, bonus=Bonus.ippatsu, zimo=False))
                    winner.ippatsu += ippatsu
                if ura_dora > 0:
                    fangchong.transaction.append(Hule(to=winner.nickname, point=self.RATE*ura_dora, cnt=ura_dora, bonus=Bonus.ura_dora, zimo=False))
                    winner.ura_dora += ura_dora
                if aka_dora > 0:
                    fangchong.transaction.append(Hule(to=winner.nickname, point=self.RATE*aka_dora, cnt=aka_dora, bonus=Bonus.aka_dora, zimo=False))
                    winner.aka_dora += aka_dora

        recordHule = self.get_recordHule()
        for record in recordHule:
            for hule in record['result']['data']['hules']:
                user = None if hule['zimo'] == True else fangchong_user(record['result']['data']['delta_scores'])
                count(hule, user)

    def _getValue(self, key, items):
        values = [x['Value'] for x in items if 'Key' in x and 'Value' in x and x['Key'] == key]
        return values[0] if values else None
    
    def show_result(self):
        for user in self.users:
            bonus_sum = ((user.ippatsu + user.ura_dora + user.aka_dora + (user.ippatsu_tumo + user.ura_dora_tumo + user.aka_dora_tumo) * 3) * self.RATE)
            less_sum = 0

            print(f"\n{user.nickname}")
            print(f"・最終得点: {user.point}")
            """
            print("――――ご祝儀――――")
            print(f"一発: {user.ippatsu+user.ippatsu_tumo}回(ツモ:{user.ippatsu_tumo}回)")
            print(f"裏ドラ: {user.ura_dora+user.ura_dora_tumo}回(ツモ:{user.ura_dora_tumo}回)")
            print(f"赤ドラ: {user.aka_dora+user.aka_dora_tumo}回(ツモ:{user.aka_dora_tumo}回)")
            print(f"合計：{bonus_sum}円")
            print(f"――――振り込み――――")
            for hule in user.transaction:
                less_sum += hule.point
                if hule.zimo:
                    print(f"{hule.bonus.value} {hule.point}円 →　{hule.to}（ロン） ")
                else:
                    print(f"{hule.bonus.value} {hule.point}円 →　{hule.to}（ツモ） ")
            print(f"合計：[red]-{less_sum}円[/]")
            print(f"――――――収支――――――\n")
            if bonus_sum - less_sum > 0:
                print(f"[green]{bonus_sum - less_sum}円[/]")
            else:
                print(f"[red]{bonus_sum - less_sum}円[/]")
            print("――――――――――――――――")
            """

            console = Console()

            bonus_table = Table(show_header=True, header_style="bold magenta")
            bonus_table.add_column("赤ドラ")
            bonus_table.add_column("裏ドラ")
            bonus_table.add_column("一発")
            bonus_table.add_column("合計", justify="right")

            bonus_table.add_row(
                f"{user.aka_dora+user.aka_dora_tumo}回(ツモ:{user.aka_dora_tumo}回)",
                f"{user.ura_dora+user.ura_dora_tumo}回(ツモ:{user.ura_dora_tumo}回)",
                f"{user.ippatsu+user.ippatsu_tumo}回(ツモ:{user.ippatsu_tumo}回)",
                f"[green]+{bonus_sum}円[/]"
            )

            less_table = Table(show_header=True, header_style="bold magenta")
            less_table.add_column("振り込み先")
            less_table.add_column("内容", Text.from_markup("[b]Total", justify="right"))
            less_table.add_column("金額", justify="right")

            less_sum = 0
            for hule in user.transaction:
                less_sum += hule.point
                desc = hule.bonus.value+"(ツモ)" if hule.zimo else hule.bonus.value+"(ロン)"
                less_table.add_row(
                    f'{hule.to}',
                    desc,
                    f'{hule.point}円'
                )
            less_table.add_row(
                "", "[red]合計[/]", f"[red]-{less_sum}円[/]",
            )
            
            console.print(bonus_table)
            console.print(less_table)

            total_table = Table(show_header=True, header_style="bold magenta")
            result = "red" if bonus_sum - less_sum < 0 else "green"
            total_table.add_column("収入", no_wrap=True)
            total_table.add_column("支出", no_wrap=True)
            total_table.add_column("結果", no_wrap=True, justify="right")
            total_table.add_row(f"{bonus_sum}円", f"{less_sum}円", f"[{result}]{bonus_sum-less_sum}円[/]")
            console.print(total_table)



        

j = Jan("./test.json")
j.calc_bonus()
j.show_result()
