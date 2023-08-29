import os
import time
import pyperclip
from morsee.morsee import Morsee


# Test message to convert: "when in the course of human"
# .-- .... . -. | .. -. | - .... . | -.-. --- ..- .-. ... . | --- ..-. | .... ..- -- .- -. |
# .__ .... . _. / .. _. / _ .... . / _._. ___ .._ ._. ... . / ___ .._. / .... .._ __ ._ _. /


morse = Morsee()
option: str = "menu"
close: bool = False
language: str = 'eng'
commands: set[str] = {"menu", "symbols", "about", "encode", "decode", "quit", "close", "convert", "exit", "language"}
# Better to save, and reuse than do this for every call.
# Maybe even delete set and make it just STR.
# But it's not a problem for now, and maybe it could be usefully to have list of all commands.
# Then trying to split string and get them.
commands_str: str = ', '.join(commands).title()
# Don't see any reasons to rebuild this into a Class or add comments.
# Because there's literally everything described in print() or input() statements.
# And Class is useless, cuz it's just simple console input().
while not close:
    if option == "menu":
        os.system("cls")
        option = input(
           f"Welcome to Morsee. Language set to -> {language.upper()}.\n"
            "If you want to Encode text in Morse, type: 'Encode'.\n"
            "If you want to Decode text from Morse, type: 'Decode'.\n\n"
            "Morse-code to 'Decode' should be in program style.\n"
            "Otherwise, first read 'About' and try using 'Convert' to adjust it.\n"
            "Additional commands: 'About', 'Symbols', 'Convert', 'Language' 'Close/Quit'.\n"
        ).lower()

    elif option == 'language':
        os.system('cls')
        language = input(
            "There's only 2 language options available: 'ENG' or 'RU'.\n"
            "Type one you want to Encode|Decode from.\n"
        ).lower()
        option = 'menu'

    elif option == "commands":
        os.system("cls")
        option = input(f"{commands_str}\nUse any of this 'commands':\n").lower()

    elif option not in commands:
        # Actually need to block Keyboard input, but it's too much bother for no actual reason.
        # And most of the solutions is not universal either Windows or Linux.
        os.system("cls")
        print("There's no such command.\nRedirecting to 'Menu'.")
        time.sleep(1)
        option = "menu"

    elif option == "symbols":
        os.system("cls")
        print("Supported symbols:'\n")
        all_symbols: dict[str: str] = morse.morse_encoding_ru | morse.morse_encoding_eng
        # Ugly, but working fast without extra saving, sorting. But not universal.
        # And 2 columns with correct distance.
        # Building in three steps.
        cur_str: str = ''
        next_str: str = ''
        step: int = 0
        print('Russian alphabet:')
        for key, value in all_symbols.items():
            # Breaking at first symbol of ENG alph.
            # Cur str is last special symbol, and next_str isn't build yet.
            if key == 'a':
                print(f'{cur_str}\n'
                      '\nEnglish alphabet:')
                # Reset and start building new row, from next symbol.
                cur_str = ''
                step = 0
            if step == 2:
                # Third -> combining with delimiter, max(cur_str) == 18.
                # So we can always fill this with leftovers from higher number.
                cur_str += ' ' * (25 - len(cur_str)) + next_str
                print(cur_str)
                # Same approach. But RU alph, rows ending correctly.
                # So we can just print w.e we want. and continue building.
                if key == '1':
                    print('\nDigits|Special symbols:')
                step = 0
            if step == 0:
                # First -> create first symbol string.
                cur_str =  f'{key.upper()} : [{value}]'
            if step == 1:
                # Second -> create second symbol string.
                next_str = f'{key.upper()} : [{value}]'
            step += 1
        # Used simple loop, and it can end building without printing, step == 1.
        if cur_str or next_str:
            print(cur_str + ' ' * (25 - len(cur_str)) + next_str)
        option = input(
            "\nMake sure to copy only what's inside of []!\n"
            "If you want to go back into 'menu', type: 'menu'\n"
        ).lower()

    elif option == "about":
        os.system("cls")
        print(
            "This is a program which Encodes and Decodes text by ITU-R M.1677-1 standard.\n"
            f"Available languages to use: 'English' and 'Russian'. Current: {language.title()}\n"
            "If you want to 'Decode' code which was created outside of this program.\n"
            "You will need to 'convert' it and use standard keys:\n"
            "  'DOT' is '.' and 'Line' is '-' or '_', no separation for letters in words.\n"
            "Word separator can be used as '/' or '|'\n"
            "Available formats to convert from:\n"
            "1) .-- .... . -. | .. -. | - .... . | -.-. --- ..- .-. ... . | --- ..-. | .... ..- -- .- -. |\n"
            "2) .__ .... . _. / .. _. / _ .... . / _._. ___ .._ ._. ... . / ___ .._. / .... .._ __ ._ _. /\n"
        )
        option = input("\nType: 'menu', if you want to go back.\n").lower()
    elif option == "encode":
        os.system("cls")
        words_to_encode: str = input("Write/Place text to encode in Morse-code:\n").strip()
        os.system("cls")
        if len(words_to_encode) > 1000:
            os.system("cls")
            print('Only 1000 symbols allowed at once.')
            continue
        encode_result: str = morse.encode(words_to_encode, language)
        if encode_result:
            pyperclip.copy(encode_result)
        option = input(
            f"Morse code of the text:\n {encode_result}\n"
            f"Result is saved into a clipboard, use Ctrl+v to paste.\n"
            f"If you want to encode again, type: 'encode'.\n"
            "For menu, type: 'menu'\n"
        ).lower()
    elif option == "decode":
        os.system("cls")
        decode_input: str = input("Write/place text to decode in Morse:\n").strip()
        os.system("cls")
        if len(decode_input) > 10000:
            os.system("cls")
            print('Only 10000 symbols allowed.\n')
            time.sleep(1)
            continue
        decode_result: str = morse.decode(decode_input, language)
        if decode_result:
            pyperclip.copy(decode_result)
        option = input(
            f"Text variant of the code:\n{decode_result}\n\n"
            f"Result is saved into a clipboard, use Ctrl+V to paste.\n"
            f"If you want to decode again, type: 'decode'\n"
            "For menu, type: 'menu'\n"
        ).lower()
    elif option == "convert":
        os.system("cls")
        print(
            "Format in which code is going to be converted:\n"
            "ITU-R M.1677-1 standard, which stands for this rules:\n"
            "1) Words should be separated by 7 spaces.\n"
            "2) Letters in words should be separated by 3 spaces.\n"
            "3) 'Dots' and 'Lines' should be separated by 1 space from each other.\n"
            "Use command: 'about' in 'menu'. To see which formats is available to convert.\n"
            "Morse-code to convert:"
        )
        string_to_convert: str = input().strip()
        os.system("cls")
        if len(string_to_convert) > 10000:
            os.system("cls")
            print('Only 10000 symbols allowed.\n')
            time.sleep(1)
            continue
        convert_result: str = morse.convert(string_to_convert)
        if not convert_result:
            print('Incorrect symbols used or not symbol used at all.\nTry again.\n')
            continue
        if convert_result:
            pyperclip.copy(convert_result)
        option = input(
            f"Converted variant to use:\n{convert_result}\n\n"
            f"Result is saved into a clipboard, use Ctrl+V to paste.\n"
            f"If you want to convert again, type: 'convert'\n"
            f"For menu, type: 'menu'\n"
        ).lower()
    elif option == "close" or "quit" or "exit":
        os.system("cls")
        print("Morsee closed")
        close = True
