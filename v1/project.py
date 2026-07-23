"""A family to-do list"""
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
import os

class GUI:
    def __init__(self, current_user):
        self.current_user = current_user
        self.current_user.read()
        
        # sets up root
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        # change this string value if you want to change the title of the
        # window!
        self.root.title("Family to-do list")
        self.root.geometry("850x500")
        
        bold_font = tkFont.Font(family="Arial", size=14, weight="bold")
        std_font = tkFont.Font(family="Arial", size=14, weight="normal")
        small_std_font = tkFont.Font(family="Arial", size=8, weight="normal")
        test_font = tkFont.Font(family="Arial", size=1, weight="normal")

        self.good_colour = "#BBF1D2"
        self.okay_colour = "#EEF8CD"
        self.eh_colour = "#FFC5AA"
        self.bad_colour = "#FF9D9D"

        # sets up frame
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill = "both", expand = True)
        
        # sets up variables

        # sets up tkvars
        self.task_text = tk.StringVar()
        self.task_text.set("Write your task here")
#         self.task_text.set("TEST TASK")

        self.quantity_text = tk.StringVar()
        self.quantity_text.set("Write your quantity of the task here, or leave"
                               " blank for no quantity")
#         self.quantity_text.set("QUANTITY TEST")
        
        # set up labels
        self._completed_tasks_label = tk.Label(self.frame,
                                              text="Completed tasks",
                                              font=bold_font)
        self._incomplete_tasks_label = tk.Label(self.frame,
                                              text="Incomplete tasks",
                                              font=bold_font)
        self._task_entry_label = tk.Label(self.frame,
                                              text="Task:",
                                              font=bold_font)
        self._quantity_entry_label = tk.Label(self.frame,
                                              text="Quantity:",
                                              font=bold_font)
                                              

        # sets up inputs
        self.task_input = tk.Entry(self.frame, textvariable = self.task_text,\
                                   font=std_font)
        
        self.quantity_input = tk.Entry(self.frame, \
                                       textvariable = self.quantity_text,\
                                       font=std_font)
        

        # sets up buttons
        self.attained = tk.Button(self.frame, text = "✓", font=std_font,\
                                  command = self._attainment, bg=self.good_colour)
        
        self.kill = tk.Button(self.frame, text = "Complete task",
                              font=std_font, command = self._kill,
                              bg=self.good_colour)
        
        self.edit = tk.Button(self.frame, text = "Edit", font=std_font,\
                              command = self._edit, bg=self.okay_colour)
        
        self.test_button = tk.Button(self.frame, text = "TEST", font=test_font,\
                              command = self._check_status, bg = "aqua")
        
        
        # sets up list boxes
        self.task_list_box = tk.Listbox(self.frame, bg=self.okay_colour)
        
        self.completed_tasks = tk.Listbox(self.frame, bg=self.good_colour)
        

        # sets up the grid
        self._task_entry_label.grid(row = 0, column = 1, sticky = "NSew")
        self.task_input.grid(row = 0, column = 2, sticky = "NSew")
        self.attained.grid(row = 0, column = 4, sticky = "NSew")
