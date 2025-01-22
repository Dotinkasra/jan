from module.jan import Jan
from module.data import User, Bonus, Hule

from components.result_table import ResultTablePage
import flet as ft

def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.title = "ご祝儀計算キット"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
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
    )

    jan = Jan()
    users = jan.load_paifu_jansoul("./test1.json")
    
    for user in users:
        page.add(ResultTablePage(user=user))
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
