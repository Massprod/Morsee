import tkinter
from tkinter import *
from tkinter import messagebox
import pyperclip

# before OOP implementation (maybe ignore OOP in this one, we'll see)
dot = '.'
line = '_'
morse_encoding = {
    "a": f"{dot} {line}",
    "b": f"{line} {dot} {dot} {dot}",
    "c": f"{line} {dot} {line} {dot}",
    "d": f"{line} {dot} {dot}",
    "e": f"{dot}",
    "f": f"{dot} {dot} {line} {dot}",
    "g": f"{line} {line} {dot}",
    "h": f"{dot} {dot} {dot} {dot}",
    "i": f"{dot} {dot}",
    "j": f"{dot} {line} {line} {line}",
    "k": f"{line} {dot} {line}",
    "l": f"{dot} {line} {dot} {dot}",
    "m": f"{line} {line}",
    "n": f"{line} {dot}",
    "o": f"{line} {line} {line}",
    "p": f"{dot} {line} {line} {dot}",
    "q": f"{line} {line} {dot} {line}",
    "r": f"{dot} {line} {dot}",
    "s": f"{dot} {dot} {dot}",
    "t": f"{line}",
    "u": f"{dot} {dot} {line}",
    "v": f"{dot} {dot} {dot} {line}",
    "w": f"{dot} {line} {line}",
    "x": f"{line} {dot} {dot} {line}",
    "y": f"{line} {dot} {line} {line}",
    "z": f"{line} {line} {dot} {dot}",
    "1": f"{dot} {line} {line} {line} {line}",
    "2": f"{dot} {dot} {line} {line} {line}",
    "3": f"{dot} {dot} {dot} {line} {line}",
    "4": f"{dot} {dot} {dot} {dot} {line}",
    "5": f"{dot} {dot} {dot} {dot} {dot}",
    "6": f"{line} {dot} {dot} {dot} {dot}",
    "7": f"{line} {line} {dot} {dot} {dot}",
    "8": f"{line} {line} {line} {dot} {dot}",
    "9": f"{line} {line} {line} {line} {dot}",
    "0": f"{line} {line} {line} {line} {line}",
    " ": " ",
    ",": f"{line} {line} {dot} {dot} {line} {line}",
    ".": f"{dot} {line} {dot} {line} {dot} {line}",
    "?": f"{dot} {dot} {line} {line} {dot} {dot}",
    "'": f"{dot} {line} {line} {line} {line} {dot}",
    "!": f"{line} {dot} {line} {dot} {line} {line}",
    # "/": f"{line} {dot} {dot} {line} {dot}",
    "(": f"{line} {dot} {line} {line} {dot}",
    ")": f"{line} {dot} {line} {line} {dot} {line}",
    "&": f"{dot} {line} {dot} {dot} {dot}",
    ":": f"{line} {line} {line} {dot} {dot} {dot}",
    ";": f"{line} {dot} {line} {dot} {line} {dot}",
    "=": f"{line} {dot} {dot} {dot} {line}",
    "-": f"{line} {dot} {dot} {dot} {dot} {line}",
    "_": f"{dot} {dot} {line} {line} {dot} {line}",
    '"': f"{dot} {line} {dot} {dot} {line} {dot}",
    "$": f"{dot} {dot} {dot} {line} {dot} {dot} {line}",
    "@": f"{dot} {line} {line} {dot} {line} {dot}",
    "+": f"{dot} {line} {dot} {line} {dot}"
}
morse_decoding = {value: key for key, value in morse_encoding.items()}


def encode(word: str) -> str:
    list_to_encode = list(word.lower())
    list_encoded = []
    for letter in list_to_encode:
        if letter in morse_encoding:
            list_encoded.append(morse_encoding[letter])
    return "   ".join(list_encoded)


def decode(morse: str) -> str:
    morse_list = morse.split("       ")
    list_decoded = []
    for element in morse_list:
        element2 = element.split("   ")
        for letter in element2:
            if letter in morse_decoding:
                list_decoded.append(morse_decoding[letter])
        list_decoded.append(" ")
    return "".join(list_decoded)


