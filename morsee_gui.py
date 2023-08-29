import os
import time
import json
import datetime
from tkinter import *
from threading import Timer
from tkinter import messagebox
from playsound import playsound
from morsee.morsee import Morsee
from tkinter.scrolledtext import ScrolledText


global SOUND_ON, history_window

morse = Morsee()

dot_path: str = r'media/dotsound024s.wav'
line_path: str = r'media/linesound068s.wav'
icon_path: str = 'media/icons/morsee_icon.png'
play_icon: str = 'media/icons/play_icon_20px.png'
russian_icon: str = 'media/icons/ru_icon_24px.png'
british_icon: str = 'media/icons/uk_icon_24px.png'
cancel_icon: str = 'media/icons/cancel_icon_20px.png'


def encode_button_command() -> None:
    """
    Enabling outputText field and placing encoded version of text
    from inputText field.
    Saving both input|output versions into a History.
    """
    text: str = text_to_encode.get("1.0", "end-1c").strip()
    if text:
        if len(text) > 1000:
            messagebox.showinfo(
                title='Over-limit',
                message='Only 1000 symbols allowed. Including spaces.',
                icon='question',
            )
            return
        text_encoded.config(state="normal")
        text_encoded.delete("1.0", END)
        encoded_text = morse.encode(text, language[0])
        text_encoded.insert("1.0", encoded_text)
        append_history()
        text_encoded.config(state="disabled")
    else:
        messagebox.showinfo(
            title="Empty",
            message="There's no Text to Encode.\nPlease fill it.",
            icon="question",
        )


def copy_button_command() -> None:
    """
    Copy text from inputText field into a clipboard.
    """
    copied_text: str = text_encoded.get("1.0", "end-1c").strip()
    if copied_text:
        main_window.clipboard_clear()
        main_window.clipboard_append(copied_text)


def clear_button_command() -> None:
    """
    Clear both input|output Text fields.
    """
    text_to_clear: str = text_encoded.get("1.0", END)
    if text_to_clear:
        text_to_encode.delete("1.0", END)
        text_encoded.config(state="normal")
        text_encoded.delete("1.0", END)
        text_encoded.config(state="disabled")


def decode_button_command() -> None:
    """
    Decode correct input from inputText field and place into outputText field.
    Raising error if inputText field is empty or have incorrect symbols.
    Saving both input|output versions into a History.
    """
    # end-1c, deletes 1 character from end, needed to remove empty line.
    text: str = text_to_encode.get("1.0", "end-1c").strip()
    if text:
        text_encoded.config(state="normal")
        text_encoded.delete("1.0", END)
        decoded_text: str = morse.decode(text, language[0])
        text_encoded.insert("1.0", decoded_text)
        append_history()
        text_encoded.config(state="disabled")
    else:
        messagebox.showinfo(
            title="Empty",
            message="There's no Morse to Decode.\nPlease fill it.",
            icon="question",  # removing sound, icons: info, warning - cause warning sound.
        )


