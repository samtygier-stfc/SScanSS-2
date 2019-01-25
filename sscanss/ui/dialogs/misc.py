from PyQt5 import QtCore, QtGui, QtWidgets


class ProjectDialog(QtWidgets.QDialog):

    formSubmitted = QtCore.pyqtSignal(str, str)
    recentItemDoubleClicked = QtCore.pyqtSignal(str)
    # max number of recent projects to show in dialog is fixed because of the
    # dimensions of the dialog window
    max_recent_size = 5

    def __init__(self, recent, parent):
        super().__init__(parent)

        self.recent = recent
        self.instruments = list(parent.presenter.model.instruments.keys())
        data = parent.presenter.model.project_data
        self.selected_instrument = None if data is None else data['instrument'].name

        if len(self.recent) > self.max_recent_size:
            self.recent_list_size = self.max_recent_size
        else:
            self.recent_list_size = len(self.recent)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Dialog)
        self.setMinimumSize(640, 480)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.createImageHeader()
        self.createTabWidgets()
        self.createStackedWidgets()
        self.createNewProjectWidgets()
        self.createRecentProjectWidgets()
        self.create_project_button.clicked.connect(self.createProjectButtonClicked)

        main_window_view = self.parent()
        self.formSubmitted.connect(main_window_view.presenter.createProject)
        self.recentItemDoubleClicked.connect(main_window_view.presenter.openProject)

        self.project_name_textbox.setFocus()

    def createImageHeader(self):
        img = QtWidgets.QLabel()
        img.setPixmap(QtGui.QPixmap('../static/images/banner.png'))
        self.main_layout.addWidget(img)

    def createTabWidgets(self):
        self.group = QtWidgets.QButtonGroup()
        self.button_layout = QtWidgets.QHBoxLayout()
        self.new_project_button = QtWidgets.QPushButton('Create New Project')
        self.new_project_button.setObjectName('CustomTab')
        self.new_project_button.setCheckable(True)
        self.new_project_button.setChecked(True)

        self.load_project_button = QtWidgets.QPushButton('Open Existing Project')
        self.load_project_button.setObjectName('CustomTab')
        self.load_project_button.setCheckable(True)

        self.group.addButton(self.new_project_button, 0)
        self.group.addButton(self.load_project_button, 1)
        self.button_layout.addWidget(self.new_project_button)
        self.button_layout.addWidget(self.load_project_button)
        self.button_layout.setSpacing(0)

        self.main_layout.addLayout(self.button_layout)

    def createStackedWidgets(self):
        self.stack = QtWidgets.QStackedLayout()
        self.main_layout.addLayout(self.stack)

        self.stack1 = QtWidgets.QWidget()
        self.stack1.setContentsMargins(30, 0, 30, 0)
        self.stack2 = QtWidgets.QWidget()
        self.stack2.setContentsMargins(30, 0, 30, 0)
        self.group.buttonClicked[int].connect(self.stack.setCurrentIndex)

        self.stack.addWidget(self.stack1)
        self.stack.addWidget(self.stack2)

    def createNewProjectWidgets(self):
        layout = QtWidgets.QVBoxLayout()
        layout.addStretch(1)

        layout.addWidget(QtWidgets.QLabel('Project Name:'))

        self.project_name_textbox = QtWidgets.QLineEdit()
        layout.addWidget(self.project_name_textbox)
        self.validator_textbox = QtWidgets.QLabel('')
        self.validator_textbox.setObjectName('Error')
        layout.addWidget(self.validator_textbox)
        layout.addStretch(1)

        layout.addWidget(QtWidgets.QLabel('Select Instrument:'))

        self.instrument_combobox = QtWidgets.QComboBox()
        self.instrument_combobox.setView(QtWidgets.QListView())
        self.instrument_combobox.addItems(self.instruments)
        self.instrument_combobox.setCurrentText(self.selected_instrument)
        layout.addWidget(self.instrument_combobox)
        layout.addStretch(1)

        button_layout = QtWidgets.QHBoxLayout()
        self.create_project_button = QtWidgets.QPushButton('Create')
        button_layout.addWidget(self.create_project_button)
        button_layout.addStretch(1)

        layout.addLayout(button_layout)
        layout.addStretch(1)

        self.stack1.setLayout(layout)

    def createProjectButtonClicked(self):
        name = self.project_name_textbox.text().strip()
        instrument = self.instrument_combobox.currentText()
        if name:
            self.formSubmitted.emit(name, instrument)
        else:
            self.validator_textbox.setText('Project name cannot be left blank.')

    def createRecentProjectWidgets(self):
        layout = QtWidgets.QVBoxLayout()
        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.setObjectName('Recents')
        self.list_widget.setSpacing(10)

        for i in range(self.recent_list_size):
            item = QtWidgets.QListWidgetItem(self.recent[i])
            item.setIcon(QtGui.QIcon('../static/images/file-black.png'))
            self.list_widget.addItem(item)

        item = QtWidgets.QListWidgetItem('Open ...')
        item.setIcon(QtGui.QIcon('../static/images/folder-open.png'))
        self.list_widget.addItem(item)

        self.list_widget.itemDoubleClicked.connect(self.projectItemDoubleClicked)
        layout.addWidget(self.list_widget)

        self.stack2.setLayout(layout)

    def projectItemDoubleClicked(self, item):
        index = self.list_widget.row(item)

        if index == self.recent_list_size:
            self.recentItemDoubleClicked.emit('')
        else:
            self.recentItemDoubleClicked.emit(item.text())
        self.accept()


class ProgressDialog(QtWidgets.QDialog):

    def __init__(self, message, parent):
        super().__init__(parent)

        progress_bar = QtWidgets.QProgressBar()
        progress_bar.setTextVisible(False)
        progress_bar.setMinimum(0)
        progress_bar.setMaximum(0)

        message = QtWidgets.QLabel(message)
        message.setAlignment(QtCore.Qt.AlignCenter)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addStretch(1)
        main_layout.addWidget(progress_bar)
        main_layout.addWidget(message)
        main_layout.addStretch(1)

        self.setLayout(main_layout)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Dialog)
        self.setMinimumSize(300, 120)

    def keyPressEvent(self, _):
        """
        This ensure the user cannot close the dialog box with the Esc key
        """
        pass
