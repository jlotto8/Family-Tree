import unittest
from io import StringIO
from unittest.mock import patch
from data_handling import read_data, validate_relationships
from person import Person

class TestDataHandling(unittest.TestCase):
    def setUp(self):
        self.csv_data = """ID,Name,Gender,Birth Date,Death Date,Spouse ID,Children IDs
1,John Doe,M,1990,,2,3;4
2,Jane Smith,F,1988,,1,
3,Child One,M,2010,,,
4,Child Two,F,2012,,,
"""
    
    def test_read_and_validate_data(self):
        csv_file1 = StringIO(self.csv_data)
        csv_file2 = StringIO(self.csv_data)

        # Separate patches for read_data and validate_relationships
        with patch('builtins.open', return_value=csv_file1):
            people = read_data("dummy_filename.csv")

        with patch('builtins.open', return_value=csv_file2):
            validate_relationships("dummy_filename.csv", people)

        self.assertEqual(len(people), 4)
        self.assertIsInstance(people[1], Person)
        self.assertEqual(people[2].spouse, people[1])
        self.assertEqual(len(people[1].children), 2)

if __name__ == '__main__':
    unittest.main()
