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
        tsumo_target_count = user.tsumo_target_count

        ron_chip_aka = user.aka_dora
        ron_chip_ura = user.ura_dora
        ron_chip_ippatsu = user.ippatsu
        ron_chip_allstar = user.allstar * user.allstar_chip_rate
        ron_chip_yiman = user.yiman * user.yiman_chip_rate
        ron_chip_tobi = user.tobi_ron

        tumo_chip_aka = user.aka_dora_tumo * tsumo_target_count
        tumo_chip_ura = user.ura_dora_tumo * tsumo_target_count
        tumo_chip_ippatsu = user.ippatsu_tumo * tsumo_target_count
        tumo_chip_allstar = user.allstar_tumo * user.allstar_chip_rate * tsumo_target_count
        tumo_chip_yiman = user.yiman_tumo * user.yiman_tumo_chip_rate * tsumo_target_count

        chip_total_aka = ron_chip_aka + tumo_chip_aka
        chip_total_ura = ron_chip_ura + tumo_chip_ura
        chip_total_ippatsu = ron_chip_ippatsu + tumo_chip_ippatsu
        chip_total_allstar = ron_chip_allstar + tumo_chip_allstar
        chip_total_yiman = ron_chip_yiman + tumo_chip_yiman
        tumo_chip_tobi = user.tobi_tumo
        chip_total_tobi = ron_chip_tobi + tumo_chip_tobi
        chip_total = (
            chip_total_aka
            + chip_total_ura
            + chip_total_ippatsu
            + chip_total_allstar
            + chip_total_yiman
            + chip_total_tobi
        )
        chip_total_yen = chip_total * user.chip_yen_unit

        self.bonus_table = ft.DataTable(
            heading_row_color=ft.Colors.BLACK12,
            vertical_lines=ft.BorderSide(1, "black"),
            horizontal_lines=ft.BorderSide(1, "black"),
            border=ft.border.all(2, "black"),
            columns=[
                ft.DataColumn(ft.Text("種類／内容")),
                ft.DataColumn(ft.Text("ロン")),
                ft.DataColumn(ft.Text("ツモ")),
                ft.DataColumn(ft.Text("チップ枚数")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("赤ドラ")),
                        ft.DataCell(ft.Text(f"{user.aka_dora}回")),
                        ft.DataCell(ft.Text(f"{user.aka_dora_tumo}回")),
                        ft.DataCell(ft.Text(f"{chip_total_aka}枚")),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("裏ドラ")),
                        ft.DataCell(ft.Text(f"{user.ura_dora}回")),
                        ft.DataCell(ft.Text(f"{user.ura_dora_tumo}回")),
                        ft.DataCell(ft.Text(f"{chip_total_ura}枚")),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("一発")),
                        ft.DataCell(ft.Text(f"{user.ippatsu}回")),
                        ft.DataCell(ft.Text(f"{user.ippatsu_tumo}回")),
                        ft.DataCell(ft.Text(f"{chip_total_ippatsu}枚")),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("オールスター")),
                        ft.DataCell(ft.Text(f"{user.allstar}回")),
                        ft.DataCell(ft.Text(f"{user.allstar_tumo}回")),
                        ft.DataCell(ft.Text(f"{chip_total_allstar}枚")),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("役満")),
                        ft.DataCell(ft.Text(f"{user.yiman}回")),
                        ft.DataCell(ft.Text(f"{user.yiman_tumo}回")),
                        ft.DataCell(ft.Text(f"{chip_total_yiman}枚")),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("飛ばし")),
                        ft.DataCell(ft.Text(f"{user.tobi_ron}回")),
                        ft.DataCell(ft.Text(f"{user.tobi_tumo}回")),
                        ft.DataCell(ft.Text(f"{chip_total_tobi}枚")),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("合計チップ枚数")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text(f"{chip_total}枚")),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("合計金額")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text(f"{chip_total_yen:,}円")),
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
                        ft.DataCell(ft.Text("0枚")),
                        ft.DataCell(ft.Text("0円")),
                    ]
                )
            )
        else:
            for hule in user.transaction:
                chip_cnt = int(hule.yen / user.chip_yen_unit) if user.chip_yen_unit > 0 else 0
                less_rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(hule.to)),
                            ft.DataCell(
                                ft.Text(f"{hule.bonus.value}(ツモ)" if hule.zimo else f"{hule.bonus.value}(ロン)")
                            ),
                            ft.DataCell(ft.Text(f"{chip_cnt}枚")),
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
                ft.DataColumn(ft.Text("チップ枚数")),
                ft.DataColumn(ft.Text("金額")),
            ],
            rows=less_rows,
        )

        less_summary_rows = []
        if len(user.opponent_summaries) <= 0:
            less_summary_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("なし")),
                        ft.DataCell(ft.Text("0円")),
                        ft.DataCell(ft.Text("0枚")),
                        ft.DataCell(ft.Text("0枚")),
                        ft.DataCell(ft.Text("0円")),
                    ]
                )
            )
        else:
            for summary in user.opponent_summaries:
                less_summary_rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(summary.to)),
                            ft.DataCell(
                                ft.Text(
                                    f"{summary.score_yen:+,}円",
                                    color=ft.Colors.RED if summary.score_yen < 0 else ft.Colors.GREEN_900,
                                )
                            ),
                            ft.DataCell(ft.Text(f"{summary.receive_chip:,}枚")),
                            ft.DataCell(ft.Text(f"{summary.pay_chip:,}枚")),
                            ft.DataCell(
                                ft.Text(
                                    f"{summary.total_yen:+,}円",
                                    color=ft.Colors.RED if summary.total_yen < 0 else ft.Colors.GREEN_900,
                                )
                            ),
                        ],
                    )
                )

        self.less_summary_table = ft.DataTable(
            heading_row_color=ft.Colors.BLACK12,
            vertical_lines=ft.BorderSide(1, "black"),
            horizontal_lines=ft.BorderSide(1, "black"),
            border=ft.border.all(2, "black"),
            columns=[
                ft.DataColumn(ft.Text("相手")),
                ft.DataColumn(ft.Text("得点精算")),
                ft.DataColumn(ft.Text("受け取りチップ")),
                ft.DataColumn(ft.Text("支払いチップ")),
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
                                        f"祝儀明細", theme_style=ft.TextThemeStyle.BODY_LARGE
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
