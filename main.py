import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as db
import tkinter.messagebox as mb
import os
import datetime
import tkinter.font as tkfont
from PIL import ImageTk, Image
import json
import tkinter.colorchooser as tkcc


class Editor(tk.Tk):
    issaved = False
    filename = None
    response_new = True
    applicationname = "V-Note"

    """********************************** CONSTRUCTOR OF EDITOR  CLASS ************************************************"""

    def __init__(self):
        super().__init__()

    """********************************** GEOMETRY OF ROOT ************************************************"""

    def geometrywin(self, width, height):

        """ THIS METHOD MANAGES THE GEOMETRY OF ROOT"""

        self.geometry(f"{width}x{height}")

    """********************************** MINIMUM SIZE OF ROOT ************************************************"""

    def minsizewin(self, width, height):

        """ THIS METHOD SET THE MINIMUM SIZE LIMIT"""

        self.minsize(width, height)

    """********************************** MAXIMUM SIZE OF ROOT ************************************************"""

    def maxsizewin(self, width, height):

        """ THIS METHOD SET THE MAXIMUM SIZE LIMIT """
        self.maxsize(width, height)

    """********************************** NEW OPTION IN FILE MENU ************************************************"""

    def New(self, event=None):

        """ THIS METHOD PERFORM NEW FILE OPERATION """
        """ CHECKING FOR AUTO SAVE"""
        with open("settings.txt") as file_object:
            str_settings = file_object.read()
            dict_settings = json.loads(str_settings)
            isautosave = dict_settings["auto_save"]

        """ IF AUTOSAVE OPTION IS ENABLED"""
        if isautosave:
            if Editor.filename != None:
                content = main_text.get(1.0, tk.END)
                with open(Editor.filename,"w") as file_object_exit:
                    file_object_exit.write(content)

        """ IF FILE IS NOT SAVED"""
        if not Editor.issaved:
            res=mb.askyesno("NEW","Do you want save changes to untitled")
            if res:
                self.Save_as()

        """ SETTING STATE OF FILE UNSAVED"""
        Editor.issaved=False

        """ CLEARING THE CONTENT OF TEXT WIDGET"""
        main_text.delete(1.0, tk.END)

    """********************************** SAVE OPTION IN FILE MENU ************************************************"""

    def Save(self, events=None):

        """ THIS METHOD PERFORM SAVE METHOD"""

        """ IF FILE IS NOT SAVED """
        if Editor.filename == None:
            self.Save_as()
        else:
            """ IF FILE IS ALREADY SAVED"""
            content = main_text.get(1.0, tk.END)
            with open(Editor.filename, "w") as file_object:
                file_object.write(content)


    """********************************** SAVE AS OPTION IN FILE MENU ************************************************"""

    def Save_as(self, events=None):

        """ THIS METHOD PERFORM SAVE AS OPERATION """

        """ OPENING SAVE AS FILE DIALOG BOX"""
        filepath = db.asksaveasfilename(initialfile="Untitled.txt", defaultextension=".txt",
                                        filetype=[("All files", "*.*"), ("Text files", "*.txt")], title="Save as",
                                        initialdir=os.getcwd())
        """ IF USER PRESS CANCEL BUTTON OR CLOSES THE DIALOG BOX"""
        if filepath == "":
            return

        """ SETTING STATE OF FILE SAVED"""
        Editor.issaved = True

        """ ASSIGNIG THE PATH OF FILE TO CLASS VARIABLE """
        Editor.filename = filepath

        """ WRITING THE CONTENT OF TEXT WIDGET TO SAVED FILE"""
        with open(filepath, "w") as file_object:
            content = main_text.get(1.0, tk.END)
            file_object.write(content)



    """********************************** OPEN OPTION IN FILE MENU ************************************************"""

    def Open(self, events=None):

        """ THIS METHOD OPEN THE FILE"""

        """ OPENING OPEN DIALOG BOX"""
        file_path = db.askopenfilename(defaultextension=".txt", filetypes=[("All files", "*.*"), ("Text files", "*.txt")],title="Open")

        """ IF USER CLOSES THE OPEN DIALOG BOX """
        if file_path == "":
            return

        else:
            """ ASSIGNING THE PATH OF OPENED FILE TO CLASS VARIABLE """
            Editor.filename = file_path

            """" WRITING THE CONTENT OF OPENED FILE TO TEXT WIDGET"""
            with open(file_path, "r") as file_object:
                content = file_object.read()
            main_text.delete(1.0, tk.END)
            main_text.insert(1.0, content)

            """ SETTING THE STATE OF OPEN FILE AS SAVED"""
            Editor.issaved=True

    """********************************** EXIT OPTION IN FILE MENU ************************************************"""

    def Exit(self, events=None):

        """ THIS METHOD EXIT THE APPLICATION"""

        """ CHECKING IF AUTO SAVE FEATURE IS ENABLED """
        with open("settings.txt") as file_object:
            str_settings = file_object.read()
            dict_settings = json.loads(str_settings)
            isautosavee = dict_settings["auto_save"]

        """ WRITING THE CONTENT OF TEXT WIDGET TO SAVED FILE """
        if isautosavee:
            if Editor.filename!=None:
                content = main_text.get(1.0, tk.END)
                with open(Editor.filename,"w") as file_object_exit:
                    file_object_exit.write(content)

        """ CLOSING THE APPLICATION"""
        response = mb.askyesno("Exit", "Are you sure you want to exit V-Note")
        if response:
            self.quit()
            self.destroy()
    """********************************** SHOW THEME *****************************************"""

    def show_theme(self):
        """ THIS METHOD SHOW THE THEME """

        """ CHECKING THE CURRENT SET THEME"""
        with open("settings.txt") as file_object_read:
            str_dict = file_object_read.read()
            dict_settings_read = json.loads(str_dict)
            theme=dict_settings_read["theme"]

        """ APPLYING THE CURRENT THEME """
        if theme == "Coal":
            main_text.configure(bg="black", fg="white", insertbackground="white")
        elif theme == "Dark -(Developer's choice)":
            main_text.configure(bg="#373737",fg="white",insertbackground="white")
        elif theme == "Liquid":
            main_text.configure(bg="#1104ae",insertbackground="white")
        elif theme == "Snow":
            main_text.configure(bg="white",insertbackground="black",fg="black")
        main_text.update()

    """*********************************************** HIDE OR SHOW STATUS BAR ********************************"""

    def Statusbar(self,isstatus_bar):

        """ THIS METHOD HIDE OR SHOW THE STATUSBAR"""

        """ IF STATUS BAR IS ENABLED """
        if isstatus_bar==0:
            try:
                frm_statusbar.pack_forget()
                lbl_statusbar.pack_forget()
            except Exception as error:
                pass
        else:
            lbl_statusbar.pack(side=tk.BOTTOM,fill=tk.X)
            frm_statusbar.pack(side=tk.BOTTOM,fill=tk.X)

    """********************************** SETTINGS OPTION IN FILE MENU ************************************************"""

    def Settings(self, events=None):

        """ THIS METHOD PERFORM THE SETTING OPERATION """

        """ VARIABLES TO MANIPULATE THE SETTINGS """
        isreplicate=tk.IntVar()
        isautosave=tk.IntVar()
        isstatusbar = tk.IntVar()

        """ APPLYING THE SAVED SETTINGS """
        with open("settings.txt") as file_object_read:
            str_dict = file_object_read.read()
            dict_settings_read = json.loads(str_dict)
        isreplicate.set(dict_settings_read["replicate"])
        isstatusbar.set(dict_settings_read["status_bar"])
        isautosave.set(dict_settings_read["auto_save"])

        """ TOPLEVEL MANAGMENT """
        root_setting = tk.Toplevel()
        root_setting.geometry("500x500")
        root_setting.minsize(500, 500)
        root_setting.maxsize(500, 500)
        root_setting.title("Settings")
        icon_photo = tk.PhotoImage(file="icon.png")
        root_setting.iconphoto(False, icon_photo)


        def Apply():
            """ SAVE FUNCTION CALLED WHEN SAVED BUTTON IS PRESSED"""

            """ NONLOCAL VARTIABLES"""
            nonlocal isautosave
            nonlocal isstatusbar
            nonlocal isreplicate

            """ SAVING THE SETTING """

            with open("settings.txt") as file_object_read:
                str_dict=file_object_read.read()
                dict_settings_read=json.loads(str_dict)

            """ ENABLING OR DISABLING THE SETTINGS """
            isreplicate.set(isreplicate.get())
            isstatusbar.set(isstatusbar.get())
            isautosave.set(isautosave.get())
            cmbbx.set(cmbbx.get())

            """ CHANGING THE SETTINGS IF CHANGED BY USER """
            dict_settings_read["auto_save"]=isautosave.get()
            dict_settings_read["replicate"]=isreplicate.get()
            dict_settings_read["theme"]=cmbbx.get()
            dict_settings_read["status_bar"]=isstatusbar.get()

            """ WRITING THE SETTING TO FILE """
            with open("settings.txt","w") as file_object_write:
                str_dict_write=json.dumps(dict_settings_read)
                file_object_write.write(str_dict_write)

            """ UPDATING THE THEME """
            self.Statusbar(isstatusbar.get())
            self.show_theme()


        """ LABEL AND CHECKBUTTONS FOR STATUS BAR"""
        ttk.Label(root_setting, text="Status bar:", font="Arial 10 bold").grid(row=0, column=0, padx=10, pady=20,sticky="w")
        ttk.Checkbutton(root_setting, text="Show Status bar", variable=isstatusbar).grid(row=0, column=1,sticky="w")

        """ LABEL AND COMBOBOX OF THEME """
        ttk.Label(root_setting, text="Theme:", font="Arial 10 bold").grid(row=1, column=0, sticky="w", padx=10)
        cmbbx = ttk.Combobox(root_setting, state="readonly")
        cmbbx.grid(row=1, column=1,sticky="w")
        cmbbx['values'] = ("Dark -(Developer's choice)", "Liquid", "Snow", "Coal")
        cmbbx.set(dict_settings_read["theme"])

        """ LABEL AND CHECKBUTTON OF REPLICATE LINE """
        ttk.Label(root_setting,text="Replicate line:", font="Arial 10 bold").grid(row=2,column=0,sticky="w", padx=10,pady=20)
        ttk.Checkbutton(root_setting,text="Press Ctrl+D to replicate a line",variable=isreplicate).grid(row=2,column=1,pady=20)

        """  LABEL AND CHECKBUTTON OF AUTO SAVE """
        ttk.Label(root_setting, text="Save:", font="Arial 10 bold").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        ttk.Checkbutton(root_setting, text="Auto save", variable=isautosave).grid(row=3, column=1,pady=5,sticky="w")

        """ ADDING SEPERATOR USING SEPARATOR WIDGET """
        ttk.Separator(root_setting).grid(row=4, column=0, columnspan=10, sticky="we")

        """ APPLY BUTTON """
        ttk.Button(root_setting, text="Save", command=Apply).grid(row=10, column=5, sticky="se", pady=280,padx=10)

        """ CANCEL BUTTON  """
        ttk.Button(root_setting, text="Cancel", command=root_setting.destroy).grid(row=10, column=6, sticky="se", pady=280,padx=10)

        """ MAIN LOOP """
        root_setting.mainloop()

    """********************************** UNDO OPTION IN EDIT MENU ************************************************"""

    def Undo(self, events=None):

        """ THIS METHOD PERFORM THE UNDO OPERATION """

        main_text.edit_undo()

    """**********************************  REDO OPTION IN EDIT MENU ************************************************"""

    def Redo(self, events=None):

        """ THIS METHOD PERFORM THE REDO OPERATION """

        main_text.edit_redo()

    """**********************************  COPY OPTION IN EDIT MENU ************************************************"""

    def Copy(self, events=None):

        """ THIS METHOD PERFORM THE COPY OPERATION"""

        """ METHOD 1"""
        main_text.event_generate("<<Copy>>")

        """ METHOD 2"""
        # selected_text = main_text.selection_get()
        # main_text.clipboard_clear()
        # main_text.clipboard_append(selected_text)

    """********************************** COPY PATH OPTION IN EDIT MENU ************************************************"""

    def Copy_path(self, events=None):

        """ THIS METHOD COPY THE PATH OF CWD"""

        """ CHECKING IF FILE PATH IS NONE """
        if Editor.filename==None:
            main_text.clipboard_clear()
            main_text.clipboard_append(os.getcwd())

        else:
            """ APPENDING THE CURRENT OPENED FILE PATH TO CLIPBOARD """
            path = Editor.filename
            main_text.clipboard_clear()
            main_text.clipboard_append(path)


    """**********************************  CUT IN EDIT MENU ************************************************"""

    def Cut(self, events=None):
        """ THIS METHOD PERFORM THE CUT OPERATION"""

        """ METHOD 1"""
        main_text.event_generate("<<Cut>>")

        """ METHOD 2"""
        # selected_text = main_text.selection_get()
        # main_text.clipboard_clear()
        # main_text.clipboard_append(selected_text)
        # main_text.delete(tk.SEL_FIRST, tk.SEL_LAST)

    """**********************************  PASTE OPTION IN EDIT MENU ************************************************"""

    def Paste(self, events=None):

        """ THIS METHOD PERFORM THE PASTE OPERATION """

        """ METHOD 1"""
        main_text.event_generate("<<Paste>>")

        """ METHOD 2 """
        # """ current position of cursor"""
        # current_pos = main_text.index(tk.INSERT)
        # """ fetching the text of clipboard """
        # clipboardtext = main_text.clipboard_get()
        # main_text.insert(current_pos, clipboardtext)

    """********************************** SELECT ALL OPTION IN EDIT MENU ************************************************"""

    def Select_all(self, events=None):

        """ THIS METHOD PERFORM THE SELECT ALL OPERATION """

        """" APPLYING TAG TO TEXT WIDGET """
        main_text.tag_add(tk.SEL, 1.0, tk.END)

    """**********************************  FIND OPTION IN EDIT MENU ************************************************"""

    def Find(self, events=None):

        """ THIS METHOD PERFORM THE FIND OPERATION """

        def search():

            """" THIS METHOD SEARCH THE TEXT IN TEXT WIDGET """

            """ NONLOCAL VARIABLES """
            nonlocal last_index
            nonlocal ent_text

            text = ent_text.get()
            first = 1.0

            """ LOOP TO SEARCH TEXT IN TEXT WIDGET """

            while True:
                first_index = main_text.search(text, first, tk.END, count=last_index)
                if first_index == "":
                    break

                """ SEACHING THE TEXT """
                firstchar_first, lastchar_second = first_index.split(".")
                last_char_index = firstchar_first + "." + str(int(lastchar_second) + int(last_index.get()))

                """ ADDING TAG TO SEARCHED TEXT """
                main_text.tag_add("match", first_index, last_char_index)
                main_text.tag_config("match",background="#208fff",foreground="white")


                """ REASSIGNING THE FIRST VARIABLE TO CONTINUE SEARCH """
                first = last_char_index



        """ VARIABLE TO MANIPULATE THE LAST INDEX """
        last_index = tk.StringVar()

        """ TOPLEVEVL MANAGEMENT """
        root_find = tk.Toplevel()
        root_find.geometry("350x150")
        root_find.minsize(350, 150)
        root_find.maxsize(350, 150)
        root_find.title("Find")
        icon_photo = tk.PhotoImage(file="icon.png")
        root_find.iconphoto(False, icon_photo)

        """ LABEL AND ENTRY WIDGET FOR SEARCH """
        tk.Label(root_find, text="Search", font="Arial 10 bold").grid(row=0, column=0, padx=15, pady=10)
        ent_text = tk.Entry(root_find)
        ent_text.grid(row=0, column=1, pady=10)
        ent_text.focus_force()

        """ FIND BUTTON """
        ttk.Button(root_find, text="Find", command=search).grid(row=0, column=2, padx=10)
        def untag():
            """ THIS METHOD REMOVE THE TAG"""
            main_text.tag_remove("match", 1.0, tk.END)
            root_find.destroy()


        root_find.protocol("WM_DELETE_WINDOW",untag)
        """ MAINLOOP """
        root_find.mainloop()

    """**********************************  REPLACE OPTION IN EDIT MENU ************************************************"""

    def Replace(self, events=None):

        """ THIS METHOD PERFORM REPLACE OPERATION """

        def replace():

            """ THIS METHOD REPLACES THE TEXT """

            text = ent_text.get()
            first = 1.0
            replace_text = ent_replace.get()

            """ LOOP TO FIND THE TEXT AND REPLACE IT """
            while True:

                """ SEARCHING THE TEXT """
                first_index = main_text.search(text, first, tk.END, count=last_index)
                if first_index == "":
                    break
                firstchar_first, lastchar_second = first_index.split(".")
                last_char_index = firstchar_first + "." + str(int(lastchar_second) + int(last_index.get()))

                """ REPLACING THE TEXT """
                main_text.replace(first_index, last_char_index, replace_text)

                """ REASSIGNING THE FIRST VARIABLE TO CONTINUE THE SEARCH """
                first = last_char_index
        """ LOCAL VARIABLE TO MANIPULATE THE LAST INDEX"""
        last_index = tk.StringVar()

        """ TOPLEVEL MANAGMENT """
        root_replace = tk.Toplevel()
        root_replace.geometry("350x150")
        root_replace.minsize(350, 150)
        root_replace.maxsize(350, 150)
        root_replace.title("Replace")

        root_replace.iconphoto(False, icon_photo)

        """ SEARCH LABEL AND ENTRY WIDGET """
        tk.Label(root_replace, text="Find", font="Arial 10 bold").grid(row=0, column=0, padx=15, pady=10)
        ent_text = tk.Entry(root_replace)
        ent_text.focus_force()
        ent_text.grid(row=0, column=1, pady=10)

        """ REPLACE LABEL AND ENTRY WIDGET """
        tk.Label(root_replace, text="Replace", font="Arial 10 bold").grid(row=1, column=0, padx=15, pady=10)
        ent_replace = tk.Entry(root_replace)
        ent_replace.grid(row=1, column=1, pady=10)


        """ REPLACE BUTTON """
        ttk.Button(root_replace, text="Replace", command=replace).grid(row=0, column=2, padx=10)

        """ MAIN LOOP"""
        root_replace.mainloop()

    """**********************************  FONT OPTION IN FONT MENU ************************************************"""

    def Font(self):

        """ THIS METHOD PERFORM THE OPERATION OF FONT """

        """ LOCAL VARIABLE """
        colour_text="black"

        def Apply():
            """ THIS FUNTION APPLY THE FONTS """
            nonlocal cmb_font_size
            nonlocal cmb_font
            nonlocal cmb_font_style

            font_size = cmb_font_size.get()
            font_style = cmb_font_style.get()
            font = cmb_font.get()
            main_text.config(foreground=colour_text, font=(font, font_size, font_style))
            main_text.update()


        def choose_color():

            """ THIS FUNCTION PROVIDE A COLOUR PALETE """

            """ DISPLAYING COLOUR CHOOSER """
            colour=tkcc.askcolor(title="Chose a colour")

            """ NONLOCAL VARIABLE """
            nonlocal colour_text

            """ ASSIGNING THE HEX VALUE OF COLUR TO VARIABLE """
            colour_text=colour[1]

        """ TOPLEVEL MANAGEMENT """
        root_font = tk.Toplevel()
        root_font.title("Font")
        root_font.geometry("550x200")
        root_font.minsize(550, 200)
        root_font.maxsize(550, 200)
        root_font.iconphoto(False, icon_photo)

        """ LABELS AND COMBO BOX OF FONT  """
        tk.Label(root_font,text="Font").grid(row=0,column=0,padx=5)
        cmb_font = ttk.Combobox(root_font, state="readonly")
        cmb_font.grid(row=1, column=0, padx=5)
        cmb_font["values"] = sorted(tkfont.families())
        cmb_font.current(38)

        """ LABELS AND COMBO BOX OF FONT STYLE """
        tk.Label(root_font,text="Font style").grid(row=0,column=1,padx=5)
        cmb_font_style = ttk.Combobox(root_font, state="readonly")
        cmb_font_style.grid(row=1, column=1, padx=5)
        cmb_font_style["values"] = (tkfont.ITALIC, tkfont.BOLD, tkfont.ROMAN)
        cmb_font_style.current(1)

        """ LABELS AND COMBOBOX OF FONT SIZE """
        tk.Label(root_font,text="Size").grid(row=0,column=2,padx=5)
        cmb_font_size = ttk.Combobox(root_font, state="readonly")
        cmb_font_size.grid(row=1, column=2, padx=5)
        cmb_font_size["values"] = tuple([size for size in range(8, 73, 2)])
        cmb_font_size.current(5)


        """ LABEL,FRAME AND BUTTON  OF COLOUR """
        frm_colour=tk.Frame(root_font)
        frm_colour.grid(row=1,column=3,padx=5)
        tk.Label(root_font,text="Colour").grid(row=0,column=3,padx=5)
        tk.Label(frm_colour, text="Choose colour:").pack()
        ttk.Button(frm_colour, text="Colors", command=choose_color).pack()
        ttk.Separator(root_font).grid(row=4, column=0, columnspan=10, sticky="we", pady=50)

        """ APPLY BUTTON """
        ttk.Button(root_font,text="Apply",command=Apply).grid(row=5,column=2)

        """ CANCEL BUTTON"""
        ttk.Button(root_font,text="Cancel",command=root_font.destroy).grid(row=5,column=3,sticky="nw")

    """**********************************  UPDATING STATUS BAR  ************************************************"""


    def update_statusbar(self,events=None):
        """ THIS METHOD UPDATES THE STATUS BAR """


        with open("settings.txt") as file_object:
            str_settings = file_object.read()
            dict_settings = json.loads(str_settings)
            isstatusbar = dict_settings["status_bar"]
        if isstatusbar == 1:
            curs_pos = main_text.index(tk.INSERT)
            newline, newchar = str(curs_pos).split(".")
            lbl_statusbar.config(text=f"Line {newline} \n Char {newchar}")
            lbl_statusbar.update()

    def Time_date(self, events=None):

        """ THIS METHOD PASTE THE CURRENT TIME AND DATE """

        """ FETCHING THE CURRENT DATE TIME """
        datetimee = str(datetime.datetime.now())
        list_datetime = datetimee.split(".")
        current_datetime = list_datetime[0]

        """ FETCHING THE CURRENT POSITION OF CURSOR """
        cursor_pos = main_text.index(tk.INSERT)

        """ PASTE THE CURRENT DATE TIME TO TEXT WIDGET """
        main_text.insert(cursor_pos, current_datetime)

    """**********************************  TIME AND DATE OPTION IN EDIT MENU ************************************************"""

    def Replicate(self,events=None):

        """THIS METHOD REPLICATE THE LINE """

        """ CHECKING IF REPLICATE LINE IS ENABLED """
        with open("settings.txt") as file_object:
            str_dict=file_object.read()
            dict_settings_replicate=json.loads(str_dict)
            isreplicate=dict_settings_replicate["replicate"]

        """ IF REPLICATE LINE IS ENABLED """
        if isreplicate==1:

            """ CURRENT POSITION OF CURSOR """
            current_cur=main_text.index(tk.INSERT)
            line,char=current_cur.split(".")
            line_content=main_text.get(line+"."+"0",line+"."+char)

            """ INSERTING THE CONTENT TO NEW LINE"""
            main_text.insert(str(int(line)+int(1))+"."+"0","\n"+line_content)

    """**********************************  ABOUT OPTION IN HELP MENU ************************************************"""

    def About(self):

        """ THIS METHOD SHOW THE ABOUT  OPTION  """

        """ TOPLEVEL MANAGEMENT """
        root_about = tk.Toplevel()
        root_about.geometry("500x5070")
        root_about.minsize(500, 500)
        root_about.maxsize(500, 500)
        root_about.title("About")
        root_about.iconphoto(False, icon_photo)

        """ SHOWWING IMAGE OF VISHWA OFFICIAL """
        photo_vishwa = Image.open("full_logo.png")
        img = ImageTk.PhotoImage(photo_vishwa)
        tk.Label(root_about, image=img, relief=tk.SUNKEN, bd=5).grid(row=0,column=0)

        """ FRAME AND LABEL OF DESCRIPTION OF V-NOTE """
        frm = tk.Frame(root_about,width=470,height=200,relief=tk.RIDGE,borderwidth=5)
        frm.grid(row=1,column=0,pady=25)
        ttk.Label(frm, text="V-Note is a lightweight and open source text editor.\nIt is 0.1 version of V-Note released by Vishwa\n under MIT license.\nV-Note is an opensource text editor with some powefull tools.\nOne can easily use it and start their work freely.\n\n\n                                                                               Vishwa -Make It Easy!",font="MicroSquare 13 roman").pack(side=tk.BOTTOM,fill=tk.X,pady=5,padx=15)

        root_about.mainloop()

    """**********************************  HELP OPTION IN HELP MENU ************************************************"""

    def Help(self):

        """ THIS METHOD PERFORM OPERATION OF HELP OPTION"""
        os.startfile("help.txt")


    """ ******************************* RIGHT CLICK MENU ************************************************************"""

    def popup(self, event):

        """ THIS METHOD POP UP THE RIGHT CLICK MENU"""

        right_clickmenu.tk_popup(event.x_root, event.y_root)
        right_clickmenu.grab_release()



