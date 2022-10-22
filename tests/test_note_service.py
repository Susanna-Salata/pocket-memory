import unittest
from services.note_service import NoteService
from schemas.note_schema import NoteAuth


class TestNoteService(unittest.TestCase):
    def setUp(self):
        print("Setup code. Lets create a new db mock if there is no")
        self.note_service = NoteService()
        self.note = NoteAuth(name="note", records=[], tags=[])

    def test_create_note(self):
        self.note_service.create_note(note=self.note)

    def test_create_str_obj(self):
        new_file = str("test_file")
        self.assertEqual(isinstance(new_file, str), True)


if __name__ == '__main__':
    unittest.main()