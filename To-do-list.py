import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from datetime import datetime
import os

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 Professional To-Do List")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        
        # Title Label
        title = tk.Label(root, text="To Do List ", font=("Arial", 18, "bold"))
        title.pack(pady=10)

        # Entry Frame
        self.entry_frame = tk.Frame(root)
        self.entry_frame.pack(pady=5)

        self.task_entry = tk.Entry(self.entry_frame, width=40, font=("Arial", 12))
        self.task_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        self.add_btn = tk.Button(self.entry_frame, text="Add Task", width=10, command=self.add_task)
        self.add_btn.pack(side=tk.LEFT)

        # Listbox with Scrollbar
        self.task_frame = tk.Frame(root)
        self.task_frame.pack(pady=10)

        self.scrollbar = tk.Scrollbar(self.task_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_listbox = tk.Listbox(self.task_frame, height=15, width=60, font=("Arial", 12), yscrollcommand=self.scrollbar.set, selectbackground="skyblue")
        self.task_listbox.pack()

        self.scrollbar.config(command=self.task_listbox.yview)

        # Button Frame
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        tk.Button(self.button_frame, text="Delete Task", width=15, command=self.delete_task).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(self.button_frame, text="Mark Completed", width=15, command=self.mark_done).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.button_frame, text="Clear All", width=15, command=self.clear_tasks).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(self.button_frame, text="Save Tasks", width=15, command=self.save_tasks).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.button_frame, text="Load Tasks", width=15, command=self.load_tasks).grid(row=2, column=0, padx=5, pady=5)

        # Load last session if exists
        self.filename = "tasks.txt"
        self.load_tasks()

    def add_task(self):
        task = self.task_entry.get().strip()
        if task == "":
            messagebox.showwarning("Input Error", "Please enter a task.")
            return
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        task_str = f"{task} (Added: {timestamp})"
        self.task_listbox.insert(tk.END, task_str)
        self.task_entry.delete(0, tk.END)

    def delete_task(self):
        try:
            selected = self.task_listbox.curselection()[0]
            self.task_listbox.delete(selected)
        except IndexError:
            messagebox.showerror("Delete Error", "Please select a task to delete.")

    def mark_done(self):
        try:
            index = self.task_listbox.curselection()[0]
            task = self.task_listbox.get(index)
            if "[Done]" not in task:
                self.task_listbox.delete(index)
                self.task_listbox.insert(index, task + " [Done ✅]")
        except IndexError:
            messagebox.showerror("Selection Error", "Please select a task to mark.")

    def clear_tasks(self):
        confirm = messagebox.askyesno("Clear All", "Are you sure you want to clear all tasks?")
        if confirm:
            self.task_listbox.delete(0, tk.END)

    def save_tasks(self):
        tasks = self.task_listbox.get(0, tk.END)
        with open(self.filename, "w") as file:
            for task in tasks:
                file.write(task + "\n")
        messagebox.showinfo("Save", "Tasks saved successfully!")

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                for line in file:
                    self.task_listbox.insert(tk.END, line.strip())

# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
