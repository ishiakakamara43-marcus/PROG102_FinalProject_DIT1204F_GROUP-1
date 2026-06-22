
import tkinter as tk
from tkinter import ttk, messagebox
import json, os

FILE_NAME = "students.json"
PRIMARY = "#1E3A8A"
BG = "#F8FAFC"

class StudentPortal:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Academic Portal")
        self.root.geometry("1300x750")
        self.root.configure(bg=BG)

        self.students = []
        self.load_students()
        self.login_screen()

    def load_students(self):
        if os.path.exists(FILE_NAME):
            try:
                with open(FILE_NAME, "r") as f:
                    self.students = json.load(f)
            except:
                self.students = []

    def save_students(self):
        with open(FILE_NAME, "w") as f:
            json.dump(self.students, f, indent=4)

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def login_screen(self):
        self.clear()

        frame = tk.Frame(self.root, bg="white", padx=40, pady=40)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Student Academic Portal",
                 font=("Segoe UI", 20, "bold"),
                 bg="white", fg=PRIMARY).pack(pady=10)

        tk.Label(frame, text="Username", bg="white").pack()
        self.user = ttk.Entry(frame, width=30)
        self.user.pack(pady=5)

        tk.Label(frame, text="Password", bg="white").pack()
        self.passw = ttk.Entry(frame, show="*", width=30)
        self.passw.pack(pady=5)

        ttk.Button(frame, text="Login", command=self.login).pack(pady=10)

    def login(self):
        if self.user.get() == "admin" and self.passw.get() == "12345":
            self.dashboard()
        else:
            messagebox.showerror("Error", "Invalid Login")

    def dashboard(self):
        self.clear()

        header = tk.Frame(self.root, bg=PRIMARY, height=70)
        header.pack(fill="x")

        tk.Label(header, text="STUDENT ACADEMIC PORTAL",
                 bg=PRIMARY, fg="white",
                 font=("Segoe UI", 20, "bold")).pack(side="left", padx=20, pady=15)

        ttk.Button(header, text="Logout", command=self.login_screen).pack(side="right", padx=20)

        self.create_cards()

        form = tk.LabelFrame(self.root, text="Student Information")
        form.pack(fill="x", padx=10, pady=10)

        labels = ["Student ID", "Name", "Gender", "Department",
                  "Level", "Course", "Score"]

        self.entries = {}

        for i, lbl in enumerate(labels):
            tk.Label(form, text=lbl).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            e = ttk.Entry(form, width=35)
            e.grid(row=i, column=1, padx=5, pady=5)
            self.entries[lbl] = e

        ttk.Button(form, text="Add", command=self.add_student).grid(row=0, column=2, padx=10)
        ttk.Button(form, text="Update", command=self.update_student).grid(row=1, column=2, padx=10)
        ttk.Button(form, text="Delete", command=self.delete_student).grid(row=2, column=2, padx=10)

        search_frame = tk.Frame(self.root, bg=BG)
        search_frame.pack(fill="x", padx=10)

        tk.Label(search_frame, text="Search ID:", bg=BG).pack(side="left")
        self.search = ttk.Entry(search_frame)
        self.search.pack(side="left", padx=5)

        ttk.Button(search_frame, text="Search", command=self.search_student).pack(side="left")
        ttk.Button(search_frame, text="Generate Report", command=self.generate_report).pack(side="left", padx=5)

        cols = ("ID","Name","Gender","Department","Level","Course","Score","GPA","Status")
        self.tree = ttk.Treeview(self.root, columns=cols, show="headings")

        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.select_student)

        self.display_students()

    def create_cards(self):
        frame = tk.Frame(self.root, bg=BG)
        frame.pack(fill="x", pady=10)

        total = len(self.students)
        passed = sum(1 for s in self.students if float(s["score"]) >= 50)
        failed = total - passed

        for title, value in [("Total Students", total),
                             ("Passed", passed),
                             ("Failed", failed)]:
            card = tk.Frame(frame, bg="white", bd=1, relief="solid")
            card.pack(side="left", padx=10)
            tk.Label(card, text=title, bg="white",
                     font=("Segoe UI", 10, "bold")).pack(padx=30, pady=5)
            tk.Label(card, text=str(value), bg="white",
                     font=("Segoe UI", 18)).pack(pady=5)

    def calculate_gpa(self, score):
        score = float(score)
        if score >= 80: return 4.0
        if score >= 70: return 3.5
        if score >= 60: return 3.0
        if score >= 50: return 2.0
        return 0.0

    def status(self, score):
        return "PASS" if float(score) >= 50 else "FAIL"

    def add_student(self):
        try:
            s = {
                "id": self.entries["Student ID"].get(),
                "name": self.entries["Name"].get(),
                "gender": self.entries["Gender"].get(),
                "department": self.entries["Department"].get(),
                "level": self.entries["Level"].get(),
                "course": self.entries["Course"].get(),
                "score": self.entries["Score"].get()
            }
            self.students.append(s)
            self.save_students()
            self.display_students()
            self.create_cards()
            messagebox.showinfo("Success", "Student Added")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_students(self):
        if not hasattr(self, "tree"):
            return
        for i in self.tree.get_children():
            self.tree.delete(i)

        for s in self.students:
            self.tree.insert("", "end", values=(
                s["id"], s["name"], s["gender"], s["department"],
                s["level"], s["course"], s["score"],
                self.calculate_gpa(s["score"]),
                self.status(s["score"])
            ))

    def select_student(self, event):
        item = self.tree.focus()
        if not item:
            return
        values = self.tree.item(item, "values")

        keys = ["Student ID","Name","Gender","Department","Level","Course","Score"]
        for i,k in enumerate(keys):
            self.entries[k].delete(0, tk.END)
            self.entries[k].insert(0, values[i])

    def update_student(self):
        sid = self.entries["Student ID"].get()
        for s in self.students:
            if s["id"] == sid:
                s["name"] = self.entries["Name"].get()
                s["gender"] = self.entries["Gender"].get()
                s["department"] = self.entries["Department"].get()
                s["level"] = self.entries["Level"].get()
                s["course"] = self.entries["Course"].get()
                s["score"] = self.entries["Score"].get()
                self.save_students()
                self.display_students()
                self.create_cards()
                messagebox.showinfo("Success","Updated")
                return

    def delete_student(self):
        sid = self.entries["Student ID"].get()
        if not messagebox.askyesno("Confirm","Delete Student?"):
            return
        self.students = [s for s in self.students if s["id"] != sid]
        self.save_students()
        self.display_students()
        self.create_cards()

    def search_student(self):
        sid = self.search.get()
        for s in self.students:
            if s["id"] == sid:
                messagebox.showinfo("Found", f"Name: {s['name']}\nScore: {s['score']}")
                return
        messagebox.showerror("Not Found","Student not found")

    def generate_report(self):
        with open("student_report.txt","w") as f:
            f.write("STUDENT ACADEMIC REPORT\n\n")
            for s in self.students:
                f.write(f"{s['id']} - {s['name']} - {s['score']}\n")
        messagebox.showinfo("Success","Report Generated")

    def create_cards(self):

        if hasattr(self, 'cards_frame'):
            self.cards_frame.destroy()

        self.cards_frame = tk.Frame(self.root, bg=BG)
        self.cards_frame.pack(fill="x", pady=10)

        total = len(self.students)

        passed = sum(
            1 for s in self.students
            if float(s["score"]) >= 50
        )

        failed = total - passed

        cards = [
            ("Total Students", total),
            ("Passed", passed),
            ("Failed", failed)
        ]

        for title, value in cards:
            card = tk.Frame(
                self.cards_frame,
                bg="white",
                bd=1,
                relief="solid"
            )

            card.pack(side="left", padx=10)

            tk.Label(
                card,
                text=title,
                bg="white",
                font=("Segoe UI", 10, "bold")
            ).pack(padx=30, pady=5)

            tk.Label(
                card,
                text=str(value),
                bg="white",
                fg="blue",
                font=("Segoe UI", 18, "bold")
            ).pack(pady=10)


root = tk.Tk()
StudentPortal(root)
root.mainloop()
