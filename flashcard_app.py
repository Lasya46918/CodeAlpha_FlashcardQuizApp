import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

FILE_NAME = "flashcards.json"
os.path.dirname(os.path.abspath(__file__)),
"flashcards.json"


class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard Quiz App")
        self.root.geometry("700x500")
        self.root.resizable(True, True)

        self.flashcards = self.load_flashcards()
        self.current_index = 0
        self.answer_visible = False

        self.create_ui()
        self.show_card()

    def load_flashcards(self):
        if os.path.exists(FILE_NAME):
            try:
                with open(FILE_NAME, "r") as file:
                    return json.load(file)
            except:
                pass

        return [
            {
                "question": "What is Python?",
                "answer": "Python is a high-level programming language."
            },
            {
                "question": "What is SQL?",
                "answer": "SQL is used to communicate with relational databases."
            },
            {
                "question": "What is a variable?",
                "answer": "A variable is used to store data in a program."
            },
            {
                "question": "What is a database?",
                "answer": "A database is an organized collection of data."
            }
        ]

    def save_flashcards(self):
        with open(FILE_NAME, "w") as file:
            json.dump(self.flashcards, file, indent=4)

    def create_ui(self):

        title = tk.Label(
            self.root,
            text="📚 Flashcard Quiz App",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=20)

        self.counter_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 12)
        )
        self.counter_label.pack()

        self.question_frame = tk.Frame(
            self.root,
            width=600,
            height=180,
            bd=2,
            relief="ridge"
        )
        self.question_frame.pack(pady=20)
        self.question_frame.pack_propagate(False)

        self.question_label = tk.Label(
            self.question_frame,
            text="",
            font=("Arial", 18, "bold"),
            wraplength=550
        )
        self.question_label.pack(expand=True)

        self.answer_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 14),
            wraplength=550
        )
        self.answer_label.pack(pady=10)

        self.show_answer_button = tk.Button(
            self.root,
            text="Show Answer",
            font=("Arial", 12),
            command=self.show_answer
        )
        self.show_answer_button.pack(pady=5)

        navigation_frame = tk.Frame(self.root)
        navigation_frame.pack(pady=15)

        tk.Button(
            navigation_frame,
            text="⬅ Previous",
            font=("Arial", 11),
            command=self.previous_card
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            navigation_frame,
            text="Next ➡",
            font=("Arial", 11),
            command=self.next_card
        ).grid(row=0, column=1, padx=10)

        management_frame = tk.Frame(self.root)
        management_frame.pack(pady=10)

        tk.Button(
            management_frame,
            text="➕ Add",
            width=10,
            command=self.add_card
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            management_frame,
            text="✏ Edit",
            width=10,
            command=self.edit_card
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            management_frame,
            text="🗑 Delete",
            width=10,
            command=self.delete_card
        ).grid(row=0, column=2, padx=5)

    def show_card(self):

        if not self.flashcards:
            self.question_label.config(text="No flashcards available")
            self.answer_label.config(text="")
            self.counter_label.config(text="0 / 0")
            return

        card = self.flashcards[self.current_index]

        self.question_label.config(
            text=card["question"]
        )

        self.answer_label.config(text="")

        self.answer_visible = False

        self.show_answer_button.config(
            text="Show Answer"
        )

        self.counter_label.config(
            text=f"Card {self.current_index + 1} / {len(self.flashcards)}"
        )

    def show_answer(self):

        if not self.flashcards:
            return

        if not self.answer_visible:

            answer = self.flashcards[self.current_index]["answer"]

            self.answer_label.config(
                text=f"Answer: {answer}"
            )

            self.show_answer_button.config(
                text="Hide Answer"
            )

            self.answer_visible = True

        else:

            self.answer_label.config(text="")

            self.show_answer_button.config(
                text="Show Answer"
            )

            self.answer_visible = False

    def next_card(self):

        if not self.flashcards:
            return

        self.current_index += 1

        if self.current_index >= len(self.flashcards):
            self.current_index = 0

        self.show_card()

    def previous_card(self):

        if not self.flashcards:
            return

        self.current_index -= 1

        if self.current_index < 0:
            self.current_index = len(self.flashcards) - 1

        self.show_card()

    def add_card(self):

        question = simpledialog.askstring(
            "Add Flashcard",
            "Enter question:"
        )

        if not question:
            return

        answer = simpledialog.askstring(
            "Add Flashcard",
            "Enter answer:"
        )

        if not answer:
            return

        self.flashcards.append({
            "question": question,
            "answer": answer
        })

        self.save_flashcards()

        self.current_index = len(self.flashcards) - 1

        self.show_card()

        messagebox.showinfo(
            "Success",
            "Flashcard added successfully!"
        )

    def edit_card(self):

        if not self.flashcards:
            return

        card = self.flashcards[self.current_index]

        question = simpledialog.askstring(
            "Edit Flashcard",
            "Edit question:",
            initialvalue=card["question"]
        )

        if not question:
            return

        answer = simpledialog.askstring(
            "Edit Flashcard",
            "Edit answer:",
            initialvalue=card["answer"]
        )

        if not answer:
            return

        card["question"] = question
        card["answer"] = answer

        self.save_flashcards()

        self.show_card()

        messagebox.showinfo(
            "Success",
            "Flashcard updated successfully!"
        )

    def delete_card(self):

        if not self.flashcards:
            return

        confirm = messagebox.askyesno(
            "Delete Flashcard",
            "Are you sure you want to delete this flashcard?"
        )

        if not confirm:
            return

        self.flashcards.pop(self.current_index)

        if self.current_index >= len(self.flashcards):
            self.current_index = max(0, len(self.flashcards) - 1)

        self.save_flashcards()

        self.show_card()


if __name__ == "__main__":
    root = tk.Tk()

    app = FlashcardApp(root)

    root.mainloop()
