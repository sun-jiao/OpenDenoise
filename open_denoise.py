import sys
from functools import partial

from PySide6.QtCore import Qt
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from sub_windows import AboutWindow, NotImplementedWindow
from utils import openUrl


class OpenDenoiseApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.app_title = "Open Denoise"
        self.selected_images = []  # List to store selected images
        self.newly_selected_images = []  # List to store selected images
        self.setAcceptDrops(True)
        self.create_menu()
        self.init_view()

    def create_menu(self):
        # create menu
        menubar = self.menuBar()

        # add menu items
        file_menu = menubar.addMenu('File')
        edit_menu = menubar.addMenu('Edit')
        view_menu = menubar.addMenu('View')
        about_menu = menubar.addMenu('About')

        # add actions to file menu
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(exit_action)

        # add actions to edit menu
        pref_action = QAction('Preferences', self)
        pref_action.triggered.connect(self.not_implemented)

        edit_menu.addAction(pref_action)

        # add actions to about menu
        release_action = QAction('Releases', self)
        release_action.triggered.connect(partial(openUrl, 'https://github.com/sun-jiao/OpenDenoise/releases'))
        code_action = QAction('Source code', self)
        code_action.triggered.connect(partial(openUrl, 'https://github.com/sun-jiao/OpenDenoise/tree/master'))
        about_action = QAction(f'About {self.app_title}', self)
        about_action.triggered.connect(self.open_about_window)

        about_menu.addAction(release_action)
        about_menu.addAction(code_action)
        about_menu.addSeparator()
        about_menu.addAction(about_action)

    def init_view(self):
        # Create widgets
        self.image_preview_label = QLabel(self)
        self.image_preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview_label.setPixmap(QPixmap("placeholder.jpg"))  # Placeholder for initial image

        self.image_list_button = QPushButton('Select Images', self)
        self.image_list_button.clicked.connect(self.selectImages)

        self.image_list_clear_button = QPushButton('Clear Images', self)
        self.image_list_clear_button.clicked.connect(self.clearImages)

        # Create a layout for GPU and CPU buttons in the same row
        image_list_button_layout = QHBoxLayout()
        image_list_button_layout.addWidget(self.image_list_button)
        image_list_button_layout.addWidget(self.image_list_clear_button)

        # Create a widget to hold the image list layout
        self.image_list_widget = QWidget()
        self.image_list_layout = QVBoxLayout(self.image_list_widget)
        self.image_list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Align buttons to the top

        # Create a scroll area for the image list
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.image_list_widget)
        self.scroll_area.setMinimumWidth(200)  # Set a minimum width for the scroll area

        self.image_operation_label = QLabel('Image Operations:')

        # define export-related
        self.export_original_checkbox = QCheckBox('Export to original directory', self)
        self.export_original_checkbox.stateChanged.connect(self.handle_export_checkbox)

        self.output_directory_button = QPushButton('Select Output Directory', self)
        self.output_directory_button.clicked.connect(self.selectOutputDirectory)

        self.use_gpu_radio = QRadioButton('Use GPU')
        self.use_cpu_radio = QRadioButton('Use CPU')
        self.process_button = QPushButton('Process and Save', self)
        self.process_button.clicked.connect(self.processAndSave)

        # Layout
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.image_preview_label)

        right_layout = QVBoxLayout()
        right_layout.addLayout(image_list_button_layout)
        right_layout.addWidget(self.scroll_area)
        right_layout.addWidget(self.image_operation_label)
        right_layout.addWidget(self.export_original_checkbox)
        right_layout.addWidget(self.output_directory_button)

        # Create a layout for GPU and CPU buttons in the same row
        gpu_cpu_layout = QHBoxLayout()
        gpu_cpu_layout.addWidget(self.use_gpu_radio)
        gpu_cpu_layout.addWidget(self.use_cpu_radio)

        right_layout.addLayout(gpu_cpu_layout)
        right_layout.addWidget(self.process_button)

        # Create a splitter and set the size ratio (2:1)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(QWidget())  # Placeholder for left side
        splitter.addWidget(QWidget())  # Placeholder for right side
        splitter.setSizes([2, 1])

        # Set the actual layouts for the placeholders
        splitter.widget(0).setLayout(left_layout)
        splitter.widget(1).setLayout(right_layout)

        # Set the central widget as the splitter
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.addWidget(splitter)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        # Set window properties
        self.setGeometry(100, 100, 800, 500)
        self.setWindowTitle(self.app_title)
        self.show()

    def selectImages(self):
        options = QFileDialog.Option.ReadOnly
        images_folder = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.PicturesLocation)
        file_names, _ = QFileDialog.getOpenFileNames(self, "Select Images", images_folder,
                                                     "Images (*.png *.jpg *.bmp *.gif *.tif)", options=options)
        if file_names:
            self.newly_selected_images = file_names
            self.updateImageList()

    def clearImages(self):
        pass

    def handle_export_checkbox(self, state):
        print(state)
        print(Qt.CheckState.Checked)
        # enable or disable select output button
        self.output_directory_button.setEnabled(state != 2)
        # self.output_directory_button.setEnabled(state != Qt.CheckState.Checked)  not work, reasons unknown

    def updateImageList(self):
        # Display the selected images in the list
        # Create buttons with checkboxes for each image
        for image in self.newly_selected_images:
            pixmap = QPixmap(image)

            # Crop the center square (assuming the image is larger than 50x50)
            size = min(pixmap.width(), pixmap.height())
            left = (pixmap.width() - size) // 2
            top = (pixmap.height() - size) // 2
            cropped_pixmap = pixmap.copy(left, top, size, size)

            # Resize the cropped image to 50x50
            resized_pixmap = cropped_pixmap.scaled(50, 50, aspectMode=Qt.AspectRatioMode.IgnoreAspectRatio)

            button = QPushButton(image.split("/")[-1])  # Use the filename as the button text
            button.setContentsMargins(0, 0, 0, 0)  # Set margins to 0 to remove spacing
            checkbox = QCheckBox()
            checkbox.setChecked(True)

            image_pix = QLabel(self)
            image_pix.setFixedSize(50, 50)
            image_pix.setScaledContents(True)
            image_pix.setPixmap(resized_pixmap)

            button_layout = QHBoxLayout()
            button_layout.addWidget(checkbox)
            button_layout.addWidget(image_pix)
            button_layout.addWidget(button)
            button_layout.setContentsMargins(0, 0, 0, 0)  # Set margins to 0 to remove spacing
            button_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Align buttons to the top
            button_widget = QWidget()
            button_widget.setLayout(button_layout)
            self.image_list_layout.addWidget(button_widget)

    def processAndSave(self):
        # Placeholder for processing and saving logic
        # You can replace this with your actual image processing code
        print('Processing and saving images...')
        print('Selected Images:', self.newly_selected_images)

    def dragEnterEvent(self, event):
        file_names = [file.toLocalFile() for file in event.mimeData().urls()]

        if file_names:
            self.newly_selected_images = file_names
            self.updateImageList()
            print("Dropped files ==> {}".format(file_names))

    def selectOutputDirectory(self):
        options = QFileDialog.Option.ReadOnly
        images_folder = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.PicturesLocation)
        output_directory = QFileDialog.getExistingDirectory(self, "Select Output Directory", images_folder, options=options)
        if output_directory:
            print("Selected Output Directory:", output_directory)

    def not_implemented(self):
        self.not_implemented_window = NotImplementedWindow()
        self.not_implemented_window.show()

    def open_about_window(self):
        self.about_windows = AboutWindow()
        self.about_windows.show()


class OpenDenoiseImage:
    def __init__(self, path):
        self.path = path
        self.filename = path.split("/")[-1]
        self.selected = True
        self.processed = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OpenDenoiseApp()
    window.show()
    sys.exit(app.exec())