def change_to_convert_command() -> None:
    """
    Change Main window to convert mode, with changing inputText field to convert
    input text from different code Morse style into a correct to use with Morsee.
    """
    disable_main_window()
    convert_info_window: Toplevel = Toplevel(main_window)
    convert_info_window.title("Converting Info")
    convert_window_x: int = main_window.winfo_rootx() + 250
    convert_window_y: int = main_window.winfo_rooty() + 160
    convert_info_window.geometry(f"+{convert_window_x}+{convert_window_y}")
    convert_info_window.resizable(False, False)
    convert_info_window.config(
        bg="#F7F6F2",
    )
    convert_info_window_text: Text = Text(
        convert_info_window,
        height=10,
        width=54,
        fg="#4B6587",
        bg="#F7F6F2",
        selectforeground="#4B6587",  # to hide selection, because didn't
        selectbackground="#FEFFAC",  # found how to disable it completely
        font=("Ariel", 12, "bold"),
        state="normal",
        relief=RIDGE,
    )
    convert_info_window_text.insert(
        1.0,
        "  If you want to 'Decode' code which wasn't created in Morsee."
        "\n  You can try to 'convert' this code, according to this rules:"
        "\n   1.  'DOT' is '.' and 'Line' '-' or '_' "
        "\n   2.  No separation for letters in words."
        "\n   3.  Word separator can be used as '/' or '|'"
        "\n\n  Example of formats to convert:"
        "\n     .__ .... . _. / .. _. / _ .... . / "
        "_._. ___ .._ ._. ... . / ___ .._. / .... .._ __ ._ _. / "
        "\n\n     .-- .... . -. | .. -. | - .... . | "
        "-.-. --- ..- .-. ... . | --- ..-. | .... ..- -- .- -. | ",
    )
    convert_info_window_text.grid(
        row=0,
        columnspan=3,
        column=0,
    )
    convert_info_window_text.config(state="disabled")
    convert_info_window_label: Label = Label(
        convert_info_window,
        text="Would you like to try Converting?",
        fg="#4B6587",
        bg="#F7F6F2",
        font=("Ariel", 14, "bold"),
    )
    convert_info_window_label.grid(
        row=1,
        column=0,
    )
    convert_info_window.protocol(
        "WM_DELETE_WINDOW",
        lambda: (convert_info_window.destroy(), enable_main_window())
    )

    def convert_info_pressed_yes() -> None:
        """
        Applying changes.
        """
        convert_info_window.withdraw()
        enable_main_window()
        sound_play_button.grid_remove()
        language_switch_button.grid_remove()
        encode_label.config(text="Code Morse to convert")
        encoded_label.config(text="Converted to Morsee")
        if encode_label.cget("text") == "Text to encode":
            encode_button.grid_remove()
            convert_button.grid()
        elif encode_label.cget("text") != "Text to encode":
            decode_button.grid_remove()
            convert_button.grid()
        change_type_button.config(
            text="CONVERTING",
            state="disabled",
        )
        change_to_convert_button.config(
            text="To Encode",
            command=change_type_button_command,
        )
        text_to_encode.delete("1.0", END)
        text_encoded.config(state="normal")
        text_encoded.delete("1.0", END)
        text_encoded.config(state="disabled")

    convert_info_window_yes_button: Button = Button(
        convert_info_window,
        width=5,
        text="YES",
        fg="#4B6587",
        activeforeground="#4B6587",
        bg="#E6E5A3",
        activebackground="#E6E5A3",
        font=("Ariel", 14, "bold"),
        relief=FLAT,
        command=convert_info_pressed_yes,
    )
    convert_info_window_yes_button.grid(
        row=1,
        column=1,
        sticky="e",
    )

    def convert_info_pressed_no() -> None:
        """
        Returns to original Main window state.
        """
        convert_info_window.withdraw()
        enable_main_window()

    convert_info_window_no_button = Button(
        convert_info_window,
        width=5,
        text="NO",
        fg="#4B6587",
        activeforeground="#4B6587",
        bg="#F7A4A4",
        activebackground="#F7A4A4",
        font=("Ariel", 14, "bold"),
        relief=FLAT,
        command=convert_info_pressed_no,
    )
    convert_info_window_no_button.grid(
        row=1,
        column=2,
        sticky="e",
    )


def convert_button_command() -> None:
    """
    Convert different style of code Morse from inputText field, and inserting correct version
    into a outputText field.
    Raising error if not allowed symbols used, or inputText field is empty.
    """
    text: str = text_to_encode.get("1.0", "end-1c")
    if text:
        if len(text) > 10000:
            messagebox.showinfo(
                title='Over-limit',
                message='Only 10000 symbols allowed. Including spaces.',
                icon='question',
            )
            return
        text_encoded.config(state="normal")
        text_encoded.delete("1.0", "end-1c")
        converted: str = morse.convert(text)
        if not converted:
            messagebox.showinfo(
                title='Error',
                message=f'Use only allowed symbols: ".", "-", "_", " ", "/", "|"\n'
                        f'Extra check "To Convert" button to check converting Rules.',
            )
            return
        text_encoded.insert("1.0", converted)
        text_encoded.delete("end-1c", END)  # Prefer to leave to delete extra space from Highlighting with cursor.
        append_history()
        text_encoded.config(state="disabled")
    else:
        messagebox.showinfo(
            title="Empty",
            message="There's no code Morse to Convert.\nPlease place something first.",
            icon="question",
        )


