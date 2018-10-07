"""The FileChunkReader class reads file in chunks.

Usage:
    from file_chunk_reader import FileChunkReader

    file_chunk_reader = FileChunkReader(file_path)
    fifth_file_chunk_text = file_chunk_reader.get_chunk(4)
    fileChunkReader.close()
"""

import math
import os
import re
import logging

logger = logging.getLogger()

__version__ = '1.0'
__author__ = 'Vaidotas Senkus <vaidas100@gmail.com>'


class FileChunkReader:

    def __init__(self, file_path, chunk_size=1000000):
        """Open file and calculate chunk count.
        :param file_path: File path.
        :param chunk_size: File chunk size. Defaults to 1 MB.
        """
        try:
            self.file_path = os.path.abspath(file_path)
            self.file_size = os.path.getsize(file_path)
            self.file_handle = open(file_path, 'rb')
        except FileNotFoundError:
            logger.error("Can't read file: %s" % file_path)
            exit(1)
        self.chunk_size = chunk_size
        self.chunk_count = math.ceil(self.file_size / chunk_size)
        self.chunk_number_first = 0
        self.chunk_number_last = self.chunk_count - 1

    def get_chunk(self, chunk_number):
        """Get file chunk text.
        :param chunk_number: Chunk number.
        :return: Text of chunk.
        """
        self.file_handle.seek(chunk_number * self.chunk_size)
        if chunk_number < self.chunk_number_first or chunk_number > self.chunk_number_last:
            return b""
        chunk_text = self.file_handle.read(self.chunk_size)
        return chunk_text

    def get_chunk_with_shift_depending_on_spaces(self, chunk_number):
        """Get file chunk text.
        Preserve word from cutting to peaces in separate chunks.
        Chunk starting text till spaces goes to previous chunk.
        :param chunk_number: Chunk number.
        :return: Text of chunk.
        """
        # Get file chunk text.
        chunk_text = self.get_chunk(chunk_number)
        # Remove starting text till space.
        if chunk_number > self.chunk_number_first:
            chunk_text = re.sub(
                b"^[^\s]*\s+",
                b"",
                chunk_text
            )
        # Add tailing from next chunk till space.
        if chunk_number != self.chunk_number_last:
            next_chunk_text = self.get_chunk(chunk_number + 1)
            match = re.match(
                b"^[^\s]*\s+",
                next_chunk_text
            )
            if match:
                chunk_text = chunk_text + match.group(0)
        return chunk_text

    def close(self):
        """Close file."""
        self.file_handle.close()
