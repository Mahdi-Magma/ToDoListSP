import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
import sqlite3

class TodoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("برنامه وظایف")
        self.root.geometry("800x600")
        self.root.config(bg="#ffffff")

        self.day_mode = True
        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        # Treeview for displaying tasks
        self.task_tree = ttk.Treeview(root, selectmode='browse')
        self.task_tree['columns'] = ('task_name', 'priority', 'date', 'time', 'description')

        self.task_tree.column("#0", width=0, stretch=tk.NO)
        self.task_tree.column("task_name", anchor=tk.W, width=150)
        self.task_tree.column("priority", anchor=tk.W, width=100)
        self.task_tree.column("date", anchor=tk.W, width=100)
        self.task_tree.column("time", anchor=tk.W, width=80)
        self.task_tree.column("description", anchor=tk.W, width=250)

        self.task_tree.heading("#0", text='', anchor=tk.W)
        self.task_tree.heading("task_name", text='نام وظیفه', anchor=tk.W)
        self.task_tree.heading("priority", text='اولویت', anchor=tk.W)
        self.task_tree.heading("date", text='تاریخ', anchor=tk.W)
        self.task_tree.heading("time", text='زمان', anchor=tk.W)
        self.task_tree.heading("description", text='توضیحات', anchor=tk.W)

        self.task_tree.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        button_frame = tk.Frame(root)
        button_frame.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        add_button = tk.Button(button_frame, text="اضافه کردن", command=self.show_add_task_popup, font=('Arial', 12), bg="#2ecc71", fg="#ecf0f1")
        add_button.grid(row=0, column=0, padx=10, pady=5, sticky="ew", ipady=10)

        edit_button = tk.Button(button_frame, text="ویرایش وظیفه", command=self.show_edit_task_popup, font=('Arial', 12), bg="#3498db", fg="#ecf0f1")
        edit_button.grid(row=0, column=1, padx=10, pady=5, sticky="ew", ipady=10)

        remove_button = tk.Button(button_frame, text="حذف وظیفه", command=self.remove_task, font=('Arial', 12), bg="#e74c3c", fg="#ecf0f1")
        remove_button.grid(row=0, column=2, padx=10, pady=5, sticky="ew", ipady=10)

        complete_button = tk.Button(button_frame, text="تکمیل وظیفه", command=self.complete_task, font=('Arial', 12), bg="#f39c12", fg="#ecf0f1")
        complete_button.grid(row=0, column=3, padx=10, pady=5, sticky="ew", ipady=10)

        theme_button = tk.Button(button_frame, text="تغییر تم", command=self.toggle_theme, font=('Arial', 12), bg="#9b59b6", fg="#ecf0f1")
        theme_button.grid(row=0, column=4, padx=10, pady=5, sticky="ew", ipady=10)

        button_frame.grid_columnconfigure(0, weight=1)

        self.load_tasks()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT,
                task_priority TEXT,
                task_date TEXT,
                task_hour INTEGER,
                task_minute INTEGER,
                task_color TEXT,
                task_description TEXT
            )
        """)
        self.conn.commit()

    def load_tasks(self):
        self.cursor.execute("SELECT * FROM tasks")
        tasks = self.cursor.fetchall()

        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        for task in tasks:
            time = f"{task[4]}:{task[5]}"  # ترکیب ساعت و دقیقه برای نمایش
            # بارگذاری صحیح
            self.task_tree.insert('', 'end', values=(task[1], task[2], task[3], time, task[7]))  # task[7] توضیحات صحیح
            item = self.task_tree.get_children()[-1]

            tag_name = f"tag_{task[0]}"
            self.task_tree.tag_configure(tag_name, foreground=task[6])  # رنگ نگه‌داری شده برای تسک
            self.task_tree.item(item, tags=(tag_name,))

    def show_add_task_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("افزودن وظیفه جدید")
        popup.geometry("400x600")

        if self.day_mode:
            popup.config(bg="#ecf0f1")
        else:
            popup.config(bg="#2c3e50")

        # Task Name
        task_name_label = tk.Label(popup, text="نام وظیفه", bg=popup.cget("bg"), fg="#2c3e50")
        task_name_label.grid(row=0, column=0, padx=10, pady=10)
        self.task_name_entry = tk.Entry(popup, width=30)
        self.task_name_entry.grid(row=0, column=1, padx=10, pady=10)

        # Task Priority
        priority_label = tk.Label(popup, text="اولویت", bg=popup.cget("bg"), fg="#2c3e50")
        priority_label.grid(row=1, column=0, padx=10, pady=10)
        priority_options = ["کم", "متوسط", "زیاد"]
        priority_var = tk.StringVar()
        priority_menu = tk.OptionMenu(popup, priority_var, *priority_options)
        priority_menu.grid(row=1, column=1, padx=10, pady=10)

        # Task Date
        date_label = tk.Label(popup, text="تاریخ", bg=popup.cget("bg"), fg="#2c3e50")
        date_label.grid(row=2, column=0, padx=10, pady=10)
        calendar = Calendar(popup, selectmode='day', date_pattern='yyyy-mm-dd')
        calendar.grid(row=2, column=1, padx=10, pady=10)

        # Task Time (Separate Hour and Minute)
        hour_label = tk.Label(popup, text="ساعت", bg=popup.cget("bg"), fg="#2c3e50")
        hour_label.grid(row=3, column=0, padx=10, pady=10)
        hour_options = [f"{i:02}" for i in range(24)]
        hour_var = tk.StringVar()
        hour_menu = tk.OptionMenu(popup, hour_var, *hour_options)
        hour_menu.grid(row=3, column=1, padx=10, pady=5)

        minute_label = tk.Label(popup, text="دقیقه", bg=popup.cget("bg"), fg="#2c3e50")
        minute_label.grid(row=4, column=0, padx=10, pady=10)
        minute_options = [f"{i:02}" for i in range(60)]
        minute_var = tk.StringVar()
        minute_menu = tk.OptionMenu(popup, minute_var, *minute_options)
        minute_menu.grid(row=4, column=1, padx=10, pady=5)

        # Task Description
        description_label = tk.Label(popup, text="توضیحات", bg=popup.cget("bg"), fg="#2c3e50")
        description_label.grid(row=5, column=0, padx=10, pady=10)
        self.description_entry = tk.Text(popup, width=30, height=5)
        self.description_entry.grid(row=5, column=1, padx=10, pady=10)

        # Task Color Options
        def change_color(color):
            self.description_entry.config(fg=color)

        color_frame = tk.Frame(popup)
        color_frame.grid(row=6, column=0, columnspan=2, pady=10)

        colors = ["#e74c3c", "#2ecc71", "#f39c12", "#3498db", "#9b59b6"]
        for i, color in enumerate(colors):
            color_rect = tk.Button(color_frame, bg=color, width=3, height=1, command=lambda c=color: change_color(c))
            color_rect.grid(row=0, column=i, padx=5)

        # Save Task
        def save_task():
            task_name = self.task_name_entry.get().strip()
            task_priority = priority_var.get()
            task_date = calendar.get_date()
            task_hour = hour_var.get()
            task_minute = minute_var.get()
            task_color = self.description_entry.cget('fg')
            task_description = self.description_entry.get('1.0', tk.END).strip()  # توضیحات

            if not task_name or not task_description:
                messagebox.showwarning("هشدار", "نام وظیفه و توضیحات الزامی است!")
                return

            self.cursor.execute("""
                INSERT INTO tasks (task_name, task_priority, task_date, task_hour, task_minute, task_color, task_description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (task_name, task_priority, task_date, task_hour, task_minute, task_color, task_description))
            self.conn.commit()
            self.load_tasks()
            popup.destroy()

        save_button = tk.Button(popup, text="ذخیره", command=save_task)
        save_button.grid(row=7, column=0, padx=10, pady=10)
        cancel_button = tk.Button(popup, text="لغو", command=popup.destroy)
        cancel_button.grid(row=7, column=1, padx=10, pady=10)

    def toggle_theme(self):
        if self.day_mode:
            self.root.config(bg="#2c3e50")
            self.day_mode = False
        else:
            self.root.config(bg="#BDC3C7")
            self.day_mode = True
        self.load_tasks()

    def show_edit_task_popup(self):
        selected_task_index = self.task_tree.focus()
        if not selected_task_index:
            messagebox.showwarning("هشدار", "یک وظیفه را انتخاب کنید تا ویرایش شود")
            return

        task_values = self.task_tree.item(selected_task_index, 'values')
        self.cursor.execute("SELECT * FROM tasks WHERE task_name = ?", (task_values[0],))
        task = self.cursor.fetchone()

        popup = tk.Toplevel(self.root)
        popup.title("ویرایش وظیفه")
        popup.geometry("400x600")

        if self.day_mode:
            popup.config(bg="#ecf0f1")
        else:
            popup.config(bg="#2c3e50")

        # Task Name
        task_name_label = tk.Label(popup, text="نام وظیفه", bg=popup.cget("bg"), fg="#2c3e50")
        task_name_label.grid(row=0, column=0, padx=10, pady=10)
        task_name_entry = tk.Entry(popup, width=30)
        task_name_entry.insert(0, task[1])
        task_name_entry.grid(row=0, column=1, padx=10, pady=10)

        # Task Priority
        priority_label = tk.Label(popup, text="اولویت", bg=popup.cget("bg"), fg="#2c3e50")
        priority_label.grid(row=1, column=0, padx=10, pady=10)
        priority_options = ["کم", "متوسط", "زیاد"]
        priority_var = tk.StringVar()
        priority_var.set(task[2])
        priority_menu = tk.OptionMenu(popup, priority_var, *priority_options)
        priority_menu.grid(row=1, column=1, padx=10, pady=10)

        # Task Date
        date_label = tk.Label(popup, text="تاریخ", bg=popup.cget("bg"), fg="#2c3e50")
        date_label.grid(row=2, column=0, padx=10, pady=10)
        calendar = Calendar(popup, selectmode='day', date_pattern='yyyy-mm-dd', date=task[3])
        calendar.grid(row=2, column=1, padx=10, pady=10)

        # Task Time
        hour_label = tk.Label(popup, text="ساعت", bg=popup.cget("bg"), fg="#2c3e50")
        hour_label.grid(row=3, column=0, padx=10, pady=10)
        hour_options = [f"{i:02}" for i in range(24)]
        hour_var = tk.StringVar()
        hour_var.set(task[4])
        hour_menu = tk.OptionMenu(popup, hour_var, *hour_options)
        hour_menu.grid(row=3, column=1, padx=10, pady=5)

        minute_label = tk.Label(popup, text="دقیقه", bg=popup.cget("bg"), fg="#2c3e50")
        minute_label.grid(row=4, column=0, padx=10, pady=10)
        minute_options = [f"{i:02}" for i in range(60)]
        minute_var = tk.StringVar()
        minute_var.set(task[5])
        minute_menu = tk.OptionMenu(popup, minute_var, *minute_options)
        minute_menu.grid(row=4, column=1, padx=10, pady=5)

        # Task Description
        description_label = tk.Label(popup, text="توضیحات", bg=popup.cget("bg"), fg="#2c3e50")
        description_label.grid(row=5, column=0, padx=10, pady=10)
        description_entry = tk.Text(popup, width=30, height=5)
        description_entry.insert(tk.INSERT, task[7])  # استفاده از task[7] برای بارگذاری توضیحات
        description_entry.grid(row=5, column=1, padx=10, pady=10)

        # Save Changes
        def save_changes():
            updated_task_name = task_name_entry.get().strip()
            updated_priority = priority_var.get()
            updated_date = calendar.get_date()
            updated_hour = hour_var.get()
            updated_minute = minute_var.get()
            updated_description = description_entry.get('1.0', tk.END).strip()

            self.cursor.execute("""
                UPDATE tasks 
                SET task_name = ?, task_priority = ?, task_date = ?, task_hour = ?, task_minute = ?, task_description = ? 
                WHERE id = ?
            """, (updated_task_name, updated_priority, updated_date, updated_hour, updated_minute, updated_description, task[0]))
            self.conn.commit()
            self.load_tasks()
            popup.destroy()

        save_button = tk.Button(popup, text="ذخیره", command=save_changes)
        save_button.grid(row=6, column=0, padx=10, pady=10)

        cancel_button = tk.Button(popup, text="لغو", command=popup.destroy)
        cancel_button.grid(row=6, column=1, padx=10, pady=10)

    def remove_task(self):
        selected_task_index = self.task_tree.focus()
        if not selected_task_index:
            messagebox.showwarning("هشدار", "یک وظیفه را انتخاب کنید")
            return

        task_values = self.task_tree.item(selected_task_index, 'values')
        self.cursor.execute("DELETE FROM tasks WHERE task_name = ?", (task_values[0],))
        self.conn.commit()
        self.load_tasks()

    def complete_task(self):
        selected_task_index = self.task_tree.focus()
        if not selected_task_index:
            messagebox.showwarning("هشدار", "یک وظیفه را انتخاب کنید")
            return

        task_values = self.task_tree.item(selected_task_index, 'values')
        self.cursor.execute("UPDATE tasks SET task_description = ? WHERE task_name = ?", (f"[انجام شد] {task_values[0]}", task_values[0]))
        self.conn.commit()
        self.load_tasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()