def change_type_button_command() -> None:
    """
    Changes Main window and Text fields from Encoding to Decoding states.
    Or from Decoding to Encoding states.
    """
    # Encoding -> Decoding.
    if encode_label.cget("text") == "Text to encode":
        encode_label.config(text="Code Morse to decode")
        encoded_label.config(text="Decoded text")
        sound_play_button.grid_remove()
        encode_button.grid_remove()
        decode_button.grid()
        change_type_button.config(text="DECODING")
        text_to_encode.delete("1.0", END)
        text_encoded.config(state="normal")
        text_encoded.delete("1.0", END)
        text_encoded.config(state="disabled")
    # Decoding -> Encoding
    elif encode_label.cget("text") != "Text to encode":
        change_to_convert_button.config(
            text="To Convert",
            command=change_to_convert_command,
        )
        encode_label.config(text="Text to encode")
        encoded_label.config(text="Encoded text")
        sound_play_button.grid()
        language_switch_button.grid()
        convert_button.grid_remove()
        decode_button.grid_remove()
        encode_button.grid()
        change_type_button.config(
            text="ENCODING",
            state="normal",
        )
        text_to_encode.delete("1.0", END)
        text_encoded.config(state="normal")
        text_encoded.delete("1.0", END)
        text_encoded.config(state="disabled")


def about_button_command() -> None:
    """
    Messagebox showing general info about ITU-R M.1677-1 standard.
    """
    messagebox.showinfo(
        title="About",
        message="Morsee Encodes and Decodes any text"
                "\n according to: ITU-R M.1677-1 standard."
                "\nIf you want to Decode code Morse, created outside."
                "\nYou need to make sure it matches standard symbols."
                "\nSymbols not included in standard will be ignored!\n\n"
                "In Morsee length of 'dash' is equal to 'dot'.\n"
                "The space between:\n"
                "  - the signals forming a letter is equal to one dot.\n"
                "  - two letters is equal to three dots.\n"
                "  - two words is equal to seven dots.\n",
        icon="question",
    )


def stop_sound() -> None:
    """
    Stops thread with playing sound, and returns Main window into an active state.
    """
    global SOUND_ON
    if sound_play_button.cget("text") != " Play":
        sound_play_button.config(
            text=" Play",
            image=sound_play_icon,
            state="normal",
            command=sound_play_clicked,
            bg="#C8C6C6",
            activebackground="#C8C6C6",
        )
        enable_main_window()
        SOUND_ON = False


def sound_play_button_command(text: str) -> None:
    """
    Change state of the Play button to Stop button.
    Play dot|line sound for every symbol from input Text.
    Return initial state of the Play button.
    :param text: string with correct code Morse.
    """
    global SOUND_ON
    if text:
        SOUND_ON = True
        disable_main_window()
        text_to_encode.config(state="normal")
        sound_play_button.config(
            text=" Cancel",
            image=sound_cancel_icon,
            state="normal",
            command=stop_sound,
            bg="#F7A4A4",
            activebackground="#F7A4A4",
        )
        index: int = 0
        while index != len(text):
            if text[index] == " " and SOUND_ON:
                time.sleep(0.16)
            elif text[index] == "_" and SOUND_ON:
                playsound(sound=line_path)
            elif text[index] == "." and SOUND_ON:
                playsound(sound=dot_path)
            index += 1
        sound_play_button.config(
            text=" Play",
            image=sound_play_icon,
            state="normal",
            command=sound_play_clicked,
            bg="#C8C6C6",
            activebackground="#C8C6C6",
        )
        enable_main_window()
        return
    else:
        return


