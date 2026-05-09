import tkinter as tk
from tkinter import messagebox, ttk
import random
from PIL import Image, ImageTk, ImageSequence

class MathQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Genius Quiz")
        self.root.geometry("450x650")
        
        # Quiz State
        self.score = 0
        self.question_count = 0
        self.attempts = 0
        self.difficulty = 0
        self.current_answer = 0
        self.mistakes = []
        
        # GIF animation variables
        self.frames = []
        self.gif_label = None
        
        self.displayMenu()

    def clear_screen(self):
        """Removes all widgets from current window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def displayMenu(self):
        """Initial menu to select difficulty."""
        self.clear_screen()
        
        tk.Label(self.root, text="DIFFICULTY LEVEL", font=("Arial", 18, "bold")).pack(pady=30)
        
        levels = [
            ("Easy (Single Digit)", 1), 
            ("Moderate (Double Digit)", 2), 
            ("Advanced (4-Digits)", 4)
        ]
        
        for text, level in levels:
            tk.Button(self.root, text=text, width=25, font=("Arial", 12),
                      command=lambda l=level: self.start_quiz(l)).pack(pady=10)

    def start_quiz(self, level):
        self.difficulty = level
        self.score = 0
        self.question_count = 0
        self.mistakes = []
        self.next_question()

    def randomInt(self):
        """Determines values based on difficulty."""
        if self.difficulty == 1:
            return random.randint(1, 9)
        elif self.difficulty == 2:
            return random.randint(10, 99)
        else:
            return random.randint(1000, 9999)

    def decideOperation(self):
        """Randomly returns '+' or '-'."""
        return random.choice(['+', '-'])

    def next_question(self):
        """Prepares a new question or ends the quiz."""
        if self.question_count < 10:
            self.attempts = 1
            num1 = self.randomInt()
            num2 = self.randomInt()
            op = self.decideOperation()
            
            # Prevent negative results for a smoother experience
            if op == '-' and num1 < num2:
                num1, num2 = num2, num1
            
            self.current_problem_text = f"{num1} {op} {num2}"
            self.current_answer = eval(self.current_problem_text)
            self.displayProblem()
        else:
            self.displayResults()

    def displayProblem(self):
        """Main quiz interface."""
        self.clear_screen()
        
        # Additional Function: Progress Bar
        progress = (self.question_count / 10) * 100
        self.pb = ttk.Progressbar(self.root, length=300, value=progress, mode='determinate')
        self.pb.pack(pady=20)
        
        tk.Label(self.root, text=f"Question {self.question_count + 1} of 10", font=("Arial", 10)).pack()
        
        self.problem_label = tk.Label(self.root, text=f"{self.current_problem_text} =", font=("Arial", 28, "bold"))
        self.problem_label.pack(pady=40)
        
        self.answer_entry = tk.Entry(self.root, font=("Arial", 20), width=10, justify='center')
        self.answer_entry.pack(pady=10)
        self.answer_entry.focus_set()
        
        tk.Button(self.root, text="Submit Answer", font=("Arial", 12), 
                  command=self.check_logic, bg="#e1e1e1").pack(pady=20)
        
        # Bind "Enter" key for faster gameplay
        self.root.bind('<Return>', lambda event: self.check_logic())

    def check_logic(self):
        user_input = self.answer_entry.get().strip()
        try:
            val = int(user_input)
            self.isCorrect(val)
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a number!")

    def isCorrect(self, user_ans):
        """Validates answer and applies points/feedback."""
        if user_ans == self.current_answer:
            points = 10 if self.attempts == 1 else 5
            self.score += points
            self.flash_screen("#ccffcc") # Green flash
            self.question_count += 1
            self.next_question()
        else:
            if self.attempts == 1:
                self.flash_screen("#fff0cc") # Orange flash
                self.attempts = 2
                messagebox.showinfo("Second Chance", "Not quite! Try one more time.")
                self.answer_entry.delete(0, tk.END)
            else:
                self.flash_screen("#ffcccc") # Red flash
                self.mistakes.append(f"{self.current_problem_text} = {self.current_answer}")
                messagebox.showerror("Incorrect", f"The correct answer was {self.current_answer}")
                self.question_count += 1
                self.next_question()

    def flash_screen(self, color):
        """Briefly changes background color for visual feedback."""
        orig = self.root.cget("bg")
        self.root.configure(bg=color)
        self.root.after(200, lambda: self.root.configure(bg=orig))

    def animate_gif(self, counter):
        """Cycles through GIF frames."""
        if not self.frames: return
        frame = self.frames[counter]
        self.gif_label.configure(image=frame)
        next_counter = (counter + 1) % len(self.frames)
        self.root.after(100, lambda: self.animate_gif(next_counter))

    def displayResults(self):
        """Final screen with score, ranking, and animated GIF."""
        self.clear_screen()
        self.root.unbind('<Return>') # Stop enter key from triggering quiz logic
        
        # Determine ranking and GIF file
        if self.score >= 80:
            rank = "A+ (Math Whiz!)"
            gif_file = "happy.gif"
        elif self.score >= 60:
            rank = "B (Good Job!)"
            gif_file = "happy.gif"
        else:
            rank = "Keep Practicing!"
            gif_file = "sad.gif"

        tk.Label(self.root, text="QUIZ RESULTS", font=("Arial", 22, "bold")).pack(pady=10)
        
        # Load and Animate GIF
        try:
            pil_img = Image.open(gif_file)
            self.frames = [ImageTk.PhotoImage(img.copy().convert('RGBA')) for img in ImageSequence.Iterator(pil_img)]
            self.gif_label = tk.Label(self.root)
            self.gif_label.pack(pady=10)
            self.animate_gif(0)
        except Exception:
            tk.Label(self.root, text="[Animation not found]", fg="grey").pack()

        tk.Label(self.root, text=f"Final Score: {self.score}/100", font=("Arial", 18)).pack()
        tk.Label(self.root, text=f"Rank: {rank}", font=("Arial", 14, "italic"), fg="blue").pack(pady=5)
        
        # Mistake Review
        if self.mistakes:
            tk.Label(self.root, text="Review these items:", font=("Arial", 10, "bold")).pack(pady=5)
            for m in self.mistakes:
                tk.Label(self.root, text=m, fg="#990000").pack()

        tk.Button(self.root, text="Play Again", width=20, command=self.displayMenu).pack(pady=20)
        tk.Button(self.root, text="Exit", width=20, command=self.root.quit).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuiz(root)
    root.mainloop()