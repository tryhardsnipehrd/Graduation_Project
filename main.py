# TODO
# Add SQL connection, and keep it persistent in the MainWindow Class
# Make Submitting actually add to the database
# Fix tabbing through things
import sqlite3

# Imports
import tkinter as tk
import tkinter.ttk as ttk
from dataclasses import dataclass
import sqlite3 as sql


# GuestEntry
# This is the class used to hold data for the database
@dataclass
class GuestEntry:
    name: str = ""
    message: str = ""
    address: str = ""


# MainWindow
# This is the class used to actually run the GUI
class MainWindow:
    def __init__(self) -> None:
        # Create our window handle
        self.__window = tk.Tk()
        self.__window.title("Digital Graduation Book")

        self.create_widgets()
        self.pack_widgets()

        # Our data class
        self.data = GuestEntry()

        # Bind the event for the Submit Button
        self.__submit_button.bind("<Button-1>", self.submit_button_clicked)

        # Bind for our text boxes
        self.__message_box.bind("<Tab>", self.message_change_focus)
        self.__address_box.bind("<Tab>", self.address_change_focus)
        self.__submit_button.bind("<Return>", self.submit_button_clicked)

        # Now set up the database connection
        self.init_database()

    def run(self) -> None:
        self.__window.mainloop()

    def create_widgets(self) -> None:
        self.__name_label = ttk.Label(text="Name")
        self.__name_entry = ttk.Entry()
        self.__message_label = ttk.Label(text="Message")
        self.__address_label = ttk.Label(text="Address")
        self.__message_box = tk.Text(height=6)
        self.__address_box = tk.Text(height=4)
        self.__submit_button = ttk.Button(text="Submit")

        # Description text
        self.__description_text_1 = ttk.Label(
            text="Please leave a message above for TryHard!"
        )
        self.__description_text_2 = ttk.Label(text="Steps")
        self.__description_text_3 = ttk.Label(
            text="1: Type your name in the box labeled Name."
        )
        self.__description_text_4 = ttk.Label(
            text="2: Type your message to Holden in the box labeled Message."
        )
        self.__description_text_5 = ttk.Label(
            text="3: (optional) Type address in box labeled Address."
        )
        self.__description_text_6 = ttk.Label(
            text="4: Press the button labeled Submit."
        )
        self.__description_text_7 = ttk.Label(
            text="If you would like to write it instead, use the guest book here -->"
        )

    def pack_widgets(self):
        # Make the label for the name entry
        self.__name_label.pack()
        # Make the name entry itself
        self.__name_entry.pack()
        # Make the label for the message Text
        self.__message_label.pack()
        # Make the message Text itself
        self.__message_box.pack()
        # Make the address label
        self.__address_label.pack()
        # Now the entry box
        self.__address_box.pack()
        # Make the Submit Button
        self.__submit_button.pack()
        # Now the giant description
        self.__description_text_1.pack()
        self.__description_text_2.pack()
        self.__description_text_3.pack()
        self.__description_text_4.pack()
        self.__description_text_5.pack()
        self.__description_text_6.pack()
        self.__description_text_7.pack()

    def init_database(self):
        self.__connection = sql.connect("Testing.db")
        self.__cursor = self.__connection.cursor()
        try:
            self.__result = self.__cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS grad_book(id INTEGER PRIMARY KEY,
                                                    name STRING,
                                                    message STRING,
                                                    address STRING)
                """
            )
        except sqlite3.OperationalError:
            print("Table already created")

    def message_change_focus(self, *_args) -> str:
        self.__address_box.focus_set()
        return "break"

    def address_change_focus(self, *_args) -> str:
        self.__submit_button.focus_set()
        return "break"

    def submit_button_clicked(self, *_event) -> str:
        # Assign everything we need
        self.data.name = self.get_name()
        self.data.message = self.get_message()
        self.data.address = self.get_address()

        # Submit the Data to the database
        self.__cursor.execute(
            """
            INSERT INTO grad_book (name, message, address)
            VALUES (?, ?, ?);
        """,
            [self.data.name, self.data.message, self.data.address],
        )
        self.__connection.commit()

        # Now clear it all out
        self.clear_name()
        self.clear_message()
        self.clear_address()
        # Set focus to the Name now
        self.__name_entry.focus_set()
        return "break"

    def get_name(self) -> str:
        return self.__name_entry.get()

    def get_message(self) -> str:
        return self.__message_box.get("1.0", tk.END)

    def get_address(self) -> str:
        return self.__address_box.get("1.0", tk.END)

    def clear_name(self) -> None:
        self.__name_entry.delete(0, tk.END)

    def clear_message(self) -> None:
        self.__message_box.delete("1.0", tk.END)

    def clear_address(self) -> None:
        self.__address_box.delete("1.0", tk.END)


if __name__ == "__main__":
    window = MainWindow()

    window.run()
