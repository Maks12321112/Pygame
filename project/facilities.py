import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QGridLayout, QMainWindow, QScrollArea, QWidget, QVBoxLayout, QButtonGroup, \
    QLabel, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os
from oun_window import Ui_MainWindow
import shutil
from functools import partial
from Register import Ui_MainWindow1
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QSpinBox, QTextEdit, QPushButton, QLabel, QMessageBox
from window_games import Ui_MainWindow3
import sqlite3

conn = sqlite3.connect('user_base.db')
cursor = conn.cursor()


def check_password(password):
    if len(password) <= 8:
        marker_glav1 = False
    else:
        marker_glav1 = True

    if not any(char.isupper() for char in password) or not any(char.islower() for char in password):
        marker_glav2 = False
    else:
        marker_glav2 = True

    if not any(char.isdigit() for char in password):
        marker_glav3 = False
    else:
        marker_glav3 = True

    keyboard_layouts = [["q", "w", "e"], ["a", "s", "d"],
                        ["z", "x", "c"], ["й", "ц", "у"], ["ф", "ы", "в", "а"], ["я", "с", "м", "и"],
                        ["ю", "б", "о", "л"]]
    for i in range(len(password) - 2):
        if [char.lower() for char in password[i:i + 3]] in keyboard_layouts:
            marker_glav4 = False
        else:
            marker_glav4 = True

    if marker_glav3 and marker_glav2 and marker_glav1 and marker_glav4:

        return True
    else:
        return False


k = 0


class ReviewWindow(QDialog):
    def __init__(self, game_id, parent=None):
        super().__init__(parent)
        self.setGeometry(100, 100, 400, 300)
        self.game_id = game_id

        self.layout = QVBoxLayout()

        self.rating_label = QLabel("Выберите оценку (1-5):")
        self.layout.addWidget(self.rating_label)

        self.rating_input = QSpinBox(self)
        self.rating_input.setRange(1, 5)
        self.layout.addWidget(self.rating_input)

        self.review_input = QTextEdit(self)
        self.review_input.setPlaceholderText("Введите ваш отзыв...")
        self.layout.addWidget(self.review_input)

        self.button = QPushButton("Отправить отзыв", self)
        self.submit_button.clicked.connect(self.submit_review)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)
        self.setWindowTitle("Отзыв о игре")

    def submit_review(self):
        rating = self.rating_input.value()
        text = self.review_input.toPlainText()

        if text:

            cursor.execute('''INSERT INTO reviews (game_id, review, rating) VALUES (?, ?, ?)''',
                           (self.game_id, text, rating))
            conn.commit()

            QMessageBox.information(self, "Успех", "Ваш отзыв был отправлен.")
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите ваш отзыв.")

    def closeEvent(self, event):
        print("Окно отзыва было закрыто.")
        event.accept()


class Description(QMainWindow, Ui_MainWindow3):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.main_layout = QVBoxLayout()
        self.contentWidget = QWidget()
        self.contentWidget.setLayout(self.main_layout)
        self.setupUi(self)
        self.description = self.textBrowser
        self.load_window("C:\\Users\\User\\PycharmProjects\\pythonProject2\\game_images")
        self.review_button = QPushButton("Оставить отзыв", self)
        self.review_button.resize(100, 50)
        self.review_button.move(550, 420)
        self.review_button.clicked.connect(self.open_review)
        self.scrollArea.setWidget(self.contentWidget)
        self.pushButton121.clicked.connect(self.download)

    def load_window(self, directory):
        game = cursor.execute('select * from games').fetchall()[int(self.game)]
        pixmap = QPixmap(os.path.join(directory, game[1]))
        self.image.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))
        new_text = f'<span style="font-size: 14pt; font-weight: bold;">{game[3]}</span>'
        self.description.setHtml(new_text)

    def open_review(self):
        self.review_window = ReviewWindow(self.game, self)
        self.review_window.finished.connect(self.on_review_closed)
        self.review_window.show()

    def on_review_closed(self):

        self.update(self.game)

    def clear(self):
        for i in range(self.main_layout.count()):
            if self.main_layout.takeAt(i).widget():
                self.main_layout.takeAt(i).widget().deleteLater()

    def update(self, game_id):
        reviews = cursor.execute('SELECT review, rating FROM reviews WHERE game_id = ?', (game_id,)).fetchall()
        self.clear()
        r = 0
        k = 0
        for review, rating in reviews:
            r += int(rating)
            k += 1
            review_text = f"Оценка: {rating}\nОтзыв: {review}\n\n"
            self.main_layout.addWidget(QLabel(review + '\n'))
            print(review)
        self.rating.setText(round(str(r / k), 1))

    def download(self):
        image_path = "C:\\Users\\User\\Desktop\\pythonProject2\\car1.png"
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        save_path = os.path.join(downloads_path, "downloaded_image.png")
        try:



            shutil.copy(image_path, save_path)
            QMessageBox.information(self, "Успех", "Изображение успешно скачано в папку 'Загрузки'!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось скачать изображение: {e}")


