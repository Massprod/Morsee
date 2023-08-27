

class Morsee:
    """
    Class object which allows to encode|decode any Text into code Morse according to ITU-R M.1677-1 standard.

    International Morse Code ITU-R M.1677-1:
     1. The length of a dot is one unit
     2. A dash is three units
     3. The space between parts of the same letter is one unit
     4. The space between letters is three units
     5. The space between words is seven units
    """
    def __init__(self):
        self.dot: str = '.'
        self.line: str = '_'
        self.morse_encoding: dict[str: str] = {
            "a": f"{self.dot} {self.line}",
            "b": f"{self.line} {self.dot} {self.dot} {self.dot}",
            "c": f"{self.line} {self.dot} {self.line} {self.dot}",
            "d": f"{self.line} {self.dot} {self.dot}",
            "e": f"{self.dot}",
            "f": f"{self.dot} {self.dot} {self.line} {self.dot}",
            "g": f"{self.line} {self.line} {self.dot}",
            "h": f"{self.dot} {self.dot} {self.dot} {self.dot}",
            "i": f"{self.dot} {self.dot}",
            "j": f"{self.dot} {self.line} {self.line} {self.line}",
            "k": f"{self.line} {self.dot} {self.line}",
            "l": f"{self.dot} {self.line} {self.dot} {self.dot}",
            "m": f"{self.line} {self.line}",
            "n": f"{self.line} {self.dot}",
            "o": f"{self.line} {self.line} {self.line}",
            "p": f"{self.dot} {self.line} {self.line} {self.dot}",
            "q": f"{self.line} {self.line} {self.dot} {self.line}",
            "r": f"{self.dot} {self.line} {self.dot}",
            "s": f"{self.dot} {self.dot} {self.dot}",
            "t": f"{self.line}",
            "u": f"{self.dot} {self.dot} {self.line}",
            "v": f"{self.dot} {self.dot} {self.dot} {self.line}",
            "w": f"{self.dot} {self.line} {self.line}",
            "x": f"{self.line} {self.dot} {self.dot} {self.line}",
            "y": f"{self.line} {self.dot} {self.line} {self.line}",
            "z": f"{self.line} {self.line} {self.dot} {self.dot}",
            "1": f"{self.dot} {self.line} {self.line} {self.line} {self.line}",
            "2": f"{self.dot} {self.dot} {self.line} {self.line} {self.line}",
            "3": f"{self.dot} {self.dot} {self.dot} {self.line} {self.line}",
            "4": f"{self.dot} {self.dot} {self.dot} {self.dot} {self.line}",
            "5": f"{self.dot} {self.dot} {self.dot} {self.dot} {self.dot}",
            "6": f"{self.line} {self.dot} {self.dot} {self.dot} {self.dot}",
            "7": f"{self.line} {self.line} {self.dot} {self.dot} {self.dot}",
            "8": f"{self.line} {self.line} {self.line} {self.dot} {self.dot}",
            "9": f"{self.line} {self.line} {self.line} {self.line} {self.dot}",
            "0": f"{self.line} {self.line} {self.line} {self.line} {self.line}",
            " ": " ",
            ",": f"{self.line} {self.line} {self.dot} {self.dot} {self.line} {self.line}",
            ".": f"{self.dot} {self.line} {self.dot} {self.line} {self.dot} {self.line}",
            "?": f"{self.dot} {self.dot} {self.line} {self.line} {self.dot} {self.dot}",
            "'": f"{self.dot} {self.line} {self.line} {self.line} {self.line} {self.dot}",
            "!": f"{self.line} {self.dot} {self.line} {self.dot} {self.line} {self.line}",
            "/": f"{self.line} {self.dot} {self.dot} {self.line} {self.dot}",
            "(": f"{self.line} {self.dot} {self.line} {self.line} {self.dot}",
            ")": f"{self.line} {self.dot} {self.line} {self.line} {self.dot} {self.line}",
            "&": f"{self.dot} {self.line} {self.dot} {self.dot} {self.dot}",
            ":": f"{self.line} {self.line} {self.line} {self.dot} {self.dot} {self.dot}",
            ";": f"{self.line} {self.dot} {self.line} {self.dot} {self.line} {self.dot}",
            "=": f"{self.line} {self.dot} {self.dot} {self.dot} {self.line}",
            "-": f"{self.line} {self.dot} {self.dot} {self.dot} {self.dot} {self.line}",
            "_": f"{self.dot} {self.dot} {self.line} {self.line} {self.dot} {self.line}",
            '"': f"{self.dot} {self.line} {self.dot} {self.dot} {self.line} {self.dot}",
            "$": f"{self.dot} {self.dot} {self.dot} {self.line} {self.dot} {self.dot} {self.line}",
            "@": f"{self.dot} {self.line} {self.line} {self.dot} {self.line} {self.dot}",
            "+": f"{self.dot} {self.line} {self.dot} {self.line} {self.dot}"
        }
        self.morse_decoding: dict[str: str] = {value: key for key, value in self.morse_encoding.items()}

    def encode(self, text: str) -> str:
        """
        Taking any text as Input and returns code Morse version of it.
        Not available symbols will be ignored.

        :param text: any string to encode.
        :return: code Morse of input string.
        """
        encoded: list[str] = []
        for letter in list(text.lower()):
            if letter in self.morse_encoding:
                encoded.append(self.morse_encoding[letter])
        return '   '.join(encoded).strip()

    def decode(self, morse: str) -> str:
        """
        Taking correct version of code Morse and returns decoded Text.
        Correct version by given standard: ITU-R M.1677-1

        :param morse: correct code Morse.
        :return: decoded Text.
        """
        decoded: list[str] = []
        for word in morse.split('       '):
            for letter in word.split('   '):
                if letter in self.morse_decoding:
                    decoded.append(self.morse_decoding[letter])
            decoded.append(' ')
        return ''.join(decoded).strip()

    def convert(self, morse: str) -> str | bool:
        """
        Converting these types of code Morse styling:
         .__ .... . _./.. _./_ .... ./_._. ___ .._ ._. ... ./___ .._./.... .._ __ ._ _./
         .-- .... . -.|.. -.|- .... .|-.-. --- ..- .-. ... .|--- ..-.|.... ..- -- .- -.|
        Into a correct style to use with decode:
        . _ _   . . . .   .   _ .       . .   _ .       _   . . . .   .       _ . _ .

        https://morsedecoder.com/ <- use for fast style reference.

        :param morse: code Morse to convert.
        :return: correct code Morse to decode.
        """
        morse = morse.strip()
        replaced: str = ''
        allowed_symbols: set[str] = {'.', '-', '_', ' ', '/', '|'}
        for symbol in morse:
            if symbol == '.':
                replaced += f'{self.dot} '
            elif symbol == '-':
                replaced += f'{self.line} '
            elif symbol == '_':
                replaced += f'{self.line} '
            elif symbol == ' ':
                replaced += '  '
            elif symbol == '/' or symbol == '|':
                replaced += '  '
            elif symbol not in allowed_symbols:
                return False
        return replaced
