from tkinter import TOP, messagebox
import tkinterdnd2
import customtkinter as ctk
import converter
from converter import constants, exceptions
from PIL import Image


# customtikinter와 tkinter를 함께 사용할 수 있게 해주는 코드
class Tk(ctk.CTk, tkinterdnd2.TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = tkinterdnd2.TkinterDnD._require(self)


img = ctk.CTkImage(
    light_image=Image.open("resources/plus.png"),
    dark_image=Image.open("resources/plus.png"),
    size=(100, 100),
)

# 전역에서 접근하여 버튼이나 레이블이 변경될 때 destory()와 clear()를 이용하여 리셋
radioBtn: list[ctk.CTkRadioButton] = []
labels: list[ctk.CTkLabel] = []


# 화면을 그리는 코드
def get_ui() -> None:
    global pathLabel
    global root
    global choice
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app_width = 600
    app_height = 500
    root = Tk()
    choice = ctk.StringVar()
    screen_width = root.winfo_screenwidth()
    center_width = int((screen_width / 2) - (app_width / 2))
    screen_height = root.winfo_screenheight()
    center_heigth = int((screen_height / 2) - (app_height / 2))
    root.geometry(f"{app_width}x{app_height}+{center_width}+{center_heigth}")
    root.title("파일 변환기")

    dndBG = ctk.CTkFrame(root, fg_color="#757575", corner_radius=10)
    dndBG.pack(side=TOP, padx=120, pady=(50, 30), fill="both")
    empty = ctk.CTkLabel(dndBG, text="")
    empty.pack()
    plusImg = ctk.CTkLabel(dndBG, image=img, text="")

    pathLabel = ctk.CTkLabel(
        root, text="변환할 파일(들)을 끌어다 놓으세요.", text_color="white"
    )
    plusImg.pack(expand=True)
    empty = ctk.CTkLabel(dndBG, text="")
    empty.pack()
    pathLabel.pack(side=TOP)
    dndBG.drop_target_register(tkinterdnd2.DND_ALL)
    dndBG.dnd_bind("<<Drop>>", get_path)

    root.mainloop()


def convert_choice():
    if choice.get() in ["xls", "json", "csv", "xlsx"]:
        for i in paths:
            converter.convert_docs(i, choice.get())
    elif choice.get() in ["png", "avif", "jpg", "jpeg", "webp"]:
        for i in paths:
            converter.convert_image(i, choice.get())


def make_radiobtn(available: list[str]):
    for btn in radioBtn:
        btn.destroy()
    radioBtn.clear()
    for option in available:
        radio = ctk.CTkRadioButton(root, text=option, variable=choice, value=option)
        radio.pack(
            side="left",
            fill="x",
            padx=(20, 0),
            anchor="center",
        )
        radioBtn.append(radio)
    btn = ctk.CTkButton(root, text="변환", command=convert_choice)
    btn.pack(side="bottom", padx=20, expand=True, fill="x")
    radioBtn.append(btn)


def get_path(event: tkinterdnd2.TkinterDnD.DnDEvent):
    global paths
    for i in labels:
        i.destroy()
    labels.clear()
    target = event.data
    paths = converter.path_devider(target.lower())
    result = set()
    for path in paths:
        result.add(converter.type_checker(path))
    if len(result) > 1:
        messagebox.showwarning("알림", "동일한 확장자명만 변환이 가능합니다.")
        raise exceptions.EXTENSION_NOT_SAME
    pathLabel.destroy()
    for i in range(len(paths)):
        if i > 4:
            label = ctk.CTkLabel(root, text=f"{len(paths)-5} more ...")
            label.pack()
            labels.append(label)
            break
        label = ctk.CTkLabel(root, text=paths[i])
        label.pack()
        labels.append(label)
    make_radiobtn(constants.type_map[result.pop()])


def main_program():
    while True:
        try:
            get_ui()
        except exceptions.EXTENSION_NOT_SAME | exceptions.UNKNOWN_ERROR:
            root.quit()
            pass
        else:
            break


main_program()
