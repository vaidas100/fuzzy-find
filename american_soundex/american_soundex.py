"""Python implementation of the American Soundex phonetic algorithm
for indexing names by sound.

Reference: https://en.wikipedia.org/wiki/Soundex#American_Soundex

American Soundex:

The Soundex code for a name consists of
a letter followed by three numerical digits:
the letter is the first letter of the name,
and the digits encode the remaining consonants.
Consonants at a similar place of articulation
share the same digit so, for example,
the labial consonants B, F, P, and V are
each encoded as the number 1.

The correct value can be found as follows:

1. Retain the first letter of the name and
drop all other occurrences of a, e, i, o, u, y, h, w.

2. Replace consonants with digits as follows (after the first letter):
  * b, f, p, v → 1
  * c, g, j, k, q, s, x, z → 2
  * d, t → 3
  * l → 4
  * m, n → 5
  * r → 6

3. If two or more letters with the same number
are adjacent in the original name (before step 1),
only retain the first letter;
also two letters with the same number separated by 'h' or 'w'
are coded as a single number,
whereas such letters separated by a vowel are coded twice.
This rule also applies to the first letter.

4. If you have too few letters in your word
that you can't assign three numbers,
append with zeros until there are three numbers.
If you have more than 3 letters,
just retain the first 3 numbers.

Using this algorithm, both "Robert" and "Rupert"
return the same string "R163" while "Rubin" yields "R150".
"Ashcraft" and "Ashcroft" both yield "A261" and not "A226"
(the chars 's' and 'c' in the name would receive
a single number of 2 and not 22 since an 'h' lies in between them).
"Tymczak" yields "T522" not "T520"
(the chars 'z' and 'k' in the name are coded
as 2 twice since a vowel lies in between them).
"Pfister" yields "P236" not "P123"
(the first two letters have the same number
and are coded once as 'P'),
and "Honeyman" yields "H555".

Usage:
    from american_soundex import AmericanSoundex

    word_code = AmericanSoundex.get_code_from_bytes(word)
"""

import logging

logger = logging.getLogger()

__version__ = '1.0'
__author__ = 'Vaidotas Senkus <vaidas100@gmail.com>'

consonant_to_digit_mapping = {
    b'bfpv': b'1',
    b'cgjkqsxz': b'2',
    b'dt': b'3',
    b'l': b'4',
    b'mn': b'5',
    b'r': b'6',
}


class AmericanSoundex:

    @staticmethod
    def get_code_from_bytes(text):
        """Generate American Soundex code for given text.
        :param text: Text.
        :return: American Soundex code.
        """

        # Convert the word to lower case
        text = text.lower()

        # 1. Retain the first letter of the name and
        # drop all other occurrences of a, e, i, o, u, y, h, w.
        first_letter = text[0:1]
        text_without_first_letter = text[1:len(text)]
        text_without_first_letter = AmericanSoundex.replace_bytes(
            text_without_first_letter, b"aeiouy", b"."
        )
        text = first_letter + text_without_first_letter

        # 2. Replace consonants with digits as follows (after the first letter):
        #   * b, f, p, v → 1
        #   * c, g, j, k, q, s, x, z → 2
        #   * d, t → 3
        #   * l → 4
        #   * m, n → 5
        #   * r → 6
        for consonant in consonant_to_digit_mapping:
            text = AmericanSoundex.replace_bytes(
                text, consonant, consonant_to_digit_mapping[consonant]
            )

        # 3. If two or more letters with the same number
        # are adjacent in the original name (before step 1),
        # only retain the first letter;
        # also two letters with the same number separated by 'h' or 'w'
        # are coded as a single number,
        # whereas such letters separated by a vowel are coded twice.
        # This rule also applies to the first letter.
        for i in [b"1", b"2", b"3", b"4", b"5", b"6"]:
            text = text.replace(i + i, i)
            text = text.replace(i + b"h" + i, i)
            text = text.replace(i + b"w" + i, i)

        text = b"+" + text[1:len(text)+1]  # protect first letter 'h' or 'w'
        text = AmericanSoundex.replace_bytes(
            text, b"hw.", b""
        )

        # 4. If you have too few letters in your word
        # that you can't assign three numbers,
        # append with zeros until there are three numbers.
        # If you have more than 3 letters,
        # just retain the first 3 numbers.
        text = text + b"000"
        text = text[:4]

        text = first_letter + text[1:len(text)+1]

        return text.upper()

    @staticmethod
    def replace_bytes(text, from_bytes, to_bytes):
        """Translate bytes."""
        for i in range(0, len(from_bytes)):
            text = text.replace(from_bytes[i:i + 1], to_bytes)
        return text
