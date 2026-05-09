import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

class StudentManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager Pro - Alexa Edition")
        self.root.geometry("1000x650")
        self.filename = "studentMarks.txt"
        self.students = []
        
        # Initialize the file with your provided data if it doesn't exist
        self.initialize_file()
        self.load_data()
        self.setup_ui()
        self.display_all()

    def initialize_file(self):
        """Initializes the text file with the specific data provided."""
        data = """10
1345,John Curry,8,15,7,45
2345,Sam Sturtivant,14,15,14,77
9876,Lee Scott,17,11,16,99
3724,Matt Thompson,19,11,15,81
1212,Ron Herrema,14,17,18,66
8439,Jake Hobbs,10,11,10,43
2344,Jo Hyde,6,15,10,55
9384,Gareth Southgate,5,6,8,33
8327,Alan Shearer,20,20,20,100
2983,Les Ferdinand,15,17,18,92"""
        with open(self.filename, "w") as f:
            f.write(data)

    def load_data(self):
        self.students = []
        try:
            if os.path.exists(self.filename):
                with open(self.filename, "r") as f:
                    lines = f.readlines()
                    # Line 0 is the count, subsequent lines are data
                    for line in lines[1:]:
                        if "," in line:
                            parts = line.strip().split(',')
                            self.students.append({
                                'id': parts[0],
                                'name': parts[1],
                                'c1': int(parts[2]),
                                'c2': int(parts[3]),
                                'c3': int(parts[4]),
                                'exam': int(parts[5])
                            })
        except Exception as e:
            messagebox.showerror("File Error", f"Error loading data: {e}")

    def save_data(self):
        try:
            with open(self.filename, "w") as f:
                f.write(f"{len(self.students)}\n")
                for s in self.students:
                    f.write(f"{s['id']},{s['name']},{s['c1']},{s['c2']},{s['c3']},{s['exam']}\n")
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save to file: {e}")

    def calculate_stats(self, s):
        cw_total = s['c1'] + s['c2'] + s['c3']
        total_score = cw_total + s['exam']
        percentage = (total_score / 160) * 100
        
        if percentage >= 70: grade = 'A'
        elif percentage >= 60: grade = 'B'
        elif percentage >= 50: grade = 'C'
        elif percentage >= 40: grade = 'D'
        else: grade = 'F'
        
        return cw_total, total_score, percentage, grade

    def setup_ui(self):
        # --- Sidebar Navigation ---
        sidebar = tk.Frame(self.root, width=200, bg="#2c3e50", padx=10, pady=10)
        sidebar.pack(side="left", fill="y")

        tk.Label(sidebar, text="COMMANDS", fg="white", bg="#2c3e50", font=("Arial", 10, "bold")).pack(pady=10)
        
        btns = [
            ("View All Records", self.display_all),
            ("Add New Student", self.add_student),
            ("Update Selection", self.update_student),
            ("Delete Selection", self.delete_student),
            ("Highest Performer", lambda: self.show_extreme("high")),
            ("Lowest Performer", lambda: self.show_extreme("low"))
        ]

        for text, cmd in btns:
            tk.Button(sidebar, text=text, command=cmd, width=18, bg="#34495e", fg="white", relief="flat").pack(pady=5)

        # --- Main Content Area ---
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(side="right", fill="both", expand=True)

        # Search Bar
        search_frame = tk.Frame(main_frame)
        search_frame.pack(fill="x", pady=(0, 10))
        tk.Label(search_frame, text="Search Student:").pack(side="left")
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=10, fill="x", expand=True)
        tk.Button(search_frame, text="🔍 Search", command=self.search_student).pack(side="left")

        # Table
        cols = ("ID", "Name", "CW Total", "Exam", "Percentage", "Grade")
        self.tree = ttk.Treeview(main_frame, columns=cols, show="headings", height=15)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill="both", expand=True)

        # Bottom Summary
        self.summary_label = tk.Label(main_frame, text="", font=("Arial", 11, "bold"), pady=10)
        self.summary_label.pack()

    def display_all(self, data_list=None):
        for i in self.tree.get_children(): self.tree.delete(i)
        
        target = data_list if data_list is not None else self.students
        if not target: return

        total_p = 0
        grade_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}

        for s in target:
            cw, total, perc, grade = self.calculate_stats(s)
            self.tree.insert("", "end", values=(s['id'], s['name'], cw, s['exam'], f"{perc:.1f}%", grade))
            total_p += perc
            grade_counts[grade] += 1
        
        avg = total_p / len(target)
        summary_text = (f"Class Size: {len(target)} | Average: {avg:.1f}% | "
                        f"Grades: A:{grade_counts['A']} B:{grade_counts['B']} C:{grade_counts['C']} D:{grade_counts['D']} F:{grade_counts['F']}")
        self.summary_label.config(text=summary_text)

    def search_student(self):
        q = self.search_entry.get().lower()
        results = [s for s in self.students if q in s['name'].lower() or q in s['id']]
        self.display_all(results)

    def show_extreme(self, mode):
        if not self.students: return
        # Find index of student with max/min percentage
        idx = 0
        ext_val = self.calculate_stats(self.students[0])[2]
        
        for i, s in enumerate(self.students):
            curr_val = self.calculate_stats(s)[2]
            if (mode == "high" and curr_val > ext_val) or (mode == "low" and curr_val < ext_val):
                ext_val = curr_val
                idx = i
        self.display_all([self.students[idx]])

    def add_student(self):
        try:
            sid = simpledialog.askstring("Input", "Student ID (1000-9999):")
            name = simpledialog.askstring("Input", "Student Name:")
            m1 = int(simpledialog.askstring("Input", "Coursework 1 (0-20):"))
            m2 = int(simpledialog.askstring("Input", "Coursework 2 (0-20):"))
            m3 = int(simpledialog.askstring("Input", "Coursework 3 (0-20):"))
            ex = int(simpledialog.askstring("Input", "Exam (0-100):"))
            
            self.students.append({'id': sid, 'name': name, 'c1': m1, 'c2': m2, 'c3': m3, 'exam': ex})
            self.save_data()
            self.display_all()
        except:
            messagebox.showerror("Error", "Invalid inputs. Record not saved.")

    def delete_student(self):
        sel = self.tree.selection()
        if not sel: return
        
        confirm = messagebox.askyesno("Confirm", "Delete this record permanently?")
        if confirm:
            sid = str(self.tree.item(sel[0])['values'][0])
            self.students = [s for s in self.students if s['id'] != sid]
            self.save_data()
            self.display_all()

    def update_student(self):
        sel = self.tree.selection()
        if not sel: return
        
        sid = str(self.tree.item(sel[0])['values'][0])
        for s in self.students:
            if s['id'] == sid:
                val = simpledialog.askinteger("Update", f"Update Exam for {s['name']}:", initialvalue=s['exam'])
                if val is not None:
                    s['exam'] = val
                    self.save_data()
                    self.display_all()
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManager(root)
    root.mainloop()