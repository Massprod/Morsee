# # right click menu from public, can be used to create standard functionality
# def menu(widget):
#     global MENU
#     MENU = tkinter.Menu(widget, tearoff=0)
#     MENU.add_command(label="Cut")
#     MENU.add_command(label="Copy")
#     MENU.add_command(label="Paste")
#
# def menu_popup(event):
#     widget = event.widget
#     MENU.entryconfigure("Cut",
#                         command=lambda: widget.event_generate("<<Cut>>"))
#     MENU.entryconfigure("Copy",
#                         command=lambda: widget.event_generate("<<Copy>>"))
#     MENU.entryconfigure("Paste",
#                         command=lambda : widget.event_generate("<<Paste>>"))
#     MENU.tk.call("tk_popup", MENU, event.x_root, event.y_root)
#
#
# menu(main_window)
# main_window.bind("<Button-3>", menu_popup)

# want to try and create it somewhat-myself.
