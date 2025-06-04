<<<<<<< HEAD
version https://git-lfs.github.com/spec/v1
oid sha256:1eb9c16503906d8244c237499146d74a05ed59985fe982954ba5b496000c22fc
size 4997
=======

import os
from PIL import Image
import turtle
import time
import tkinter as tk
from tkinter import filedialog
from tqdm import tqdm
import json
import ctypes
import locale
import subprocess


def load_language(lang_code):
    lang_file = f"./locales/{lang_code}.json"
    fallback_file = "./locales/en.json"
    try:
        with open(lang_file, "r", encoding="utf-8") as file:
            translations = json.load(file)
        return translations
    except FileNotFoundError:
        print(f"Translation file for '{lang_code}' not found. Falling back to English.")
        with open(fallback_file, "r", encoding="utf-8") as file:
            translations = json.load(file)
        return translations


# Detect keyboard language
def get_keyboard_language():
    if os.name == "nt":
        user32 = ctypes.WinDLL('user32', use_last_error=True)
        keyboard_layout = user32.GetKeyboardLayout(0) & 0xFFFF
        lang_code = locale.windows_locale.get(keyboard_layout, "en-US")
        return lang_code
    else:
        try:
            result = subprocess.run(["setxkbmap", "-query"], capture_output=True, text=True, check=True)
            for line in result.stdout.splitlines():
                if line.startswith("layout:"):
                    layout = line.split(":")[1].strip()
                    if layout == "pt":
                        return "pt"
                    elif layout in {"us", "uk"}:
                        return "en"
            return "en"
        except Exception as e:
            print(f"Error detecting keyboard layout: {e}")
            return "en"


def detect_language():
    lang_code = get_keyboard_language()
    if lang_code.startswith("pt"): 
        return "pt"
    elif lang_code.startswith("en"):
        return "en"
    else:
        return "en"


user_language = detect_language()
translations = load_language(user_language)


def t(key):
    return translations.get(key, key)


def choose_image():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title=t("selec_image"),
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    if file_path:
        print(f"{t('selec')}: {file_path}")
    else:
        print(t("image_not_found"))
    return file_path


def main():
    clear = "cls" if os.name == "nt" else "clear"

    print(t("choice"))
    print(f"1 - {t('choice1')}")
    print(f"2 - {t('choice2')}")

    escolha = input(f"{t('choice3')}: \n > ")
    os.system(clear)
    if escolha == "1":
        n = input(f"{t('input_image')}: \n > ")
        image_path = f"./imagens/{n}.png"
        os.system(clear)
    elif escolha == "2":
        image_path = choose_image()
        if not image_path:
            print(t("image_not_found"))
            os.system(clear)
            return
    else:
        print(f"\n---{t('invalid_choice')}---")
        os.system(clear)
        return

    escala = float(input(f"{t('scale')}: \n > "))
    os.system(clear)
    opcao = input(f"{t('print_speed')} \n >")
    os.system(clear)

    for _ in range(3):
        for char in ["/", "-", "\\", "|"]:
            print(f"{t('analyze')}... {char}")
            time.sleep(0.5)
            os.system(clear)

    try:
        img = Image.open(image_path)
        img = img.convert("RGBA")
    except FileNotFoundError:
        print(f"{t('image_not_found_path')}: {image_path}")
        return

    l, a = img.size
    img = img.resize((int(l * escala), int(a * escala)), Image.NEAREST)
    l, a = img.size

    if opcao.lower() == "n":
        time.sleep(1)
        print(f"{t('size')}: {l}x{a}")
        time.sleep(2.5)
        turtle.shape("classic")
        turtle.speed(0)
        turtle.penup()
        desenhar(img, l, a, escala)

        print(f"\n{t('finish')}")
        turtle.done()

    elif opcao.lower() == "r":
        time.sleep(1)
        print(f"{t('size')}: {l}x{a}")
        time.sleep(2.5)
        turtle.speed(0)
        turtle.penup()
        turtle.tracer(0, 0)
        desenhar(img, l, a, escala)

        print(f"\n{t('finish')}")
        turtle.update()
        turtle.done()

    else:
        print(f"\n---{t('invalid_choice')}---")
        time.sleep(1.5)
        os.system(clear)
        main()


def desenhar(img, l, a, escala):
    total = l * a
    with tqdm(total=total, desc=t("progress"), unit=" px") as progress_bar:
        for x in range(0, l):
            for y in range(0, a):
                px = img.getpixel((x, y))
                color = '#%02x%02x%02x' % (px[0], px[1], px[2])
                pintar_pontos(escala, l, a, xOriginal=x, yOriginal=y, color=color)
                progress_bar.update(1)


def pintar_pontos(escala, l, a, color, xOriginal, yOriginal):
    x_scaled = xOriginal * escala
    y_scaled = yOriginal * escala

    turtle.setpos(x_scaled - l / 2, a / 2 - y_scaled)
    turtle.pendown()
    turtle.color(color)
    turtle.begin_fill()
    turtle.dot(escala * 2)
    turtle.penup()


if __name__ == "__main__":
    main()
>>>>>>> a0a29d2904f504e32bfc0521f0095bbdcf541173
