import os
import sys
import subprocess  # Идеально работает с русскими буквами в путях
import tkinter as tk
from tkinter import messagebox


# Функция проверки пароля
def check_password():
    entered_password = password_entry.get()
    CORRECT_PASSWORD = "StartGame"  # Ваш секретный пароль

    if entered_password == CORRECT_PASSWORD:
        root.destroy()  # Закрываем окно с паролем

        current_dir = os.path.dirname(os.path.abspath(__file__))
        game_file_name = "game_space.py"
        full_path = os.path.join(current_dir, game_file_name)

        # 🌟 ГЛАВНЫЙ ФИКС: Перезапускаем игру через subprocess без багов кодировки
        subprocess.Popen([sys.executable, full_path])
        sys.exit()
    else:
        messagebox.showerror("Ошибка", "❌ НЕВЕРНЫЙ ПАРОЛЬ!\nДоступ к Space Attack заблокирован.")
        password_entry.delete(0, tk.END)  # Очищаем поле ввода


# Создаем красивое графическое окно
root = tk.Tk()
root.title("Space Attack - Авторизация")
root.geometry("400x210")
root.configure(bg="#1e1e2e")
root.resizable(False, False)

# Текст заголовка
title_label = tk.Label(root, text="🛸 ВЕРИФИКАЦИЯ ПИЛОТА", font=("Arial", 14, "bold"), fg="#00ffcc", bg="#1e1e2e")
title_label.pack(pady=15)

# Поле ввода пароля
password_entry = tk.Entry(root, font=("Arial", 14), show="*", justify="center", bd=2, relief="flat")
password_entry.pack(pady=2, ipady=5, ipadx=10)
password_entry.focus()

# Маааленькая надпись Password...
password_hint_label = tk.Label(root, text="Password...", font=("Arial", 9, "italic"), fg="#626880", bg="#1e1e2e")
password_hint_label.pack(pady=2)

# Кнопка «Войти»
login_button = tk.Button(root, text="СТАРТ", font=("Arial", 12, "bold"), fg="#1e1e2e", bg="#00ffcc",
                         activebackground="#00cc99", relief="flat", width=15, command=check_password)
login_button.pack(pady=12)

# Позволяет отправлять пароль по нажатию клавиши Enter
root.bind('<Return>', lambda event: check_password())

root.mainloop()