class Games_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Окно2")
        self.setGeometry(100, 100, 800, 600)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)

        self.contentWidget = QWidget()
        self.main_layout = QVBoxLayout()

        self.contentWidget.setLayout(self.main_layout)
        self.button_group = QButtonGroup(self)

        self.load_images_and_text("C:\\Users\\User\\PycharmProjects\\pythonProject2\\game_images")

        self.scrollArea.setWidget(self.contentWidget)
        self.setCentralWidget(self.scrollArea)

    def load_images_and_text(self, directory):
        self.game_list = []
        k = 0
        for i in cursor.execute('select * from games').fetchall():
            if i[1].endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                h_layout = QHBoxLayout()

                label = QLabel(self)
                pixmap = QPixmap(os.path.join(directory, i[1]))
                label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
                label.setAlignment(Qt.AlignCenter)

                text_label = QLabel(f"Описание для {i[2]}", self)
                text_label.setAlignment(Qt.AlignLeft)
                button = QPushButton("Игра" + str(k), self)
                setattr(self, 'button{}'.format(k), button)
                self.button_group.addButton(getattr(self, 'button{}'.format(k)))
                self.game_list.append((getattr(self, 'button{}'.format(k))))

                h_layout.addWidget(label)
                h_layout.addWidget(text_label)
                h_layout.addWidget(button)

                self.main_layout.addLayout(h_layout)
                k += 1
        self.button_group.buttonClicked.connect(self.chek)

    def chek(self, button):
        self.second_window = Description(button.text()[4:])

        self.second_window.show()


class Registration(QMainWindow, Ui_MainWindow1):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.reg.clicked.connect(self.registr)
        self.flag = False

    def registr(self):
        try:
            con = sqlite3.connect('user_base.db')
            cur = con.cursor()
            data_user = []

            for i in range(2, 7):
                data_user.append((getattr(self, 'lineEdit_{}'.format(i))).text())
            mail_check = cur.execute('SELECT mail FROM users WHERE mail = ?', (data_user[1],)).fetchall()
            password_check = cur.execute('SELECT passwords FROM users WHERE passwords = ?', (data_user[2],)).fetchall()

            if mail_check:
                self.lineEdit_3.setText('такой mail уже имеется')
            if password_check:
                self.lineEdit_4.setText('такой password уже имеется')
            if not check_password(data_user[2]):
                self.lineEdit_4.setText('ваш пароль не подходит')
            else:
                print(check_password(data_user[2]))
                cur.execute("INSERT INTO users (name, surname, mail, passwords, nick) VALUES (?, ?, ?, ?, ?)",
                            (data_user[4], data_user[0], data_user[1], data_user[2], data_user[3]))
                con.commit()
                self.flag = True
            if self.flag == True:
                self.check()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            con.close()

    def check(self):

        self.second_window = Games_window()
        self.close()
        self.second_window.show()


class Entrance(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.reg.clicked.connect(self.registr)


class MyNotes(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(1000, 500)
        self.UI()

    def UI(self):
        self.a = ''
        self.b = ''
        self.GuestButton.clicked.connect(self.check)
        self.RegistrationButton.clicked.connect(self.check2)

    def check(self):
        self.second_window = Games_window()
        self.close()
        self.second_window.show()

    def check2(self):
        self.second_window = Registration()
        self.close()
        self.second_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = MyNotes()
    ex.show()
    sys.exit(app.exec())