def sound_play_clicked() -> None:
    """
    Starts a thread for sound playing code Morse from inputText field.
    """
    code_morse: str = text_encoded.get("1.0", "end-1c")
    # Second call to this, overrides this Thread and insta Return eliminates it after.
    thread: Timer = Timer(0.1, sound_play_button_command, args=(code_morse,))
    thread.start()


def right_click(event) -> None:  # event_bind = Button-3
    """
    Open Right click menu for copy, delete, cut, paste options.
    Only allowed on Text fields.
    """
    try:
        x, y = main_window.winfo_pointerxy()  # pointer coordinates
        widget: Tk = main_window.winfo_containing(x, y)  # widget with mouse_pointer over it
        if widget.winfo_class() == "Text" and widget["state"] != "disabled":
            widget.focus_set()
            menu.tk_popup(event.x_root, event.y_root)
        # Disabling cut, delete, paste for inactive outputField.
        # Only copying from this Field allowed.
        elif widget.winfo_class() == "Text":
            menu.entryconfig("Cut", state="disabled")
            menu.entryconfig("Delete", state="disabled")
            menu.entryconfig("Paste", state="disabled")
            menu.tk_popup(event.x_root, event.y_root)
    # Close menu, and reset default options.
    finally:
        menu.grab_release()
        menu.entryconfig("Cut", state="normal")
        menu.entryconfig("Delete", state="normal")
        menu.entryconfig("Paste", state="active")


def right_click_copy() -> None:
    """
    Copy selected text into a clipboard.
    """
    try:
        selected_text: str = main_window.selection_get()
        main_window.clipboard_clear()
        main_window.clipboard_append(selected_text)
    except TclError:
        pass


# cut command
def right_click_cut() -> None:
    """
    Cut selected text from Text field and save into a clipboard.
    """
    try:
        widget: Tk = main_window.focus_get()
        selected_text: str = main_window.selection_get()
        main_window.clipboard_clear()
        main_window.clipboard_append(selected_text)
        widget.delete("sel.first", "sel.last")
    except TclError:
        pass


def right_click_paste() -> None:
    """
    Paste any text from a clipboard into a inputText field.
    """
    try:
        copied_text: str = main_window.clipboard_get()
        widget: Tk = main_window.focus_get()
        position: Tk = widget.index(INSERT)
        # INSERT at the highlighted position in inputText field.
        if widget.winfo_class() == "Text":
            if widget["state"] != "disabled":
                widget.insert(position, copied_text)
                widget.delete("sel.first", "sel.last")
    except TclError:
        pass


def right_click_delete() -> None:
    """
    Delete selected text from inputText field.
    """
    try:
        widget: Tk = main_window.focus_get()
        widget.delete("sel.first", "sel.last")
    except TclError:
        pass


def disable_main_window() -> None:
    """
    Fully disable Main window, and make everything inactive.
    """
    for widget in main_window.winfo_children():
        try:
            widget["state"] = "disabled"
        except TclError:
            pass


def enable_main_window() -> None:
    """
    Return Main window to a normal state with enabling every widget.
    """
    for widget in main_window.winfo_children():
        try:
            widget["state"] = "normal"
        except TclError:
            pass


