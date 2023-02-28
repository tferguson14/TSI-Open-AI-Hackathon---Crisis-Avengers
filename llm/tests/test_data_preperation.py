import unittest
import json
import os
import tempfile
from code.data_preperation import DataProcessor


class TestDataPreparation(unittest.TestCase):
    def setUp(self):
        self.keyword_dict = {
            "positive": ["good", "great"],
            "negative": ["bad"],
        }
        self.ids_to_skip_file = "tests/test_ids_to_skip.txt"
        self.data = {
                    "1": {"_c0": "1", "Themes": "good things", "Text": "This is a good   item."},
                    "2": {"_c0": "2", "Themes": "bad things", "Text": "\nThis is\n\na bad <HTML>\nitem.\n\n"},
                    "3": {"_c0": "3", "Themes": "great things", "Text": "This is a great item."},
                }

    def test_prep_items(self):
        # Write data to temporary file
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(self.data, f)

        # Initialize data processor
        data_processor = DataProcessor(f.name, self.keyword_dict, self.ids_to_skip_file)

        # Call prep_items method
        results = data_processor.prep_items()

        # Define expected results
        expected_results = [
            {
                "_c0": "1",
                "Themes": "good things",
                "Text": "This is a good item.",
                "keyword": "positive",
            },
            {
                "_c0": "2",
                "Themes": "bad things",
                "Text": "This is a bad item.",
                "keyword": "negative",
            },

        ]

        # Assert that expected_results length is 1 less than results length
        self.assertEqual(len(results), len(expected_results))

         # Assert that the Text in expected_results matches the cleaned up Text in results
        for i in range(len(results)):
            self.assertEqual(results[i]["Text"], expected_results[i]["Text"])



    def test_load_ids_to_skip(self):
        processor = DataProcessor("dummy_file.json", self.keyword_dict, self.ids_to_skip_file)
        processor.load_ids_to_skip()
        self.assertEqual(len(processor.c0_set_for_file), 1)
        for item in processor.c0_set_for_file:
            self.assertTrue(item.isdigit())

    #def tearDown(self):
        # clean up ids_to_skip file
        #with open(self.ids_to_skip_file, "w") as f:
        #    f.write("")

if __name__ == "__main__":
    unittest.main()
