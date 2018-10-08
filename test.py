import logging
import os
import sys
import unittest
from unittest import TestCase

from american_soundex import AmericanSoundex
from file_chunk_reader import FileChunkReader

logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s'
)
logger = logging.getLogger()

# ensure python 3 is used
if sys.version_info[0] < 3:
    logger.error("Must be using Python 3")
    exit(1)

root_dir = os.path.abspath(os.path.dirname(__file__))


class TestAmericanSoundex(TestCase):

    def test_get_american_soundex_code(self):
        test_data = {
            b"Robert": b"R163",
            b"Rupert": b"R163",
            b"Rubin": b"R150",
            b"Ashcraft": b"A261",
            b"Ashcroft": b"A261",
            b"Tymczak": b"T522",
            b"Pfister": b"P236",
            b"Honeyman": b"H555",
        }
        for text in test_data:
            expected = test_data[text]
            result = AmericanSoundex.get_code_from_bytes(text)
            self.assertEqual(
                expected,
                result,
                "AmericanSoundex.get_code_from_bytes(%s) returns %s instead of %s" % (
                    text,
                    result,
                    expected
                )
            )


class TestFileChunkReader(TestCase):

    def test_get_chunk(self):
        file_path = os.path.join(root_dir, "file_chunk_reader/__init__.py")
        fcr = FileChunkReader(file_path, chunk_size=10)
        file_chunk_text0 = fcr.get_chunk(0)
        file_chunk_text1 = fcr.get_chunk(1)
        fcr.close()
        self.assertEqual(file_chunk_text0, b"from .file")
        self.assertEqual(file_chunk_text1, b"_chunk_rea")

    def test_get_chunk_with_shift_depending_on_spaces(self):
        file_path = os.path.join(root_dir, "file_chunk_reader/__init__.py")
        fcr = FileChunkReader(file_path, chunk_size=20)
        file_chunk_text0 = fcr.get_chunk_with_shift_depending_on_spaces(0)
        file_chunk_text1 = fcr.get_chunk_with_shift_depending_on_spaces(1)
        fcr.close()
        self.assertEqual(file_chunk_text0, b"from .file_chunk_reader ")
        self.assertEqual(file_chunk_text1, b"import FileChunkReader\n")


if __name__ == '__main__':
    unittest.main()
