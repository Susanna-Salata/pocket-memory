import unittest
from models.models_mongo import Tag, File, Note
from uuid import UUID, uuid4
from pydantic import Field


class TestApp(unittest.TestCase):
    def setUp(self):
        print("Setup code. Lets create a new db mock if there is no")
        if not hasattr(self, "db"):
            self.db = {}

    def tearDown(self):
        print("Clear after test")
        self.db.clear()

    def test_create_file_obj(self):
        new_file = File()
        new_file.file = "test_file"
        self.assertEqual(isinstance(new_file, File), True)

    def test_create_str_obj(self):
        new_file = str("test_file")
        self.assertEqual(isinstance(new_file, str), True)


if __name__ == '__main__':
    unittest.main()