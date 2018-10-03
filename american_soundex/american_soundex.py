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
and "Honeyman" yields "H555"."""

import logging
import re

logger = logging.getLogger()

__version__ = '1.0'
__author__ = 'Vaidotas Senkus <vaidas100@gmail.com>'

digit_to_consonant_mapping = {
    '1': 'bfpv',
    '2': 'cgjkqsxz',
    '3': 'dt',
    '4': 'l',
    '5': 'mn',
    '6': 'r'
}
consonant_to_digit_mapping = {}
for digit in digit_to_consonant_mapping:
    consonant_list = digit_to_consonant_mapping[digit]
    for consonant in consonant_list:
        consonant_to_digit_mapping[consonant] = digit


class AmericanSoundex:

    @staticmethod
    def get_code(text):
        """Generate American Soundex code for given text.
        :param text: Text.
        :return: American Soundex code.
        """

        # Convert bytes to string
        if isinstance(text, (bytes, bytearray)):
            success = False
            for encoding in ["utf-8", "latin_1", "ascii"]:
                try:
                    decoded = text.decode(encoding)
                    text = decoded
                    logger.debug("Bytes decoded with %s encoding successfully." % encoding)
                    success = True
                    break
                except:
                    logger.debug("Bytes decoding with %s encoding failed." % encoding)
            if not success:
                logger.error("Can't decode bytes to string")
                exit(1)

        # Convert the word to lower case
        text = text.lower()

        # 3. If two or more letters with the same number
        # are adjacent in the original name (before step 1),
        # only retain the first letter;
        # also two letters with the same number separated by 'h' or 'w'
        # are coded as a single number,
        # whereas such letters separated by a vowel are coded twice.
        # This rule also applies to the first letter.
        for digit in digit_to_consonant_mapping:
            consonants = digit_to_consonant_mapping[digit]
            # "Pfister" - first two letters have the same number and are coded once as 'P':
            # pfister
            # -->
            # pister
            text = re.sub(
                r"([%s])[%s]+" % (consonants, consonants),
                r"\1",
                text
            )
            # "Ashcraft" - chars 's' and 'c' in the name would receive
            # a single number since an 'h' lies in between them:
            # ashcraft
            # -->
            # asraft
            text = re.sub(
                r"([%s])[hw][%s]" % (consonants, consonants),
                r"\1",
                text
            )

        # 1. Retain the first letter of the name and
        # drop all other occurrences of a, e, i, o, u, y, h, w.
        first_letter = text[0]
        text_without_first_letter = re.sub(
            r"[aeiouyhw]*",
            '',
            text[1:]
        )

        # 2. Replace consonants with digits as follows (after the first letter):
        #   * b, f, p, v → 1
        #   * c, g, j, k, q, s, x, z → 2
        #   * d, t → 3
        #   * l → 4
        #   * m, n → 5
        #   * r → 6
        for consonant in consonant_to_digit_mapping:
            digit = str(consonant_to_digit_mapping[consonant])
            text_without_first_letter = text_without_first_letter.replace(consonant, digit)

        text = first_letter + text_without_first_letter

        # 4. If you have too few letters in your word
        # that you can't assign three numbers,
        # append with zeros until there are three numbers.
        # If you have more than 3 letters,
        # just retain the first 3 numbers.
        text = text + "000"
        text = text[:4]

        return text.upper()
