"""CLI tool that finds phrases in a given text file.
Software returns the top unique 5 matched words.
Search phrase (single word) can be misspelled.
For word matching and scoring software uses:
1. American Soundex algorithm:
    https://en.wikipedia.org/wiki/Soundex#American_Soundex
2. The Levenshtein distance:
    https://en.wikipedia.org/wiki/Levenshtein_distance
3. Length difference

Sample usage:
    $ python3 find.py wiki_lt.txt lituania

Sample output:
    Lithuania
    Lietuva
    Lithuanian
    Latvia
    Lithuanians

"""

import argparse
import glob
import itertools
import json
import Levenshtein
import logging
import multiprocessing
import os
import shutil
import sys
import time

logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s'
)
logger = logging.getLogger()

# ensure python 3 is used
if sys.version_info[0] < 3:
    logger.error("Must be using Python 3")
    exit(1)

from file_chunk_reader import FileChunkReader
from american_soundex import AmericanSoundex

program_dir, program_name = os.path.split(os.path.realpath(__file__))
program_name, program_ext = os.path.splitext(program_name)

__version__ = '1.0'
__author__ = 'Vaidotas Senkus <vaidas100@gmail.com>'


def process_text(args, process_num, file_chunk_num, file_chunk_text):

    logger.setLevel(args.logging_level)  # logging fix for Windows OS

    # search for words, soundex codes and levenshtein distance
    words = {}
    word = b""
    for i in range(0, len(file_chunk_text)):
        byte = file_chunk_text[i:i+1]
        # same word while alphabetic characters
        if byte.isalpha():
            word += byte
        # word found if not alphabetic character
        elif word:
            # check only first word occurrence
            if word not in words:
                # get soundex code
                word_code = AmericanSoundex.get_code_from_bytes(word)
                # first letter of soundex code should match
                if word_code[0:1] == args.phrase_code[0:1]:
                    # get levenshtein distance of soundex codes
                    levenshtein_distance = Levenshtein.distance(
                        word_code,
                        args.phrase_code
                    )
                    # get length difference
                    length_difference = abs(len(word) - len(args.phrase))
                    # to get word score
                    # combine levenshtein distance of soundex codes with length difference
                    # (result is float)
                    word_score = levenshtein_distance + length_difference / 10
                    words[word.decode(encoding='ascii')] = word_score
            word = b""

    # leave top unique 5 matched words
    words_5_best = {}
    for word in sorted(words.keys(), key=words.get)[:5]:
        words_5_best[word] = words[word]

    logger.debug(
        "CPU:{process_num} CHUNK:{file_chunk_num} WORDS:\n{words}".format(
            process_num=process_num,
            file_chunk_num=file_chunk_num,
            words=json.dumps(words_5_best, indent=3)
        )
    )

    # write result to JSON file
    result_file_path = os.path.join(
        args.results_dir,
        "%s.json" % file_chunk_num
    )
    with open(result_file_path, 'w') as result_file:
        result_file.write(json.dumps(words_5_best, indent=3))


def worker(args, process_num, file_chunk_nums):
    for file_chunk_num in file_chunk_nums:

        # get file chunk text
        file_chunk_reader = FileChunkReader(args.file_path)
        file_chunk_text = file_chunk_reader.get_chunk_with_shift_depending_on_spaces(file_chunk_num)
        file_chunk_reader.close()

        # process chunk text
        process_text(args, process_num, file_chunk_num, file_chunk_text)


if __name__ == '__main__':

    start_time = time.time()

    # parse command-line arguments
    parser = argparse.ArgumentParser(
        description="""CLI tool that finds phrases in a given text file.
Returns the top unique 5 matched words.
Search phrase (single word) can be misspelled.""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False
    )
    parser.add_argument(
        '-h',
        '--help',
        action='help',
        default=argparse.SUPPRESS,
        help='Show this help message and exit.'
    )
    parser.add_argument(
        '-l',
        '--logging_level',
        dest='logging_level',
        help='Logging level.',
        choices=['ERROR', 'DEBUG'],
        default='ERROR',
    )
    parser.add_argument(
        "file_path",
        help="Text file path.",
    )
    parser.add_argument(
        "phrase",
        help="Search phrase.",
    )
    args = parser.parse_args()
    if args.logging_level == "DEBUG":
        args.logging_level = logging.DEBUG
    else:
        args.logging_level = logging.ERROR
    logger.setLevel(args.logging_level)
    if os.path.exists(args.file_path):
        args.file_path = os.path.abspath(args.file_path)
        args.file_dir = os.path.dirname(args.file_path)
        args.results_dir = os.path.join(args.file_dir, 'results')
    else:
        logger.error("File not found: %s" % args.file_path)
        exit(1)
    try:
        # convert phrase to bytes
        args.phrase = args.phrase.encode()
        # get phrase soundex code
        args.phrase_code = AmericanSoundex.get_code_from_bytes(args.phrase)
    except:
        logger.error("Can't convert given phrase to bytes: %s" % args.phrase)
        exit(1)

    # count file chunks
    file_chunk_reader = FileChunkReader(args.file_path)
    chunk_nums = list(range(0, file_chunk_reader.chunk_count))
    file_chunk_reader.close()
    if file_chunk_reader.chunk_count > 1:
        logger.debug(
            'Splitting file to {chunks_count} chunks'.format(
                chunks_count=file_chunk_reader.chunk_count,
            )
        )

    # create empty dir for results
    if os.path.exists(args.results_dir):
        shutil.rmtree(args.results_dir)
    os.mkdir(args.results_dir)

    # split work for each CPU
    processes_num = multiprocessing.cpu_count()
    procs = []
    proc = multiprocessing.Process
    for process_num in range(1, processes_num + 1):
        proc = multiprocessing.Process(
            target=worker,
            args=(
                args,
                process_num,
                itertools.islice(
                    chunk_nums,
                    process_num - 1,
                    None,
                    processes_num
                ),
            )
        )
        procs.append(proc)
        proc.start()
    for proc in procs:
        proc.join()

    # combine results
    words_combined = {}
    for file in glob.glob(args.results_dir + "/*.json"):
        with open(file) as f:
            words_current = json.load(f)
        for word in words_current:
            words_combined[word] = words_current[word]

    # print top unique 5 matched words
    best_5_words = sorted(words_combined.keys(), key=words_combined.get)[:5]
    for word in best_5_words:
        print(word)

    elapsed_time = time.time() - start_time
    logger.debug('Done in {elapsed:.2f}s'.format(
        elapsed=elapsed_time,
    ))
