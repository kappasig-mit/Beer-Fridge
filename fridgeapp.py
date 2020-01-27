#!/usr/bin/python3
# feedback_template.py by Barron Stone
# This is an exercise file from Python GUI Development with Tkinter on lynda.com

from tkinter import *
import tkinter.ttk as ttk
import requests

pin = 6
t = 8
API_URL = "http://localhost/beer/"


class GUI:
    def __init__(self, master):
        master.geometry("800x480+0+0")
        master.title("Kappa Sigma Beer Fridge")
        self.style = ttk.Style()
        self.BEER_ID = None
        # self.style.theme_use('vista')

        # Noteboook Frame --------------------------------------------------------------
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill=BOTH, expand=True)
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Inventory Entry")
        self.notebook.add(self.tab2, text="Beer Checkout")

        # Header Frame - Chile of Notebook Frame----------------------------------------
        self.frame_header = ttk.Frame(self.tab1)
        self.frame_header.pack(fill=BOTH, expand=True)

        self.header1 = ttk.Label(
            self.frame_header, text="Inventory", font="Arial 30 bold", justify="center"
        ).grid(row=0, column=1, stick="s")
        self.header2 = ttk.Label(
            self.frame_header,
            text="Please fill out for every variety of beer!",
            font="Arial 20 italic",
            justify="center",
        ).grid(row=1, column=1, sticky=N)
        self.logo = PhotoImage(file="KappaSigma.gif").subsample(2, 2)
        logo_image = ttk.Label(self.frame_header, image=self.logo).grid(
            row=0, column=0, rowspan=2, padx=10, pady=10, sticky=E
        )
        self.frame_header.columnconfigure(1, weight=1)

        self.begin_inventory = ttk.Button(
            self.frame_header, text="Start Beer Inventory", command=self.start_inventory
        )
        self.begin_inventory.grid(row=2, column=1)
        # Content Frame = Child of Notebook Frame-----------------------------------------------------------------------------------------------
        self.frame_content = ttk.Frame(self.tab1)
        self.frame_content.pack(expand=True)

        self.frame_content.columnconfigure(0, weight=3)
        self.frame_content.columnconfigure(1, weight=3)

        ttk.Label(self.frame_content, text="UPC:", font="Arial, 13").grid(
            row=0, column=0, pady=5, sticky=E
        )
        ttk.Label(self.frame_content, text="Beer Name + Brand:", font="Arial, 13").grid(
            row=1, column=0, pady=5, sticky=E
        )
        ttk.Label(self.frame_content, text="Beer Type", font="Arial, 15").grid(
            row=2, column=0, sticky=E
        )
        ttk.Label(self.frame_content, text="Quantity:", font="Arial, 13").grid(
            row=3, column=0, pady=5, sticky=E
        )

        self.entry_UPC = ttk.Entry(self.frame_content, width=30, font=("Arial, 15"))
        self.entry_UPC.grid(row=0, column=1, sticky=W)
        self.entry_UPC.state(["disabled"])

        self.entry_beertype = ttk.Entry(self.frame_content, width=30, font="Arial, 15")
        self.entry_beertype.grid(row=1, column=1, sticky=W)
        self.entry_beertype.state(["disabled"])

        self.entry_quantity = ttk.Entry(self.frame_content, width=30, font="Arial, 15")
        self.entry_quantity.grid(row=3, column=1, sticky=W)
        self.entry_quantity.state(["disabled"])

        self.beer_kind = StringVar(self.frame_content)
        self.kinds = [
            None,
            "IPA",
            "Stout",
            "Porter",
            "Pale Ale",
            "Ale",
            "Wheat",
            "Amber",
            "Lager",
            "Pilsner",
            "Barley Wine",
            "Sour",
            "Bock",
            "Cider",
        ]
        self.entry_beerkind = ttk.OptionMenu(
            self.frame_content, self.beer_kind, *self.kinds
        )
        self.entry_beerkind.grid(row=2, column=1, sticky=W)

        # self.entry_submitUPC = ttk.Button(self.frame_content, text = "Submit UPC", command = self.submitUPC).grid(row = 0, column = 3, sticky = E, padx = 10)
        self.notebook.unbind_all("<Return>")
        self.notebook.bind_all("<Return>", self.submitUPC)

        # Button Frame - Child of Notebook Frame---------------------------------------------------------------------------------------------------
        self.frame_button = ttk.Frame(self.tab1)
        self.frame_button.pack()

        self.submit = ttk.Button(
            self.frame_button, text="Submit", command=self.confirmation
        ).grid(row=0, column=0, padx=10, pady=10)
        self.clear = ttk.Button(
            self.frame_button, text="Clear", command=self.clearAll
        ).grid(row=0, column=1, padx=10, pady=10)

        # Kendall Beer Checkout Frame -----------------------------------------------------------------------------------------------------

        self.buildFrame()

    # Functions ---------------------------------------------------------------------------------------------------
    def buildFrame(self):
        self.frame_header2 = ttk.Frame(self.tab2)
        self.frame_header2.pack(fill=BOTH, expand=True)

        # Beer Header
        Header1 = ttk.Label(
            self.frame_header2,
            text="Beer Checkout",
            font="Arial 26 bold",
            justify="center",
        )
        Header1.grid(row=0, column=2, columnspan=5, stick=S)

        # Please Scan Header
        Header2 = ttk.Label(
            self.frame_header2,
            text="Please scan each beer you take!",
            font="Arial 20 italic",
            justify="center",
        )
        Header2.grid(row=1, column=2, columnspan=5, sticky=N, padx=10)

        # Logo
        logo_image = ttk.Label(self.frame_header2, image=self.logo)
        logo_image.grid(
            row=0, column=0, rowspan=3, padx=10, pady=10, sticky=N + E + W + S
        )

        # Weighting
        self.frame_header2.columnconfigure(1, weight=0)
        self.frame_header2.rowconfigure(2, weight=0)

        # PIN Prompt
        self.scanPrompt = ttk.Label(
            self.frame_header2,
            text="Please enter your pin: ",
            font="Arial 22 bold",
            justify="center",
        )
        self.scanPrompt.grid(row=2, column=2, stick=S, columnspan=5, pady=32)

        # PIN Entry Boxes
        self.pinEntry1 = ttk.Entry(self.frame_header2, width=2, font=("Arial", 20))
        self.pinEntry1.grid(row=3, column=2, padx=40)

        self.pinEntry2 = ttk.Entry(self.frame_header2, width=2, font=("Arial", 20))
        self.pinEntry2.grid(row=3, column=3, sticky=W, padx=40)

        self.pinEntry3 = ttk.Entry(self.frame_header2, width=2, font=("Arial", 20))
        self.pinEntry3.grid(row=3, column=4, sticky=W, padx=40)

        self.pinEntry4 = ttk.Entry(self.frame_header2, width=2, font=("Arial", 20))
        self.pinEntry4.grid(row=3, column=5, sticky=W, padx=40)

        self.initializeButton = ttk.Button(
            self.frame_header2, text="Begin Scanning Beers", command=self.Initialize
        )
        self.initializeButton.grid(row=4, column=3, pady=30)

        self.exitPrompt = ttk.Label(
            self.frame_header2,
            text="Press Delete or Enter to Exit/Restart: ",
            font="Arial 12",
            justify="center",
        )
        self.exitPrompt.grid(row=5, column=2, stick=S, columnspan=5, rowspan=6, pady=30)

        self.d = [self.pinEntry1, self.pinEntry2, self.pinEntry3, self.pinEntry4]
        self.current_digit = 0
        self.pinID = ""
        self.upcString = ""
        self.Initials = ""
        self.count = 3
        self.checkedBeers = []
        self.quantity = []

    def Initialize(self):
        self.initializeButton.destroy()
        self.notebook.bind_all("<Key>", self.keypress)
        self.notebook.bind_all("<KP_Decimal>", self.Exit)
        self.notebook.bind_all("<KP_Enter>", self.Exit)
        self.current_digit = 0
        self.begin_inventory.destroy()
        self.begin_inventory = ttk.Button(
            self.frame_header, text="Start Beer Inventory", command=self.start_inventory
        )
        self.begin_inventory.grid(row=2, column=1)
        self.entry_UPC.state(["disabled"])
        self.entry_beertype.state(["disabled"])
        self.entry_quantity.state(["disabled"])
        print("Initialize")

    def Exit(self, event):
        print("Exit")
        self.frame_header2.destroy()
        self.buildFrame()
        self.Initialize()

    def ping(self, uri, data):
        url = API_URL + uri
        response = requests.post(url, json=data)
        print(response)
        return response.json()

    def submitBeer(self, event):
        print("submitBeer")
        headers = {"upc": str(self.upcString), "code": str(self.pinID)}
        response = self.ping("charge", headers)
        print(self.upcString, self.pinID, time)
        print(response)

        if "failure" in response["result"]:
            print("FAILURE DETECTED")
            print("upc string: " + self.upcString)

        else:
            if self.upcString in self.checkedBeers:
                print("True")
                self.quantity[self.checkedBeers.index(self.upcString)] += 1
                self.beer = ttk.Label(
                    self.frame_header2,
                    text=str(self.quantity[self.checkedBeers.index(self.upcString)])
                    + ": "
                    + response["name"],
                    font="Arial 18",
                    justify="center",
                )

                if self.checkedBeers.index(self.upcString) < 4:
                    self.beer.grid(
                        row=self.checkedBeers.index(self.upcString) + 3, column=2
                    )

                else:
                    self.beer.grid(
                        row=self.checkedBeers.index(self.upcString) - 1, column=3
                    )

            else:
                print("Appending")
                self.checkedBeers.append(self.upcString)
                self.quantity.append(1)
                self.beer = ttk.Label(
                    self.frame_header2,
                    text=str(self.quantity[self.checkedBeers.index(self.upcString)])
                    + ": "
                    + response["name"],
                    font="Arial 18",
                    justify="center",
                )
                if self.checkedBeers.index(self.upcString) < 4:
                    self.beer.grid(row=self.count, column=2)

                else:
                    self.beer.grid(row=self.count - 4, column=3)

                self.count += 1

            self.exitPrompt.destroy
            self.exitPrompt.grid(row=self.count + 1, column=2, stick=S, pady=5)
            print("Quantity: ", self.quantity)
            print("Checked beers: ", self.checkedBeers)

        self.upcString = ""

    def scanMode(self, event):
        print("scanMode")
        x = event.char
        self.notebook.unbind_all("<Return>")
        self.notebook.bind_all("<Return>", self.submitBeer)
        if x in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0"):
            self.upcString += x
            print(x)
            print("String: ", self.upcString)

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
            self.d[self.current_digit].delete(0, END)
            self.d[self.current_digit].insert(0, " " + x[3])
            self.current_digit += 1
            self.pinID += x[3]
            if self.current_digit < 4:
                self.d[self.current_digit].focus()
            else:
                # Hardcoded response until endpoint is created
                headers = {"code": str(self.pinID)}
                response = self.ping("login", headers)
                # response = {
                #     "result": "success",
                #     "name": "Michael Kulinski",
                #     "initials": "MAK",
                # }

                self.scanPrompt.destroy()
                nameLabel = ttk.Label(
                    self.frame_header2,
                    text="Please scan your beers: " + response["initials"] + "!",
                    font="Arial 22 underline",
                    justify="center",
                )
                nameLabel.grid(row=2, column=2, columnspan=4, stick=S, pady=50, padx=30)
                print(response)
                print(self.pinID)
                self.pinEntry1.destroy()
                self.pinEntry2.destroy()
                self.pinEntry3.destroy()
                self.pinEntry4.destroy()

                print("Pin Destroy")

                self.notebook.unbind_all("<Key>")
                self.notebook.bind_all("<Key>", self.scanMode)

                beerLabel = ttk.Label(
                    self.frame_header2,
                    text="Beers: ",
                    font="Arial 22",
                    justify="center",
                )
                beerLabel.grid(row=3, column=0, stick=N)

    def get_data(self):
        self.UPC = str(self.entry_UPC.get())
        self.Beer_Type = str(self.entry_beertype.get())
        self.Quantity = self.entry_quantity.get()
        print(self.UPC)
        print(self.Beer_Type)
        print(self.Quantity)

    def clearAll(self):
        self.entry_UPC.delete(0, "end")
        self.entry_beertype.delete(0, "end")
        self.entry_quantity.delete(0, "end")
        self.entry_beertype.state(["disabled"])
        self.entry_UPC.focus()

    def confirmation(self):
        self.get_data()

        if self.BEER_ID is not None:  # return beer id and quantity
            headers = {"ID": self.BEER_ID, "QUANTITY": int(self.Quantity)}
            response = self.ping("add", headers)
        else:  # return name, quantity, and upc
            headers = {
                "upc": str(self.UPC),
                "name": str(self.Beer_Type),
                "quantity": int(self.Quantity),
                "type": str(self.beer_kind.get()),
            }
            response = self.ping("add", headers)
        self.clearAll()
        self.beer_kind.set(self.kinds[0])
        self.entry_UPC.focus_set()

    # Checks to see if the UPC has already existed and autofills the info
    # If not, then user must manually enter the information
    def submitUPC(self, event):
        # ** Hardcoded result until website endpoint created **

        UPC = str(self.entry_UPC.get())
        headers = {"upc": UPC}
        response = self.ping("upc", headers)
        # response = {
        #     "result": "success",
        #     "beer_id": 1,
        #     "name": "Natural Light",
        #     "type": "Lager",
        #     "total_consumed": 420,
        # }

        if "success" in response["result"]:
            self.BEER_ID = int(response["beer_id"])
            self.entry_beertype.state(["!disabled"])
            self.entry_beertype.insert(0, response["name"])
            self.beer_kind.set(self.kinds[self.kinds.index(response["type"])])
            self.entry_quantity.focus_set()

        else:
            self.BEER_ID = None
            self.entry_beertype.state(["!disabled"])
            self.entry_beertype.focus_set()

    def start_inventory(self):
        self.begin_inventory.destroy()
        self.initializeButton.destroy()
        self.initializeButton = ttk.Button(
            self.frame_header2, text="Begin Scanning Beers", command=self.Initialize
        )
        self.initializeButton.grid(row=4, column=3, pady=30)
        self.frame_header2.destroy()
        self.buildFrame()
        self.notebook.unbind_all("<Key>")
        self.notebook.unbind_all("BackSpace")
        self.notebook.unbind_all("Return")
        self.notebook.bind_all("<Return>", self.submitUPC)
        self.entry_UPC.state(["!disabled"])
        self.entry_UPC.focus_set()
        self.entry_quantity.state(["!disabled"])


# --------------------------------------------------------------------------------------------------
def main():
    root = Tk()
    root.attributes("-fullscreen", True)
    gui = GUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
