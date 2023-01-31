from tkinter import *#работа с окнами
import keyboard as keyb#клавиатура
import sys
from PyQt5 import QtCore, QtGui, QtWidgets#работа с окнами и более высоким функционалом
from PIL import ImageGrab#работа с изображениями
import pytesseract#нэйросеть для распознавания текста
from PIL import Image
import keyboard as keyb

#настройки окна Tk
root = Tk()
root.title("printscreen")
root.geometry("300x300+100+100")
root.resizable(width=False, height=False)
#извлечение текста из изображения
img =Image.open("testpic/testImage.png")
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
text = pytesseract.image_to_string(img, lang="rus")#выбираем язык и задаем переменную текст
#при нажатии на ctrl будет писать то что написано в изображении
keyb.add_hotkey("SHiFT", lambda: keyb.write(text, value.get()))
keyb.add_hotkey("8", lambda: keyb.write(value1.get(), value.get()))
print("to start automatic text writing, there are two options 1 option - enter the text speed in the upper line with a fractional value (the lower the value, the faster) and in the lower line of the text you want to write, then you need to press ok and use the shift key and text input will begin 2 option - close 1 window and take a screenshot of the area where the text is located, then restart the program, specify the speed in the first line (you do not need to touch the bottom one), press ok and after using the ctrl key, text input will begin.")
#работа с переменными и строками
speed = 1
value =DoubleVar()
texstt = 23
value1 = StringVar()

canvas = Canvas(bg="white", width=250, height=200)
canvas.pack(anchor=CENTER, expand=1)

python_image = PhotoImage(file="karandah.png")

canvas.create_image(10, 10, anchor=NW, image=python_image)

l = Label(text="for more information, read the message in the console")
o = Entry(textvariable=value1)
e = Entry(textvariable=value)
b = Button(text="Ok")

def test(event):
    get = value.get()
    l["text"] = get
    print(value.get())

b.bind("<Button-1>", test)

l.pack(side=BOTTOM)
e.pack()
b.pack()
o.pack()
root.mainloop()

#настройки окна скрин шота
class SnippingWidget(QtWidgets.QMainWindow):
    closed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(SnippingWidget, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background:transparent;")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.outsideSquareColor = "red"
        self.squareThickness = 2

        self.start_point = QtCore.QPoint()
        self.end_point = QtCore.QPoint()

    def mousePressEvent(self, event):
        self.start_point = event.pos()
        self.end_point = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        self.end_point = event.pos()
        self.update()
#сохранение скрин шота в папку testpic
    def mouseReleaseEvent(self, QMouseEvent):
        r = QtCore.QRect(self.start_point, self.end_point).normalized()
        self.hide()
        img = ImageGrab.grab(bbox=r.getCoords())
        #                 vvvvvvv <---- создайте папку, например testpic
        img.save("testpic/testImage.png")
        QtWidgets.QApplication.restoreOverrideCursor()
        self.closed.emit()
        self.start_point = QtCore.QPoint()
        self.end_point = QtCore.QPoint()

    def paintEvent(self, event):
        trans = QtGui.QColor(22, 100, 233)
        r = QtCore.QRectF(self.start_point, self.end_point).normalized()
        qp = QtGui.QPainter(self)
        trans.setAlphaF(0.2)
        qp.setBrush(trans)
        outer = QtGui.QPainterPath()
        outer.addRect(QtCore.QRectF(self.rect()))
        inner = QtGui.QPainterPath()
        inner.addRect(r)
        r_path = outer - inner
        qp.drawPath(r_path)
        qp.setPen(
            QtGui.QPen(QtGui.QColor(self.outsideSquareColor), self.squareThickness)
        )
        trans.setAlphaF(0)
        qp.setBrush(trans)
        qp.drawRect(r)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)

        self.label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignCenter)
        self.button = QtWidgets.QPushButton('Делать скриншот')
        self.button.clicked.connect(self.activateSnipping)
        self.button = QtWidgets.QPushButton('Делать скриншот')
        self.button.clicked.connect(self.activateSnipping)

        layout = QtWidgets.QVBoxLayout(self.centralWidget)
        layout.addWidget(self.label, 1)
        layout.addWidget(self.button, 0)
        layout.addWidget(self.button, 0)

        self.snipper = SnippingWidget()
        self.snipper.closed.connect(self.on_closed)

    def activateSnipping(self):
        self.snipper.showFullScreen()
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CrossCursor)
        self.hide()

    def on_closed(self):
        pixmap = QtGui.QPixmap("testpic/testImage.png")
        self.label.setPixmap(pixmap)
        self.show()
        self.adjustSize()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.resize(400, 300)
    w.show()
    sys.exit(app.exec_())


keyb.wait()
