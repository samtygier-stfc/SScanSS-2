import unittest
import unittest.mock as mock
from sscanss.ui.windows.main.model import MainWindowModel
from sscanss.core.scene import Node
from sscanss.core.instrument import Instrument


class TestMainWindowModel(unittest.TestCase):
    def setUp(self):
        self.model = MainWindowModel()
        self.instrument = mock.create_autospec(Instrument)
        self.instrument.detectors = []

    @mock.patch('sscanss.ui.windows.main.model.read_instrument_description_file', autospec=True)
    def testCreateProjectData(self, mocked_function):
        mocked_function.return_value = self.instrument
        self.assertIsNone(self.model.project_data)
        self.model.createProjectData('Test', 'ENGIN-X')
        self.assertIsNotNone(self.model.project_data)

    @mock.patch('sscanss.ui.windows.main.model.createSampleNode', autospec=True)
    @mock.patch('sscanss.ui.windows.main.model.read_instrument_description_file', autospec=True)
    def testAddAndRemoveMesh(self, mock_read_idf, mock_create_sample):
        mock_create_sample.return_value = Node()
        mock_read_idf.return_value = self.instrument

        self.model.createProjectData('Test', 'ENGIN-X')

        self.model.addMeshToProject('demo', None)
        self.model.addMeshToProject('demo', None)  # should be added as 'demo 1'
        self.assertEqual(len(self.model.sample), 2)
        self.model.removeMeshFromProject('demo')
        self.assertEqual(len(self.model.sample), 1)
