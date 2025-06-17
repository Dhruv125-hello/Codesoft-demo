import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import os

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional To-Do List App - Task Manager")
        self.root.geometry("500x500")
        self.root.config(bg="#f0f0f0")

        self.tasks = []

        # Title Label
        tk.Label(root, text="📝 To-Do List", font=("Helvetica", 18, "bold"), bg="#f0f0f0").pack(pady=10)

        # Task Entry
        self.task_entry = tk.Entry(root, font=("Arial", 14), width=30)
        self.task_entry.pack(pady=10)

        # Button Frame
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="➕ Add Task", command=self.add_task).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="✏️ Edit Task", command=self.edit_task).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="❌ Delete Task", command=self.delete_task).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="✅ Mark Done", command=self.mark_done).grid(row=0, column=3, padx=5)

        # Task Listbox
        self.task_listbox = tk.Listbox(root, font=("Arial", 12), width=50, height=15, selectbackground="#a6a6a6")
        self.task_listbox.pack(pady=10)

        # Scrollbar
        scrollbar = tk.Scrollbar(root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_listbox.yview)

        # Save & Load Buttons
        file_frame = tk.Frame(root, bg="#f0f0f0")
        file_frame.pack()

        tk.Button(file_frame, text="💾 Save Tasks", command=self.save_tasks).grid(row=0, column=0, padx=5)
        tk.Button(file_frame, text="📂 Load Tasks", command=self.load_tasks).grid(row=0, column=1, padx=5)

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append(task)
            self.update_task_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Empty Task", "Please enter a task before adding.")

    def edit_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            current_task = self.tasks[selected_index]
            updated_task = simpledialog.askstring("Edit Task", "Update your task:", initialvalue=current_task)
            if updated_task:
                self.tasks[selected_index] = updated_task
                self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a task to edit.")

    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            del self.tasks[selected_index]
            self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a task to delete.")

    def mark_done(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            task = self.tasks[selected_index]
            if not task.startswith("✔️"):
                self.tasks[selected_index] = "✔️ " + task
                self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a task to mark as done.")

    def save_tasks(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filepath:
            with open(filepath, "w") as f:
                for task in self.tasks:
                    f.write(task + "\n")
            messagebox.showinfo("Saved", f"Tasks saved successfully to:\n{filepath}")

    def load_tasks(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filepath and os.path.exists(filepath):
            with open(filepath, "r") as f:
                self.tasks = [line.strip() for line in f]
            self.update_task_listbox()

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)

# Main Execution
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
