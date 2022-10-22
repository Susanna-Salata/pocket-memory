import unittest
from services.record_service import RecordService
from schemas.record_schema import RecordAuth


class TestRecordService(unittest.TestCase):
    def setUp(self):
        print("Setup code. Lets create a new db mock if there is no")
        self.record_service = RecordService()
        self.record = RecordAuth(id = "bb32960c-052d-492d-a1b5-459e48ac7ce8",
                                 name = "record name",
                                 # birth_date = record.birth_date,
                                 address = "record address",
                                 phones = [],
                                 emails = []
        )

    def test_create_record(self):
        self.record_service.create_record(record=self.record)


if __name__ == '__main__':
    unittest.main()