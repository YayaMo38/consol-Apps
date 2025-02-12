import tkinter as tk
from tkinter import messagebox
import bcrypt  

class Person:
    def __init__(self, name, id, age, email, address, password, gender):
        self.name = name
        self.id = id
        self.age = age
        self.email = email
        self.address = address
        self.password = password  # This will store the hashed password
        self.gender = gender

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password)

    def get_address(self):
        return self.address

    def set_address(self, address):
        self.address = address

    def get_age(self):
        return self.age

    def get_gender(self):
        return self.gender

class Client(Person):
    def __init__(self, name, id, username, age, email, address, password, gender):
        # Hash the password before storing
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        super().__init__(name, id, age, email, address, hashed_password, gender)
        self.username = username
        self.subscription_plan = None
        self.bmi_data = None
        self.target = None
        self.workout_schedule = None
        self.plan = None

    def get_username(self):
        return self.username

    def set_username(self, username):
        self.username = username

    def subscribe_to_plan(self, plan_id):
        self.subscription_plan = plan_id
        return True

    def upload_bmi(self, weight, height):
        bmi = weight / (height ** 2)
        self.bmi_data = {'weight': weight, 'height': height, 'bmi': round(bmi, 2)}
        return self.bmi_data

    def set_plan(self, plan):
        self.plan = plan

class Admin:
    def __init__(self, username, password):
        # Hash the password before storing
        self.username = username
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def verify_credentials(self, username, password):
        if self.username != username:
            return False
        return bcrypt.checkpw(password.encode(), self.password)

class GymSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gym System")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")

        self.clients = {}
        self.admin = Admin("admin", "admin123")

        # Login Screen
        self.login_screen()

    def login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Gym Management System", bg="#004080", fg="white",
                 font=("Arial", 18, "bold"), height=2).pack(fill=tk.X)

        login_frame = tk.Frame(self.root, bg="#f0f0f0")
        login_frame.pack(pady=50)

        tk.Label(login_frame, text="Login as:", font=("Arial", 14), bg="#f0f0f0").grid(row=0, column=0, columnspan=2, pady=10)

        tk.Button(login_frame, text="Client", command=self.client_login, font=("Arial", 12),
                  bg="#0080ff", fg="white", width=15).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(login_frame, text="Admin", command=self.admin_login, font=("Arial", 12),
                  bg="#0080ff", fg="white", width=15).grid(row=1, column=1, padx=10, pady=10)

    def client_login(self):
        self.login("client")

    def admin_login(self):
        self.login("admin")

    def login(self, user_type):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"{user_type.capitalize()} Login", bg="#004080", fg="white",
                 font=("Arial", 18, "bold"), height=2).pack(fill=tk.X)

        login_frame = tk.Frame(self.root, bg="#f0f0f0")
        login_frame.pack(pady=50)

        tk.Label(login_frame, text="Username:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, pady=10)
        entry_username = tk.Entry(login_frame, font=("Arial", 12))
        entry_username.grid(row=0, column=1, pady=10)

        tk.Label(login_frame, text="Password:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, pady=10)
        entry_password = tk.Entry(login_frame, show="*", font=("Arial", 12))
        entry_password.grid(row=1, column=1, pady=10)

        def authenticate():
            username = entry_username.get().strip()
            password = entry_password.get().strip()

            if not username or not password:
                messagebox.showerror("Error", "Please enter both username and password.")
                return

            if user_type == "admin":
                if self.admin.verify_credentials(username, password):
                    messagebox.showinfo("Success", "Admin login successful!")
                    self.admin_dashboard()
                else:
                    messagebox.showerror("Error", "Invalid admin credentials.")
            elif user_type == "client":
                if username in self.clients and self.clients[username].verify_password(password):
                    messagebox.showinfo("Success", "Client login successful!")
                    self.client_dashboard(username)
                else:
                    messagebox.showerror("Error", "Invalid client credentials.")

        tk.Button(login_frame, text="Login", command=authenticate, font=("Arial", 12),
                  bg="#0080ff", fg="white", width=15).grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(login_frame, text="Back", command=self.login_screen, font=("Arial", 12),
                  bg="#ff0000", fg="white", width=15).grid(row=3, column=0, columnspan=2, pady=5)

    def admin_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Admin Dashboard", bg="#004080", fg="white",
                 font=("Arial", 18, "bold"), height=2).pack(fill=tk.X)

        menu_frame = tk.Frame(self.root, bg="#f0f0f0")
        menu_frame.pack(pady=20)

        tk.Button(menu_frame, text="Add Client", command=self.add_client, font=("Arial", 12),
                  bg="#0080ff", fg="white", width=15, height=2).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(menu_frame, text="View Clients", command=self.view_clients, font=("Arial", 12),
                  bg="#0080ff", fg="white", width=15, height=2).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(menu_frame, text="Set Plans", command=self.set_plans, font=("Arial", 12),
                  bg="#0080ff", fg="white", width=15, height=2).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(menu_frame, text="Logout", command=self.login_screen, font=("Arial", 12),
                  bg="#ff0000", fg="white", width=15, height=2).grid(row=1, column=1, padx=10, pady=10)

    def client_dashboard(self, username):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Client Dashboard", bg="#004080", fg="white",
                 font=("Arial", 18, "bold"), height=2).pack(fill=tk.X)

        client = self.clients[username]
        bmi_data = client.bmi_data

        info_frame = tk.Frame(self.root, bg="#f0f0f0")
        info_frame.pack(pady=20)

        tk.Label(info_frame, text=f"Name: {client.get_name()}", font=("Arial", 14), bg="#f0f0f0").pack(anchor=tk.W, pady=5)
        tk.Label(info_frame, text=f"Age: {client.get_age()}", font=("Arial", 14), bg="#f0f0f0").pack(anchor=tk.W, pady=5)
        tk.Label(info_frame, text=f"Email: {client.get_email()}", font=("Arial", 14), bg="#f0f0f0").pack(anchor=tk.W, pady=5)
        tk.Label(info_frame, text=f"Address: {client.get_address()}", font=("Arial", 14), bg="#f0f0f0").pack(anchor=tk.W, pady=5)
        tk.Label(info_frame, text=f"Gender: {client.get_gender()}", font=("Arial", 14), bg="#f0f0f0").pack(anchor=tk.W, pady=5)

        if bmi_data:
            tk.Label(info_frame, text=f"BMI: {bmi_data['bmi']} "
                                       f"(Weight: {bmi_data['weight']}kg, Height: {bmi_data['height']}m)",
                     font=("Arial", 14), bg="#f0f0f0").pack(anchor=tk.W, pady=5)
        else:
            tk.Label(info_frame, text="BMI: Not Uploaded", font=("Arial", 14), bg="#f0f0f0").pack(anchor=tk.W, pady=5)

        if client.plan:
            tk.Label(info_frame, text=f"Plan: {client.plan}", font=("Arial", 14), bg="#f0f0f0").pack(anchor=tk.W, pady=5)
        else:
            tk.Label(info_frame, text="Plan: Not Assigned", font=("Arial", 14), bg="#f0f0f0").pack(anchor=tk.W, pady=5)

        tk.Button(self.root, text="Logout", command=self.login_screen, font=("Arial", 12),
                  bg="#ff0000", fg="white", width=15).pack(pady=10)

    def add_client(self):
        def save_client():
            name = entry_name.get().strip()
            id = entry_id.get().strip()
            username = entry_username.get().strip()
            age = entry_age.get().strip()
            email = entry_email.get().strip()
            address = entry_address.get().strip()
            password = entry_password.get().strip()
            gender = gender_var.get()

            # Input Validation
            if not all([name, id, username, age, email, address, password, gender]):
                messagebox.showwarning("Error", "Please fill out all fields!")
                return

            try:
                age = int(age)
                if age <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Invalid age. Please enter a positive integer.")
                return

            if username in self.clients:
                messagebox.showerror("Error", "Username already exists. Please choose a different one.")
                return

            # Create and add the new client
            self.clients[username] = Client(name, id, username, age, email, address, password, gender)
            messagebox.showinfo("Success", "Client added successfully!")
            add_window.destroy()

        add_window = tk.Toplevel(self.root)
        add_window.title("Add Client")
        add_window.geometry("400x500")
        add_window.configure(bg="#f0f0f0")

        tk.Label(add_window, text="Add New Client", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

        form_frame = tk.Frame(add_window, bg="#f0f0f0")
        form_frame.pack(pady=10, padx=10)

        # Name
        tk.Label(form_frame, text="Name:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, sticky=tk.W, pady=5)
        entry_name = tk.Entry(form_frame, font=("Arial", 12))
        entry_name.grid(row=0, column=1, pady=5)

        # ID
        tk.Label(form_frame, text="ID:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, sticky=tk.W, pady=5)
        entry_id = tk.Entry(form_frame, font=("Arial", 12))
        entry_id.grid(row=1, column=1, pady=5)

        # Username
        tk.Label(form_frame, text="Username:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, sticky=tk.W, pady=5)
        entry_username = tk.Entry(form_frame, font=("Arial", 12))
        entry_username.grid(row=2, column=1, pady=5)

        # Age
        tk.Label(form_frame, text="Age:", font=("Arial", 12), bg="#f0f0f0").grid(row=3, column=0, sticky=tk.W, pady=5)
        entry_age = tk.Entry(form_frame, font=("Arial", 12))
        entry_age.grid(row=3, column=1, pady=5)

        # Email
        tk.Label(form_frame, text="Email:", font=("Arial", 12), bg="#f0f0f0").grid(row=4, column=0, sticky=tk.W, pady=5)
        entry_email = tk.Entry(form_frame, font=("Arial", 12))
        entry_email.grid(row=4, column=1, pady=5)

        # Address
        tk.Label(form_frame, text="Address:", font=("Arial", 12), bg="#f0f0f0").grid(row=5, column=0, sticky=tk.W, pady=5)
        entry_address = tk.Entry(form_frame, font=("Arial", 12))
        entry_address.grid(row=5, column=1, pady=5)

        # Password
        tk.Label(form_frame, text="Password:", font=("Arial", 12), bg="#f0f0f0").grid(row=6, column=0, sticky=tk.W, pady=5)
        entry_password = tk.Entry(form_frame, show="*", font=("Arial", 12))
        entry_password.grid(row=6, column=1, pady=5)

        # Gender
        tk.Label(form_frame, text="Gender:", font=("Arial", 12), bg="#f0f0f0").grid(row=7, column=0, sticky=tk.W, pady=5)
        gender_var = tk.StringVar(value="Select")
        gender_options = ["Male", "Female", "Other"]
        gender_menu = tk.OptionMenu(form_frame, gender_var, *gender_options)
        gender_menu.config(font=("Arial", 12), width=10)
        gender_menu.grid(row=7, column=1, pady=5)

        # Buttons
        button_frame = tk.Frame(add_window, bg="#f0f0f0")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Save", command=save_client, font=("Arial", 12),
                  bg="#0080ff", fg="white", width=10).grid(row=0, column=0, padx=10)

        tk.Button(button_frame, text="Cancel", command=add_window.destroy, font=("Arial", 12),
                  bg="#ff0000", fg="white", width=10).grid(row=0, column=1, padx=10)

    def set_plans(self):
        def save_plan():
            client_username = entry_client_username.get().strip()
            meal_plan = entry_meal_plan.get().strip()
            training_plan = entry_training_plan.get().strip()
            training_time = entry_training_time.get().strip()

            if not all([client_username, meal_plan, training_plan, training_time]):
                messagebox.showwarning("Error", "Please fill out all fields!")
                return

            if client_username in self.clients:
                client = self.clients[client_username]
                plan = f"Meals: {meal_plan}, Training: {training_plan}, Time: {training_time}"
                client.set_plan(plan)
                messagebox.showinfo("Success", "Plan set successfully!")
                set_plan_window.destroy()
            else:
                messagebox.showerror("Error", "Client username not found.")

        set_plan_window = tk.Toplevel(self.root)
        set_plan_window.title("Set Plans")
        set_plan_window.geometry("400x450")
        set_plan_window.configure(bg="#f0f0f0")

        tk.Label(set_plan_window, text="Set Plan for Client", font=("Arial", 16, "bold"),
                 bg="#f0f0f0").pack(pady=10)

        form_frame = tk.Frame(set_plan_window, bg="#f0f0f0")
        form_frame.pack(pady=10, padx=10)

        # Client Username
        tk.Label(form_frame, text="Client Username:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, sticky=tk.W, pady=5)
        entry_client_username = tk.Entry(form_frame, font=("Arial", 12))
        entry_client_username.grid(row=0, column=1, pady=5)

        # Meal Plan
        tk.Label(form_frame, text="Meal Plan:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, sticky=tk.W, pady=5)
        entry_meal_plan = tk.Entry(form_frame, font=("Arial", 12))
        entry_meal_plan.grid(row=1, column=1, pady=5)

        # Training Plan
        tk.Label(form_frame, text="Training Plan:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, sticky=tk.W, pady=5)
        entry_training_plan = tk.Entry(form_frame, font=("Arial", 12))
        entry_training_plan.grid(row=2, column=1, pady=5)

        # Training Time
        tk.Label(form_frame, text="Training Time:", font=("Arial", 12), bg="#f0f0f0").grid(row=3, column=0, sticky=tk.W, pady=5)
        entry_training_time = tk.Entry(form_frame, font=("Arial", 12))
        entry_training_time.grid(row=3, column=1, pady=5)

        # Buttons
        button_frame = tk.Frame(set_plan_window, bg="#f0f0f0")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Save Plan", command=save_plan, font=("Arial", 12),
                  bg="#0080ff", fg="white", width=10).grid(row=0, column=0, padx=10)

        tk.Button(button_frame, text="Cancel", command=set_plan_window.destroy, font=("Arial", 12),
                  bg="#ff0000", fg="white", width=10).grid(row=0, column=1, padx=10)

    def view_clients(self):
        view_window = tk.Toplevel(self.root)
        view_window.title("View Clients")
        view_window.geometry("600x500")
        view_window.configure(bg="#f0f0f0")

        tk.Label(view_window, text="Client List", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

        if not self.clients:
            tk.Label(view_window, text="No clients found.", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
            return

        # Create a canvas and scrollbar for scrollable content
        canvas = tk.Canvas(view_window, bg="#f0f0f0")
        scrollbar = tk.Scrollbar(view_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Dynamically add client info to scrollable_frame
        for username, client in self.clients.items():
            bmi_info = "No BMI Data" if not client.bmi_data else f"BMI: {client.bmi_data['bmi']}"
            plan_info = "No Plan" if not client.plan else client.plan
            client_info = f"Username: {username}, ID: {client.get_id()}, Name: {client.get_name()}, {bmi_info}, {plan_info}"
            tk.Label(scrollable_frame, text=client_info, font=("Arial", 12), bg="#f0f0f0", anchor="w",
                     justify=tk.LEFT).pack(fill=tk.X, padx=10, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = GymSystemApp(root)
    root.mainloop()
