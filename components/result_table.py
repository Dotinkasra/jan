import flet as ft

from module.data import User, Hule, Bonus

class ResultTablePage(ft.UserControl):

    def __init__(self, user: User):
        super().__init__()
        self.user = user

    def did_mount(self):
        self.page.update()

    def build(self):
        user = self.user
        self.bonus_table = ft.DataTable(
            heading_row_color=ft.Colors.BLACK12,
            vertical_lines=ft.BorderSide(1, "black"),
            horizontal_lines=ft.BorderSide(1, "black"),
            border=ft.border.all(2, "black"),
            columns=[
                ft.DataColumn(ft.Text("赤ドラ")),
                ft.DataColumn(ft.Text("裏ドラ")),
                ft.DataColumn(ft.Text("一発")),
                ft.DataColumn(ft.Text("オールスター")),
                ft.DataColumn(ft.Text("役満")),
                ft.DataColumn(ft.Text("飛ばし")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{user.aka_dora}（{user.aka_dora_tumo}）回")),
                        ft.DataCell(ft.Text(f"{user.ura_dora}（{user.ura_dora_tumo}）回")),
                        ft.DataCell(ft.Text(f"{user.ippatsu}（{user.ippatsu_tumo}）回")),
                        ft.DataCell(ft.Text(f"{user.allstar}（{user.allstar_tumo}）回")),
                        ft.DataCell(ft.Text(f"{user.yiman}（{user.yiman}）回")), 
                        ft.DataCell(ft.Text(f"{user.tobi}回")),
                    ],
                ),
            ],
        )

        less_rows = []
        less_total = 0
        for hule in user.transaction:
            less_rows.append(
                ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(hule.to)),
                            ft.DataCell(ft.Text(f"{hule.bonus.value}(ツモ)" if hule.zimo else f"{hule.bonus.value}(ロン)")),
                            ft.DataCell(ft.Text(f"{hule.yen}円")),
                        ],
                    )
            )
            less_total += hule.yen

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
            rows=less_rows
        )
        
        bonus_total = user.bonus_yen - less_total
        result = user.score_yen + bonus_total

        self.result_table = ft.DataTable(
            heading_row_color=ft.Colors.BLACK12,
            vertical_lines=ft.BorderSide(1, "black"),
            horizontal_lines=ft.BorderSide(1, "black"),
            border=ft.border.all(2, "black"),
            columns=[
                ft.DataColumn(ft.Text("収入")),
                ft.DataColumn(ft.Text("支出")),
                ft.DataColumn(ft.Text("結果")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{user.score_yen}円")),
                        ft.DataCell(ft.Text(f"{bonus_total}円")),
                        ft.DataCell(ft.Text(f"{result}円", color = ft.Colors.RED if result < 0 else ft.Colors.GREEN_900 )),
                    ],
                ),
            ],
        )
#        return [bonus, user_less_table, user_result_table]
        container = ft.Column([
            ft.Container(
                ft.Column([
                    ft.Row([
                        ft.Text(f"【{user.nickname}】", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                        ft.Text(user.point, theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,),
                        ft.Text(f"({user.score})", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, color = ft.Colors.RED if user.score < 0 else ft.Colors.GREEN)
                        ], alignment=ft.MainAxisAlignment.START
                        
                    ),
                    ft.Row([
                        self.result_table,
                    ], alignment=ft.MainAxisAlignment.START),
                    ft.Row([
                        self.bonus_table,
                    ], alignment=ft.MainAxisAlignment.START),
                    ft.Row([
                        self.less_table,
                    ], alignment=ft.MainAxisAlignment.START),
                    
                    
                ]),
                margin=10,
                padding=10,
            )
        ])
        
        return container