def append_history() -> None:
    """
    Save command for saving input and output Text fields into a History.
    Creates History in the same directory as main script.
    History -> simple Json with Timestamp and contents both fields saved.
    """
    # Getting current system Time zone.
    timezone: datetime = datetime.datetime.now(datetime.timezone.utc).astimezone()
    # Strf to normal visual. Y/M/D - H/M/S
    system_time: str = timezone.strftime("%Y-%m-%d %H:%M:%S")
    input_text: str = text_to_encode.get("1.0", "end-1c").strip()
    output_text: str = text_encoded.get("1.0", "end-1c").strip()
    # Better to cull duplicates, but it's either O(n) traversing of whole dict,
    #  cuz we're saving INPUT inside of system_time. Or extra dict to check.
    # Actually if we're using system_time to show, is it better to cull them?
    # Like there's no search, so if ever something equal created it could be done after a long time.
    # And this is going to be ignored and previously stored after like 100+ records.
    # So it's better to either leave duplicates, or make a search for already existed records.
    # Or let's just override them, it's doable.
    if output_text:
        new_record: dict[str, str] = {
            "Input": input_text,
            "Result": output_text,
        }
        try:
            with open("history.json", "r+") as history:
                history_data = json.load(history)
                # If input was already used.
                if input_text in history_data['inputs']:
                    old_record: dict[str, str] = history_data['inputs'][input_text]
                    # We can take its system_time and delete old record from History.
                    history_data.pop(old_record['system_time'])
                    # And update stored INPUT system_time with a new one.
                    old_record['system_time'] = system_time
                else:
                    # If it's a new INPUT we need to save it.
                    history_data['inputs'][input_text] = {'system_time': system_time}
                # Input|Result from new_record is the same as old one.
                # And old system_time record is already deleted.
                history_data[system_time] = new_record
                history.seek(0)
                json.dump(history_data, history, indent=4)
                history.truncate()
        except FileNotFoundError:
            with open("history.json", "w") as history:
                # 'inputs' <- extra dictionary to store previous result and their call time.
                json.dump({
                    system_time: new_record,
                    'inputs': {
                        input_text: {
                            'system_time': system_time,
                            }
                        }
                    },
                    history, indent=4
                )
    else:
        return


def clear_history_button_command() -> None:
    """
    Delete History Json if it's present in the same directory as main script.
    """
    global history_window
    if os.path.exists("history.json"):
        os.remove("history.json")
        history_window.destroy()
        enable_main_window()
    else:
        pass