#         self.test_button.grid(row = 0, column = 4, sticky="NSew")

        self._quantity_entry_label.grid(row = 1, column = 1, sticky = "NSew")
        self.quantity_input.grid(row = 1, column = 2, sticky = "NSew")

        self._incomplete_tasks_label.grid(row = 3, column = 2, sticky = "NSew")
        self.task_list_box.grid(row = 4, column = 2, sticky = "NSew",
                                rowspan=5)
        self.edit.grid(row = 4, column = 4, sticky = "NSew")
        self.kill.grid(row = 5, column = 4, sticky = "NSew")
        

        self._completed_tasks_label.grid(row = 9, column = 2, sticky = "NSew")
        self.completed_tasks.grid(row = 10, column = 2, sticky = "NSew",
                                  rowspan=2)
        
        self.frame.columnconfigure(0, weight = 1)
        self.frame.columnconfigure(1, weight = 1)
        self.frame.columnconfigure(2, weight = 20)
        self.frame.columnconfigure(3, weight = 1)
        self.frame.columnconfigure(4, weight = 1)
        self.frame.columnconfigure(5, weight = 0)
        self.frame.columnconfigure(6, weight = 1)
        
        self.frame.rowconfigure(0, weight = 5)
        self.frame.rowconfigure(1, weight = 5)
        self.frame.rowconfigure(2, weight = 50)
        self.frame.rowconfigure(3, weight = 1)
        self.frame.rowconfigure(4, weight = 1)
        self.frame.rowconfigure(5, weight = 1)
        self.frame.rowconfigure(6, weight = 5)
        self.frame.rowconfigure(7, weight = 1)
        self.frame.rowconfigure(8, weight = 1)
        self.frame.rowconfigure(9, weight = 1)
        self.frame.rowconfigure(10, weight = 1)

        # adds all tasks to the list box
        try:
            for i in range(len(self.current_user.return_user_tasks())):
                print(self.current_user.return_user_tasks()[i])
                self.task_list_box.insert("end", \
                    self.current_user.return_user_tasks()[i])
                
        except TypeError:
            self.task_list_box.insert(0, "Try adding a task!")
        
        self.frame.after(1000, self._check_status)
        
    
    def start(self):
        self.root.mainloop()
    
    def _attainment(self):
        """make the task"""
        task_text_str = self.task_text.get()
        quantity_text_str = self.quantity_text.get()
        if not task_text_str in ["Write your task here", ""] and not quantity_text_str in\
           ["Write your quantity of the task here, or leave blank for no quantity"]:
            initial_len = len(self.current_user.return_user_tasks())
            # makes new task
            self.current_user.new_task(task_text_str, quantity_text_str)
            if initial_len != len(self.current_user.return_user_tasks()):
                self._add_to_list()
                self.task_text.set("")
                self.quantity_text.set("")
            else:
                tk.messagebox.showwarning("Action Failed",
                                          "Task already exists!")
    
    def _edit(self):
        """edits a task"""
        # in case there is a task there already
        task = self.task_text.get()
        quantity = self.quantity_text.get()
        if self._check_attainment(task, quantity):
            self._attainment()

        edit_index = self.task_list_box.curselection()
        if len(edit_index) >= 1:
            edit_index = edit_index[0]
            temp_task = self.current_user.return_user_tasks()[edit_index]
            self._kill()
            self.task_text.set(temp_task.return_task())
            self.quantity_text.set(temp_task.return_quantity())
    
    def _kill(self):
        dead_index = self.task_list_box.curselection()
        if len(dead_index) >= 1:
            dead_index = dead_index[0]
        if isinstance(dead_index, int):
            marked_task = self.current_user.return_user_tasks()[dead_index]
            # add to completed_tasks
            self.completed_tasks.insert(0, marked_task)
            
            # delete task
            self.task_list_box.delete(dead_index)
            self.current_user.remove_task(marked_task)
            print(self.current_user.return_user_tasks())

    def _on_closing(self):
        self.current_user.write()
        self.root.destroy()

    def _add_to_list(self):
        """refreshes the shown tasks"""
        self.task_list_box.insert("end", \
                    self.current_user.return_user_tasks()[-1])
    
    def _check_status(self):
        task = self.task_text.get()
        quantity = self.quantity_text.get()
        self._check_attainment(task, quantity)
        
        
        self.frame.after(1000, self._check_status)
    
    def _check_attainment(self, task, quantity):
        if not task in ["Write your task here", ""] \
           and not quantity in\
           ["Write your quantity of the task here, or leave blank for no quantity"]:
            if len(self.current_user.return_user_tasks()) < 1:
                self.attained.config(state="normal", bg=self.good_colour)
#                 print('normal')
                return True
            else:
                if self._check_user_tasks(task, quantity) == False:
                    return False
                else:
                    return True
            
            
        else:
            self.attained.config(state="disabled", bg=self.bad_colour)
#             print('disabled')
            return False
        return True
    
    def _check_user_tasks(self, task, quantity):
        for i in range(len(self.current_user.return_user_tasks())):
            real_task = self.current_user.return_user_tasks()[i].return_task()
            real_quantity = self.current_user.return_user_tasks()[i].return_quantity()
            if task != real_task or quantity != real_quantity:
                self.attained.config(state="normal", bg=self.good_colour)
