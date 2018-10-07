# tesonet-word-search

CLI tool that finds phrases in a given text file.

Software returns the top unique 5 matched words.

Search phrase (single word) can be misspelled.

For word matching and scoring software uses:

1. American Soundex algorithm:

    https://en.wikipedia.org/wiki/Soundex#American_Soundex

2. The Levenshtein distance:

    https://en.wikipedia.org/wiki/Levenshtein_distance

3. Length difference

## Getting Started

### Prerequisites

Install:
1. Python 3 (recommended 3.6.6):

    https://www.python.org/

2. python-Levenshtein module:

    https://pypi.org/project/python-Levenshtein/

### Source code

Clone or download:

    https://github.com/vaidas100/tesonet-word-search

### Testing

To ensure that everything is working run:

    $ python3 ./test.py

Output should look like this:

    ...
    ----------------------------------------------------------------------
    Ran 3 tests in 0.001s
    
    OK

## Usage

### Help

To get help run:

    $ python3 ./find.py --help

You should see information about arguments:

    usage: find.py [-h] [-l {ERROR,DEBUG}] file_path phrase

    positional arguments:
      file_path             Text file path.
      phrase                Search phrase.

    optional arguments:
      -h, --help            Show this help message and exit.
      -l {ERROR,DEBUG}, --logging_level {ERROR,DEBUG}
                            Logging level.

### Sample usage

You can use sample text file like this:

    $ python3 ./find.py wiki_lt.txt lituania

And you get 5 best matching words:

    Lithuania
    Lietuva
    Lithuanian
    Latvia
    Lithuanians


### Author

Vaidotas Senkus
<vaidas100@gmail.com>
