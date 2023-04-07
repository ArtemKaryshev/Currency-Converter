import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox
import requests
from currency_converter import CurrencyConverter
from PyQt5.QtCore import Qt


# работа с парсингом сайта openexchangerates.org
class ExchangeRates:
    def __init__(self):
        self.api_url = 'https://openexchangerates.org/api/latest.json'
        self.app_id = 'a7bc878c7b3d48dcbdf4449d23789f91'
        self.exchange_rates = {}

    # обновление курса валют
    def update_exchange_rates(self):
        response = requests.get(f'{self.api_url}?app_id={self.app_id}')
        if response.status_code == 200:
            exchange_rates = response.json().get('rates', {})
            self.exchange_rates.update(exchange_rates)

    # получение списка валют и их значения
    def get_exchange_rate(self, from_currency, to_currency):
        if not self.exchange_rates:
            self.update_exchange_rates()
        from_rate = self.exchange_rates.get(from_currency)
        to_rate = self.exchange_rates.get(to_currency)
        if from_rate and to_rate:
            return round(to_rate / from_rate, 3)
        return None


exchange_rates = ExchangeRates()


# создание окна приложения
class Convert(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setFixedSize(420, 205)
        self.setStyleSheet('background-color: rgb(76, 252, 220)')

        self.setWindowIcon(QtGui.QIcon('./photo.png'))

        self.setWindowTitle('Конвертер')
        self.main_layout = QVBoxLayout(self)

        # Модуль комбобоксов
        self.combo_box_layout = QHBoxLayout()
        self.c = CurrencyConverter()

        self.currencies = sorted(self.c.currencies)
        self.combo_box_input = QComboBox()
        self.combo_box_input.addItems(self.currencies)
        self.combo_box_input.setCurrentText('USD')
        self.replace_btn = QPushButton(self)
        self.replace_btn.setIcon(QtGui.QIcon('./replace.png'))
        self.replace_btn.clicked.connect(self.replace_currencies)
        self.replace_btn.setFixedSize(42, 32)

        self.combo_box_output = QComboBox()
        self.combo_box_output.addItems(self.currencies)
        self.combo_box_output.setCurrentText('RUB')
        self.combo_box_input.setFixedSize(169, 32)
        self.combo_box_output.setFixedSize(169, 32)
        self.combo_box_input.setStyleSheet('background-color: rgb(186, 217, 255);'
                                           'board: 10px;'
                                           'border: 2px solid #094065;')
        self.combo_box_output.setStyleSheet('background-color: rgb(186, 217, 255);'
                                            'board: 10px;'
                                            'border: 2px solid #094065;')
        self.replace_btn.setStyleSheet('background-color: rgb(186, 217, 255);'
                                       'board: 10px;'
                                       'border: 2.3px solid #094065;')
        self.combo_box_layout.addWidget(self.combo_box_input)
        self.combo_box_layout.addWidget(self.replace_btn)
        self.combo_box_layout.addWidget(self.combo_box_output)
        self.main_layout.addLayout(self.combo_box_layout)
        # Конец модуля комбобоксов

        # Модуль ввода, вывода
        self.line_layout = QVBoxLayout()

        self.input = QLineEdit()
        self.input.setAlignment(Qt.AlignCenter)
        self.input.setFixedSize(394, 30)
        self.input.setPlaceholderText('Введите сумму')
        self.input.setStyleSheet('color: black;'
                                 'background-color: rgb(0, 255, 127);'
                                 'board: 10px;'
                                 'border: 2px solid #094065;')
        self.input.textChanged.connect(self.line_edit_changed)
        self.combo_box_input.currentTextChanged.connect(self.line_edit_changed)
        self.combo_box_output.currentTextChanged.connect(self.line_edit_changed)
        self.output = QLabel('Результат')
        self.output.setFixedSize(394, 30)
        self.output.setStyleSheet('color: black;'
                                  'background-color: rgb(0, 255, 127);'
                                  'board: 10px;'
                                  'border: 2px solid #094065')
        self.output.setAlignment(Qt.AlignCenter)
        self.last_layout = QHBoxLayout
        self.line_layout.addWidget(self.input)
        self.line_layout.addWidget(self.output)
        self.main_layout.addLayout(self.line_layout)
        # конец модуля ввода, вывода

        # создание дополнительных кнопок
        self.reset_button = QPushButton('Сброс', self)
        self.reset_button.setStyleSheet('background-color: rgb(186, 217, 255);'
                                        'board: 10px;'
                                        'border: 2px solid #094065')
        self.reset_button.setFixedSize(394, 30)
        self.reset_button.clicked.connect(self.reset_btn)

        self.exit_btn = QPushButton('Выйти', self)
        self.exit_btn.setStyleSheet('background-color: rgb(186, 217, 255);'
                                    'board: 10px;'
                                    'border: 2px solid #094065')
        self.exit_btn.setFixedSize(394, 30)
        self.exit_btn.clicked.connect(self.close)

        self.main_layout.addWidget(self.reset_button)
        self.main_layout.addWidget(self.exit_btn)
        self.show()

    # функция для сброса данных по умолчанию
    def reset_btn(self):
        self.combo_box_input.setCurrentText('USD')
        self.combo_box_output.setCurrentText('RUB')
        self.input.clear()
        self.output.setText('Результат')

    # функция для смены валют между собой
    def replace_currencies(self):
        current_input = self.combo_box_input.currentText()
        current_output = self.combo_box_output.currentText()

        self.combo_box_input.setCurrentText(current_output)
        self.combo_box_output.setCurrentText(current_input)

        self.line_edit_changed()

    # конвертация и вывод в строку output
    def line_edit_changed(self):
        if self.combo_box_input.currentText() == self.combo_box_output.currentText():
            self.output.setText(self.input.text())
        else:
            from_currency = self.combo_box_input.currentText()
            to_currency = self.combo_box_output.currentText()
            exchange_rate = exchange_rates.get_exchange_rate(from_currency, to_currency)
            if exchange_rate:
                try:
                    val_input = self.input.text()
                    val_input = round(float(val_input) * exchange_rate, 2)
                    self.output.setText(str("{:.2f}".format(val_input)))
                except ValueError:
                    self.output.setText('Введите число')
                if len(str(self.input.text())) > 55:
                    self.output.setText('Вы ввели максимальное количество символов')

            else:
                self.output.setText('Не удалось получить курс обмена валюты')


# запуск программы
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Convert()
    sys.exit(app.exec())
