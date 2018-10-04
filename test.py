from unittest import TestCase

from american_soundex import AmericanSoundex
from file_chunk_reader import FileChunkReader

import time

# Compare string vs bytes AmericanSoundex.get_code... methods

number = 10000

start = time.time()
for x in range(number + 1):
    aaa = AmericanSoundex.get_code_from_string("Honeyman")
elapsed = time.time() - start
print("AmericanSoundex.get_code_from_string %s times done in %s s" % (
    number,
    elapsed
))

start = time.time()
for x in range(number + 1):
    aaa = AmericanSoundex.get_code_from_bytes(b"Honeyman")
elapsed = time.time() - start
print("AmericanSoundex.get_code_from_bytes %s times done in %s s" % (
    number,
    elapsed
))


class TestAmericanSoundex(TestCase):
    def test_get_american_soundex_code(self):
        test_data = {
            "Robert": "R163",
            "Rupert": "R163",
            "Rubin": "R150",
            "Ashcraft": "A261",
            "Ashcroft": "A261",
            "Tymczak": "T522",
            "Pfister": "P236",
            "Honeyman": "H555",
        }
        for text in test_data:
            expected = test_data[text]
            result = AmericanSoundex.get_code_from_string(text)
            self.assertEqual(
                expected,
                result,
                "AmericanSoundex.get_code_from_string(%s) returns %s instead of %s" % (
                    text,
                    result,
                    expected
                )
            )
        test_data_bytes = {
            b"Robert": b"R163",
            b"Rupert": b"R163",
            b"Rubin": b"R150",
            b"Ashcraft": b"A261",
            b"Ashcroft": b"A261",
            b"Tymczak": b"T522",
            b"Pfister": b"P236",
            b"Honeyman": b"H555",
        }
        for text in test_data_bytes:
            expected = test_data_bytes[text]
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
