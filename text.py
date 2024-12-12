import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage


# Dictionary to store registered users' credentials and balances
registered_users = {}
user_balances = {}


# Motorcycle parts services data
motorcycle_parts = [
    {"category": "Parts", "features": "Motor Suspension", "price": 50},
    {"category": "Parts", "features": "Motor Engine", "price": 1000},
    {"category": "Parts", "features": "Motor Wheels", "price": 200}
]
motorcycle_services = [
    {"category": "Services", "features": "Car Wash", "price": 100},
    {"category": "Services", "features": "Change Oil", "price": 30},
    {"category": "Services", "features": "Maintenance", "price": 200}
]

def register():
    # Function to handle user registration
    role = role_var.get()
    username = username_entry.get()
    password = password_entry.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "Please enter username and password")
        return

    if username in registered_users:
        messagebox.showerror("Error", "Username already exists")
    else:
        registered_users[username] = {"password": password, "role": role}
        user_balances[username] = 0  # Initialize user balance
        messagebox.showinfo("Success", "User registered successfully")
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

def login():
    # Function to handle user login
    username = username_entry.get()
    password = password_entry.get()

    if username in registered_users and registered_users[username]["password"] == password:
        messagebox.showinfo("Success", f"Login successful as {registered_users[username]['role']}")
        if registered_users[username]["role"] == "USER":
            show_services(username)
        elif registered_users[username]["role"] == "ADMIN":
            show_admin_panel()
    else:
        messagebox.showerror("Error", "Invalid username or password")

def show_services(username):
    # Function to display motorcycle parts services
    services_window = tk.Toplevel(root)
    services_window.title("Motorcycle Parts Services")
    services_window.geometry("1000x600")

    image_path = r"C:\Users\EDWIN\Downloads\OIP (1).png"  # Ensure the correct path to your image
    bg_image = PhotoImage(file=image_path)

    bg_label = tk.Label(services_window, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)  # Use services_window as the parent for the label

    header_label = tk.Label(services_window, text="Available Parts and Services", font=("Arial", 14))
    header_label.pack()

    back_button = tk.Button(services_window, text="Back", command=services_window.destroy)  # Close the current window
    back_button.pack(pady=5)

    selected_services = []

    def select_service(service):
        if service not in selected_services:
            selected_services.append(service)
        else:
            selected_services.remove(service)

    for service in motorcycle_parts:
        service_checkbutton = tk.Checkbutton(services_window,
                                             text=f"{service['category']}: {service['features']} - Php{service['price']}",
                                             command=lambda s=service: select_service(s))
        service_checkbutton.pack(anchor=tk.W)

    deposit_button = tk.Button(services_window, text="Deposit Money",
                               command=lambda: deposit_money(username))
    deposit_button.pack(pady=5)

    payment_button = tk.Button(services_window, text="Payment",
                               command=lambda: proceed_to_payment(selected_services, username))
    payment_button.pack()

def deposit_money(username):
    # Function to handle money deposit
    deposit_window = tk.Toplevel(root)
    deposit_window.title("Deposit Money")
    deposit_window.geometry("1000x600")

    image_path = r"C:\Users\EDWIN\Downloads\OIP.png"  # Ensure the correct path to your image
    bg_image = PhotoImage(file=image_path)

    bg_label = tk.Label(deposit_window, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)  # Use deposit_window as the parent for the label

    amount_label = tk.Label(deposit_window, text="Enter amount to deposit:")
    amount_label.pack()
    amount_entry = tk.Entry(deposit_window)
    amount_entry.pack()

    def perform_deposit():
        try:
            amount = float(amount_entry.get())
            user_balances[username] += amount
            messagebox.showinfo("Success", f"Successfully deposited Php{amount}")
            deposit_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")

    deposit_button = tk.Button(deposit_window, text="Deposit", command=perform_deposit)
    deposit_button.pack(pady=10)

    back_button = tk.Button(deposit_window, text="Back", command=deposit_window.destroy)
    back_button.pack(pady=5)

