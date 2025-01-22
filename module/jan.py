import json
from module.jansoul import Jansoul
from pathlib import Path

from module.data import User, Bonus

from rich import print
from rich.table import Table
from rich.console import Console
from rich.text import Text

class Jan:
    def __init__(
            self,
            samma: bool = False,
            rate = 50,
            uma_1 = 10, uma_2 = 20, 
            oka_1 = 25000, oka_2 = 30000,
            all_star_chip = 5,
            yiman_tumo_chip = 5,
            yiman_chip = 10
        ):
        self.samma = samma
        self.rate = rate
        self.uma_1 = uma_1
        self.uma_2 = uma_2
        self.oka_1 = oka_1
        self.oka_2 = oka_2
        self.allstar_chip = all_star_chip
        self.yiman_tumo_chip = yiman_tumo_chip
        self.yiman_chip = yiman_chip

    def load_paifu_jansoul(self, path: str, samma: bool = False):
        paifu_path = Path(path)
        with open(paifu_path, 'r') as paifu:
            paifu_json = json.load(paifu)
            j = Jansoul(paifu=paifu_json, samma=samma)
            users = j.get_users()
        self.users = sorted(users, key=lambda x:x.point, reverse=True)
        self._count()
        self.show_result()
        return self.users

    def _count(self):
        for i, user in enumerate(self.users):
            total_point = user.point - self.oka_2
            total_point /= 1000
            match i:
                case 0:
                    total_point += self.uma_2
                    total_point += (self.oka_2 - self.oka_1) * 4 / 1000
                case 1:
                    total_point += self.uma_1
                case 2:
                    total_point -= self.uma_1
                case 3:
                    total_point -= self.uma_2
            user.score = total_point
            user.chip = self._count_chip(user)
            user.bonus_yen = self._count_bonus(user)
            user.score_yen = self._count_yen(user)

            for t in user.transaction:
                yen = 0
                match t.bonus:
                    case Bonus.ippatsu:
                        yen += self.rate * 10 * t.cnt
                    case Bonus.ura_dora:
                        yen += self.rate * 10 * t.cnt
                    case Bonus.aka_dora:
                        yen += self.rate * 10 * t.cnt
                    case Bonus.allstar:
                        yen += self.rate * 10 * t.cnt * self.allstar_chip
                    case Bonus.yiman:
                        if t.zimo:
                            yen += self.rate * 10 * t.cnt * self.yiman_tumo_chip
                        else:
                            yen += self.rate * 10 * t.cnt * self.yiman_chip
                    case Bonus.tobi:
                        yen += self.rate * 10 
                    
                t.yen = yen

    def _count_chip(self, user: User) -> int:
        members_count = 2 if self.samma else 3
        chip_sum = user.ura_dora + user.aka_dora + user.ippatsu
        chip_sum += user.allstar * self.allstar_chip
        chip_sum += user.yiman * self.yiman_chip

        chip_sum += (user.ura_dora_tumo + user.aka_dora_tumo + user.ippatsu_tumo) * members_count
        chip_sum += user.allstar_tumo * self.allstar_chip * members_count 
        chip_sum += user.yiman_tumo * self.yiman_tumo_chip * members_count

        chip_sum += user.tobi

        return chip_sum
    
    def _count_yen(self, user: User) -> int:
        return round(user.score * self.rate)
    
    def _count_bonus(self, user: User) -> int:
        return int(user.chip * (self.rate * 10))
    
    def show_result(self):
        for user in self.users:
            print(f"\n{user.nickname}")
            print(f"・最終得点: {user.point} ({user.score})")

            console = Console()

            bonus_table = Table(show_header=True, header_style="bold magenta")
            bonus_table.add_column("赤ドラ")
            bonus_table.add_column("裏ドラ")
            bonus_table.add_column("一発")
            bonus_table.add_column("オールスター")
            bonus_table.add_column("役満")
            bonus_table.add_column("飛ばし")
            bonus_table.add_column("合計", justify="right")

            bonus_table.add_row(
                f"{user.aka_dora+user.aka_dora_tumo}回(ツモ:{user.aka_dora_tumo}回)",
                f"{user.ura_dora+user.ura_dora_tumo}回(ツモ:{user.ura_dora_tumo}回)",
                f"{user.ippatsu+user.ippatsu_tumo}回(ツモ:{user.ippatsu_tumo}回)",
                f"{user.allstar+user.allstar_tumo}回(ツモ:{user.allstar_tumo}回)",
                f"{user.yiman+user.yiman_tumo}回(ツモ:{user.yiman_tumo}回)",
                f"{user.tobi}回",
                f"[green]+{user.bonus_yen}円[/]"
            )

            less_table = Table(show_header=True, header_style="bold magenta")
            less_table.add_column("振り込み先")
            less_table.add_column("内容", Text.from_markup("[b]Total", justify="right"))
            less_table.add_column("金額", justify="right")

            less_sum = 0
            for hule in user.transaction:
                less_sum += hule.yen
                desc = hule.bonus.value+"(ツモ)" if hule.zimo else hule.bonus.value+"(ロン)"
                less_table.add_row(
                    f'{hule.to}',
                    desc,
                    f'{hule.yen}円'
                )
            less_table.add_row(
                "", "[red]合計[/]", f"[red]-{less_sum}円[/]",
            )

            bonus_total = user.bonus_yen - less_sum

            total_table = Table(show_header=True, header_style="bold magenta")
            result = "red" if bonus_total < 0 else "green"
            total_table.add_column("収入", no_wrap=True)
            total_table.add_column("支出", no_wrap=True)
            total_table.add_column("結果", no_wrap=True, justify="right")
            total_table.add_row(f"{user.bonus_yen}円", f"{less_sum}円", f"[{result}]{bonus_total}円[/]")
            

            result_table = Table(show_header=True, header_style="bold magenta")
            result = "red" if user.score_yen + bonus_total < 0 else "green"
            result_table.add_column("得点", no_wrap=True)
            result_table.add_column("祝儀", no_wrap=True)
            result_table.add_column("結果", no_wrap=True, justify="right")
            result_table.add_row(f"{user.score_yen}円", f"{user.bonus_yen - less_sum}円", f"[{result}]{user.score_yen + bonus_total}円[/]")
            console.print(result_table)

            console.print(bonus_table)
            console.print(less_table)
            #console.print(total_table)

