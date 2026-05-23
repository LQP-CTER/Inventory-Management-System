import tkinter
import tkinter.ttk
import sqlite3

tkinter_umlauts = ['odiaeresis', 'adiaeresis', 'udiaeresis', 'Odiaeresis', 'Adiaeresis', 'Udiaeresis', 'ssharp']

# Custom Entry class for autocompletion
class myentry(tkinter.Entry):
    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list, key=str.lower)
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)

    def autocomplete(self, delta=0):
        if delta:
            self.delete(self.position, tkinter.END)
        else:
            self.position = len(self.get())
        _hits = [element for element in self._completion_list if element.lower().startswith(self.get().lower())]
        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits
        if _hits == self._hits and self._hits:
            self._hit_index = (self._hit_index + delta) % len(self._hits)
        if self._hits:
            self.delete(0, tkinter.END)
            self.insert(0, self._hits[self._hit_index])
            self.select_range(self.position, tkinter.END)

    def handle_keyrelease(self, event):
        if event.keysym in ("BackSpace", "Left", "Right", "Down", "Up"):
            if event.keysym == "BackSpace":
                self.position = self.index(tkinter.END)
            elif event.keysym == "Left" and self.position < self.index(tkinter.END):
                self.position -= 1
            elif event.keysym == "Right":
                self.position = self.index(tkinter.END)
            elif event.keysym == "Down":
                self.autocomplete(1)
            elif event.keysym == "Up":
                self.autocomplete(-1)
        elif len(event.keysym) == 1 or event.keysym in tkinter_umlauts:
            self.autocomplete()

# Custom Combobox class for autocompletion
class mycombobox(tkinter.ttk.Combobox):
    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list, key=str.lower)
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._completion_list

    def autocomplete(self, delta=0):
        if delta:
            self.delete(self.position, tkinter.END)
        else:
            self.position = len(self.get())
        _hits = [element for element in self._completion_list if element.lower().startswith(self.get().lower())]
        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits
        if _hits == self._hits and self._hits:
            self._hit_index = (self._hit_index + delta) % len(self._hits)
        if self._hits:
            self.delete(0, tkinter.END)
            self.insert(0, self._hits[self._hit_index])
            self.select_range(self.position, tkinter.END)

    def handle_keyrelease(self, event):
        if event.keysym in ("BackSpace", "Left", "Right", "Down", "Up"):
            if event.keysym == "BackSpace":
                self.position = self.index(tkinter.END)
            elif event.keysym == "Left" and self.position < self.index(tkinter.END):
                self.position -= 1
            elif event.keysym == "Right":
                self.position = self.index(tkinter.END)
            elif event.keysym == "Down":
                self.autocomplete(1)
            elif event.keysym == "Up":
                self.autocomplete(-1)
        elif len(event.keysym) == 1 or event.keysym in tkinter_umlauts:
            self.autocomplete()

# Function to get completion list from the inventory database
def get_inventory_completion_list():
    conn = sqlite3.connect("inventory_management_system.db")  # Update with your actual DB path
    cursor = conn.cursor()
    cursor.execute("SELECT Product_Name FROM inventory")
    items = [row[0] for row in cursor.fetchall()]
    conn.close()
    return items

# Test function to demonstrate autocompletion
def test():
    root = tkinter.Tk(className=' AutocompleteEntry Demo')
    entry = myentry(root)
    completion_list = get_inventory_completion_list()
    entry.set_completion_list(completion_list)
    entry.pack()
    entry.focus_set()

    combo = mycombobox(root)
    combo.set_completion_list(completion_list)
    combo.pack()
    combo.focus_set()

    root.bind('<Control-Q>', lambda event=None: root.destroy())
    root.bind('<Control-q>', lambda event=None: root.destroy())
    root.mainloop()
