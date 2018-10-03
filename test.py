from unittest import TestCase
from file_chunk_reader import FileChunkReader


class TestFileChunkReader(TestCase):
    def test_get_chunk(self):
        file_path = "file_chunk_reader/__init__.py"
        fcr = FileChunkReader(file_path, chunk_size=10)
        file_chunk_text0 = fcr.get_chunk(0)
        file_chunk_text1 = fcr.get_chunk(1)
        fcr.close()
        self.assertEqual(file_chunk_text0, b"from .file")
        self.assertEqual(file_chunk_text1, b"_chunk_rea")

    def test_get_chunk_with_shift_depending_on_spaces(self):
        file_path = "file_chunk_reader/__init__.py"
        fcr = FileChunkReader(file_path, chunk_size=20)
        file_chunk_text0 = fcr.get_chunk_with_shift_depending_on_spaces(0)
        file_chunk_text1 = fcr.get_chunk_with_shift_depending_on_spaces(1)
        fcr.close()
        self.assertEqual(file_chunk_text0, b"from .file_chunk_reader ")
        self.assertEqual(file_chunk_text1, b"import FileChunkReader\n")
