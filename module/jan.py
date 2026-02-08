import json
from pathlib import Path

from rich import print
from rich.console import Console
from rich.table import Table
from rich.text import Text

from module.data import Bonus, Settlement, User
from module.jansoul import Jansoul


class Jan:
    def __init__(
        self,
        samma: bool = False,
        rate=50,
        chip=500,
        uma_1=10,
        uma_2=20,
        oka_1=25000,
        oka_2=30000,
        all_star_chip=5,
        yiman_tumo_chip=5,
        yiman_chip=10,
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
        self.chip = chip

    def load_paifu_jansoul(self, path: str, samma: bool = False):
        paifu_path = Path(path)
        with open(paifu_path, "r", encoding="utf-8") as paifu:
            paifu_json = json.load(paifu)
            j = Jansoul(paifu=paifu_json, samma=samma)
            users = j.get_users()
        self.users = sorted(users, key=lambda x: x.point, reverse=True)
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
                        yen += self.chip * t.cnt
                    case Bonus.ura_dora:
                        yen += self.chip * t.cnt
                    case Bonus.aka_dora:
                        yen += self.chip * t.cnt
                    case Bonus.allstar:
                        yen += self.chip * t.cnt * self.allstar_chip
                    case Bonus.yiman:
                        if t.zimo:
                            yen += self.chip * t.cnt * self.yiman_tumo_chip
                        else:
                            yen += self.chip * t.cnt * self.yiman_chip
                    case Bonus.tobi:
                        yen += self.chip

                t.yen = yen

        self._count_score_transaction()

    def _count_score_transaction(self):
        # 胴元なし精算:
        # 下位から上位へ、min(支払い残, 受け取り残)で順に充当する
        rank_index = {id(user): i for i, user in enumerate(self.users)}
        debtors = sorted(
            [user for user in self.users if user.score_yen < 0],
            key=lambda user: rank_index[id(user)],
            reverse=True,
        )
        creditors = sorted(
            [user for user in self.users if user.score_yen > 0],
            key=lambda user: rank_index[id(user)],
        )
        creditor_remaining = {id(user): user.score_yen for user in creditors}

        for debtor in debtors:
            debtor.score_transaction.clear()
            remain = -debtor.score_yen

            for creditor in creditors:
                if remain <= 0:
                    break

                cid = id(creditor)
                c_remain = creditor_remaining[cid]
                if c_remain <= 0:
                    continue

                pay = min(remain, c_remain)
                debtor.score_transaction.append(Settlement(to=creditor.nickname, yen=pay))
                remain -= pay
                creditor_remaining[cid] -= pay

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
        return int(user.chip * (self.chip))

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
                f"[green]+{user.bonus_yen}円[/]",
            )

            less_table = Table(show_header=True, header_style="bold magenta")
            less_table.add_column("振り込み先")
            less_table.add_column("内容", Text.from_markup("[b]Total", justify="right"))
            less_table.add_column("金額", justify="right")

            less_summary = {}
            less_sum = 0
            for hule in user.transaction:
                less_sum += hule.yen
                less_summary[hule.to] = less_summary.get(hule.to, 0) + hule.yen
                desc = hule.bonus.value + "(ツモ)" if hule.zimo else hule.bonus.value + "(ロン)"
                less_table.add_row(f"{hule.to}", desc, f"{hule.yen}円")
            less_table.add_row(
                "",
                "[red]合計[/]",
                f"[red]-{less_sum}円[/]",
            )

            score_summary = {}
            for s in user.score_transaction:
                score_summary[s.to] = score_summary.get(s.to, 0) + s.yen

            less_summary_table = Table(show_header=True, header_style="bold magenta")
            less_summary_table.add_column("振り込み先")
            less_summary_table.add_column("得点精算", justify="right")
            less_summary_table.add_column("祝儀", justify="right")
            less_summary_table.add_column("合計金額", justify="right")
            all_tos = set(less_summary.keys()) | set(score_summary.keys())
            if len(all_tos) == 0:
                less_summary_table.add_row("なし", "0円", "0円", "0円")
            else:
                merged = []
                for to in all_tos:
                    score_total = score_summary.get(to, 0)
                    bonus_total = less_summary.get(to, 0)
                    merged.append((to, score_total, bonus_total, score_total + bonus_total))
                for to, score_total, bonus_total, total in sorted(merged, key=lambda x: x[3], reverse=True):
                    less_summary_table.add_row(to, f"{score_total}円", f"{bonus_total}円", f"{total}円")

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
            result_table.add_row(
                f"{user.score_yen}円",
                f"{user.bonus_yen - less_sum}円",
                f"[{result}]{user.score_yen + bonus_total}円[/]",
            )
            console.print(result_table)

            console.print(bonus_table)
            console.print(less_table)
            console.print(less_summary_table)
            # console.print(total_table)