def encode_button_command():
    if text_to_encode.get("1.0", "end-1c"):  # end-1c, deletes 1 character from end, needed to remove empty line.
        text_encoded.config(state="normal")
        text_encoded.delete("1.0", END)
        text = text_to_encode.get("1.0", END)
        # print(text)
        encoded_text = encode(text)
        # print(encoded_text)
        text_encoded.insert("1.0", encoded_text)
        text_encoded.config(state="disabled")
    else:
        messagebox.showinfo(title="Empty",
                            message="There's no Text to Encode.\nPlease fill it.",
                            icon="question",  # removing sound, icons: info, warning - cause warning sound.
                            )


# there's fully working solution in Scraps, but need to try it myself, at least once.
# right_click showing menu
def right_click(event):
    try:
        menu.tk_popup(event.x_root, event.y_root)
    finally:
        menu.grab_release()


# copy command #
def right_click_copy():
    try:
        selected_text = main_window.selection_get()
        main_window.clipboard_clear()
        main_window.clipboard_append(selected_text)
    except TclError:
        pass


# cut command #
def right_click_cut():
    try:
        selected_text = main_window.selection_get()
        main_window.clipboard_clear()
        main_window.clipboard_append(selected_text)
        text_to_encode.delete("sel.first", "sel.last")
    except TclError:
        pass


# paste command #
def right_click_paste():
    try:
        if main_window.focus_get() == text_to_encode:
            copied_text = main_window.selection_get(selection="CLIPBOARD")
            text_to_encode.insert(tkinter.INSERT, copied_text)  # tkinter.INSERT current position of a cursor
    except TclError:
        pass


# delete command #
def right_click_delete():
    try:
        text_to_encode.delete("sel.first", "sel.last")
    except TclError:
        pass
# Menu is working, but I can't find any decent info about, making paste and delete actions universal.
# It's working fine with just One active text_widget, but if I will ever want to add other widget's
# guess I will need to add focus_check for every text_widget or entry_widget, looks scrappy.
# Otherwise, need to find other solution or use One from Scrap_storage,
# which is maybe universal (tested only for 1 field, anyway).


# Gui setup
main_window = Tk()

# right click menu
menu = Menu(main_window, tearoff=0)
menu.add_command(label="Cut", command=right_click_cut)
menu.add_command(label="Copy", command=right_click_copy)
menu.add_command(label="Paste", command=right_click_paste)
menu.add_separator()
menu.add_command(label="Delete", command=right_click_delete)
main_window.bind("<Button-3>", right_click)

# icon and window setup
icon = tkinter.PhotoImage(file='morsee_icon.png')
main_window.iconphoto(False, icon)
main_window.title("Morsee")
main_window.config(padx=50,
                   pady=50,
                   )

# input/output frames
encode_label = Label()
encode_label.config(
    text="Text to encode:",
    fg="Black",
    font=("Ariel", 15, "bold"),
    anchor="w",
    bg="yellow",
)
encode_label.grid(
    column=1,
    row=0,
    sticky="w",
    pady=10,
)
text_to_encode = Text()
text_to_encode.config(
    width=75,
    height=10,
    font=("Ariel", 14, "bold"),
    bg="light blue",
    border=2,
    fg="Black",
)
text_to_encode.grid(
    column=1,
    row=1,
)

encoded_label = Label()
encoded_label.config(
    text="Encoded text:",
    fg="Black",
    font=("Ariel", 15, "bold"),
    anchor="w",
    bg="yellow",
)
encoded_label.grid(
    column=1,
    row=2,
    sticky="w",
    pady=10,
)

text_encoded = Text()
text_encoded.config(
    width=75,
    height=10,
    font=("Ariel", 14, "bold"),
    bg="light blue",
    border=2,
    fg="Black",
    state="disabled",
)
text_encoded.grid(
    column=1,
    row=3,
)
# encode/copy1 buttons
encode_button = Button()
encode_button.config(
    width=25,
    text="Encode",
    fg="Black",
    font=("Ariel", 12),
    command=encode_button_command,
)
encode_button.grid(
    row=2,
    column=1,
    sticky="e",
)

copy_button = Button()
copy_button.grid(
    row=4,
    column=1,
    sticky="e",
)

main_window.mainloop()
