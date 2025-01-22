from module.jan import Jan
from module.data import User, Bonus, Hule

from components.result_table import ResultTablePage
import flet as ft

def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.title = "ご祝儀計算キット"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT

    def open_repo(e):
        page.launch_url('https://github.com/Dotinkasra/jan')

    def pick_files_result(e: ft.FilePickerResultEvent):
        parameta["paifu"] = e.files[0].path

    def home_view():
        def pick_files_result_wrapper(e: ft.FilePickerResultEvent):
            pick_files_result(e)
            paifu_path.value = e.files[0].name
            paifu_path.update()

        def btn():
            print(parameta['paifu'])
            parameta["samma"] = samma_radiobutton.value
            if not parameta['paifu'] == '':
                page.go("/result")

        pick_files_dialog = ft.FilePicker(on_result=pick_files_result_wrapper)
        page.overlay.append(pick_files_dialog)
        paifu_path = ft.Text()

        do_btn = ft.ElevatedButton(
            "実行する",
            on_click=lambda x: btn()
        )

        samma_radiobutton = ft.Switch(label="三麻", value=False)

        home = ft.View("/home", [
            ft.AppBar(
                leading=ft.Icon(ft.Icons.PALETTE),
                leading_width=40,
                title=ft.Text("ご祝儀計算"),
                center_title=False,
                bgcolor=ft.Colors.BLUE,
                actions=[ft.IconButton(icon = ft.Icons.CODE, on_click=open_repo)]
            ),
            ft.Column([
                ft.Container(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "ファイルを選択",
                                icon = ft.Icons.UPLOAD_FILE,
                                on_click=lambda _: pick_files_dialog.pick_files(
                                    allow_multiple=False,
                                    allowed_extensions=['json', 'txt']
                                ),
                            ),do_btn,
                        ]),
                        ft.Row([
                            paifu_path,
                        ])                              
                    ]),
                ),
            ]),
        ])

        return home
    
    def create_table_view():
        try:
            jan = Jan()
            users = jan.load_paifu_jansoul(parameta['paifu'], parameta['samma'])
        except Exception as e:
            print(e)
            return None
        
        table_view = ft.View("/結果", [
            ft.AppBar(
                title=ft.Text("精算表"),
                bgcolor=ft.Colors.BLUE,
                actions=[ft.IconButton(icon = ft.Icons.CODE, on_click=open_repo)]
            ),
        ])
        table_view.scroll =ft.ScrollMode.ALWAYS
        table_view.controls.append(
            ft.ElevatedButton("牌譜読み込みに戻る", on_click=lambda _: page.go("/home"))
        )
        for user in users:
            table_view.controls.append(ResultTablePage(user=user))
        return table_view

    def route_change(handler):
        troute = ft.TemplateRoute(handler.route)
        
        page.views.clear()
        if troute.match("/home"):
            page.views.append(home_view())
        elif troute.match("/result"):
            table_view = create_table_view()
            if table_view is not None:
                page.views.append(create_table_view())
            else:
                page.go("/home")
        page.update()

    paifu_path = ""
    uma_1 = 10
    uma_2 = 20
    oka_1 = 25000
    oka_2 = 30000
    samma = False
    parameta = {
        "paifu": paifu_path,
        "uma_1": uma_1,
        "uma_2": uma_2,
        "oka_1": oka_1,
        "oka_2": oka_2,
        "samma": samma
    }
    print(samma)
    page.on_route_change = route_change
    page.views.clear()

    page.go("/home")

if __name__ == "__main__":
    ft.app(target=main)
