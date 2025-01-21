import json
from module.jansoul import Jansoul
from pathlib import Path

from module.data import User

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


    def load_paifu_jansoul(self, path: str, cpu: int = 0, samma: bool = False):
        paifu_path = Path(path)
        with open(paifu_path, 'r') as paifu:
            paifu_json = json.load(paifu)
            j = Jansoul(paifu=paifu_json, cpu=cpu, samma=samma)
            users = j.get_users()

        self.users = sorted(users, key=lambda x:x.point, reverse=True)
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
            user.chip = self.count_chip(user)
        
        self.show_result()
    
    def count_chip(self, user: User) -> int:
        members_count = 2 if self.samma else 3
        chip_sum = user.ura_dora + user.aka_dora + user.ippatsu
        chip_sum += user.allstar * self.allstar_chip
        chip_sum += user.yiman * self.yiman_chip

        chip_sum += (user.ura_dora_tumo + user.aka_dora_tumo + user.ippatsu_tumo) * members_count
        chip_sum += user.allstar_tumo * self.allstar_chip * members_count 
        chip_sum += user.yiman_tumo * self.yiman_tumo_chip * members_count

        chip_sum += user.tobi

        return chip_sum
        

    def show_result(self):
        for user in self.users:
            bonus_sum = int(user.chip * (self.rate * 10))
            score_sum = round(user.score * self.rate)
 

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
                f"[green]+{bonus_sum}円[/]"
            )

            less_table = Table(show_header=True, header_style="bold magenta")
            less_table.add_column("振り込み先")
            less_table.add_column("内容", Text.from_markup("[b]Total", justify="right"))
            less_table.add_column("金額", justify="right")

            less_sum = 0
            for hule in user.transaction:
                less_sum += hule.cnt * 10 * self.rate
                desc = hule.bonus.value+"(ツモ)" if hule.zimo else hule.bonus.value+"(ロン)"
                less_table.add_row(
                    f'{hule.to}',
                    desc,
                    f'{self.rate * 10 * hule.cnt}円'
                )
            less_table.add_row(
                "", "[red]合計[/]", f"[red]-{less_sum}円[/]",
            )

            bonus_total = bonus_sum - less_sum

            total_table = Table(show_header=True, header_style="bold magenta")
            result = "red" if bonus_sum - less_sum < 0 else "green"
            total_table.add_column("収入", no_wrap=True)
            total_table.add_column("支出", no_wrap=True)
            total_table.add_column("結果", no_wrap=True, justify="right")
            total_table.add_row(f"{bonus_sum}円", f"{less_sum}円", f"[{result}]{bonus_total}円[/]")
            

            result_table = Table(show_header=True, header_style="bold magenta")
            result = "red" if score_sum + bonus_total < 0 else "green"
            result_table.add_column("得点", no_wrap=True)
            result_table.add_column("祝儀", no_wrap=True)
            result_table.add_column("結果", no_wrap=True, justify="right")
            result_table.add_row(f"{score_sum}円", f"{bonus_sum - less_sum}円", f"[{result}]{score_sum + bonus_total}円[/]")
            console.print(result_table)

            console.print(bonus_table)
            console.print(less_table)
            #console.print(total_table)




