import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2

class App(QWidget):
    def __init__(self):
        super(App, self).__init__()

        # Set Title to the APP
        self.set_Title()

        # Set Main Vertical Layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Heading
        self.heading_layout = QHBoxLayout()
        self.set_Heading()

        # Make a Group Box
        self.groupbox = QGroupBox("Data Collector")
        self.groupbox.setCheckable(False)
        self.main_layout.addWidget(self.groupbox)

        # Create a Horizontal Layout in side the groupbox
        self.groupbox_layout = QHBoxLayout()
        self.groupbox.setLayout(self.groupbox_layout)

        # Create 2 Vertical Layouts in the Groupbox Layout
        self.button_layout = QVBoxLayout()
        self.feed_layout = QVBoxLayout()
        self.groupbox_layout.addLayout(self.button_layout)
        self.groupbox_layout.addLayout(self.feed_layout)

        # Add Buttons i.e. required functions
        self.add_Buttons()

        # Thread
        self.worker = Worker(0)
        self.worker1 = Worker(0)

        # Show Feed
        self.img = QLabel()
        self.img.setAlignment(Qt.AlignTop)
        # image_3 = QPixmap("2.png")
        # self.img.setPixmap(image_3)
        self.feed_layout.addWidget(self.img)


    def add_Buttons(self):
        # Create 6 Horizontal Layouts
        self.hbox_1 = QHBoxLayout()
        self.hbox_1.setSpacing(15)
        self.hbox_1.setAlignment(Qt.AlignLeft)

        self.hbox_2 = QHBoxLayout()
        self.hbox_2.setSpacing(10)
        self.hbox_2.setAlignment(Qt.AlignLeft)

        self.hbox_3 = QHBoxLayout()
        self.hbox_3.setSpacing(10)
        self.hbox_3.setAlignment(Qt.AlignLeft)

        self.hbox_4 = QHBoxLayout()
        self.hbox_4.setSpacing(20)
        self.hbox_4.setAlignment(Qt.AlignLeft)
        self.hbox_4.setAlignment(Qt.AlignTop)

        self.hbox_5 = QHBoxLayout()
        self.hbox_5.setSpacing(10)
        self.hbox_5.setAlignment(Qt.AlignLeft)
        self.hbox_5.setAlignment(Qt.AlignTop)

        self.hbox_6 = QHBoxLayout()
        self.hbox_6.setSpacing(50)
        self.hbox_6.setAlignment(Qt.AlignHCenter)

        # Layout 1
        name_label = QLabel("Name of the Class")
        self.name_dialog = QLineEdit()

        self.name_dialog.setMaximumWidth(150)
        self.name_dialog.setAlignment(Qt.AlignCenter)
        self.name_dialog.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Add widgets to Layout 1
        self.hbox_1.addWidget(name_label)
        self.hbox_1.addWidget(self.name_dialog)
        self.button_layout.addLayout(self.hbox_1)


        # Layout 2
        count_label = QLabel("Count of the Image")
        self.count_dialog = QLineEdit()
        self.count_dialog.setMaximumWidth(150)
        self.count_dialog.setValidator(QIntValidator())
        self.count_dialog.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        # Add widgets to Layout 2
        self.hbox_2.addWidget(count_label)
        self.hbox_2.addWidget(self.count_dialog)
        self.button_layout.addLayout(self.hbox_2)

        # Layout 3
        start_camera = QPushButton("Start Feed")
        stop_camera = QPushButton("Stop Feed")
        start_camera.setMaximumSize(200, 30)
        stop_camera.setMaximumSize(200, 30)
        start_camera.setIcon(QIcon("start.jpg"))
        stop_camera.setIcon(QIcon("stop.png"))
        start_camera.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        stop_camera.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        start_camera.clicked.connect(self.start_Feed)
        stop_camera.clicked.connect(self.stop_Feed)


        # Add widgets to Layout 3
        self.hbox_3.addWidget(start_camera)
        self.hbox_3.addWidget(stop_camera)
        self.button_layout.addLayout(self.hbox_3)

        # Layout 4
        zoom_label = QLabel("Zoom Camera", self)
        self.zoom_value_label = QLabel("0")
        zoom_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.zoom_value_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.zoom_slider = QSlider()
        self.zoom_slider.setMaximumSize(100,10)
        self.zoom_slider.setOrientation(Qt.Horizontal)
        self.zoom_slider.setTickPosition(QSlider.TicksBelow)
        self.zoom_slider.setTickInterval(5)
        self.zoom_slider.setMinimum(0)
        self.zoom_slider.setMaximum(5)
        self.zoom_slider.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.zoom_slider.valueChanged.connect(self.change_Slider_Value)

        # Add widgets to Layout 4
        self.hbox_4.addWidget(zoom_label)
        self.hbox_4.addWidget(self.zoom_slider)
        self.hbox_4.addWidget(self.zoom_value_label)
        self.button_layout.addLayout(self.hbox_4)

        # Layout 5
        self.take_picture = QPushButton("Take Snap")
        self.take_picture.setMaximumSize(200,30)
        self.take_picture.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.take_picture.clicked.connect(self.take_Snap)

        # Add widgets to Layout 5
        self.hbox_5.addWidget(self.take_picture)
        self.button_layout.addLayout(self.hbox_5)

        # Layout 6
        self.clicked_image = QLabel()
        self.count_number = QLabel("0")
        self.clicked_image.setAlignment(Qt.AlignTop)
        image_2 = QPixmap("2.png")
        self.clicked_image.setPixmap(image_2)

        # Add widgets to Layout 6
        self.hbox_6.addWidget(self.clicked_image)
        self.hbox_6.addWidget(self.count_number)
        self.button_layout.addLayout(self.hbox_6)

    def start_Feed(self):
        self.worker.start()
        self.worker.image_update.connect(self.image_Update_Slot)


    def image_Update_Slot(self, image):
        self.img.setPixmap(QPixmap.fromImage(image))
        if self.take_picture.isChecked == True:
            image.save('1.jpg')
            print("DONE")

    def take_Snap(self):
        print("Here" )
        self.worker.stop()
        self.worker1.start()
        self.worker1.image_update.connect(self.save_Image)
        self.worker1.stop()
        self.worker.start()

    def save_Image(self, image):
        print('**')
        image.save("1.png")

    def stop_Feed(self):
        self.worker.stop()

    def change_Slider_Value(self):
        size = self.zoom_slider.value()
        self.zoom_value_label.setText(str(size))

    def set_Title(self):
        # Set Title
        self.title = "DATA COLLECTION APPLICATION"
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon("camera.jpg"))
        # self.setFixedSize(1000,500)

    def set_Heading(self):
        # Set Heading
        self.heading_label = QLabel("Data Collection Application for Deep Learning", self)
        self.heading_label.setAlignment(Qt.AlignCenter)

        # Quit Button
        self.quit_button = QPushButton("QUIT", self)
        self.quit_button.setMaximumSize(100, 25)
        self.quit_button.setIcon(QIcon("quit.png"))
        self.quit_button.clicked.connect(self.close)

        # Add to Layout
        self.heading_layout.addWidget(self.heading_label)
        self.heading_layout.addWidget(self.quit_button)

        # Add to Main Layout
        self.main_layout.addLayout(self.heading_layout)

class Worker(QThread):
    image_update = pyqtSignal(QImage)
    def __init__(self, n):
        super(Worker, self).__init__()
        self.n = n
    def run(self):
        self.thread_active = True
        capture = cv2.VideoCapture(self.n, cv2.CAP_V4L)
        while self.thread_active:
            ret, frame = capture.read()
            if ret:
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                flipped_img = cv2.flip(img,1)
                to_qt = QImage(flipped_img.data, flipped_img.shape[1], flipped_img.shape[0], QImage.Format_RGB888)
                pic = to_qt.scaled(640, 480, Qt.KeepAspectRatio)
                self.image_update.emit(pic)

    def stop(self):
        self.thread_active = False
        self.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    root = App()
    root.show()
    sys.exit(app.exec())
