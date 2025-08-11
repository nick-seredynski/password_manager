
import os
import json
from tkinter import *
from tkinter import messagebox


# main UI
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)


# Login screen ui and login
def prompt_master_password():

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

        # check if master password entry already exists
        if "MASTER_PASSWORD" not in data:
            data.update(new_entry)
            messagebox.showinfo(title="First Login", message="Master password and email set successfully.")
            show_password_manager_ui()

        elif new_entry != data:
            messagebox.showinfo(title="Error", message="Wrong email or password")
        else:
            messagebox.showinfo(title="Login Successful", message="Welcome to Password Manager.")
            show_password_manager_ui()
        # Save data back to file
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    # Master Password UI

    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=3)
    window.grid_columnconfigure(2, weight=1)

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
    password_frame = Frame(window)
    password_frame.grid(row=3, column=1, columnspan=2, sticky="w")

    password_entry = Entry(password_frame, width=30)
    password_entry.pack(side="left")

    login_button = Button(password_frame, text="Login", command=master_password_login)
    login_button.pack(side="left", padx=5)

    window.mainloop()



def show_password_manager_ui():

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


    # Optional: Configure column weights
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=3)
    window.grid_columnconfigure(2, weight=1)

    # Logo
    canvas = Canvas(height=200, width=200)
    logo = PhotoImage(file="padlock_logo_resized.png")
    canvas.create_image(90, 90, image=logo)


    canvas.grid(row=0, column=1)

    #labels
    # website
    website_label = Label(text="Website:")
    website_label.grid(row=1, column=0, sticky="e")

    # email
    email_label = Label(text="Email/Username:")
    email_label.grid(row=2, column=0, sticky="e")

    # password
    password_label = Label(text="Password:")
    password_label.grid(row=3, column=0, sticky="e")

    # Entries
    website_entry = Entry(width=49)
    website_entry.grid(row=1, column=1, columnspan=2, sticky="w")
    website_entry.focus()

    email_entry = Entry(width=49)
    email_entry.grid(row=2, column=1, columnspan=2, sticky="w")


    # Frame for password + generate button
    password_frame = Frame(window)
    password_frame.grid(row=3, column=1, columnspan=2, sticky="w")

    password_entry = Entry(password_frame, width=30)
    password_entry.pack(side="left")

    generate_password_button = Button(password_frame, text="Generate Password")
    generate_password_button.pack(side="left", padx=5)

    # Add Button
    add_button = Button(text="Add", width=41, command=submit_password)
    add_button.grid(row=4, column=1, columnspan=2, sticky="w")

    window.mainloop()

prompt_master_password()
