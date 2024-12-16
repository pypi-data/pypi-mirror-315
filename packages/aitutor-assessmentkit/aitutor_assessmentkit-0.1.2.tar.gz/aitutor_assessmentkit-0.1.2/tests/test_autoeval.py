import sys
import os
import tempfile
import json
import unittest

# Import necessary modules and the AutoEvaluation classes
from aitutor_assessmentkit.autoevaluator import (
    AutoProvidingGuidanceEvaluator,
    AutoCoherenceEvaluator,
    AutoHumanlikenessEvaluator,
    AutoTutorToneEvaluator,
    AutoMistakeIdentificationEvaluator,
    AutoMistakeLocationEvaluator,
    AutoRevealingOfTheAnswerEvaluator,
    AutoActionabilityEvaluator,
    AutoEvaluationReport
)

class TestAutoEvaluationReport(unittest.TestCase):

    def setUp(self):
        # Sample JSON data to simulate input
        self.sample_data = [{
                "conversation_id": "930-b01cb51d-748d-460c-841a-08e4d5cd5cc7",
                "conversation_history": "Tutor: Hi, could you please provide a step-by-step solution for the question below? The question is: Elliott is trying to walk 10,000 steps a day. He finished half of his steps on his walks to and from school and did another 1,000 steps going for a short walk with his friend. He also went for a short jog around the block and realized that after he had finished his jog, he only had 2,000 steps left to take. How many steps did Elliott take during his jog?\u00a0\n\u00a0Student: Elliott finished half of his steps on his walks to and from school, so he took 10,000/2 = 5000 steps during these walks.\nAdding the 1,000 steps he took with his friend, he has taken 5000+1000 = 6000 steps.\nSubtracting 6000 from his goal of 10,000, he has 10,000-6000 = 4000 steps left to take.\nTherefore, he took 4000 steps during his jog.\u00a0\n\u00a04000\u00a0\n\u00a0Tutor: can you tell me how you got to your answer?\u00a0\n\u00a0Student: Sure. I started by figuring out how many steps Elliott had taken before his jog. I knew he had finished half of his steps on his walks to and from school so I calculated that he had taken 10000/2 = 5000 steps during these walks. Then I added the 1000 steps he took with his friend so I had taken 5000+1000 = 6000 steps. After that I subtracted 6000 from his goal of 10000 so I had 10000-6000 = 4000 steps left to take. This meant that he had taken 4000 steps during his jog.",
                "Data": "MathDial",
                "Split": "test",
                "Topic": "Not Available",
                "Ground_Truth_Solution": "Elliott took half of his steps on his school journey, which was 10,000 steps / 2 = 5,000 steps.\nAdding this to his short walk means he has taken 5,000 + 1,000 = 6,000 steps.\nHe only has 2,000 steps left, which means that during the day, he has taken 10,000 goal steps \u2013 2,000 remaining steps = 8,000 steps.\nThe difference between these is therefore the steps he took during his jog, which was 8,000 total steps \u2013 6,000 steps on his school walks and short walks = 2,000 steps.\n 2000",
                "anno_llm_responses": {
                "model": {
                    "response": "It looks like you're on the right track, but remember that Elliott still had 2,000 steps left to take *after* his jog.",
                    }}}
            ]

        # Create temporary directories and files
        self.temp_output_dir = tempfile.TemporaryDirectory()
        self.temp_input_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")

        # Write sample data to the temporary JSON file
        with open(self.temp_input_file.name, 'w') as f:
            json.dump(self.sample_data, f)

        self.temp_input_path = self.temp_input_file.name

    def tearDown(self):
        # Clean up temporary files and directories
        self.temp_input_file.close()
        os.unlink(self.temp_input_file.name)
        self.temp_output_dir.cleanup()

    def test_generate_automated_evaluation_report_all_models(self):
        evaluator = AutoEvaluationReport(
            file_names=[self.temp_input_path],
            output_data_dir=self.temp_output_dir.name,
            tutor_models=['Novice', 'Expert'],
            num_conv_examples=-1,
        )

        report, data = evaluator.get_automated_evaluation_report_with_all_models(save_eval=True, save_report=True)

        # Assert that the report and data are not empty
        self.assertIsNotNone(report)
        self.assertIsNotNone(data)

        # Additional checks for report structure
        self.assertIn('model', report.columns)
        self.assertIn('evaluation_score', report.columns)

    def test_generate_automated_evaluation_report_best_models(self):
        evaluator = AutoEvaluationReport(
            file_names=[self.temp_input_path],
            output_data_dir=self.temp_output_dir.name,
            tutor_models=['Novice', 'Expert'],
            num_conv_examples=-1,
        )

        report, data = evaluator.get_automated_evaluation_report_with_best_models(save_eval=True, save_report=True)

        # Assert that the report and data are not empty
        self.assertIsNotNone(report)
        self.assertIsNotNone(data)

        # Additional checks for report structure
        self.assertIn('model', report.columns)
        self.assertIn('evaluation_score', report.columns)

if __name__ == '__main__':
    unittest.main()