def history_button_command() -> None:
    """
    Create History window with all records saved in History.
    Every record is having Timestamp, Input and Result.
    """
    # Bad solution, but I made this long time ago and only visiting to clean it.
    # No reasons to learn Tkinter for now. Made after 100d of python as recommended.
    # This History_window should be created outside of this function and then populated,
    #  and I don't know how to clear canvas and repopulate it again. Leaving it like this.
    # Tested with 100+ records, it's building fast, so either Tkinter not building it from scratch.
    # Or it's just fast enough to create and populate new window for press of a button.
    # Still bad solution, tho. Should be reusing this window, not rebuilding.
    global history_window
    try:
        with open("history.json", "r") as history:
            history_data: dict[str, dict[str, str]] = json.load(history)
            disable_main_window()
            # History window setup.
            history_window = Toplevel(main_window)
            history_window.title("History")
            history_window.configure(bg="black")
            main_x: int = history_window.winfo_rootx()
            main_y: int = history_window.winfo_rooty()
            history_window.geometry(f"+{main_x + 250}+{main_y + 250}")
            history_window.geometry("770x700")
            history_window.resizable(False, False)

            def onFrameConfigure(canvas):
                """Reset the scroll region to encompass the inner frame"""
                canvas.configure(scrollregion=canvas.bbox("all"))

            def on_mousewheel(event):
                """
                Allows scrolling inside the canvas.
                """
                try:
                    history_window_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                except TclError:
                    pass

            history_window_canvas: Canvas = Canvas(history_window, borderwidth=0, background="#F0E5CF")
            history_window_frame: Frame = Frame(history_window_canvas, bg="#F0E5CF", border=0, )
            history_window_scrollbar: Scrollbar = Scrollbar(
                history_window, orient="vertical",
                command=history_window_canvas.yview
            )
            history_window_canvas.configure(
                yscrollcommand=history_window_scrollbar.set,
                height=700,
                width=770,
                border=0,
            )
            history_window_scrollbar.grid(row=0, column=0, sticky="nse")
            history_window_canvas.grid(row=0, column=0, sticky="nsew")
            history_window_canvas.create_window((0, 0), window=history_window_frame, anchor="nw")
            history_window_canvas.bind_all("<MouseWheel>", on_mousewheel)
            history_window_frame.bind(
                "<Configure>",
                lambda event, canvas=history_window_canvas: onFrameConfigure(history_window_canvas)
            )
            history_window.protocol(
                "WM_DELETE_WINDOW",
                lambda: (history_window.destroy(), enable_main_window())
            )

            time_label_row: int = 1
            input_label_column: int = 0
            input_label_row: int = 0
            input_text_row: int = 1
            result_label_row: int = 0
            result_text_row: int = 1
            for key in history_data:
                # 'inputs' <- extra key to cull duplicates.
                if key == 'inputs':
                    continue
                # Save time of the record.
                time_label: Text = Text(
                    history_window_frame,
                    height=4,
                    width=10,
                    fg="#4B6587",
                    bg="#F0E5CF",
                    selectforeground="#4B6587",
                    selectbackground="#F7F6F2",
                    font=("Ariel", 14, "bold"),
                    state="normal",
                    relief=FLAT,
                )
                time_label.insert("1.0", f"\n{key}")
                time_label.configure(state="disabled")
                time_label.grid(
                    column=1,
                    row=time_label_row,
                )
                time_label_row += 4
                # Input label.
                input_label = Label(
                    history_window_frame,
                    text="Input",
                    font=("Ariel", 15, "bold"),
                    anchor="n",
                    bg="#F0E5CF",
                )
                input_label.grid(
                    column=input_label_column,
                    row=input_label_row,
                    sticky="s",
                    pady=(10, 0),
                )
                input_label_row += 4
                # Input data from record.
                # For every record creating scrollbar, to be able to see it fully.
                input_text: ScrolledText = ScrolledText(
                    history_window_frame,
                    height=4,
                    width=25,
                    fg="#4B6587",
                    bg="#C8C6C6",
                    font=("Ariel", 14, "bold"),
                    state="normal",
                    relief=SUNKEN,
                    wrap="word",
                )
                input_text.insert("1.0", history_data[key]["Input"])
                input_text.configure(state="disabled")
                input_text.grid(
                    row=input_text_row,
                    column=0,
                    padx=15,
                )
                input_text_row += 4
                # Result label.
                result_label = Label(
                    history_window_frame,
                    text="Result",
                    font=("Ariel", 15, "bold"),
                    bg="#F0E5CF",
                )
                result_label.grid(
                    column=2,
                    row=result_label_row,
                    sticky="s",
                    pady=(10, 0)
                )
                result_label_row += 4
                # Result data from record
                result_text: ScrolledText = ScrolledText(
                    history_window_frame,
                    height=4,
                    width=25,
                    fg="#4B6587",
                    bg="#C8C6C6",
                    font=("Ariel", 14, "bold"),
                    state="normal",
                    relief=FLAT,
                    wrap="word",
                )
                result_text.insert("1.0", history_data[key]["Result"])
                result_text.configure(state="disabled")
                result_text.grid(
                    row=result_text_row,
                    column=2,
                    padx=(0, 15),
                )
                result_text_row += 4

            clear_history_button: Button = Button(
                history_window_frame,
                width=15,
                text="Clear history",
                fg="#4B6587",
                bg="#F7F6F2",
                font=("Ariel", 14, "bold"),
                state="normal",
                relief=FLAT,
                command=clear_history_button_command,
            )
            clear_history_button.grid(
                row=(result_text_row + 1),
                columnspan=3,
                sticky="s",
                pady=(40, 20)
            )
    except FileNotFoundError:
        messagebox.showinfo(
            title="Empty",
            message="There's no History yet.\nTry to use Morsee first.",
            icon="question",
        )


def switch_language_command() -> None:
    if language[0] == 'eng':
        language_switch_button.config(
            image=language_switch_ru_image,
        )
        language[0] = 'ru'
    elif language[0] == 'ru':
        language_switch_button.config(
            image=language_switch_uk_image,
        )
        language[0] = 'eng'


