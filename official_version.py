import sys
from PyQt5 import QtCore, QtWidgets, QtGui

COLORS = [
'#000000', '#141923', '#414168', '#3a7fa7', '#35e3e3', '#8fd970', '#5ebb49', 
'#458352', '#dcd37b', '#fffee5', '#ffd035', '#cc9245', '#a15c3e', '#a42f3b', 
'#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#ffffff'
]

user_bg_color = input('Enter background color for your application:\n')

PEN_WIDTH = 6



if QtGui.QColor(user_bg_color).isValid():
    BG_COLOR = QtGui.QColor(user_bg_color)              #    Check if given color is valid
else:
    raise NameError('Please select valid color name')





class MainWindow(QtWidgets.QMainWindow):
    
    global PEN_WIDTH


    def __init__(self):
        super().__init__()


        self.setWindowTitle('MyPaint')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.canvas = Canvas()
        self.eraser = Eraser()


        self.spin = QtWidgets.QSpinBox()
        self.spin.setValue(PEN_WIDTH)
        self.spin.valueChanged.connect(self.canvas.changeWidth)         #   self.spin controls pen width
        self.eraser.clicked.connect(self.canvas.enableEraser)

        w = QtWidgets.QWidget()
        l = QtWidgets.QVBoxLayout()
        w.setLayout(l)
        l.addWidget(self.canvas)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.canvas.setSizePolicy(sizePolicy)       #   This enables you to draw normally even if you resize the window

        palette = QtWidgets.QHBoxLayout()
        self.add_palette_buttons(palette)
        palette.addWidget(self.eraser)
        palette.addWidget(self.spin)                #   lay widgets out
        l.addLayout(palette)

        self.setCentralWidget(w)




    def add_palette_buttons(self, layout):
        for c in COLORS:
            b = QPaletteButton(c)
            b.pressed.connect(lambda c=c: self.canvas.setPenColor(c))       #   add color buttons and enable them to select pen color
            layout.addWidget(b)





class Canvas(QtWidgets.QLabel):



    def __init__(self):
        super().__init__()
        pixmap = QtGui.QPixmap(790, 500)
        pixmap.fill(BG_COLOR)                           #   set self.pixmap and fill it with user color
        self.setPixmap(pixmap)

        self.last_x, self.last_y = None, None
        self.pen_color = QtGui.QColor('#000000')



    def setPenColor(self, c):
        self.pen_color = QtGui.QColor(c)                #   this function works when clicking on color button



    def enableEraser(self):
        self.pen_color = BG_COLOR                       #   eraser draws wirh a background color, erasing all other colors



    def changeWidth(self):

        global PEN_WIDTH
        PEN_WIDTH = window.spin.value()                     #   this function changes pen width to spin value



    '''IF WE DREW ONLY POINTS, PICTURE WON/'T BE WHOLE (IT TAKES TIME TO DRAW NEW POINT), SO WE DRAW A LINE BETWEEN LAST AND NEW POINT'''
    def mouseMoveEvent(self, e):
        if self.last_x is None:     
            self.last_x = e.x()                         #   if the mouse was released/unpressed, make new point
            self.last_y = e.y()
            return

        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(PEN_WIDTH)
        p.setColor(self.pen_color)
        painter.setPen(p)

        painter.drawLine(self.last_x, self.last_y, e.x(), e.y())     #  draws a line between 2 points 
       
        self.last_x = e.x()
        self.last_y = e.y()
        painter.end()
        self.update()




    def mouseReleaseEvent(self, e):
        self.last_x, self.last_y = None, None







class QPaletteButton(QtWidgets.QPushButton):
    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QtCore.QSize(24, 24))                     #   create class of color buttons
        self.color = color
        self.setStyleSheet('background-color: {}'.format(color))




class Eraser(QtWidgets.QPushButton):
    def __init__(self):
        super().__init__()
        self.setIcon(QtGui.QIcon('eraser.png'))                      #   create class of eraser
        self.setIconSize(QtCore.QSize(25, 30))
        self.setFixedSize(30, 35)





app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()