def proceed_to_payment(selected_services, username):
    # Function to proceed to payment
    if not selected_services:
        messagebox.showerror("Error", "Please select at least one service")
        return

    payment_window = tk.Toplevel(root)
    payment_window.title("Payment")
    payment_window.geometry("1000x600")

    # Label and entry for inputting amount
    amount_label = tk.Label(payment_window, text="Enter amount:")
    amount_label.pack()
    amount_entry = tk.Entry(payment_window)
    amount_entry.pack()

    # Payment method selection
    payment_method_label = tk.Label(payment_window, text="Select payment method:")
    payment_method_label.pack()
    payment_method_var = tk.StringVar(value="cash")
    payment_method_cash = tk.Radiobutton(payment_window, text="Cash", variable=payment_method_var, value="cash")
    payment_method_cash.pack()
    payment_method_deposit = tk.Radiobutton(payment_window, text="Card", variable=payment_method_var, value="deposit")
    payment_method_deposit.pack()


    # Validate receipt button
    validate_button = tk.Button(payment_window, text="Buy", padx=15,
                                command=lambda: validate_receipt(selected_services, amount_entry.get(), payment_method_var.get(), username, payment_window))
    validate_button.pack(pady=5)

def validate_receipt(selected_services, amount, payment_method, username, payment_window):
    # Function to validate receipt
    total_price = sum(service["price"] for service in selected_services)
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount")
        return

    if payment_method == "deposit":
        if amount > user_balances[username]:
            messagebox.showerror("Error", "Insufficient balance")
            return
        user_balances[username] -= amount
    elif payment_method == "cash":
        if amount < total_price:
            messagebox.showerror("Error", "Insufficient amount")
            return
        user_balances[username] += amount - total_price  # Add the change to the user's balance
    elif payment_method == "card":
        if amount < total_price:
            messagebox.showerror("Error", "Insufficient amount")
            return
        # Assume card payment is successful; no balance update needed

    change = amount - total_price if payment_method in ["cash", "card"] else 0

    message = "Purchased Items:\n"
    for service in selected_services:
        message += f"- {service['category']}: {service['features']} - Php{service['price']}\n"
    message += f"\nTotal Price: Php{total_price}\n"
    if payment_method in ["cash", "card"]:
        message += f"Change: Php{change}\n"
    message += f"Remaining Balance: Php{user_balances[username]}"

    messagebox.showinfo("Receipt", message)

    if messagebox.askyesno("Purchase Again", "Do you want to purchase again?"):
        payment_window.destroy()
        show_services(username)
    else:
        payment_window.destroy()
        root.deiconify()

def show_admin_panel():
    # Function to display admin panel
    admin_panel = tk.Toplevel(root)
    admin_panel.title("Admin Panel")
    admin_panel.geometry("1000x600")

    add_item_button = tk.Button(admin_panel, text="Add Item", padx=20, command=add_item)
    add_item_button.pack(pady=5)

    delete_item_button = tk.Button(admin_panel, text="Delete Item", padx=15, command=delete_item)
    delete_item_button.pack()

    edit_item_button = tk.Button(admin_panel, text="Edit Item", padx=22, command=edit_item)
    edit_item_button.pack(pady=5)

    clear_all_items_button = tk.Button(admin_panel, text="Clear All Items", padx=8, command=clear_all_items)
    clear_all_items_button.pack()

    back_button = tk.Button(admin_panel, text="Back", command=lambda: navigate_menu(admin_panel))
    back_button.pack(pady=5)

def add_item():
    add_item_window = tk.Toplevel(root)
    add_item_window.title("Add Item")
    add_item_window.geometry("1000x600")

    category_label = tk.Label(add_item_window, text="Category:")
    category_label.pack()
    category_entry = tk.Entry(add_item_window)
    category_entry.pack()

    features_label = tk.Label(add_item_window, text="New Item:")
    features_label.pack()
    features_entry = tk.Entry(add_item_window)
    features_entry.pack()

    price_label = tk.Label(add_item_window, text="Price:")
    price_label.pack()
    price_entry = tk.Entry(add_item_window)
    price_entry.pack()

    add_button = tk.Button(add_item_window, text="Add", padx=15,
                           command=lambda: add_item_to_list(category_entry.get(), features_entry.get(), price_entry.get(), add_item_window))
    add_button.pack(pady=10)

def add_item_to_list(category, features, price, add_item_window):
    try:
        price = float(price)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid price")
        return

    new_item = {"category": category, "features": features, "price": price}
    motorcycle_parts.append(new_item)
    messagebox.showinfo("Success", "Item added successfully")
    add_item_window.destroy()