#                 print('normal')
            else:
                self.attained.config(state="disabled", bg=self.bad_colour)
#                 print('disabled')
                return False
        return True

    def change_user(self, new_user):
        """changes the user"""
        self.current_user = new_user
        

class Task:
    def __init__(self, whole_task):
        try:
            self.task, self.quantity = whole_task.split(",")
        except ValueError:
            print(self.task, self.quantity)
            raise Exception("Task is formatted incorrectly!")
    def __str__(self):
        if self.quantity != "":
            return(f"{self.task}: {self.quantity}")
        else:
            return(f"{self.task}")
    def return_task(self):
        return self.task
    def return_quantity(self):
        return self.quantity

class Tasks:
    def __init__(self, tasks):
        if isinstance(tasks, list):
            self.raw_tasks = []
            self.tasks = []
            for i in range(len(tasks)):
                self.raw_tasks.append(tasks[i])
                self.tasks.append(Task(tasks[i]))
        else:
            if len(tasks) < 1:
                self.tasks = [Task('No tasks found, 0')]
            else:
                self.tasks = [Task(tasks)]

    def __str__(self):
        task_list = []
        for i in range(len(self.tasks)):
            task_list.append(str(self.tasks[i]))
        return(f"Tasks: {str(task_list)}")
    
    def __len__(self):
        return(len(self.tasks))
    
    def __getitem__(self, index):
        return self.tasks[index]
    
    def __add__(self, task_quantity):
        new_task, new_quantity = task_quantity
        exist = False
        for i in range(len(self.tasks)):
            if self.tasks[i].return_task() == new_task:
                if self.tasks[i].return_quantity() == new_quantity:
                    exist = True
        if not exist:
            well_done_task = new_task.strip() + ',' + new_quantity.strip()
            self.tasks.append(Task(well_done_task))

        return self
    
    def __sub__(self, task_obj):
        i = 0
        while i != len(self.tasks):
            if self.tasks[i] == task_obj:
                self.tasks.remove(self.tasks[i])
                i -= 1
            i += 1
        return self
    
    def return_tasks(self):
        return self.tasks

class File:
    def __init__(self, file):
        self.file_name = file

    def read(self):
        """reads the files"""
        try:
            with open(self.file_name) as f:
                data = f.readlines()
            for i in range(len(data)):
                data[i] = data[i].strip()

        except FileNotFoundError:
            data = ['']

        tasks = Tasks(data)

        return tasks

    def write(self, tasks_obj):
        """writes tasks to the to-do list"""
        if isinstance(tasks_obj, Tasks):
            tasks = tasks_obj.return_tasks()
            with open(self.file_name, 'w') as f:
                f.write('')

            with open(self.file_name, 'a') as f:
                for i in range(len(tasks)):
                    f.write(f"{tasks[i].return_task()},{tasks[i].return_quantity()}\n")
                    print(f"Writing task '{tasks[i]}'.")
        else:
            with open(self.file_name, 'w') as f:
                f.write('')
class User:
    def __init__(self, username):
        self.user_file = File(f"{username}.txt")
        self.tasks = Tasks([])
        
    def read(self):
        self.tasks = self.user_file.read()
    
    def return_user_tasks(self):
        return self.tasks
    
    def write(self):
        if len(self.tasks) > 0:
            self.user_file.write(self.tasks)
        else:
            print('User has no tasks to write!')
            self.user_file.write('Write nothing')
    
    def new_task(self, task, quantity):
        """makes a new task"""
        self.tasks += (task.strip(), quantity.strip())
    
    def remove_task(self, task_obj):
        """removes a task"""
        self.tasks -= task_obj


def main():
    """The main project loop"""
    kid1 = User('kid1')
    gui = GUI(kid1)
    kid1.read()
#     task = 'go, 3'
#     while not task.lower() in ['quit','q']:
#         task = input('whats ur task: ')
#         if not task.lower() in ['quit', 'q']:
#             task, quantity = task.split(',')
#             kid1.new_task(task, quantity)
#     kid1.write()
#     task = input('What task do you want to remove? ')
#     kid1.remove_task(task)
#     kid1.write()
    gui.start()

main()
