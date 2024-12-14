import tkinter as tk

from tkcalendar import Calendar


class Front:
    def __init__(self, back):
        self.master = tk.Tk()

        self.master.geometry("1200x700")
        self.master.title("User wählen")
        self.master.config(bg="#E8D0B9")

        self.user_list = back.get_user()

        # StringVar erstellen
        clicked = tk.StringVar()
        clicked.set(self.user_list[0])  # default value setzen

        # dropdown menu erstellen
        drop = tk.OptionMenu(self.master, clicked, *self.user_list)
        drop.config(bg="#C0A08F", fg="white", font="Arial 20")

        drop["menu"].config(bg="#D8C7B9", fg="white", font="Arial 16")  # menüzeilen konfigurieren
        drop.place(relx=0.3, rely=0.2, width=500, height=80)

        # Button um User auszuwählen
        choose_button = tk.Button(
            self.master,
            text="Auswählen",
            command=lambda: [self.fenster_erstellen(back, clicked.get())],
            bg="#A09391",
            fg="white",
            font="Arial 20",
        )
        choose_button.place(relx=0.3, rely=0.4, width=500, height=80)

        # Button 'User hinzufügen'
        new_user_button = tk.Button(
            self.master,
            text="User hinzufügen",
            command=lambda: self.new_user(back),
            bg="#C0C0C1",
            fg="white",
            font="Arial 20",
        )
        new_user_button.place(relx=0.05, rely=0.8, width=270, height=60)

        self.master.mainloop()

    # Fenster um neuen Benutzer zu erstellen
    def new_user(self, back):
        new_user_window = tk.Toplevel(self.master)
        new_user_window.title("Neuer User")
        new_user_window.geometry("1000x700")
        new_user_window.config(bg="#A67F78")

        entry = tk.Entry(new_user_window, bd=0, width=80, bg="#E1DCD9", fg="black")
        entry.bind(
            "<Return>",
            lambda event: [back.new_user_back(entry.get()), back.__init__(), self.fenster_erstellen(back, entry.get())],
        )

        entry.place(relx=0.2, rely=0.2)

        new_user_label = tk.Label(
            new_user_window, text="Geben Sie den neuen Usernamen ein:", bg="#A67F78", font=("Arial", 15)
        )
        new_user_label.place(relx=0.33, rely=0.1)

        accept_button = tk.Button(
            new_user_window,
            text="Akzeptieren",
            command=lambda: [back.new_user_back(entry.get()), back.__init__(), self.fenster_erstellen(back, entry.get())],
            bg="#8F8681",
            fg="white",
        )
        accept_button.place(relx=0.45, rely=0.4, width=120, height=40)

    # Task-Fenster erstellen
    def fenster_erstellen(self, back, user):
        self.master.destroy()
        self.fenster = tk.Tk()

        self.user = user
        print(self.user)

        self.fenster.geometry("1200x700")
        self.fenster.title(self.user)
        self.fenster.config(bg="#7991a2")

        # Eingabefeld konfigurieren und mit Enter bestätigen
        self.eingabefeld = tk.Entry(self.fenster, bd=0, width=80, bg="#c3cccf", fg="black")
        self.eingabefeld.bind(
            "<Return>",
            lambda event: [back.add_task(self.eingabefeld.get()), self.change_label_add_task(self.eingabefeld.get())],
        )
        self.eingabefeld.place(relx=0.2, rely=0.1)

        # Label s.Text
        anfangs_label = tk.Label(self.fenster, text="Gib deine Aufgabe ein: ", bg="#7991a2")
        anfangs_label.place(relx=0.05, rely=0.1)

        # Label, dass die Aufgabe als gespeichert anzeigt
        self.task_label = tk.Label(self.fenster, bg="#7991a2")
        self.task_label.place(relx=0.36, rely=0.155)

        # Button, um task zu bestätigen
        task_button = tk.Button(
            self.fenster,
            text="Bestätigen",
            command=lambda: [back.add_task(self.eingabefeld.get()), self.change_label_add_task(self.eingabefeld.get())],
            bg="#3c3735",
            fg="white",
        )

        task_button.place(relx=0.41, rely=0.2, width=100, height=40)

        # Button, um Daten in Json zu speichern
        speicher_button = tk.Button(
            self.fenster,
            text="Speichern",
            command=lambda: [back.save_task(self.user), self.change_speicher_label()],
            bg="#535D55",
            fg="white",
        )
        speicher_button.place(relx=0.56, rely=0.85, width=100, height=40)

        # Button, um Daten aus Json zu laden
        lade_button = tk.Button(
            self.fenster,
            text="Laden",
            command=lambda: [back.load_task(self.aufgabenliste, self.user), self.change_lade_label()],
            bg="#535D55",
            fg="white",
        )
        lade_button.place(relx=0.705, rely=0.85, width=100, height=40)

        # Label, um Speichern/Laden zu bestätigen
        self.speicher_label = tk.Label(self.fenster, bg="#7991a2")
        self.speicher_label.place(relx=0.34, rely=0.45)
        self.lade_label = tk.Label(self.fenster, bg="#7991a2")
        self.lade_label.place(relx=0.36, rely=0.45)

        # Exit Button
        exit_button = tk.Button(
            self.fenster, text="Beenden", command=lambda: self.fenster.destroy(), bg="#8B0000", fg="white"
        )
        exit_button.place(relx=0.07, rely=0.85, width=100, height=40)

        # Bearbeiten-Button
        bearbeiten_button = tk.Button(
            self.fenster, text="Bearbeiten", command=lambda: [self.create_new_window(back)], bg="#c2cccf", fg="black"
        )
        bearbeiten_button.place(relx=0.9, rely=0.03, width=100, height=40)

        # Auflistung hinzufügen
        self.aufgabenliste = tk.Listbox(self.fenster, width=28, height=28, bd=0, bg="#c2cccf")
        self.aufgabenliste.place(relx=0.79, rely=0.1)

        # Scrollbar der Liste
        scrollbar = tk.Scrollbar(self.fenster, bg="#FFF5EE")
        scrollbar.place(in_=self.aufgabenliste, relx=1.0, relheight=1.0, bordermode="outside")
        self.aufgabenliste.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.aufgabenliste.yview)

        # mit Doppelklick bearbeiten
        self.aufgabenliste.bind(
            "<Double-1>", lambda event: self.task_edit(self.aufgabenliste.index(f"@{event.x},{event.y}"), back)
        )

        aufgaben_label = tk.Label(self.fenster, text="Deine Aufgaben:", bg="#7991a2")
        aufgaben_label.place(relx=0.79, rely=0.06)

        # Button um task zu löschen
        loesch_button = tk.Button(
            self.fenster,
            text="Löschen",
            command=lambda: [back.delete_task(self.aufgabenliste), self.change_loesch_label()],
            bg="#535D55",
            fg="white",
        )
        loesch_button.place(relx=0.85, rely=0.85, width=100, height=40)

        self.loesch_label = tk.Label(self.fenster, bg="#7991a2")
        self.loesch_label.place(relx=0.82, rely=0.92)

        # Button zurück zur User-Auswahl
        self.back_button = tk.Button(
            self.fenster,
            text="Zurück",
            command=lambda: [self.fenster.destroy(), self.__init__(back)],
            bg="#c2cccf",
            fg="black",
        )
        self.back_button.place(relx=0.05, rely=0.018, width=100, height=30)

        # Button um User zu löschen
        user_loesch_button = tk.Button(
            self.fenster,
            text="User löschen",
            command=lambda: [
                self.delete_user(self.user),
                back.del_user(self.user),
                self.fenster.destroy(),
                self.__init__(back),
            ],
            bg="#8B0000",
            fg="white",
        )

        user_loesch_button.place(relx=0.215, rely=0.85, width=100, height=40)

        back.load_task(self.aufgabenliste, self.user)

        self.fenster.mainloop()

    # Ändert task-label und fügt task in liste ein
    def change_label_add_task(self, task):
        if task == "":
            self.task_label.config(text="Gib zuerst eine Aufgabe ein!")
        else:
            bestaetigung_task = "Die Aufgabe: '" + task + "' wurde gespeichert."
            self.task_label.config(text=bestaetigung_task)
            self.eingabefeld.delete(0, tk.END)
            self.aufgabenliste.insert(tk.END, task)
        self.label_loeschen_eingabe()

    def change_speicher_label(self):
        self.speicher_label.config(text="Ihre Aufgaben wurden gespeichert!")
        self.label_loeschen_speichern()

    def change_lade_label(self):
        self.lade_label.config(text="Ihre Aufgaben wurden geladen!")
        self.label_loeschen_laden()

    def change_loesch_label(self):
        self.loesch_label.config(text="Die ausgewählte Aufgabe\n wurde gelöscht!")
        self.label_loeschen_loeschen()

    # Loesch-Funktionen, um nur 1 Label gleichzeitig anzuzeigen
    def label_loeschen_eingabe(self):
        self.speicher_label.config(text="\n")
        self.lade_label.config(text="\n")
        self.loesch_label.config(text="\n")

    def label_loeschen_speichern(self):
        self.task_label.config(text="\n")
        self.lade_label.config(text="\n")
        self.loesch_label.config(text="\n")

    def label_loeschen_laden(self):
        self.task_label.config(text="\n")
        self.speicher_label.config(text="\n")
        self.loesch_label.config(text="\n")

    def label_loeschen_loeschen(self):
        self.task_label.config(text="\n")
        self.speicher_label.config(text="\n")
        self.lade_label.config(text="\n")

    def delete_user(self, user):
        print("delete" + user)

    # Einbinden Doppelklick und dann entsprechende Bearbeitung
    def task_edit(self, index, back):
        print(index)

        self.aufgabenliste.edit_item = index
        text = self.aufgabenliste.get(index)
        y0 = self.aufgabenliste.bbox(index)[1]
        entry = tk.Entry(self.fenster, borderwidth=0, highlightthickness=1)
        entry.bind(
            "<Return>",
            lambda event: [
                self.accept_edit(event.widget.get()),
                back.accept_edit(index, event.widget.get()),
                event.widget.destroy(),
            ],
        )
        entry.bind("<Escape>", self.cancel_edit)

        entry.insert(0, text)
        entry.selection_from(0)
        entry.selection_to("end")
        entry.place(relx=0.788, y=y0 + 70, relwidth=0.2, width=-1)
        entry.focus_set()

    # bei 'ESC' berabeiten abbrechen
    def cancel_edit(self, event):
        print("exit")
        event.widget.destroy()

    # bei 'Enter' alten Eintrag löschen und neuen hinzufügen
    def accept_edit(self, new_data):
        print("accept")

        self.aufgabenliste.delete(self.aufgabenliste.edit_item)
        self.aufgabenliste.insert(self.aufgabenliste.edit_item, new_data)

    # neues Fenster für Bearbeitung erstellen
    def create_new_window(self, back):
        self.new_window = tk.Toplevel(self.fenster)
        self.new_window.geometry("1000x600")
        self.new_window.config(bg="#E4B660")

        sel_task = self.aufgabenliste.curselection()


        task, beschreibung, self.sel_dict = back.get_values(sel_task)

        speicher_button = tk.Button(
            self.new_window,
            text="Speichern",
            command=lambda: [
                back.bearbeitung_speichern(self.textfeld.get("1.0", tk.END), self.sel_dict, self.user),
                self.new_window.destroy(),
            ],
            bg="#7e5a16",
            fg="white",
        )
        speicher_button.place(relx=0.78, rely=0.85, width=100, height=40)

        task_label = tk.Label(self.new_window, text=f"Aufgabe: '{task}'", font=("Arial", 20), bg="#E4B660")
        task_label.place(relx=0.42, rely=0.05)

        self.textfeld = tk.Text(self.new_window, height=18, width=30)
        self.textfeld.place(relx=0.7, rely=0.2)
        self.textfeld.insert(tk.END, beschreibung)

        self.cal = Calendar(self.new_window, selectmode="day", year=2024, month=11, day=10, font="Arial 12")
        self.cal.place(relx=0.1, rely=0.48)
        self.cal_button = tk.Button(
            self.new_window,
            text="Auswählen",
            command=lambda: [
                back.get_datum(self.sel_dict, self.cal.get_date()),
                self.cal_label.config(text="Fälligkeitstermin: " + self.cal.get_date()),
            ],
            bg="#7e5a16",
            fg="white",
        )
        self.cal_button.place(relx=0.2, rely=0.85, width=100, height=40)

        self.cal_label = tk.Label(self.new_window, font="Arial 12", bg="#E4B660")
        self.cal_label.place(relx=0.4, rely=0.85)

        erstellt_label = tk.Label(
            self.new_window, text="Erstellt am: " + self.sel_dict["erstellung"], font="Arial 12", bg="#E4B660"
        )
        erstellt_label.place(relx=0.1, rely=0.18)
        faellig_label = tk.Label(
            self.new_window, text="Fällig am: " + self.sel_dict["faelligkeit"], font="Arial 12", bg="#E4B660"
        )
        faellig_label.place(relx=0.1, rely=0.25)

        check_status = back.get_check_status(self.sel_dict)
        self.check_label = tk.Label(self.new_window, text=check_status, font="Arial 12", bg="#E4B660")
        self.check_label.place(relx=0.11, rely=0.32)

        self.var1 = tk.IntVar()

        self.var1.set(1) if check_status == "  Abgeschlossen!" else self.var1.set(0)

        check = tk.Checkbutton(
            self.new_window,
            text="",
            variable=self.var1,
            onvalue=1,
            offvalue=0,
            command=lambda: [back.checkbox(self.sel_dict, self.var1.get()), self.change_check_label()],
            bg="#E4B660",
        )
        check.place(relx=0.09, rely=0.32)

    def change_check_label(self):
        if self.var1.get() == 1:
            self.check_label.config(text="  Abgeschlossen!")
        else:
            self.check_label.config(text="  Noch nicht erledigt!")
