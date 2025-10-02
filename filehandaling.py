import tkinter as tk
import getpass
import socket
import sys

class EmulatorApp:
    def __init__(self, root):
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

        self.write("Прототип эмулятора готов. Введите команду (ls, cd, exit).\n")

    def write(self, message):
        """Вывод текста в окно"""
        self.text.config(state="normal")
        self.text.insert(tk.END, message + "\n")
        self.text.see(tk.END)
        self.text.config(state="disabled")

    def process_command(self, event):
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
        elif command == "exit":
            self.write("Выход из эмулятора...")
            sys.exit(0)
        else:
            self.write(f"Неизвестная команда: {command}")


if __name__ == "__main__":
    root = tk.Tk()
    app = EmulatorApp(root)
    root.mainloop()
