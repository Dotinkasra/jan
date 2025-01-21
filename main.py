from jantama import User, Hule, Bonus, Jan

import flet as ft

class UserTable():
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

    def get_user_tables(self, user: User) -> list[ft.DataTable]:
        bonus = ft.DataTable(
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
                        ft.DataCell(ft.Text(user.aka_dora)),
                        ft.DataCell(ft.Text(user.ura_dora)),
                        ft.DataCell(ft.Text(user.ippatsu)),
                        ft.DataCell(ft.Text(user.allstar)),
                        ft.DataCell(ft.Text(user.yiman)),
                        ft.DataCell(ft.Text(user.tobi)),
                    ],
                ),
            ],
        )
        less_rows = []
        for hule in user.transaction:
            less_rows.append(
                ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(hule.to)),
                            ft.DataCell(ft.Text(f"{hule.bonus.value}(ツモ)" if hule.zimo else f"{hule.bonus.value}(ロン)")),
                            ft.DataCell(ft.Text(f"{hule.point}円")),
                        ],
                    )
            )

        user_less_table = ft.DataTable(
            border=ft.border.all(2, "black"),
            columns=[
                ft.DataColumn(ft.Text("振込先")),
                ft.DataColumn(ft.Text("内容")),
                ft.DataColumn(ft.Text("金額")),
            ],
            rows=less_rows
        )
        
        user_result_table = ft.DataTable(
            border=ft.border.all(2, "black"),
            columns=[
                ft.DataColumn(ft.Text("収入")),
                ft.DataColumn(ft.Text("支出")),
                ft.DataColumn(ft.Text("結果")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(user.mychip()*500)),
                        ft.DataCell(ft.Text(user.myless())),
                        ft.DataCell(ft.Text(user.mychip()*500 - user.myless())),
                    ],
                ),
            ],
        )
        return [bonus, user_less_table, user_result_table]

    def main(self):


        jan = Jan("./test.json")
        jan.calc_bonus()
        for user in jan.users:
            self.page.add(ft.Container(content=ft.Text(user.nickname)))
            self.page.add(ft.Column(controls=self.get_user_tables(user), expand=True))

#        page.add(user_table)
def main(page: ft.Page):
    usertable = UserTable(page)
    usertable.main()

    page.title = "JanTama"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.ALWAYS
    
    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()

    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.PALETTE),
        leading_width=40,
        title=ft.Text("ご祝儀計算"),
        center_title=False,
        bgcolor=ft.Colors.SURFACE_VARIANT,
        actions=[
            ft.Icon(ft.Icons.WB_SUNNY_OUTLINED),
            ft.Icon(ft.Icons.FILTER_3),
            ft.IconButton(
                items=[
                    ft.PopupMenuItem(text="Item 1"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        text="Checked item", checked=False, on_click=check_item_clicked
                    ),
                ]
            ),
        ],
    )

    page.update()

if __name__ == "__main__":
    ft.app(target=main)
