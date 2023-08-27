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
commands: set[str] = {"menu", "symbols", "about", "encode", "decode", "quit", "close", "convert", "exit"}
# Don't see any reasons to rebuild this into a Class or add comments.
# Because there's literally everything described in print() or input() statements.
# And Class is useless, cuz it's just simple console input().
while not close:
    if option == "menu":
        os.system("cls")
        option = input("Welcome to Morsee.\nIf you want to Encode text in Morse, type: 'Encode'.\n"
                       "If you want to Decode text from Morse, type: 'Decode'.\n\n"
                       "Morse-code to 'Decode' should be in program style.\n"
                       "Otherwise, first read 'About' and try using 'Convert' to adjust it.\n"
                       "Additional commands: 'About', 'Symbols', 'Convert', 'Close/Quit'.\n").lower()
    elif option == "commands":
        os.system("cls")
        option = input(f"{', '.join(commands).title()}\nUse any of this 'commands':\n").lower()
    elif option not in commands:
        # Actually need to block Keyboard input, but it's too much bother for no actual reason.
        # And most of the solutions is not universal either Windows or Linux.
        os.system("cls")
        print("There's no such command.\nRedirecting to 'Menu'.")
        time.sleep(1)
        option = "menu"
    elif option == "symbols":
        os.system("cls")
        print("Supported symbols. According to ITU-R M.1677-1 standard.")
        for key, value in morse.morse_encoding.items():
            print(key + ": " + f"[{value}]")
        option = input("Make sure to copy only what's inside of []!\n"
                       "If you want to go back into 'menu', type: 'menu'\n").lower()
    elif option == "about":
        os.system("cls")
        print("This is a program which Encodes and Decodes text by ITU-R M.1677-1 standard.\n"
              "If you want to 'Decode' code which was created outside of this program.\n"
              "You will need to 'convert' it and use standard keys:\n"
              "  'DOT' is '.' and 'Line' is '-' or '_', no separation for letters in words.\n"
              "Word separator can be used as '/' or '|'\n"
              "Available formats to convert from:\n"
              "1) .-- .... . -. | .. -. | - .... . | -.-. --- ..- .-. ... . | --- ..-. | .... ..- -- .- -. |\n"
              "2) .__ .... . _. / .. _. / _ .... . / _._. ___ .._ ._. ... . / ___ .._. / .... .._ __ ._ _. /\n")
        option = input("\nType: 'menu', if you want to go back.\n").lower()
    elif option == "encode":
        os.system("cls")
        words_to_encode: str = input("Write/Place text to encode in Morse-code:\n").strip()
        os.system("cls")
        if len(words_to_encode) > 1000:
            os.system("cls")
            print('Only 1000 symbols allowed at once.')
            continue
        encode_result: str = morse.encode(words_to_encode)
        pyperclip.copy(encode_result)
        option = input(f"Morse code of the text:\n {encode_result}\n"
                       f"Result is saved into a clipboard, use Ctrl+v to paste.\n"
                       f"If you want to encode again, type: 'encode'.\n"
                       "For menu, type: 'menu'\n").lower()
        continue
    elif option == "decode":
        os.system("cls")
        decode_input: str = input("Write/place text to decode in Morse:\n").strip()
        os.system("cls")
        decode_result: str = morse.decode(decode_input)
        pyperclip.copy(decode_result)
        option = input(f"Text variant of the code:\n{decode_result}\n\n"
                       f"Result is saved into a clipboard, use Ctrl+V to paste.\n"
                       f"If you want to decode again, type: 'decode'\n"
                       "For menu, type: 'menu'\n").lower()
    elif option == "convert":
        os.system("cls")
        print("Format in which code is going to be converted:\n"
              "ITU-R M.1677-1 standard, which stands for this rules:\n"
              "1) Words should be separated by 7 spaces.\n"
              "2) Letters in words should be separated by 3 spaces.\n"
              "3) 'Dots' and 'Lines' should be separated by 1 space from each other.\n"
              "Use command: 'about' in 'menu'. To see which formats is available to convert.\n"
              "Morse-code to convert:")
        string_to_convert: str = input().strip()
        os.system("cls")
        convert_result: str = morse.convert(string_to_convert)
        if not convert_result:
            print('Incorrect symbols used. Remove and try again.\n')
            continue
        pyperclip.copy(convert_result)
        option = input(f"Converted variant to use:\n{convert_result}\n\n"
                       f"Result is saved into a clipboard, use Ctrl+V to paste.\n"
                       f"If you want to convert again, type: 'convert'\n"
                       f"For menu, type: 'menu'\n").lower()
    elif option == "close" or "quit" or "exit":
        os.system("cls")
        print("Morsee closed")
        close = True
