

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
        self.morse_encoding_eng: dict[str: str] = {
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
        self.morse_decoding_eng: dict[str: str] = {value: key for key, value in self.morse_encoding_eng.items()}
        self.morse_encoding_ru: dict[str: str] = {
            'а': f'{self.dot} {self.line}',
            'б': f'{self.line} {self.dot} {self.dot} {self.dot}',
            'в': f'{self.dot} {self.line} {self.line}',
            'г': f'{self.line} {self.line} {self.dot}',
            'д': f'{self.line} {self.dot} {self.dot}',
            'е': f'{self.dot}',
            'ж': f'{self.dot} {self.dot} {self.dot} {self.line}',
            'з': f'{self.line} {self.line} {self.dot} {self.dot}',
            'и': f'{self.dot} {self.dot}',
            'й': f'{self.dot} {self.line} {self.line} {self.line}',
            'к': f'{self.line} {self.dot} {self.line}',
            'л': f'{self.dot} {self.line} {self.dot} {self.dot}',
            'м': f'{self.line} {self.line}',
            'н': f'{self.line} {self.dot}',
            'о': f'{self.line} {self.line} {self.line}',
            'п': f'{self.dot} {self.line} {self.line} {self.dot}',
            'р': f'{self.dot} {self.line} {self.dot}',
            'с': f'{self.dot} {self.dot} {self.dot}',
            'т': f'{self.line}',
            'у': f'{self.dot} {self.dot} {self.line}',
            'ф': f'{self.dot} {self.dot} {self.line} {self.dot}',
            'х': f'{self.dot} {self.dot} {self.dot} {self.dot}',
            'ц': f'{self.line} {self.dot} {self.line} {self.dot}',
            'ч': f'{self.line} {self.line} {self.line} {self.dot}',
            'ш': f'{self.line} {self.line} {self.line} {self.line}',
            'щ': f'{self.line} {self.line} {self.dot} {self.line}',
            'ъ': f'{self.line} {self.line} {self.dot} {self.line} {self.line}',
            'ы': f'{self.line} {self.dot} {self.line} {self.line}',
            'ь': f'{self.line} {self.dot} {self.dot} {self.line}',
            'э': f'{self.dot} {self.dot} {self.line} {self.dot} {self.dot}',
            'ю': f'{self.dot} {self.dot} {self.line} {self.line}',
            'я': f'{self.dot} {self.line} {self.dot} {self.line}',
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
        self.morse_decoding_ru: dict[str: str] = {value: key for key, value in self.morse_encoding_ru.items()}

    def encode(self, text: str, lang: str = 'eng') -> str:
        """
        Taking any Text as Input and returns code Morse version of it.
        Not available symbols will be ignored.
        Default language -> ENG.

        :param lang: language from which to encode, only 2 available: 'eng', 'ru'
        :param text: any string to encode.
        :return: code Morse of input string.
        """
        text = text.strip()
        if len(text) > 10000:
            try:
                print(1 / 0)
            except Exception:
                raise ValueError('Only 10000 symbols allowed.') from None

        encoded: str = ''
        last_space: bool = False
        morse_dict: dict[str: str] = {}
        if lang == 'ru':
            morse_dict = self.morse_encoding_ru
        elif lang == 'eng':
            morse_dict = self.morse_encoding_eng
        else:
            try:
                print(1 / 0)
            except Exception:
                raise ValueError('Only ENG or RU languages allowed.') from None

        for letter in list(text.lower()):
            # Ignoring any not allowed symbols.
            if letter in morse_dict:
                # According to standard.
                # For every SPACE we need to make 7 spaces.
                if letter == ' ':
                    encoded += ' ' * 7
                    last_space = True
                    continue
                # If last symbol was SPACE we don't need extra 3.
                if last_space:
                    encoded += morse_dict[letter]
                    last_space = False
                    continue
                # According to standard.
                # Every letter should be separated from another by 3 SPACES.
                encoded += ' ' * 3 + morse_dict[letter]
        return encoded.strip()

    def decode(self, morse: str, lang: str = 'eng') -> str:
        """
        Taking correct version of code Morse and returns decoded Text.
        Correct version by given standard: ITU-R M.1677-1.
        Default language -> ENG.

        :param lang: language from which to decode, only 2 available: 'eng', 'ru'
        :param morse: correct code Morse.
        :return: decoded Text.
        """
        morse = morse.strip()
        if len(morse) > 10000:
            try:
                print(1 / 0)
            except Exception:
                raise ValueError('Only 10000 symbols allowed.') from None

        decoded: str = ''
        cur_word: str = ''
        space_count: int = 0
        morse_dict: dict[str: str] = {}
        if lang == 'ru':
            morse_dict = self.morse_decoding_ru
        elif lang == 'eng':
            morse_dict = self.morse_decoding_eng
        else:
            try:
                print(1 / 0)
            except Exception:
                raise ValueError('Only ENG or RU languages allowed.') from None

        for x in range(len(morse)):
            # Count every space.
            if morse[x] == ' ':
                space_count += 1
                # Every letter divided from another by 3 spaces.
                # So when we passed 3 spaces we need to add this letter.
                if space_count == 3 and cur_word:
                    # Bad way, need to rebuild it later.
                    # Cuz we're adding extra space and slice it.
                    # It can be done without extra.
                    decoded += morse_dict[cur_word[:-1]]
                    cur_word = ''
                # Symbols for code Morse.
                # If currently some symbols are found|stored.
                # We need to separate every symbol by one space.
                elif space_count == 1 and cur_word:
                    cur_word += ' '
                # If no symbols found we need to add SPACE for every,
                #  7 spaces. By the standard.
                elif space_count == 7:
                    space_count = 0
                    decoded += ' '
            # Ignoring any incorrect symbols.
            elif morse[x] != self.dot and morse[x] != self.line:
                continue
            # Store DOT|LINE to find letter.
            elif morse[x] != ' ':
                space_count = 0
                cur_word += morse[x]
        # We always end with some symbols stored,
        #  because we're strip() input.
        # And cuz every letter recorded only when space_count == 3.
        # We need to extra record last word, it will never have space_count at all.
        if cur_word:
            decoded += morse_dict[cur_word]
        return decoded.strip()

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
        if len(morse) > 10000:
            try:
                print(1 / 0)
            except Exception:
                raise ValueError('Only 10000 symbols allowed.') from None
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
        return replaced.strip()