if __name__ == '__main__':
    """***************************************** MAIN WINDOW *********************************************************"""
    root = Editor()
    root.geometrywin(1200, 900)
    root.title("V-Note")
    """ MAIN TEXT WIDGET """
    main_text = tk.Text(undo=True)
    icon_photo=tk.PhotoImage(file="icon.png")
    root.iconphoto(False,icon_photo)

    """ ************************************ MENU BAR ************************************** """
    main_menu = tk.Menu(root)

    """ ************************************* FILE MENU *********************************** """
    file_menu = tk.Menu(main_menu, tearoff=0)

    main_menu.add_cascade(label="File", menu=file_menu)

    file_menu.add_command(label="New",accelerator=" Ctrl+N", command=root.New)
    file_menu.add_command(label="Open",accelerator="Ctrl+O", command=root.Open)
    file_menu.add_command(label="Save",accelerator="Ctrl+S", command=root.Save)
    file_menu.add_command(label="Save as ", command=root.Save_as)
    file_menu.add_separator()
    file_menu.add_command(label="Settings",accelerator="Ctrl+Alt+S", command=root.Settings)
    file_menu.add_separator()
    file_menu.add_command(label="Exit",accelerator=" Esc", command=root.Exit)

    """ ************************************ EDIT MENU ************************************** """
    edit_menu = tk.Menu(main_menu, tearoff=0)

    main_menu.add_cascade(label="Edit", menu=edit_menu)

    edit_menu.add_command(label="Undo",accelerator="Ctrl+Z", command=root.Undo)
    edit_menu.add_command(label="Redo ",accelerator="Ctrl+Y", command=root.Redo)
    edit_menu.add_command(label="Select all",accelerator="Ctrl+A", command=root.Select_all)
    edit_menu.add_separator()
    edit_menu.add_command(label="Cut",accelerator="Ctrl+X", command=root.Cut)
    edit_menu.add_command(label="Copy",accelerator="Ctrl+C", command=root.Copy)
    edit_menu.add_command(label="Paste",accelerator="Ctrl+V", command=root.Paste)
    edit_menu.add_command(label="Copy path",accelerator=" Ctrl+Shift+V", command=root.Copy_path)
    edit_menu.add_separator()
    edit_menu.add_command(label="Find",accelerator="Ctrl+F", command=root.Find)
    edit_menu.add_command(label="Replace",accelerator="Ctrl+R", command=root.Replace)
    edit_menu.add_separator()
    edit_menu.add_command(label="Time and date",accelerator="F5", command=root.Time_date)


    """ ************************************ FONT MENU ****************************************"""

    font_menu = tk.Menu(main_menu, tearoff=0)

    main_menu.add_cascade(label="Font", menu=font_menu)

    font_menu.add_command(label="Font", command=root.Font)



    """ ************************************ HELP MENU  **************************************"""

    help_menu = tk.Menu(main_menu, tearoff=0)

    main_menu.add_cascade(label="Help", menu=help_menu)

    help_menu.add_command(label=f"About {Editor.applicationname}", command=root.About)
    help_menu.add_command(label="Help", command=root.Help)


    """ ************************************ RIGHT CLICK MENU ****************************"""

    right_clickmenu = tk.Menu(root, tearoff=0)

    right_clickmenu.add_command(label="Cut",accelerator="Ctrl+X", command=root.Cut)
    right_clickmenu.add_command(label="Copy",accelerator="Ctrl+C", command=root.Copy)
    right_clickmenu.add_command(label="Paste",accelerator="Ctrl+V", command=root.Paste)
    right_clickmenu.add_command(label="Copy path",accelerator="Ctrl+Shift+V", command=root.Copy_path)
    right_clickmenu.add_separator()
    right_clickmenu.add_command(label="Undo",accelerator="Ctrl+Z", command=root.Undo)
    right_clickmenu.add_command(label="Redo",accelerator="Ctrl+Y", command=root.Redo)
    right_clickmenu.add_command(label="Replicate line",accelerator="Ctrl+D", command=root.Replicate)
    right_clickmenu.add_command(label="Settings",accelerator="Ctrl+Alt+S", command=root.Settings)
    root.config(menu=main_menu)

    """********************************** VERTICAL SCROLLBAR AND MAIN TEXT WIDGET **************************************"""
    scrl_y = ttk.Scrollbar(main_text, cursor="arrow")

    """ MAIN TEXT WIDGET """
    main_text.config(yscrollcommand=scrl_y.set)
    main_text.pack(expand=1, fill=tk.BOTH)

    """ SCROLLBAR """
    scrl_y.pack(side=tk.RIGHT, fill=tk.Y)
    scrl_y.config(command=main_text.yview)
    main_text.focus_force()
    """ *********************************************** EVENTS HANDLING ***************************************"""
    """ NEW FILE"""
    root.bind("<Control-n>", root.New)
    root.bind("<Control-N>", root.New)

    """ OPEN FILE """
    root.bind("<Control-o>", root.Open)
    root.bind("<Control-O>", root.Open)

    """ SAVE FILE """
    root.bind("<Control-s>", root.Save)
    root.bind("<Control-S>", root.Save)


    """ SETTINGS """
    root.bind("<Control-Alt-s>", root.Settings)
    root.bind("<Control-Alt-S>", root.Settings)

    """ UNDO """
    root.bind("<Control-z>", root.Undo)
    root.bind("<Control-Z>", root.Undo)

    """ REDO """
    root.bind("<Control-y>", root.Redo)
    root.bind("<Control-Y>", root.Redo)

    """ SELECT ALL"""
    root.bind("<Control-a>", root.Select_all)
    root.bind("<Control-A>", root.Select_all)

    """ CUT """
    root.bind("<Control-x>", root.Cut)
    root.bind("<Control-X>", root.Cut)

    """ COPY """
    root.bind("<Control-c>", root.Copy)
    root.bind("<Control-C>", root.Copy)

    """ PASTE """
    root.bind("<Control-v>", root.Paste)
    root.bind("<Control-V>", root.Paste)

    """ COPY CURRENT WORKING DIRECTORY  """
    root.bind("<Control-Shift-v>", root.Copy_path)
    root.bind("<Control-Shift-V>", root.Copy_path)

    """ FIND """
    root.bind("<Control-f>", root.Find)
    root.bind("<Control-F>", root.Find)

    """ REPLACE """
    root.bind("<Control-r>", root.Replace)
    root.bind("<Control-R>", root.Replace)

    """ PASTE TIME AND DATE """
    root.bind("<F5>", root.Time_date)

    """ RIGHT CLICK MENU """
    root.bind("<Button-3>", root.popup)

    """ UPDATING STATUS BAR """
    root.bind("<KeyPress>", root.update_statusbar)
    main_text.bind("<Button-1>", root.update_statusbar)
    main_text.bind("<Button-2>", root.update_statusbar)
    main_text.bind("<Button-3>", root.update_statusbar)

    """ REPLICATE A LINE """
    main_text.bind("<Control-D>", root.Replicate)
    main_text.bind("<Control-d>", root.Replicate)


    """ EXIT THE WINDOW """
    root.protocol("WM_DELETE_WINDOW",root.Exit)
    root.bind("<Escape>", root.Exit)

    """*********************************** SHOW STATUS BAR ***********************************************************"""
    with open("settings.txt") as file_object:
        str_settings = file_object.read()
        dict_settings = json.loads(str_settings)
        isstatusbar = dict_settings["status_bar"]
    if isstatusbar == 1:
        curs_pos = main_text.index(tk.INSERT)
        line, char = str(curs_pos).split(".")
        frm_statusbar = tk.Frame()
        frm_statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        lbl_statusbar = tk.Label(frm_statusbar, text=f"Line {line} \n Char {char}", bg="#a4a4a4", relief=tk.GROOVE,bd=5,font="Arial 10 bold")
        lbl_statusbar.pack(side=tk.BOTTOM, fill=tk.X)
    """ ************************************* SHOW THEME *************************************************************"""
    root.show_theme()
    """ ************************************** MAIN LOOP ****************************************************************"""
    root.mainloop()
