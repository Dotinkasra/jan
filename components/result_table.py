import flet as ft

from module.data import Bonus, Hule, User


class ResultTablePage(ft.UserControl):

    def __init__(self, user: User):
        super().__init__()
        self.user = user

    def did_mount(self):
        if self.page:
            self.page.update()

    def build(self):
        user = self.user
        self.bonus_table = ft.DataTable(
            heading_row_color=ft.Colors.BLACK12,
            vertical_lines=ft.BorderSide(1, "black"),
            horizontal_lines=ft.BorderSide(1, "black"),
            border=ft.border.all(2, "black"),
            columns=[
                ft.DataColumn(ft.Text("赤")),
                ft.DataColumn(ft.Text("裏")),
                ft.DataColumn(ft.Text("一発")),
                ft.DataColumn(ft.Text("オールスター")),
                ft.DataColumn(ft.Text("役満")),
                ft.DataColumn(ft.Text("飛")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{user.aka_dora}回")),
                        ft.DataCell(ft.Text(f"{user.ura_dora}回")),
                        ft.DataCell(ft.Text(f"{user.ippatsu}回")),
                        ft.DataCell(ft.Text(f"{user.allstar}回")),
                        ft.DataCell(ft.Text(f"{user.yiman}回")),
                        ft.DataCell(ft.Text(f"{user.tobi}回")),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{user.aka_dora_tumo}回")),
                        ft.DataCell(ft.Text(f"{user.ura_dora_tumo}回")),
                        ft.DataCell(ft.Text(f"{user.ippatsu_tumo}回")),
                        ft.DataCell(ft.Text(f"{user.allstar_tumo}回")),
                        ft.DataCell(ft.Text(f"{user.yiman_tumo}回")),
                        ft.DataCell(ft.Text(f"-")),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("合計")),
                        ft.DataCell(ft.Text(f"{user.bonus_yen:,}円")),
                    ],
                ),
            ],
        )

        less_rows = []
        less_summary_map = {}
        less_total = 0
        if len(user.transaction) <= 0:
            less_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("なし")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("0円")),
                    ]
                )
            )
        else:
            for hule in user.transaction:
                less_rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(hule.to)),
                            ft.DataCell(
                                ft.Text(f"{hule.bonus.value}(ツモ)" if hule.zimo else f"{hule.bonus.value}(ロン)")
                            ),
                            ft.DataCell(ft.Text(f"{hule.yen:,}円")),
                        ],
                    )
                )
                less_total += hule.yen
                less_summary_map[hule.to] = less_summary_map.get(hule.to, 0) + hule.yen

        self.less_table = ft.DataTable(
            heading_row_color=ft.Colors.BLACK12,
            vertical_lines=ft.BorderSide(1, "black"),
            horizontal_lines=ft.BorderSide(1, "black"),
            border=ft.border.all(2, "black"),
            columns=[
                ft.DataColumn(ft.Text("振込先")),
                ft.DataColumn(ft.Text("内容")),
                ft.DataColumn(ft.Text("金額")),
            ],
            rows=less_rows,
        )

        score_summary_map = {}
        for settlement in user.score_transaction:
            score_summary_map[settlement.to] = score_summary_map.get(settlement.to, 0) + settlement.yen

        all_payers = set(less_summary_map.keys()) | set(score_summary_map.keys())
        less_summary_rows = []
        if len(all_payers) <= 0:
            less_summary_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("なし")),
                        ft.DataCell(ft.Text("0円")),
                        ft.DataCell(ft.Text("0円")),
                        ft.DataCell(ft.Text("0円")),
                    ]
                )
            )
        else:
            merged = []
            for to in all_payers:
                score_total = score_summary_map.get(to, 0)
                bonus_total = less_summary_map.get(to, 0)
                merged.append((to, score_total, bonus_total, score_total + bonus_total))

            for to, score_total, bonus_total, total in sorted(merged, key=lambda x: x[3], reverse=True):
                less_summary_rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(to)),
                            ft.DataCell(ft.Text(f"{score_total:,}円")),
                            ft.DataCell(ft.Text(f"{bonus_total:,}円")),
                            ft.DataCell(ft.Text(f"{total:,}円")),
                        ],
                    )
                )

        self.less_summary_table = ft.DataTable(
            heading_row_color=ft.Colors.BLACK12,
            vertical_lines=ft.BorderSide(1, "black"),
            horizontal_lines=ft.BorderSide(1, "black"),
            border=ft.border.all(2, "black"),
            columns=[
                ft.DataColumn(ft.Text("振込先")),
                ft.DataColumn(ft.Text("得点精算")),
                ft.DataColumn(ft.Text("祝儀")),
                ft.DataColumn(ft.Text("合計金額")),
            ],
            rows=less_summary_rows,
        )

        bonus_total = user.bonus_yen - less_total
        result = user.score_yen + bonus_total

        self.result_table = ft.DataTable(
            heading_row_color=ft.Colors.BLACK12,
            vertical_lines=ft.BorderSide(1, "black"),
            horizontal_lines=ft.BorderSide(1, "black"),
            border=ft.border.all(2, "black"),
            columns=[
                ft.DataColumn(ft.Text("得点")),
                ft.DataColumn(ft.Text("祝儀収益")),
                ft.DataColumn(ft.Text("祝儀支払")),
                ft.DataColumn(ft.Text("結果")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{user.score_yen:,}円")),
                        ft.DataCell(ft.Text(f"{user.bonus_yen:,}円")),
                        ft.DataCell(
                            ft.Text(
                                f"-{less_total:,}円",
                                color=ft.Colors.RED if less_total > 0 else None,
                            )
                        ),
                        ft.DataCell(
                            ft.Text(f"{result:,}円", color=ft.Colors.RED if result < 0 else ft.Colors.GREEN_900)
                        ),
                    ],
                ),
            ],
        )
        container = ft.Column(
            [
                ft.Container(
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(f"【{user.nickname}】", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                                    ft.Text(
                                        f"{user.point:,}",
                                        theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                                    ),
                                    ft.Text(
                                        f"({user.score})",
                                        theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                                        color=ft.Colors.RED if user.score < 0 else ft.Colors.GREEN,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            ft.Row(
                                [
                                    self.result_table,
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            ft.Row(
                                [
                                    ft.Text(
                                        f"祝儀明細（上段：ロン、下段：ツモ）", theme_style=ft.TextThemeStyle.BODY_LARGE
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            ft.Row(
                                [
                                    self.bonus_table,
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            ft.Row(
                                [
                                    ft.Text(f"支払い明細", theme_style=ft.TextThemeStyle.BODY_LARGE),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            ft.Row(
                                [
                                    self.less_table,
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            ft.Row(
                                [
                                    ft.Text(f"支払い集計（振込先別）", theme_style=ft.TextThemeStyle.BODY_LARGE),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            ft.Row(
                                [
                                    self.less_summary_table,
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                        ]
                    ),
                    margin=10,
                    padding=10,
                )
            ]
        )

        return container
