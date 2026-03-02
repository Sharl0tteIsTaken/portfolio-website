"""
A modified version of morse code converter for website demo purpose.
"""


from string import ascii_letters, digits, punctuation
from typing import Literal

from demo_morse_code_converter.convert_tables import ConvertTables

EXCLUDE = r'''#%*<>[\]^`{|}~'''
for symbols in EXCLUDE:
    SYMBOLS = punctuation.replace(symbols, "")
INCLUDE_WORDS = ascii_letters + digits + SYMBOLS

type MorseCode = Literal[
    "dot", "dash", "code_space", "letter_space", "word_space"
    ]
type MorseValue = str


class Converter:
    """
    where the convertion is done.
    """
    def __init__(self) -> None:
        """
        Explanation
        -----------
        dot (dot or dit): short mark, one time unit long.
        dash (dash or dah): long mark, three time units long.
        code_space: inter-element gap between the dits and dahs within
            a character, one time unit long.
        letter_space: short gap between letters, three time units long.
        word_space: medium gap between words, seven time units long.
        """
        self.dot = ConvertTables.dot
        self.dash = ConvertTables.dash
        self.code_space = ConvertTables.code_space
        self.letter_space = ConvertTables.letter_space
        self.word_space = ConvertTables.word_space

        # for demo only
        self.history = ""

        self.codes = self.morsecode_regulator()

    def morsecode_regulator(self) -> dict[str, str]:
        """
        Check if any value in convert table(3 dictionaries: letters,
        numbers, punctuations) is not acceptable codes(dot or dash)
        - if any: raise error with message contain key-value pair in
            convert table that will causes error.
        - if not: merge letter, numbers and punctuations from convert
            table into a single dictionary.

        Returns
        -------
        dict[str, str]
            Concatenated convert tables, morse code key-value pairs are
            all suitable for the following steps.
        """
        def unpack_dict(**kwargs: dict) -> str:
            """
            Take error message from Converter.morsecode_regulator() when
            ConvertTables contain unsupported code, returns formatted
            string contain the letter, position, morse code caused the
            error.

            Returns
            -------
            str
                The letter, position, and which morse code caused the
                error.
            """
            unpacked = ''
            for letter in kwargs:  # pylint: disable=consider-using-dict-items
                for position in kwargs[letter]:
                    unpacked = unpacked + (
                        f"at letter: '{letter}', "
                        f"position(left to right): {position}, "
                        f"unacceptable: '{kwargs[letter][position]}'" + '\n'
                        )
            return unpacked

        codes = (
            ConvertTables.letters
            | ConvertTables.numbers
            | ConvertTables.punctuations
            )
        unacceptable = {}
        for key in codes:
            error_place = {}
            for idx, letter in enumerate(codes[key]):
                if letter != self.dot and letter != self.dash:
                    error_place[idx+1] = letter
            if error_place:
                unacceptable[key] = error_place
        if unacceptable:
            raise ValueError(
                "the morse code convert tables contain values unacceptable for"
                f"convertion, acceptable: dot='{self.dot}', dash='{self.dash}'"
                f"nall unacceptable:\n{unpack_dict(**unacceptable)}"
                )
        return codes

    def update_configs(
        self, *, configs: dict[MorseCode, MorseValue] | None
    ) -> None:
        """
        Configures the output morse code with nearly every aspect of the
        code. Configs should only take argument pass in by
        Organizer.commands().

        Parameters
        ----------
        configs: dict[MorseCode, MorseValue] | None
            The morse code value to use.
        """
        if configs is None:
            return

        for key, val in self.codes.items():
            temp = val.replace(self.dot, configs['dot'])
            self.codes[key] = temp.replace(self.dash, configs['dash'])

        self.dot = configs['dot']
        self.dash = configs['dash']
        self.code_space = configs['code_space']
        self.letter_space = configs['letter_space']
        self.word_space = configs['word_space']

    def convert(self, user_input: str) -> str:
        """
        Takes user input and convert it into morse code.

        Parameters
        ----------
        user_input: str
            Text to convert into morse code.

        Returns
        -------
        str
            String converted to morse code.
        """
        output = ''
        for letter in user_input:
            if letter == '\r':
                continue
            if letter == '\n':
                output += '\n'
            elif letter == ' ':
                output = output.rstrip(self.letter_space) + self.word_space
            elif letter in INCLUDE_WORDS:
                code = list(self.codes[letter.upper()])
                code_space = self.code_space.join(code)
                output = output + code_space + self.letter_space
            else:
                output += f'(invalid_letter:{letter})'
        return output.rstrip(self.letter_space)
