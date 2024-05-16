import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod
import logging

logging.basicConfig(filename='calculator.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class Calculating(ABC):
    @abstractmethod
    def sum(self, arg):
        pass

    @abstractmethod
    def sub(self, arg):
        pass

    @abstractmethod
    def multi(self, arg):
        pass

    @abstractmethod
    def div(self, arg):
        pass

    @abstractmethod
    def get_result(self):
        pass

class Calculator(Calculating):
    def __init__(self, primary_arg):
        self.primary_arg = primary_arg
        logging.info(f'Начальный аргумент: {primary_arg}')

    def sum(self, arg):
        self.primary_arg += arg
        logging.info(f'Сложение с {arg}. Текущий результат: {self.primary_arg}')
        return self

    def sub(self, arg):
        self.primary_arg -= arg
        logging.info(f'Вычитание на {arg}. Текущий результат: {self.primary_arg}')
        return self

    def multi(self, arg):
        self.primary_arg *= arg
        logging.info(f'Умножение на {arg}. Текущий результат: {self.primary_arg}')
        return self

    def div(self, arg):
        self.primary_arg /= arg
        logging.info(f'Деление на {arg}. Текущий результат: {self.primary_arg}')
        return self

    def get_result(self):
        logging.info(f'Получен результат: {self.primary_arg}')
        return self.primary_arg

class CalculatingFactory:
    @staticmethod
    def create(primary_arg):
        return Calculator(primary_arg)

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор")
        self.primary_arg = 0
        self.current_operation = None
        self.create_widgets()

    # def validate_input(self, text):
    #     allowed_chars = "0123456789+-*/"  
    #     if text in allowed_chars:
    #         return True
    #     else:
    #         return False

    def create_widgets(self):
        # Виджет для отображения ввода и результата        
        self.entry = ttk.Entry(self.root, font=('Helvetica', 20), justify='right')#, validate='key', validatecommand=(self.root.register(self.validate_input), '%S'))
        self.entry.grid(row=0, column=0, columnspan=4, sticky='nsew')
        
        # Создание кнопок для цифр и операций
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('C', 4, 1), ('=', 4, 2), ('+', 4, 3)
        ]

        for (text, row, col) in buttons:
            btn = ttk.Button(self.root, text=text, command=lambda t=text: self.on_button_click(t))
            btn.grid(row=row, column=col, sticky='nsew')
            self.root.grid_rowconfigure(row, weight=1)
            self.root.grid_columnconfigure(col, weight=1)

    def on_button_click(self, button_text):
        if button_text.isdigit():
            self.entry.insert(tk.END, button_text)
        elif button_text == 'C':
            self.entry.delete(0, tk.END)
        elif button_text in ['+', '-', '*', '/']:
            self.primary_arg = float(self.entry.get())
            self.current_operation = button_text
            self.entry.delete(0, tk.END)
        elif button_text == '=':
            second_arg = float(self.entry.get())
            result = self.perform_operation(self.primary_arg, second_arg, self.current_operation)
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(result))

    def perform_operation(self, arg1, arg2, operation):
        calculating_factory = CalculatingFactory()
        calculator = calculating_factory.create(arg1)

        if operation == '+':
            return calculator.sum(arg2).get_result()
        elif operation == '-':
            return calculator.sub(arg2).get_result()
        elif operation == '*':
            return calculator.multi(arg2).get_result()
        elif operation == '/':
            return calculator.div(arg2).get_result()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.resizable(False, False)
    root.mainloop()