def delete_item():
    delete_item_window = tk.Toplevel(root)
    delete_item_window.title("Delete Item")
    delete_item_window.geometry("1000x600")

    features_label = tk.Label(delete_item_window, text="Enter the feature of the item to delete:")
    features_label.pack()
    features_entry = tk.Entry(delete_item_window)
    features_entry.pack()

    delete_button = tk.Button(delete_item_window, text="Delete", padx=15,
                              command=lambda: delete_item_from_list(features_entry.get(), delete_item_window))
    delete_button.pack(pady=10)

def delete_item_from_list(features, delete_item_window):
    for item in motorcycle_parts:
        if item["features"] == features:
            motorcycle_parts.remove(item)
            messagebox.showinfo("Success", "Item deleted successfully")
            break
    else:
        messagebox.showerror("Error", "Item not found")
    delete_item_window.destroy()

def edit_item():
    edit_item_window = tk.Toplevel(root)
    edit_item_window.title("Edit Item")
    edit_item_window.geometry("200x250")

    features_label = tk.Label(edit_item_window, text="Enter the feature of the item to edit:")
    features_label.pack()
    features_combobox = ttk.Combobox(edit_item_window, values=[item["features"] for item in motorcycle_parts])
    features_combobox.pack()

    new_category_label = tk.Label(edit_item_window, text="New Category:")
    new_category_label.pack()
    new_category_entry = tk.Entry(edit_item_window)
    new_category_entry.pack()

    new_features_label = tk.Label(edit_item_window, text="New Item:")
    new_features_label.pack()
    new_features_entry = tk.Entry(edit_item_window)
    new_features_entry.pack()

    new_price_label = tk.Label(edit_item_window, text="New Price:")
    new_price_label.pack()
    new_price_entry = tk.Entry(edit_item_window)
    new_price_entry.pack()

    edit_button = tk.Button(edit_item_window, text="Edit", padx=10,
                            command=lambda: edit_item_in_list(features_combobox.get(), new_category_entry.get(),
                                                              new_features_entry.get(), new_price_entry.get(),
                                                              edit_item_window))
    edit_button.pack(pady=10)

def edit_item_in_list(features, new_category, new_features, new_price, edit_item_window):
    try:
        new_price = float(new_price)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid price")
        return

    for item in motorcycle_parts:
        if item["features"] == features:
            item["category"] = new_category
            item["features"] = new_features
            item["price"] = new_price
            messagebox.showinfo("Success", "Item edited successfully")
            break
    else:
        messagebox.showerror("Error", "Item not found")
    edit_item_window.destroy()

def clear_all_items():
    motorcycle_parts.clear()
    messagebox.showinfo("Success", "All items cleared successfully")

def about_us():
    messagebox.showinfo("About", "GROUP MEMBER: \nJonard John Beldia \nPiolo Mendoza\nGenre James Gones\nKai Torres\n"
                        "Features:\nMOTOR CYCLE PARTS: SERVICES\nWELCOME\nThis Project is for all who loves Motors, This platform helps everyone to purchase easily and buy the products they want. It also helps the admin to add, edit, delete, or monitor the product. Aside from that, it also helps the customers purchase easier.")

def navigate_user():
    username = username_entry.get()
    show_services(username)

    back_button = tk.Button(navigate_user, text="Back", command=navigate_menu.destroy)
    back_button.pack(pady=5)
    
def navigate_admin():
    show_admin_panel()

# Create main window
root = tk.Tk()
root.title("Motorcycle Parts: Services")
root.geometry("1000x600")

image_path = r"C:\Users\EDWIN\Downloads\motorcyle image.png"  # Ensure the correct path to your image
bg_image = PhotoImage(file=image_path)

bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1) 

role_label = tk.Label(root, text="Choose role:")
role_label.pack()
role_var = tk.StringVar()
role_combobox = ttk.Combobox(root, textvariable=role_var, values=["ADMIN", "USER"])
role_combobox.pack()

username_label = tk.Label(root, text="Username:")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

password_label = tk.Label(root, text="Password:")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

register_button = tk.Button(root, text="Register", padx=30, command=register)
register_button.pack(pady=25)

login_button = tk.Button(root, text="Login", padx=30, command=login)
login_button.pack()

exit_button = tk.Button(root, text="Exit", padx=30, command=root.quit)
exit_button.pack(pady=100)

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

navigate_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Navigation", menu=navigate_menu)

navigate_menu.add_command(label="Services", command=navigate_user)
navigate_menu.add_command(label="Admin", command=navigate_admin)

root.mainloop()
