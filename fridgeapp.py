#!/usr/bin/python3
# feedback_template.py by Barron Stone
# This is an exercise file from Python GUI Development with Tkinter on lynda.com

from tkinter import *
import tkinter.ttk as ttk
import requests
import enum
from recordtype import recordtype

# API_URL = "http://localhost/beer/"
API_URL = "http://18.21.207.103:80/beer/"


class BeerType(enum.Enum):
    NONE = None
    IPA = "IPA"
    STOUT = "Stout"
    PORTER = "Porter"
    PALE_ALE = "Pale Ale"
    ALE = "Ale"
    WHEAT = "Wheat"
    AMBER = "Amber"
    LAGER = "Lager"
    BARLEY_WINE = "Barley Wine"
    SOUR = "Sour"
    BOCK = "Bock"
    PILSNER = "Pilsner"
    CIDER = "Cider"

    def __str__(self):
        return str(self.value)

    @staticmethod
    def get_values():
        return list(map(lambda t: t.value, BeerType))


BeerCheckout = recordtype("BeerCheckout", "index quantity")


def send_request(uri, data):
    url = API_URL + uri
    response = requests.post(url, json=data)
    print(response)
    return response.json()


class GUI:
    def __init__(self, master):
        master.geometry("800x480+0+0")
        master.title("Kappa Sigma Beer Fridge")
        self.style = ttk.Style()

        # Notebook Frames --------------------------------------------------------------
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill=BOTH, expand=True)
        self.checkin_tab = ttk.Frame(self.notebook)
        self.checkout_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.checkin_tab, text="Inventory Entry")
        self.notebook.add(self.checkout_tab, text="Beer Checkout")

        # Logo
        self.logo = PhotoImage(file="KappaSigma.gif").subsample(2, 2)

        # Different Tabs
        self.create_checkin_frame()
        self.create_checkout_frame()

    # ---------------------  Checkin Frame -----------------------

    def create_checkin_frame(self):
        self.BEER_ID = None

        # --- Checkin Header Frame
        self.frame_checkin_header = ttk.Frame(self.checkin_tab)
        self.frame_checkin_header.pack(fill=BOTH, expand=True)

        # Logo
        ttk.Label(self.frame_checkin_header, image=self.logo).grid(
            row=0, column=0, rowspan=2, padx=10, pady=10, sticky=E
        )

        ttk.Label(
            self.frame_checkin_header,
            text="Inventory",
            font="Arial 30 bold",
            justify="center",
        ).grid(row=0, column=1, stick="s")

        ttk.Label(
            self.frame_checkin_header,
            text="Please fill out for every variety of beer!",
            font="Arial 20 italic",
            justify="center",
        ).grid(row=1, column=1, sticky=N)

        self.frame_checkin_header.columnconfigure(1, weight=1)

        self.start_checkin_button = ttk.Button(
            self.frame_checkin_header,
            text="Start Beer Inventory",
            command=self.start_checkin,
        )
        self.start_checkin_button.grid(row=2, column=1)

        # --- Content Frame ---
        self.frame_checkin_content = ttk.Frame(self.checkin_tab)
        self.frame_checkin_content.pack(expand=True)

        self.frame_checkin_content.columnconfigure(0, weight=3)
        self.frame_checkin_content.columnconfigure(1, weight=3)

        ttk.Label(self.frame_checkin_content, text="UPC:", font="Arial, 13").grid(
            row=0, column=0, pady=5, sticky=E
        )
        ttk.Label(
            self.frame_checkin_content, text="Beer Name + Brand:", font="Arial, 13"
        ).grid(row=1, column=0, pady=5, sticky=E)
        ttk.Label(self.frame_checkin_content, text="Beer Type", font="Arial, 15").grid(
            row=2, column=0, sticky=E
        )
        ttk.Label(self.frame_checkin_content, text="Quantity:", font="Arial, 13").grid(
            row=3, column=0, pady=5, sticky=E
        )

        self.entry_UPC = ttk.Entry(
            self.frame_checkin_content, width=30, font=("Arial, 15")
        )
        self.entry_UPC.grid(row=0, column=1, sticky=W)

        self.entry_beer_name = ttk.Entry(
            self.frame_checkin_content, width=30, font="Arial, 15"
        )
        self.entry_beer_name.grid(row=1, column=1, sticky=W)

        self.entry_quantity = ttk.Entry(
            self.frame_checkin_content, width=30, font="Arial, 15"
        )
        self.entry_quantity.grid(row=3, column=1, sticky=W)

        self.beer_type = StringVar(self.frame_checkin_content)
        self.beer_type.set(BeerType.NONE)
        self.entry_beer_type = ttk.OptionMenu(
            self.frame_checkin_content, self.beer_type, *BeerType.get_values()
        )
        self.entry_beer_type.grid(row=2, column=1, sticky=W)

        self.notebook.unbind_all("<Return>")
        self.notebook.bind_all("<Return>", self.submit_upc)

        # --- Button Frame ---
        self.frame_button = ttk.Frame(self.checkin_tab)
        self.frame_button.pack()

        self.submit = ttk.Button(
            self.frame_button, text="Submit", command=self.submit_checkin
        )
        self.submit.grid(row=0, column=0, padx=10, pady=10)

        self.clear = ttk.Button(
            self.frame_button, text="Clear", command=self.clear_checkin_entries
        )
        self.clear.grid(row=0, column=1, padx=10, pady=10)

        self.disable_checkin_objects()

    def start_checkin(self):
        # Remove checkin button
        self.start_checkin_button.destroy()

        # Add checkout button back
        self.start_checkout_button.destroy()
        self.start_checkout_button = ttk.Button(
            self.frame_checkout_header,
            text="Begin Scanning Beers",
            command=self.start_checkout,
        )
        self.start_checkout_button.grid(row=4, column=3, pady=30)

        # Refresh checkout frame
        self.frame_checkout_header.destroy()
        self.create_checkout_frame()

        # Key bindings and focus
        self.notebook.unbind_all("<Key>")
        self.notebook.unbind_all("BackSpace")
        self.notebook.unbind_all("<Return>")
        self.notebook.bind_all("<Return>", self.submit_upc)

        self.enable_checkin_objects()
        self.entry_UPC.focus_set()

    def enable_checkin_objects(self):
        self.entry_UPC.state(["!disabled"])
        self.entry_beer_name.state(["!disabled"])
        self.entry_beer_type.state(["!disabled"])
        self.entry_quantity.state(["!disabled"])
        self.submit.state(["!disabled"])
        self.clear.state(["!disabled"])

    def disable_checkin_objects(self):
        self.entry_UPC.state(["disabled"])
        self.entry_beer_name.state(["disabled"])
        self.entry_beer_type.state(["disabled"])
        self.entry_quantity.state(["disabled"])
        self.submit.state(["disabled"])
        self.clear.state(["disabled"])

    # Checks to see if the UPC has already existed and autofills the info
    # If not, then user must manually enter the information
    def submit_upc(self, event):
        UPC = str(self.entry_UPC.get())
        headers = {"upc": UPC}
        response = send_request("upc", headers)

        if "success" in response["result"]:
            self.BEER_ID = int(response["beer_id"])
            self.entry_beer_name.delete(0, "end")
            self.entry_beer_name.insert(0, response["name"])
            self.beer_type.set(BeerType(response["beer_type"]))
            self.entry_quantity.focus_set()

        else:
            self.BEER_ID = None
            self.entry_beer_name.focus_set()

        self.notebook.unbind_all("<Return>")
        self.notebook.bind_all("<Return>", self.submit_checkin)

    def get_checkin_entries(self):
        upc = str(self.entry_UPC.get())
        beer_name = str(self.entry_beer_name.get())
        beer_type = str(self.beer_type.get())
        quantity = int(self.entry_quantity.get())
        print(upc, beer_name, beer_type, quantity)

        return upc, beer_name, beer_type, quantity

    def submit_checkin(self, event=None):
        UPC, BEER_NAME, BEER_TYPE, QUANTITY = self.get_checkin_entries()

        # If beer already exists in database
        if self.BEER_ID is not None:
            headers = {"beer_id": self.BEER_ID, "quantity": QUANTITY}
            response = send_request("checkin", headers)
        else:
            headers = {
                "upc": UPC,
                "name": BEER_NAME,
                "beer_type": BEER_TYPE,
                "quantity": QUANTITY,
            }
            response = send_request("checkin", headers)

        if response["result"] == "failure":
            print(f"Error checking in beer")

        self.clear_checkin_entries()
        self.entry_UPC.focus_set()
        self.notebook.unbind_all("<Return>")
        self.notebook.bind_all("<Return>", self.submit_upc)

    def clear_checkin_entries(self):
        self.entry_UPC.delete(0, "end")
        self.entry_beer_name.delete(0, "end")
        self.beer_type.set(BeerType.NONE)
        self.entry_quantity.delete(0, "end")

        self.entry_UPC.focus()
        self.notebook.unbind_all("<Return>")
        self.notebook.bind_all("<Return>", self.submit_upc)

    # ---------------------     Checkout Frame -----------------------

    def create_checkout_frame(self):
        self.frame_checkout_header = ttk.Frame(self.checkout_tab)
        self.frame_checkout_header.pack(fill=BOTH, expand=True)

        # Logo
        ttk.Label(self.frame_checkout_header, image=self.logo).grid(
            row=0, column=0, rowspan=2, padx=10, pady=10, sticky=E
        )

        # Beer Header
        ttk.Label(
            self.frame_checkout_header,
            text="Beer Checkout",
            font="Arial 26 bold",
            justify="center",
        ).grid(row=0, column=2, columnspan=5, stick=S)

        # Please Scan Header
        ttk.Label(
            self.frame_checkout_header,
            text="Please scan each beer you take!",
            font="Arial 20 italic",
            justify="center",
        ).grid(row=1, column=2, columnspan=5, sticky=N, padx=10)

        # Weighting
        self.frame_checkout_header.columnconfigure(1, weight=0)
        self.frame_checkout_header.rowconfigure(2, weight=0)

        # Start checkout Button
        self.start_checkout_button = ttk.Button(
            self.frame_checkout_header,
            text="Begin Scanning Beers",
            command=self.start_checkout,
        )
        self.start_checkout_button.grid(row=4, column=3, pady=30)

        # PIN Prompt
        self.scan_prompt = ttk.Label(
            self.frame_checkout_header,
            text="Please enter your pin: ",
            font="Arial 22 bold",
            justify="center",
        )
        self.scan_prompt.grid(row=2, column=2, stick=S, columnspan=5, pady=32)

        # PIN Entry Boxes
        self.pin_entry1 = ttk.Entry(
            self.frame_checkout_header, width=2, font=("Arial", 20)
        )
        self.pin_entry1.grid(row=3, column=2, padx=40)

        self.pin_entry2 = ttk.Entry(
            self.frame_checkout_header, width=2, font=("Arial", 20)
        )
        self.pin_entry2.grid(row=3, column=3, sticky=W, padx=40)

        self.pin_entry3 = ttk.Entry(
            self.frame_checkout_header, width=2, font=("Arial", 20)
        )
        self.pin_entry3.grid(row=3, column=4, sticky=W, padx=40)

        self.pin_entry4 = ttk.Entry(
            self.frame_checkout_header, width=2, font=("Arial", 20)
        )
        self.pin_entry4.grid(row=3, column=5, sticky=W, padx=40)

        self.exit_prompt = ttk.Label(
            self.frame_checkout_header,
            text="Press Delete or Enter to Exit/Restart: ",
            font="Arial 12",
            justify="center",
        )
        self.exit_prompt.grid(
            row=5, column=2, stick=S, columnspan=5, rowspan=6, pady=30
        )

        # Checkout state information
        self.pin_entries = [
            self.pin_entry1,
            self.pin_entry2,
            self.pin_entry3,
            self.pin_entry4,
        ]

        self.disable_checkout_objects()

    def start_checkout(self):
        # Remove checkout button
        self.start_checkout_button.destroy()
        self.enable_checkout_objects()

        # Refresh checkin frame
        self.start_checkin_button.destroy()
        self.start_checkin_button = ttk.Button(
            self.frame_checkin_header,
            text="Start Beer Inventory",
            command=self.start_checkin,
        )
        self.start_checkin_button.grid(row=2, column=1)
        self.disable_checkin_objects()

        # Key bindings and focus
        self.notebook.bind_all("<Key>", self.keypress)
        self.notebook.bind_all("<KP_Decimal>", self.restart_checkout)
        self.notebook.bind_all("<KP_Enter>", self.restart_checkout)

        self.current_digit = 0
        self.beer_code = ""
        self.upc_string = ""
        self.initials = ""
        self.checked_beers = {}

    def enable_checkout_objects(self):
        for pin in self.pin_entries:
            pin.state(["!disabled"])

    def disable_checkout_objects(self):
        for pin in self.pin_entries:
            pin.state(["disabled"])

    def restart_checkout(self, event):
        print("Restarting Checkout")
        self.frame_checkout_header.destroy()
        self.create_checkout_frame()
        self.start_checkout()

    def keypress(self, event):
        print("keypress")
        x = event.keysym
        print(x)
        if x in (
            "KP_1",
            "KP_2",
            "KP_3",
            "KP_4",
            "KP_5",
            "KP_6",
            "KP_7",
            "KP_8",
            "KP_9",
            "KP_0",
        ):
            self.pin_entries[self.current_digit].delete(0, END)
            self.pin_entries[self.current_digit].insert(0, " " + x[3])
            self.current_digit += 1
            self.beer_code += x[3]
            if self.current_digit < 4:
                self.pin_entries[self.current_digit].focus()
            else:
                headers = {"beer_code": str(self.beer_code)}
                response = send_request("login", headers)

                self.scan_prompt.destroy()
                nameLabel = ttk.Label(
                    self.frame_checkout_header,
                    text="Please scan your beers: " + response["initials"] + "!",
                    font="Arial 22 underline",
                    justify="center",
                )
                nameLabel.grid(row=2, column=2, columnspan=4, stick=S, pady=50, padx=30)

                self.pin_entry1.destroy()
                self.pin_entry2.destroy()
                self.pin_entry3.destroy()
                self.pin_entry4.destroy()

                print("Pin Destroy")

                self.notebook.unbind_all("<Key>")
                self.notebook.bind_all("<Key>", self.scan_mode)

                beer_label = ttk.Label(
                    self.frame_checkout_header,
                    text="Beers: ",
                    font="Arial 22",
                    justify="center",
                )
                beer_label.grid(row=3, column=0, stick=N)

    def scan_mode(self, event):
        print("Scan Mode")
        x = event.char
        self.notebook.unbind_all("<Return>")
        self.notebook.bind_all("<Return>", self.submit_beer)
        if x in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0"):
            self.upc_string += x

    def submit_beer(self, event):
        print("Submitting Beer")
        headers = {"upc": str(self.upc_string), "beer_code": str(self.beer_code)}
        response = send_request("checkout", headers)

        if "failure" in response["result"]:
            print("FAILURE DETECTED")
            print("upc string: " + self.upc_string)

        else:
            if self.upc_string in self.checked_beers:
                self.checked_beers[self.upc_string].quantity += 1
                self.beer = ttk.Label(
                    self.frame_checkout_header,
                    text=f"{self.checked_beers[self.upc_string].quantity}: {response['name']}",
                    font="Arial 18",
                    justify="center",
                )

                if self.checked_beers[self.upc_string].index < 4:
                    self.beer.grid(
                        row=self.checked_beers[self.upc_string].index + 3, column=2
                    )

                else:
                    self.beer.grid(
                        row=self.checked_beers[self.upc_string].index - 1, column=3
                    )

            else:
                print("Appending")
                self.checked_beers[self.upc_string] = BeerCheckout(
                    amount=1, index=len(self.checked_beers)
                )
                self.beer = ttk.Label(
                    self.frame_checkout_header,
                    text=f"{self.checked_beers[self.upc_string].amount}: {response['name']}",
                    font="Arial 18",
                    justify="center",
                )

                if self.checked_beers[self.upc_string].index < 4:
                    self.beer.grid(row=len(self.checked_beers) + 3, column=2)
                else:
                    self.beer.grid(row=len(self.checked_beers) - 1, column=3)

            self.exit_prompt.destroy()
            self.exit_prompt = ttk.Label(
                self.frame_checkout_header,
                text="Press Delete or Enter to Exit/Restart: ",
                font="Arial 12",
                justify="center",
            )
            self.exit_prompt.grid(
                row=len(self.checked_beers) + 4, column=2, stick=S, pady=5
            )
            print("Checked beers: ", self.checked_beers)

        self.upc_string = ""


# --------------------------------------------------------------------------------------------------
def main():
    root = Tk()
    root.attributes("-fullscreen", True)
    GUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