# GUI setup.
main_window: Tk = Tk()
language: list[str] = ['eng']
# Main window setup.
icon: PhotoImage = PhotoImage(file=icon_path)
main_window.iconphoto(True, icon)
main_window.title("Morsee")
main_window.config(
    padx=50,
    pady=50,
    bg="#F0E5CF",
)
main_window.resizable(False, False)
main_window.bind_all("<Button-3>", right_click)
# Right click menu
menu: Menu = Menu(main_window, tearoff=0)
menu.add_command(label="Copy", command=right_click_copy)
menu.add_command(label="Paste", command=right_click_paste)
menu.add_separator()
menu.add_command(label="Cut", command=right_click_cut)
menu.add_command(label="Delete", command=right_click_delete)
menu.config(
    bg="#FFF8EA",
    font=("Ariel", 10, "bold"),
    fg="#4B6587"
)
# Input Text field.
encode_label: Label = Label()
encode_label.config(
    text="Text to encode",
    fg="#4B6587",
    font=("Ariel", 16, "bold"),
    anchor="w",
    bg="#F0E5CF",
)
encode_label.grid(
    column=1,
    row=0,
    sticky="w",
    pady=10,
)
text_to_encode: Text = Text()
text_to_encode.config(
    width=75,
    height=10,
    font=("Ariel", 14, "bold"),
    bg="#C8C6C6",
    border=2,
    fg="#4B6587",
    relief=FLAT,
    selectforeground="#4B6587",
    selectbackground="#F7F6F2",
    wrap="word",
    undo=True,
)
text_to_encode.grid(
    column=1,
    row=1,
)
# Output Text field.
encoded_label: Label = Label()
encoded_label.config(
    text="Encoded text",
    fg="#4B6587",
    font=("Ariel", 16, "bold"),
    anchor="w",
    bg="#F0E5CF",
)
encoded_label.grid(
    column=1,
    row=2,
    sticky="w",
    pady=10,
)
text_encoded: Text = Text()
text_encoded.config(
    width=75,
    height=10,
    font=("Ariel", 14, "bold"),
    bg="#C8C6C6",
    border=2,
    fg="#4B6587",
    state="disabled",
    relief=FLAT,
    selectforeground="#4B6587",
    selectbackground="#F7F6F2",
)
text_encoded.grid(
    column=1,
    row=3,
)
# Encode button.
encode_button: Button = Button()
encode_button.config(
    width=15,
    text="Encode",
    fg="#4B6587",
    font=("Ariel", 15, "bold"),
    command=encode_button_command,
    relief=FLAT,
    bg="#F7F6F2",
    activebackground="#F7F6F2",
    activeforeground="#4B6587",
)
encode_button.grid(
    row=2,
    column=0,
    columnspan=2,
    sticky="e",
    pady=5,
)
# Copy button.
copy_button: Button = Button()
copy_button.config(
    width=15,
    text="Copy",
    fg="#4B6587",
    activeforeground="#4B6587",
    font=("Ariel", 15, "bold"),
    relief=FLAT,
    bg="#F7F6F2",
    activebackground="#F7F6F2",
    command=copy_button_command,
)
copy_button.grid(
    row=4,
    column=1,
    sticky="e",
    pady=5,
)
# Clear Text fields button.
clear_button: Button = Button()
clear_button.config(
    width=12,
    text="Clear",
    font=("Ariel", 15, "bold"),
    fg="#4B6587",
    activeforeground="#4B6587",
    bg="#F7F6F2",
    activebackground="#F7F6F2",
    command=clear_button_command,
    relief=FLAT,
)
clear_button.grid(
    row=4,
    column=0,
    columnspan=2,
    sticky="w",
    pady=5,
)
# Change type of Text fields button.
change_type_button: Button = Button()
change_type_button.config(
    width=12,
    text="ENCODING",
    font=("Ariel", 15, "bold"),
    fg="#4B6587",
    activeforeground="#4B6587",
    bg="#F7F6F2",
    activebackground="#F7F6F2",
    command=change_type_button_command,
    relief=FLAT,
)
change_type_button.grid(
    row=0,
    column=1,
    sticky="n",
    pady=5,
)
# Change Text fields to converting state button.
change_to_convert_button: Button = Button()
change_to_convert_button.config(
    width=12,
    text="To Convert",
    font=("Ariel", 15, "bold"),
    fg="#4B6587",
    activeforeground="#4B6587",
    bg="#F7F6F2",
    activebackground="#F7F6F2",
    command=change_to_convert_command,
    relief=FLAT,
)
change_to_convert_button.grid(
    row=0,
    column=1,
    sticky="e",
    pady=5,
)
# Decode text from inputText field button.
decode_button: Button = Button()
decode_button.config(
    width=15,
    text="Decode",
    font=("Ariel", 15, "bold"),
    fg="#4B6587",
    activeforeground="#4B6587",
    bg="#F7F6F2",
    activebackground="#F7F6F2",
    command=decode_button_command,
    relief=FLAT,
)
decode_button.grid(
    row=2,
    column=0,
    columnspan=2,
    sticky="e",
    pady=5,
)
# First state is Encoding, hiding after creation.
decode_button.grid_remove()
# Convert different style of code Morse from inputText field button.
convert_button: Button = Button()
convert_button.config(
    width=15,
    text="Convert",
    font=("Ariel", 15, "bold"),
    fg="#4B6587",
    activeforeground="#4B6587",
    bg="#F7F6F2",
    activebackground="#F7F6F2",
    command=convert_button_command,
    relief=FLAT,
)
convert_button.grid(
    row=2,
    column=0,
    columnspan=2,
    sticky="e",
    pady=5,
)
# First state is Encoding, hiding after creation.
convert_button.grid_remove()
# About standard button.
about_button: Button = Button()
about_button.config(
    width=10,
    text="About",
    font=("Ariel", 15, "bold"),
    fg="#4B6587",
    activeforeground="#4B6587",
    bg="#F7F6F2",
    activebackground="#F7F6F2",
    command=about_button_command,
    relief=FLAT,
)
about_button.grid(
    row=4,
    column=0,
    columnspan=2,
    sticky="n",
    pady=5,
)
# Open history if it's exist button.
history_button: Button = Button()
history_button.config(
    width=10,
    text="History",
    font=("Ariel", 15, "bold"),
    fg="#4B6587",
    activeforeground="#4B6587",
    bg="#F7F6F2",
    activebackground="#F7F6F2",
    command=history_button_command,
    relief=FLAT,
)
history_button.grid(
    row=2,
    column=0,
    columnspan=2,
    sticky="n",
    pady=5,
)
# Play code Morse with sound button.
sound_play_button: Button = Button()
sound_play_icon: PhotoImage = PhotoImage(file=play_icon)
sound_cancel_icon: PhotoImage = PhotoImage(file=cancel_icon)
sound_play_button.config(
    height=20,
    width=75,
    image=sound_play_icon,
    text=" PLAY",
    compound=LEFT,
    font=("Ariel", 10, "bold"),
    fg="#4B6587",
    activeforeground="#4B6587",
    bg="#C8C6C6",
    activebackground="#C8C6C6",
    command=sound_play_clicked,
    relief=FLAT,
)
sound_play_button.grid(
    row=3,
    column=1,
    columnspan=1,
    sticky="se",
)
# Change language to Encode|Decode from button.
language_switch_button: Button = Button()
language_switch_ru_image: PhotoImage = PhotoImage(file=russian_icon)
language_switch_uk_image: PhotoImage = PhotoImage(file=british_icon)
language_switch_button.config(
    height=25,
    width=30,
    image=language_switch_uk_image,
    fg="#4B6587",
    activeforeground="#4B6587",
    bg="#C8C6C6",
    activebackground="#C8C6C6",
    command=switch_language_command,
    relief=FLAT,
)
language_switch_button.grid(
    row=1,
    column=1,
    columnspan=1,
    sticky='se',
)

main_window.mainloop()
