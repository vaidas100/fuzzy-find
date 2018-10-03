from unittest import TestCase

from american_soundex import AmericanSoundex
from file_chunk_reader import FileChunkReader


class TestAmericanSoundex(TestCase):
    def test_get_american_soundex_code(self):
        test_data = {
            b"Robert": "R163",
            b"Rupert": "R163",
            b"Rubin": "R150",
            b"Ashcraft": "A261",
            b"Ashcroft": "A261",
            b"Tymczak": "T522",
            b"Pfister": "P236",
            b"Honeyman": "H555",
        }
        for text in test_data:
            self.assertEqual(
                AmericanSoundex.get_code(text),
                test_data[text]
            )


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