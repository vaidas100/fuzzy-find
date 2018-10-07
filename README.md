# tesonet-word-search

CLI tool that finds phrases in a given text file.

Returns the top unique 5 matched words.

Search phrase (single word) can be misspelled.

For word matching and shoring uses:

1. American Soundex algorithm:
    https://en.wikipedia.org/wiki/Soundex#American_Soundex
2. The Levenshtein distance:
    https://en.wikipedia.org/wiki/Levenshtein_distance
3. Length difference

### Usage

    usage: find.py [-h] [-l {ERROR,DEBUG}] file_path phrase

    positional arguments:
      file_path             Text file path.
      phrase                Search phrase.

    optional arguments:
      -h, --help            Show this help message and exit.
      -l {ERROR,DEBUG}, --logging_level {ERROR,DEBUG}
                            Logging level.

### Sample usage

    $ python3 ./find.py wiki_lt.txt lituania

### Sample output

    Lithuania
    Lietuva
    Lithuanian
    Latvia
    Lithuanians

### Testing

    $ python3 ./test.py
