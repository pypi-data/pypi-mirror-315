import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import tempfile

# Assuming the code you provided is inside a module named 'llm_evaluation'
from aitutor_assessmentkit.llmevaluator import LLMEvaluator

class TestLLMEvaluator(unittest.TestCase):

    @patch('aitutor_assessmentkit.llmevaluator.LLMEvaluator')
    def test_llm_model_initialization(self, MockLLMEvaluator):
        # Test the initialization of LLMEvaluator with mock inputs
        mock_evaluator = MagicMock()
        MockLLMEvaluator.return_value = mock_evaluator
        
        with tempfile.TemporaryDirectory() as temp_dir:
            evaluator = LLMEvaluator(
                llm_model_name="meta-llama/Meta-Llama-3.1-8B-Instruct",
                llm_model_parama={"max_tokens": 1024, "temperature": 0.0},
                evaluation_type='absolute',
                prompting_type='zero-shot',
                file_names=[os.path.join(temp_dir, "MRBench_V5.json")],  # Temporary file
                output_data_dir=temp_dir,  # Output directory is a temporary directory
                with_ref=False,
                ngpus=1,
                num_conv_examples=10
            )

            # Ensure the evaluator is initialized correctly
            self.assertEqual(evaluator.llm_model_name, "meta-llama/Meta-Llama-3.1-8B-Instruct")
            self.assertEqual(evaluator.llm_model_parama["max_tokens"], 1024)
            self.assertEqual(evaluator.llm_model_parama["temperature"], 0.0)
            self.assertEqual(evaluator.evaluation_type, 'absolute')
            self.assertEqual(evaluator.prompting_type, 'zero-shot')

    @patch('aitutor_assessmentkit.llmevaluator.LLMEvaluator.compute_mistake_identification')
    def test_compute_mistake_identification(self, mock_compute_mistake_identification):
        # Mock the return value of the compute_mistake_identification method
        mock_compute_mistake_identification.return_value = ({'Expert': 90, 'Llama31405B': 85}, None, None, None)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            evaluator = LLMEvaluator(
                llm_model_name="meta-llama/Meta-Llama-3.1-8B-Instruct",
                llm_model_parama={"max_tokens": 1024, "temperature": 0.0},
                evaluation_type='absolute',
                prompting_type='zero-shot',
                file_names=[os.path.join(temp_dir, "MRBench_V5.json")],  # Temporary file
                output_data_dir=temp_dir,  # Output directory is a temporary directory
                with_ref=False,
                ngpus=1,
                num_conv_examples=10
            )

            # Test the compute_mistake_identification function
            scores, _, _, _ = evaluator.compute_mistake_identification(tutor_models=['Expert', 'Llama31405B'])
            
            # Check if the mocked method returns the expected values
            self.assertEqual(scores['Expert'], 90)
            self.assertEqual(scores['Llama31405B'], 85)

    @patch('aitutor_assessmentkit.llmevaluator.LLMEvaluator.get_llm_evaluation_report')
    def test_get_llm_evaluation_report(self, mock_get_llm_evaluation_report):
        # Mock the return value of get_llm_evaluation_report method
        mock_get_llm_evaluation_report.return_value = {'Mistake_Identification': 90, 'Mistake_Location': 85}
        
        with tempfile.TemporaryDirectory() as temp_dir:
            evaluator = LLMEvaluator(
                llm_model_name="meta-llama/Meta-Llama-3.1-8B-Instruct",
                llm_model_parama={"max_tokens": 1024, "temperature": 0.0},
                evaluation_type='absolute',
                prompting_type='zero-shot',
                file_names=[os.path.join(temp_dir, "MRBench_V5.json")],  # Temporary file
                output_data_dir=temp_dir,  # Output directory is a temporary directory
                with_ref=False,
                ngpus=1,
                num_conv_examples=10
            )

            # Test the get_llm_evaluation_report function
            report = evaluator.get_llm_evaluation_report(
                tutor_models=['Novice', 'Expert'],
                dimensions=['Mistake_Identification', 'Mistake_Location'],
                save_eval=True,
                save_report=True
            )

            # Check if the report contains the expected values
            self.assertEqual(report['Mistake_Identification'], 90)
            self.assertEqual(report['Mistake_Location'], 85)

    @patch('aitutor_assessmentkit.llmevaluator.LLMEvaluator.save_llm_evaluation_report')
    def test_save_llm_evaluation_report(self, mock_save_llm_evaluation_report):
        # Mock the save_llm_evaluation_report method
        mock_save_llm_evaluation_report.return_value = None
        
        with tempfile.TemporaryDirectory() as temp_dir:
            evaluator = LLMEvaluator(
                llm_model_name="meta-llama/Meta-Llama-3.1-8B-Instruct",
                llm_model_parama={"max_tokens": 1024, "temperature": 0.0},
                evaluation_type='absolute',
                prompting_type='zero-shot',
                file_names=[os.path.join(temp_dir, "MRBench_V5.json")],  # Temporary file
                output_data_dir=temp_dir,  # Output directory is a temporary directory
                with_ref=False,
                ngpus=1,
                num_conv_examples=10
            )

            # Test the save_llm_evaluation_report function
            evaluator.save_llm_evaluation_report(save_file_name='bridge_3170_llm_evaluation_report.csv')
            
            # Ensure the save_llm_evaluation_report method was called
            mock_save_llm_evaluation_report.assert_called_once_with(save_file_name='bridge_3170_llm_evaluation_report.csv')


if __name__ == '__main__':
    unittest.main()
