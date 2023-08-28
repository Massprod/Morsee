from morsee import Morsee
from random import randint, choice
from pytest import raises


def create_string(symbols: list[str], length: int = 1000,) -> str:
    """
    Creating random string from given symbols.
    :param symbols: symbols to build from.
    :param length: desired length.
    :return: randomly generated string from given symbols.
    """
    random_string: str = ''
    for _ in range(length):
        if randint(1, 3) == 1:
            random_string += ' '
            continue
        random_string += choice(symbols)

    return random_string


def test_encoding_decoding_ru() -> None:
    """
    Testing:
     - correct Encoding and Decoding of RU language.
    """
    test_morse: Morsee = Morsee()
    # Creating list from a dict to choose from for every string is too much.
    # And I don't want to bother with random choice from keys on my own.
    test_symbols: list[str] = list(test_morse.morse_encoding_ru.keys())
    for _ in range(5000):
        test_string: str = create_string(test_symbols, randint(1, 1000))
        test_encoded: str = test_morse.encode(test_string, 'ru')
        test_decoded: str = test_morse.decode(test_encoded, 'ru')
        assert test_string.strip() == test_decoded


def test_encoding_decoding_eng() -> None:
    """
    Testing:
     - correct Encoding and Decoding of ENG language.
    """
    test_morse: Morsee = Morsee()
    test_symbols = list(test_morse.morse_encoding_eng.keys())
    for _ in range(5000):
        test_string = create_string(test_symbols, randint(1, 1000))
        test_encoded = test_morse.encode(test_string, 'eng')
        test_decoded = test_morse.decode(test_encoded, 'eng')
        assert test_string.strip() == test_decoded


def test_encoding_decoding_errors() -> None:
    """
    Testing:
     - correct raising of errors for Encode|Decode methods.
    """
    test_morse: Morsee = Morsee()
    with raises(ValueError):
        test_morse.encode('', 'kjk')
        test_morse.encode('a' * 10001, 'ru')
        test_morse.decode('', 'kjk')
        test_morse.decode('a' * 10001, 'ru')


def test_encoding_decoding_incorrect() -> None:
    """
    Testing:
     - incorrect symbols inside input text.
    """
    test_morse: Morsee = Morsee()
    # allowed + some random high ASCII.
    test_base_ru: list[str] = list(test_morse.morse_encoding_ru.keys())
    test_base_eng: list[str] = list(test_morse.morse_encoding_ru.keys())
    test_extra_symbols: list[str] = [chr(_) for _ in range(123, 256)]
    for _ in range(5000):
        test_string: str = create_string(test_base_ru + test_extra_symbols, randint(1, 1000))
        test_encoded: str = test_morse.encode(test_string, 'ru')
        test_decoded: str = test_morse.decode(test_encoded, 'ru')
        test_out_string: str = ''
        for _ in test_string:
            if _ in test_morse.morse_encoding_ru:
                test_out_string += _
        # We always strip() all encoded|decoded outputs.
        # And dictionary have space character, which can stay after culling incorrect.
        # So if there were some spaces, we need to extra strip().
        assert test_out_string.strip() == test_decoded
    for _ in range(5000):
        test_string: str = create_string(test_base_eng + test_extra_symbols, randint(1, 1000))
        test_encoded: str = test_morse.encode(test_string, 'eng')
        test_decoded: str = test_morse.decode(test_encoded, 'eng')
        test_out_string: str = ''
        for _ in test_string:
            if _ in test_morse.morse_encoding_eng:
                test_out_string += _
        assert test_out_string.strip() == test_decoded
