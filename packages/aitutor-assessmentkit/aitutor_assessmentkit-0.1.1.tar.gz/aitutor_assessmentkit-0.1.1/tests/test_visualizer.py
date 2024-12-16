import unittest
import tempfile
import os
from unittest.mock import patch, MagicMock

class TestVisualizer(unittest.TestCase):
    def setUp(self):
        """Set up the mocked Visualizer instance and temporary paths."""
        # Create temporary directory for mock output
        self.temp_output_dir = tempfile.TemporaryDirectory()
        
        # Sample data to simulate input
        self.mock_file_names = [
            tempfile.NamedTemporaryFile(delete=False, suffix=".json").name
        ]
        with open(self.mock_file_names[0], 'w') as f:
            f.write('{"key": "value"}')  # Example JSON content

        self.mock_output_dir = self.temp_output_dir.name
        self.mock_tutor_models = [
            'Novice', 'Expert', 'Llama31405B', 'GPT4', 'Sonnet',
            'Phi3', 'Llama318B', 'Mistral', 'Gemini'
        ]

        # Patch the Visualizer class
        patcher = patch('aitutor_assessmentkit.visualizer.Visualizer', autospec=True)
        self.mock_visualizer_class = patcher.start()
        self.addCleanup(patcher.stop)

        # Create a mocked Visualizer instance
        self.mock_visualizer = MagicMock()
        self.mock_visualizer_class.return_value = self.mock_visualizer

    def tearDown(self):
        """Clean up temporary files and directories."""
        for file_name in self.mock_file_names:
            os.unlink(file_name)  # Remove temporary files
        self.temp_output_dir.cleanup()

    def test_initialization(self):
        """Test if Visualizer initializes with correct parameters."""
        from aitutor_assessmentkit.visualizer import Visualizer

        visualizer = Visualizer(
            file_names=self.mock_file_names,
            output_data_dir=self.mock_output_dir,
            tutor_models=self.mock_tutor_models
        )

        # Assert that the Visualizer is initialized with correct arguments
        self.mock_visualizer_class.assert_called_once_with(
            file_names=self.mock_file_names,
            output_data_dir=self.mock_output_dir,
            tutor_models=self.mock_tutor_models
        )

    def test_get_evaluation_scores(self):
        """Test retrieving evaluation scores."""
        self.mock_visualizer.get_evaluation_scores.return_value = {
            'human_evaluation_scores': {'overall': [1, 2, 3]},
            'auto_evaluation_scores': {'overall': [3, 2, 1]},
            'llm_evaluation_scores': {'overall': [2, 3, 1]}
        }

        scores = self.mock_visualizer.get_evaluation_scores(normalize=True)

        # Verify the method was called with the correct parameter
        self.mock_visualizer.get_evaluation_scores.assert_called_once_with(normalize=True)

        # Validate the returned scores
        self.assertEqual(scores['human_evaluation_scores']['overall'], [1, 2, 3])

    def test_label_distribution_plot(self):
        """Test generating a label distribution plot."""
        self.mock_visualizer.label_distribution_plot.return_value = None

        self.mock_visualizer.label_distribution_plot(
            dimension="Overall",
            normalize=True,
            plot_name='violin_label_distribution.png',
            plot_type='violin'
        )

        # Verify the method was called with correct arguments
        self.mock_visualizer.label_distribution_plot.assert_called_once_with(
            dimension="Overall",
            normalize=True,
            plot_name='violin_label_distribution.png',
            plot_type='violin'
        )

    def test_spider_plot(self):
        """Test generating a spider plot."""
        self.mock_visualizer.spider_plot.return_value = None

        self.mock_visualizer.spider_plot(
            normalize=True,
            evaluation_type='autoeval',
            plot_type="tutor",
            plot_name="spider_plot_tutor.png"
        )

        # Verify the method was called with correct arguments
        self.mock_visualizer.spider_plot.assert_called_once_with(
            normalize=True,
            evaluation_type='autoeval',
            plot_type="tutor",
            plot_name="spider_plot_tutor.png"
        )

    def test_user_interaction(self):
        """Test enabling user interaction mode."""
        self.mock_visualizer.user_interaction.return_value = None

        self.mock_visualizer.user_interaction(normalize=True)

        # Verify the method was called with correct arguments
        self.mock_visualizer.user_interaction.assert_called_once_with(normalize=True)

if __name__ == '__main__':
    unittest.main()
