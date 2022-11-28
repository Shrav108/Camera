import sys
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox, QFileDialog, QLineEdit, QSlider, QWidget, QSizePolicy, QApplication
from PyQt5.QtGui import QIntValidator, QIcon, QImage, QFont, QPixmap
from PyQt5.QtCore import Qt, QRect, QThread, pyqtSignal
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

        # Count variable to Count the images
        self.count = 0

        # Thread
        self.worker = Worker(0)

        # Show Feed
        self.img = QLabel()
        self.img.setAlignment(Qt.AlignCenter)
        self.feed_layout.addWidget(self.img)

        self.show()

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

        self.hbox_5 = QHBoxLayout()
        self.hbox_5.setSpacing(10)
        self.hbox_5.setAlignment(Qt.AlignLeft)
        self.hbox_5.sizeConstraint()

        self.resultbox = QGroupBox("Results")
        self.resultbox.setCheckable(False)
        self.resultbox.setMaximumSize(600, 450)
        self.result_layout = QVBoxLayout()
        self.result_layout.setAlignment(Qt.AlignTop)
        self.result_layout.setSpacing(30)
        self.resultbox.setLayout(self.result_layout)

        self.hbox_6 = QHBoxLayout()
        self.hbox_6.setSpacing(15)
        self.hbox_6.setAlignment(Qt.AlignLeft)

        self.hbox_7 = QHBoxLayout()
        self.hbox_7.setSpacing(15)
        self.hbox_7.setAlignment(Qt.AlignLeft)

        self.hbox_8 = QHBoxLayout()
        self.hbox_8.setSpacing(10)
        self.hbox_8.setAlignment(Qt.AlignLeft)

        # Layout 1
        name_label = QLabel("Name of the Class")
        self.name_dialog = QLineEdit()
        self.name_freeze_button = QPushButton("Freeze Name")
        self.name_dialog.setMaximumWidth(150)
        self.name_dialog.setAlignment(Qt.AlignCenter)
        self.name_dialog.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.name_freeze_button.setMaximumSize(100, 30)
        self.name_freeze_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.name_freeze_button.clicked.connect(self.name_Freeze)

        # Add widgets to Layout 1
        self.hbox_1.addWidget(name_label)
        self.hbox_1.addWidget(self.name_dialog)
        self.hbox_1.addWidget(self.name_freeze_button)
        self.button_layout.addLayout(self.hbox_1)

        # Layout 2
        count_label = QLabel("Count of the Image")
        self.count_dialog = QLineEdit()
        self.count_freeze = QPushButton("Freeze Count")
        self.count_dialog.setMaximumWidth(150)
        self.count_dialog.setAlignment(Qt.AlignCenter)
        self.count_dialog.setValidator(QIntValidator())
        self.count_dialog.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.count_freeze.clicked.connect(self.freeze_Count)
        # Add widgets to Layout 2
        self.hbox_2.addWidget(count_label)
        self.hbox_2.addWidget(self.count_dialog)
        self.hbox_2.addWidget(self.count_freeze)
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

        self.file_dir_button = QPushButton("Select Folder")
        self.file_dir_button.setMaximumSize(100, 30)
        self.file_dir_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.file_dir_button.clicked.connect(self.get_Dir)

        # Add widgets to Layout 3
        self.hbox_3.addWidget(start_camera)
        self.hbox_3.addWidget(stop_camera)
        self.hbox_3.addWidget(self.file_dir_button)
        self.button_layout.addLayout(self.hbox_3)

        # Layout 4
        zoom_label = QLabel("Zoom Camera", self)
        self.zoom_value_label = QLabel("1")
        zoom_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.zoom_value_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.zoom_slider = QSlider()
        self.zoom_slider.setMaximumSize(100, 10)
        self.zoom_slider.setOrientation(Qt.Horizontal)
        self.zoom_slider.setTickPosition(QSlider.TicksBelow)
        self.zoom_slider.setTickInterval(5)
        self.zoom_slider.setMinimum(1)
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
        self.take_picture.setMaximumSize(100, 30)
        self.take_picture.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.take_picture.clicked.connect(self.take_Snap)

        # Add widgets to Layout 5
        self.hbox_5.addWidget(self.take_picture)
        self.button_layout.addLayout(self.hbox_5)

        self.button_layout.addWidget(self.resultbox)

        # Layout 6
        self.count_label = QLabel("Image Count :")
        self.count_number = QLabel("0")
        self.count_label.setMaximumSize(100, 20)
        self.count_number.setMaximumSize(50, 20)
        self.count_label.setAlignment(Qt.AlignLeft)

        # Add widgets to Layout 6
        self.hbox_6.addWidget(self.count_label)
        self.hbox_6.addWidget(self.count_number)
        self.result_layout.addLayout(self.hbox_6)

        # Layout 7
        self.saved_label = QLabel("Saved In & As :")
        self.saved_in_as = QLabel("Not Saved Yet")
        self.saved_label.setMaximumSize(100, 20)
        self.saved_in_as.setMaximumSize(600, 20)
        self.saved_in_as.setFont(QFont('Arial', 9))
        self.saved_label.setAlignment(Qt.AlignLeft)

        # Add widgets to Layout 7
        self.hbox_7.addWidget(self.saved_label)
        self.hbox_7.addWidget(self.saved_in_as)
        self.result_layout.addLayout(self.hbox_7)

        # Layout 7
        self.show_image_label = QLabel("Saved Image :")
        self.show_image_label.setMaximumSize(100, 20)
        self.show_image_label.setAlignment(Qt.AlignTop)

        self.show_image = QLabel("")
        self.show_image.setAlignment(Qt.AlignCenter)

        # Add widgets to Layout 7
        self.hbox_8.addWidget(self.show_image_label)
        self.hbox_8.addWidget(self.show_image)
        self.result_layout.addLayout(self.hbox_8)

    def get_Dir(self):
        self.folder_path = QFileDialog.getExistingDirectory(None, "Select Folder")

    def freeze_Count(self):
        self.count_dialog.setReadOnly(True)

    def name_Freeze(self):
        self.name_dialog.setReadOnly(True)

    def start_Feed(self):
        self.worker.start()
        self.worker.image_update.connect(self.image_Update_Slot)

    def image_Update_Slot(self, image):
        self.img.setPixmap(QPixmap.fromImage(image))

    def take_Snap(self):
        if self.count == 0:
            count = self.count_dialog.text()
            self.count = self.count + int(count)
        else:
            self.count += 1

        # Save Image
        image = self.worker.get_image()
        name = self.name_dialog.text()
        image.save(f'{self.folder_path}/{name}_{self.count}.jpeg')

        # Update Count Label
        self.count_number.setText(f"{self.count}")

        # Update Folder Label
        self.saved_in_as.setText(f'{self.folder_path}/{name}_{self.count}.jpeg')

        # Display the image
        image_dummy = QPixmap(f'{self.folder_path}/{name}_{self.count}.jpeg').scaled(450, 250, Qt.KeepAspectRatio)
        self.show_image.setPixmap(image_dummy)

    def stop_Feed(self):
        self.worker.stop()

    def change_Slider_Value(self):
        self.size = self.zoom_slider.value()
        self.worker.get_Scale(self.size)
        self.zoom_value_label.setText(str(self.size))

    def set_Title(self):
        # Set Title
        self.title = "DATA COLLECTION APPLICATION"
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon("camera.jpg"))
        self.showMaximized()

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
        self.scale = 1
        self.rect = QRect()

    def run(self):
        self.thread_active = True
        capture = cv2.VideoCapture(self.n, cv2.CAP_V4L)
        while self.thread_active:
            ret, frame = capture.read()
            if ret:
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                flipped_img = cv2.flip(img, 1)
                flipped_img = self.zoom_Image(flipped_img)
                to_qt = QImage(flipped_img.data, flipped_img.shape[1], flipped_img.shape[0], QImage.Format_RGB888)
                pic = to_qt.scaled(640, 720, Qt.KeepAspectRatio)
                copy_to_qt = to_qt.copy(self.rect.x(), self.rect.y(), to_qt.width(), to_qt.height())
                self.image_update.emit(pic)
                self.send_image(copy_to_qt)


    def zoom_Image(self, img):
        # Get the size of image
        y_size = img.shape[0]
        x_size = img.shape[1]

        # Crop Coordinates to the area of zoom
        x1 = int(0.5 * x_size * (1 - 1 / self.scale))
        y1 = int(0.5 * y_size * (1 - 1 / self.scale))
        x2 = int(x_size - 0.5 * x_size * (1 - 1 / self.scale))
        y2 = int(y_size - 0.5 * y_size * (1 - 1 / self.scale))

        # Crop the Image
        crop_img = img[y1:y2, x1:x2]

        # Return Zoomed Image
        return cv2.resize(crop_img, None, fx=self.scale, fy=self.scale, interpolation="INTER_LANCZOS4")

    def send_image(self, x):
        self.copy_image = x

    def get_image(self):
        return self.copy_image

    def get_Scale(self, scale):
        self.scale = scale

    def stop(self):
        self.thread_active = False
        self.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    root = App()
    # root.show()
    sys.exit(app.exec())
