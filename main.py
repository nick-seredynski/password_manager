
import os
import json
from random import randint, choice, shuffle
from tkinter import *
from tkinter import messagebox


# --- Master Login UI ---
# Login screen ui and login
def prompt_master_password():
    login_window = Tk()
    login_window.title("Master Login")
    login_window.config(padx=50, pady=50)


    # check if master password created and meets requirements
    def master_password_login():
        master_email = email_entry.get().strip()
        master_password = password_entry.get().strip()

        # check if fields are not empty
        if not master_email or not master_password:
            messagebox.showerror("Error", "Please don't leave any fields empty.")
            return

        # create entry in memory
        new_entry = {"MASTER_PASSWORD": {"email": master_email, "password": master_password}}
        filename = "data.json"

        # Load existing data
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = {}
        else:
            data = {}

        # First time login create new master password
        if "MASTER_PASSWORD" not in data:
            data.update(new_entry)
            messagebox.showinfo(title="First Login", message="Master password and email set successfully.")
            login_window.destroy()
            show_password_manager_ui()
            return

        # If master password exists authenticate correct credentials
        else:
            stored_master = data.get("MASTER_PASSWORD", {})
            if master_email == stored_master.get("email") and master_password == stored_master.get("password"):
                messagebox.showinfo(title="Login Successful", message="Welcome to Password Manager.")
                login_window.destroy()
                show_password_manager_ui()

            # incorrect password
            else:
                messagebox.showinfo(title="Error", message="Wrong email or password")
                return


    # Master Password UI

    login_window.grid_columnconfigure(0, weight=1)
    login_window.grid_columnconfigure(1, weight=3)
    login_window.grid_columnconfigure(2, weight=1)

    # Logo
    canvas = Canvas(height=200, width=200)
    logo = PhotoImage(file="padlock_logo_resized.png")
    canvas.create_image(90, 90, image=logo)

    canvas.grid(row=0, column=1)

    # email
    email_label = Label(text="Email/Username:")
    email_label.grid(row=2, column=0, sticky="e")

    # password
    password_label = Label(text="Password:")
    password_label.grid(row=3, column=0, sticky="e")


    email_entry = Entry(width=49)
    email_entry.grid(row=2, column=1, columnspan=2, sticky="w")

    # Frame for password + generate button
    password_frame = Frame(login_window)
    password_frame.grid(row=3, column=1, columnspan=2, sticky="w")

    password_entry = Entry(password_frame, width=30)
    password_entry.pack(side="left")

    login_button = Button(password_frame, text="Login", command=master_password_login)
    login_button.pack(side="left", padx=5)

    login_window.mainloop()


# --- Main UI ---
def show_password_manager_ui():
    main_window = Tk()
    main_window.title("Password Manager")
    main_window.config(padx=50, pady=50)

    # check if password meets requirements and create password
    def submit_password():
        website = website_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get().strip()

    # check if fields are not empty
        if not website or not email or not password:
            messagebox.showerror("Error", "Please don't leave any fields empty.")
            return

    # create entry in memory
        new_entry = {website: {"email": email, "password": password}}
        filename = "data.json"

    # Load existing data
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = {}
        else:
            data = {}

    # check if website entry already exists
        if website in data:
            response = messagebox.askyesnocancel(title="Warning", message=f"An entry for '{website}' already exists.\nDo you want to overwrite it?")
            if response is True:
                data.update(new_entry)
                messagebox.showinfo("Updated", f"{website} has been updated.")
            elif response is False:
    # Create a duplicate entry with suffix
                i = 1
                while f"{website}{i}" in data:
                    i += 1
                data[f"{website}{i}"] = new_entry[website]
                messagebox.showinfo("Added", f"A new entry '{website}{i}' has been created.")
            else:
    # cancelled, do nothing
                return

    #create a new entry
        else:
            data.update(new_entry)
            messagebox.showinfo("Saved", f"{website} has been added.")

    # Save data back to file
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    # generate random password
    def generate_random_password():

        # list of possible characters
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                   'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        # creates 3 lists containing random letters, symbols and numbers with a random number of each within a range
        password_letters = [choice(letters) for i in range(randint(6,8))]
        password_symbols = [choice(symbols) for i in range(randint(1,2))]
        password_numbers = [choice(numbers) for i in range(randint(1,2))]

        # password list combines previous three lists
        password_list = password_letters + password_symbols + password_numbers

        # shuffles the order in which characters appear within password list
        shuffle(password_list)

        # joins the characters in the password list so that they form a string
        password = "".join(password_list)

        # delete existing text from password field
        password_entry.delete(0, END)

        # insert password into password entry
        password_entry.insert(0, password)

    # search for email and password based on user input in website field
    def search():

        website_query = website_entry.get().strip()
        filename = "data.json"
        # check if website field is empty
        if not website_query:
            messagebox.showerror("Error", "Please fill in website field.")
            return
        else:
            if os.path.exists(filename):
                try:
                    with open(filename, "r") as f:
                        data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
            else:
                data = {}

            # check if website entry already exists
            if website_query in data:
                stored_credentials = data.get(website_entry, {[0], [0]})
                messagebox.showinfo("Success", f"Credentials exist.{stored_credentials}")

            else:
                messagebox.showinfo("Error", f"Credentials dont exist.")



    # Optional: Configure column weights
    main_window.grid_columnconfigure(0, weight=1)
    main_window.grid_columnconfigure(1, weight=3)
    main_window.grid_columnconfigure(2, weight=1)

    # Logo
    canvas = Canvas(height=200, width=200)
    logo = PhotoImage(file="padlock_logo_resized.png")
    canvas.create_image(90, 90, image=logo)


    canvas.grid(row=0, column=1)

    # --- LABELS ---
    # Website
    website_label = Label(text="Website:")
    website_label.grid(row=1, column=0, sticky="e")

    # Email
    email_label = Label(text="Email/Username:")
    email_label.grid(row=2, column=0, sticky="e")

    # Password
    password_label = Label(text="Password:")
    password_label.grid(row=3, column=0, sticky="e")


    # --- ENTRIES ---
    # Website Entry
    search_frame = Frame(main_window)
    search_frame.grid(row=1, column=1, columnspan=2, sticky="w")

    website_entry = Entry(search_frame, width=40)
    website_entry.pack(side="left")
    website_entry.focus()

    # Email Entry
    email_entry = Entry(width=49)
    email_entry.grid(row=2, column=1, columnspan=2, sticky="w")

    # Password Entry
    password_frame = Frame(main_window)
    password_frame.grid(row=3, column=1, columnspan=2, sticky="w")

    password_entry = Entry(password_frame, width=30)
    password_entry.pack(side="left")


    # --- BUTTONS ---
    # Search Button
    search_button = Button(search_frame, text=" Search ", command=search)
    search_button.pack(side="left", padx=5)

    # Generate Password Button
    generate_password_button = Button(password_frame, text="Generate Password", command=generate_random_password)
    generate_password_button.pack(side="left", padx=5)

    # Add Button
    add_button = Button(text="Add", width=41, command=submit_password)
    add_button.grid(row=4, column=1, columnspan=2, sticky="w")

    main_window.mainloop()


# on start open login window
prompt_master_password()
