from morsee import Morsee
from random import randint, choice
from pytest import raises


def create_string(symbols: list[str], length: int = 1000, both: bool = True) -> list[str] | str:
    """
    Creating random strings from given symbols.

    :param symbols: Symbols to build from.
    :param length: Desired length of a string.
    :param both:
    True == both string options.
    False == only one with unlimited spaces.
    :return:
    One or Two strings generated from input symbols.
    One with unlimited spaces between words.
    Second with only 1 space between every word.
    """
    # We're culling extra spaces when Encoding.
    # So we need 2 strings, one with w.e spaces,
    #  another only with 1 space between every word.
    random_string: str = ''
    # Initializing with ' ' placed for easier track of [-1].
    random_string_no_spaces: str = ' '
    last_space: bool = False
    for _ in range(length):
        if both:
            # Blocking using of space if it was already placed ->
            if random_string_no_spaces[-1] == ' ':
                last_space = True
            # Semi random space injection.
            if randint(1, 3) == 1:
                random_string += ' '
                if not last_space:
                    random_string_no_spaces += ' '
                continue
            symbol: str = choice(symbols)
            random_string += symbol
            # -> until we find any other symbol to place.
            if symbol != ' ':
                random_string_no_spaces += symbol
                last_space = False
            elif symbol == ' ' and not last_space:
                random_string_no_spaces += symbol
        else:
            if randint(1, 3) == 1:
                random_string += ' '
                continue
            random_string += choice(symbols)
    if both:
        return [random_string, random_string_no_spaces]
    else:
        return random_string


def test_encoding_decoding_ru() -> None:
    """
    Testing:
     Correct Encoding and Decoding of RU language.
    """
    test_morse: Morsee = Morsee()
    # Creating list from a dict to choose from for every string is too much.
    # And I don't want to bother with random choice from keys on my own.
    test_symbols: list[str] = list(test_morse.morse_encoding_ru.keys())
    for _ in range(5000):
        test_string, correct_test_out = create_string(test_symbols, randint(1, 1000))
        test_encoded: str = test_morse.encode(test_string, 'ru')
        test_decoded: str = test_morse.decode(test_encoded, 'ru')
        assert correct_test_out.strip() == test_decoded


def test_encoding_decoding_eng() -> None:
    """
    Testing:
      Correct Encoding and Decoding of ENG language.
    """
    test_morse: Morsee = Morsee()
    test_symbols: list[str] = list(test_morse.morse_encoding_eng.keys())
    for _ in range(5000):
        test_string, correct_test_out = create_string(test_symbols, randint(1, 1000))
        test_encoded: str = test_morse.encode(test_string, 'eng')
        test_decoded: str = test_morse.decode(test_encoded, 'eng')
        assert correct_test_out.strip() == test_decoded


def test_encoding_decoding_errors() -> None:
    """
    Testing:
      Correct raising of errors for Encode|Decode methods.
    """
    test_morse: Morsee = Morsee()
    with raises(ValueError):
        test_morse.encode('', 'kjk')
        test_morse.encode('a' * 1001, 'ru')
        test_morse.decode('', 'kjk')
        test_morse.decode('a' * 10001, 'ru')
        test_morse.convert('a' * 10001)
    assert test_morse.convert('a' * 100) is False


def test_encoding_decoding_incorrect_ru() -> None:
    """
    Testing:
     Incorrect symbols inside inputs of Encode or Decode.
     Should be ignored and correct parts of the input processed correctly.
     But it's only testing cases with CORRECT code Morse to decode.
    """
    test_morse: Morsee = Morsee()
    # Allowed + some random high ASCII.
    # But it's still using correct sequence of LINE and DOTS.
    # Incorrect sequences will be ignored, and it's x10 harder to test.
    # Because some of the parts with shuffle Morse, still could make correct symbols.
    # But they will be not even close to original. So it either don't test and ignore.
    # Or make check for CORRUPT input and return False while decoding.
    # It's easier to test, but I prefer to leave it with ignoring and just try to build something of it.
    # But this is untestable, at least with random cases. Maybe make it later.
    test_base_ru: list[str] = list(test_morse.morse_encoding_ru.keys())
    test_extra_symbols: list[str] = [chr(_) for _ in range(123, 256)]
    for _ in range(500):
        test_string: str = create_string(test_base_ru + test_extra_symbols, randint(1, 1000), False)
        test_encoded: str = test_morse.encode(test_string, 'ru')
        corrupted_list: list[str] = list(test_encoded)
        # Corrupting only with incorrect symbols not shuffling original placement.
        for code in corrupted_list:
            for _ in range(randint(2, 5)):
                code = choice(test_extra_symbols) + code + choice(test_extra_symbols)
        test_decoded: str = test_morse.decode(''.join(corrupted_list), 'ru')
        test_out_string: str = ''
        last_space: bool = True
        for _ in test_string:
            if _ in test_morse.morse_encoding_ru:
                if _ != ' ':
                    test_out_string += _
                    last_space = False
                if _ == ' ' and not last_space:
                    test_out_string += _
                    last_space = True
        # We always strip() all encoded|decoded outputs.
        # And dictionary have space character, which can stay after culling incorrect symbols.
        # So if there were some spaces, we need to extra strip().
        assert test_out_string.strip() == test_decoded


def test_encoding_decoding_incorrect_eng() -> None:
    """
    Testing:
     Incorrect symbols inside inputs of Encode or Decode.
     Should be ignored and correct parts of the input processed correctly.
     But it's only testing cases with CORRECT code Morse to decode.
    """
    test_morse: Morsee = Morsee()
    test_base_eng: list[str] = list(test_morse.morse_encoding_eng.keys())
    test_extra_symbols: list[str] = [chr(_) for _ in range(123, 256)]
    for _ in range(500):
        test_string: str = create_string(test_base_eng + test_extra_symbols, randint(1, 1000), False)
        test_encoded: str = test_morse.encode(test_string, 'eng')
        list_corruption = list(test_encoded)
        for code in list_corruption:
            for _ in range(randint(2, 5)):
                code = choice(test_extra_symbols) + code + choice(test_extra_symbols)
        test_decoded = test_morse.decode(''.join(list_corruption), 'eng')
        test_out_string: str = ''
        last_space: bool = True
        for _ in test_string:
            if _ in test_morse.morse_encoding_eng:
                if _ != ' ':
                    test_out_string += _
                    last_space = False
                if _ == ' ' and not last_space:
                    test_out_string += _
                    last_space = True
        assert test_out_string.strip() == test_decoded
