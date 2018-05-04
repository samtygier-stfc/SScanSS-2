from PyQt5 import QtCore, QtGui, QtWidgets
from .presenter import MainWindowPresenter
from sscanss.ui.dialogs.project.view import ProjectDialog


MAIN_WINDOW_TITLE = 'SScanSS 2'

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.presenter = MainWindowPresenter(self)

        self.undo_stack = QtWidgets.QUndoStack(self)
        self.undo_view = QtWidgets.QUndoView(self.undo_stack)
        self.undo_view.setWindowTitle('History')
        self.undo_view.setAttribute(QtCore.Qt.WA_QuitOnClose, False)

        self.createActions()
        self.createMenus()

        self.setWindowTitle(MAIN_WINDOW_TITLE)
        self.setMinimumSize(800, 600)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.settings = QtCore.QSettings(
            QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope, 'SScanSS 2', 'SScanSS 2')
        self.readSettings()

        self.isInitialized = False

    def createActions(self):
        self.new_project_action = QtWidgets.QAction('&New Project', self)
        self.new_project_action.setShortcut(QtGui.QKeySequence.New)
        self.new_project_action.triggered.connect(self.showNewProjectDialog)

        self.open_project_action = QtWidgets.QAction('&Open Project', self)
        self.open_project_action.setShortcut(QtGui.QKeySequence.Open)
        self.open_project_action.triggered.connect(self.presenter.openProject)

        # self.open_recent_action = QtWidgets.QAction('Open Recent', self)

        self.save_project_action = QtWidgets.QAction('&Save Project', self)
        self.save_project_action.setShortcut(QtGui.QKeySequence.Save)
        self.save_project_action.triggered.connect(self.presenter.saveProject)

        self.save_as_action = QtWidgets.QAction('Save &As...', self)
        self.save_as_action.setShortcut(QtGui.QKeySequence.SaveAs)
        self.save_as_action.triggered.connect(self.presenter.saveProject)

        self.exit_action = QtWidgets.QAction('E&xit', self)
        self.exit_action.setShortcut(QtGui.QKeySequence.Quit)
        self.exit_action.triggered.connect(self.close)

    def createMenus(self):
        main_menu = self.menuBar()

        file_menu = main_menu.addMenu('&File')
        file_menu.addAction(self.new_project_action)
        file_menu.addAction(self.open_project_action)
        file_menu.addAction(self.save_project_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)


        edit_menu = main_menu.addMenu('&Edit')
        view_menu = main_menu.addMenu('&View')
        insert_menu = main_menu.addMenu('&Insert')
        instrument_menu = main_menu.addMenu('I&nstrument')
        simulation_menu = main_menu.addMenu('Sim&ulation')
        help_menu = main_menu.addMenu('&Help')

    def readSettings(self):
        """ Loads window geometry from INI file """
        self.restoreGeometry(self.settings.value('geometry', bytearray(b'')))
        self.restoreState(self.settings.value('windowState', bytearray(b'')))

    def closeEvent(self, event):
        """Override of the QWidget Close Event"""
        self.settings.setValue('geometry', self.saveGeometry())
        self.settings.setValue('windowState', self.saveState())
        super().closeEvent(event)

    def showEvent(self, event):
        super().showEvent(event)

        if self.isInitialized:
            return

        if not self.presenter.isProjectCreated():
            self.showNewProjectDialog()

        self.isInitialized = True

    def showNewProjectDialog(self):
        self.project_dialog = ProjectDialog(self)
        self.project_dialog.setModal(True)
        self.project_dialog.show()

    def showProjectName(self, project_name):
        title = '{} - {}'.format(project_name, MAIN_WINDOW_TITLE)
        self.setWindowTitle(title)

    def showSaveDialog(self, filters, name=''):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                            'Save Project',
                                                            name,
                                                            filters)
        return filename

    def showOpenDialog(self, filters):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                             'Open Project', '',
                                                             filters)
        return filename

