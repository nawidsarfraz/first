import tkinter as tk
import getpass
import socket
import sys
import argparse
import os

class EmulatorApp:
    def __init__(self, root, vfs_path, script_path):
        # Сохраняем параметры
        self.vfs_path = vfs_path
        self.script_path = script_path

        # Получаем username и hostname
        username = getpass.getuser()
        hostname = socket.gethostname()
        root.title(f"Эмулятор - [{username}@{hostname}]")

        # Поле вывода
        self.text = tk.Text(root, height=20, width=80, state="disabled", bg="black", fg="white")
        self.text.pack(padx=10, pady=10)

        # Поле ввода
        self.entry = tk.Entry(root, width=80, bg="black", fg="white", insertbackground="white")
        self.entry.pack(padx=10, pady=5)
        self.entry.bind("<Return>", self.process_command)

        self.write("Прототип эмулятора готов. Введите команду (ls, cd, conf-dump, exit).\n")

        # Отладочный вывод параметров
        self.write("Отладочный вывод параметров:")
        self.write(f"  VFS path: {self.vfs_path}")
        self.write(f"  Script path: {self.script_path}\n")

        # Если есть стартовый скрипт — выполняем
        if self.script_path and os.path.isfile(self.script_path):
            self.run_script(self.script_path)

    def write(self, message):
        """Вывод текста в окно"""
        self.text.config(state="normal")
        self.text.insert(tk.END, message + "\n")
        self.text.see(tk.END)
        self.text.config(state="disabled")

    def process_command(self, event=None, command_line=None):
        """Обработка команды из GUI или скрипта"""
        if command_line is None:
            command_line = self.entry.get().strip()
            self.entry.delete(0, tk.END)

        if not command_line:
            return

        # Парсим команду и аргументы
        parts = command_line.split()
        command = parts[0]
        args = parts[1:]

        self.write(f"> {command_line}")

        # Заглушки для команд
        if command == "ls":
            self.write(f"Выполнена команда: ls, аргументы: {args}")
        elif command == "cd":
            self.write(f"Выполнена команда: cd, аргументы: {args}")
        elif command == "conf-dump":
            self.write("Конфигурация эмулятора:")
            self.write(f"  VFS path = {self.vfs_path}")
            self.write(f"  Script path = {self.script_path}")
        elif command == "exit":
            self.write("Выход из эмулятора...")
            sys.exit(0)
        else:
            self.write(f"Неизвестная команда: {command}")

    def run_script(self, script_file):
        """Выполнение команд из скрипта"""
        self.write(f"Выполнение стартового скрипта: {script_file}")
        try:
            with open(script_file, "r", encoding="utf-8") as f:
                for line in f:
                    cmd = line.strip()
                    if not cmd or cmd.startswith("#"):  # пропуск пустых и закомментированных строк
                        continue
                    try:
                        self.process_command(command_line=cmd)
                    except Exception as e:
                        self.write(f"[Ошибка выполнения команды '{cmd}']: {e}")
        except Exception as e:
            self.write(f"Не удалось открыть скрипт: {e}")


if __name__ == "__main__":
    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(description="Эмулятор файловой системы")
    parser.add_argument("--vfs", required=True, help="Путь к физическому расположению VFS")
    parser.add_argument("--script", required=False, help="Путь к стартовому скрипту")
    args = parser.parse_args()

    root = tk.Tk()
    app = EmulatorApp(root, args.vfs, args.script)
    root.mainloop()
