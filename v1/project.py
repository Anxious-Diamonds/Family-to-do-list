"""A family to-do list"""
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
import os

class GUI:
    def __init__(self, current_user):
        self.current_user = current_user
        self.current_user.read()
        
        # colours
        self._bg_colour = "#FFFFFF"

        self._good_colour = "#BBF1D2"
        self._okay_colour = "#EEF8CD"
        self._eh_colour = "#FFC5AA"
        self._bad_colour = "#FF9D9D"
        
        # sets up root
        self._root = tk.Tk()
        self._root.protocol("WM_DELETE_WINDOW", self._on_closing)
        # change this string value if you want to change the title of the
        # window!
        self._root.title("Family to-do list")
        self._root.geometry("850x500")
        
        # fonts
        self._bold_font = tkFont.Font(family="Arial", size=14, weight="bold")
        self._std_font = tkFont.Font(family="Arial", size=14, weight="normal")
        self._small_std_font = tkFont.Font(family="Arial", size=8, weight="normal")
        self._test_font = tkFont.Font(family="Arial", size=1, weight="normal")

        # sets up frame
        self._frame = tk.Frame(self._root, bg=self._bg_colour)
        self._frame.pack(fill = "both", expand = True)
        
        # sets up variables

        # sets up tkvars
        self._task_text = tk.StringVar()
        self._task_text.set("Write your task here")
#         self._task_text.set("TEST TASK")

        self._quantity_text = tk.StringVar()
        self._quantity_text.set("Write your quantity of the task here, or leave"
                               " blank for no quantity")
#         self._quantity_text.set("QUANTITY TEST")
        
        # set up labels
        self._completed_tasks_label = tk.Label(self._frame, bg=self._bg_colour,
                                              text="Completed tasks",
                                              font=self._bold_font)
        self._incomplete_tasks_label = tk.Label(self._frame,
                                                bg=self._bg_colour,
                                                text="Incomplete tasks",
                                                font=self._bold_font)
        self._task_entry_label = tk.Label(self._frame, bg=self._bg_colour,
                                          text="Task:",
                                          font=self._bold_font)
        self._quantity_entry_label = tk.Label(self._frame, bg=self._bg_colour,
                                              text="Quantity:",
                                              font=self._bold_font)
                                              

        # sets up inputs
        self._task_input = tk.Entry(self._frame, textvariable = self._task_text,\
                                   font=self._std_font)
        
        self._quantity_input = tk.Entry(self._frame, \
                                       textvariable = self._quantity_text,\
                                       font=self._std_font)
        

        # sets up buttons
        self._attained_button = tk.Button(self._frame, text = "✓",
                                          font=self._std_font,
                                          command = self._attainment,
                                          bg=self._bad_colour,
                                          state="disabled")
        
        self._complete_task_button = tk.Button(self._frame,
                                               text = "Complete task",
                                               font=self._std_font,
                                               command = self._kill,
                                               bg=self._good_colour)
        
        self._edit_button = tk.Button(self._frame, text = "Edit", font=self._std_font,\
                              command = self._edit, bg=self._okay_colour)
        
        self._test_button = tk.Button(self._frame, text = "TEST", font=self._test_font,\
                              command = self._check_status, bg = "aqua")
        
        
        # sets up list boxes
        self._task_list_box = tk.Listbox(self._frame, bg=self._okay_colour)
        
        self._completed_tasks = tk.Listbox(self._frame, bg=self._good_colour)
        

        # sets up the grid
        self._task_entry_label.grid(row = 0, column = 1, sticky = "NSew")
        self._task_input.grid(row = 0, column = 2, sticky = "NSew")
        self._attained_button.grid(row = 0, column = 4, sticky = "NSew")
#         self._test_button.grid(row = 0, column = 4, sticky="NSew")

        self._quantity_entry_label.grid(row = 1, column = 1, sticky = "NSew")
        self._quantity_input.grid(row = 1, column = 2, sticky = "NSew")

        self._incomplete_tasks_label.grid(row = 3, column = 2, sticky = "NSew")
        self._task_list_box.grid(row = 4, column = 2, sticky = "NSew",
                                rowspan=5)
        self._edit_button.grid(row = 4, column = 4, sticky = "NSew")
        self._complete_task_button.grid(row = 5, column = 4, sticky = "NSew")
        

        self._completed_tasks_label.grid(row = 9, column = 2, sticky = "NSew")
        self._completed_tasks.grid(row = 10, column = 2, sticky = "NSew",
                                  rowspan=2)
        
        self._frame.columnconfigure(0, weight = 1)
        self._frame.columnconfigure(1, weight = 1)
        self._frame.columnconfigure(2, weight = 20)
        self._frame.columnconfigure(3, weight = 1)
        self._frame.columnconfigure(4, weight = 1)
        self._frame.columnconfigure(5, weight = 0)
        self._frame.columnconfigure(6, weight = 1)
        
        self._frame.rowconfigure(0, weight = 5)
        self._frame.rowconfigure(1, weight = 5)
        self._frame.rowconfigure(2, weight = 50)
        self._frame.rowconfigure(3, weight = 1)
        self._frame.rowconfigure(4, weight = 1)
        self._frame.rowconfigure(5, weight = 1)
        self._frame.rowconfigure(6, weight = 5)
        self._frame.rowconfigure(7, weight = 1)
        self._frame.rowconfigure(8, weight = 1)
        self._frame.rowconfigure(9, weight = 1)
        self._frame.rowconfigure(10, weight = 1)

        # adds all tasks to the list box
        try:
            for i in range(len(self.current_user.return_user_tasks())):
                print(self.current_user.return_user_tasks()[i])
                self._task_list_box.insert("end", \
                    self.current_user.return_user_tasks()[i])
                
        except TypeError:
            self._task_list_box.insert(0, "Try adding a task!")
        
        self._frame.after(1000, self._check_status)
        
    
    def start(self):
        self._root.mainloop()
    
    def _attainment(self):
        """make the task"""
        task_text_str = self._task_text.get()
        quantity_text_str = self._quantity_text.get()
        if not task_text_str in ["Write your task here", ""] and not quantity_text_str in\
           ["Write your quantity of the task here, or leave blank for no quantity"]:
            initial_len = len(self.current_user.return_user_tasks())
            # makes new task
            self.current_user.new_task(task_text_str, quantity_text_str)
            if initial_len != len(self.current_user.return_user_tasks()):
                self._add_to_list()
                self._task_text.set("")
                self._quantity_text.set("")
            else:
                tk.messagebox.showwarning("Action Failed",
                                          "Task already exists!")
    
    def _edit(self):
        """edits a task"""
        # in case there is a task there already
        #TODO: allow completed tasks to be edited too, should be pretty simple
        task = self._task_text.get()
        quantity = self._quantity_text.get()
        if self._check_attainment(task, quantity):
            self._attainment()

        edit_index = self._task_list_box.curselection()
        if len(edit_index) >= 1:
            edit_index = edit_index[0]
            temp_task = self.current_user.return_user_tasks()[edit_index]
            self._kill()
            self._task_text.set(temp_task.return_task())
            self._quantity_text.set(temp_task.return_quantity())
    
    def _kill(self):
        dead_index = self._task_list_box.curselection()
        if len(dead_index) >= 1:
            dead_index = dead_index[0]
        if isinstance(dead_index, int):
            marked_task = self.current_user.return_user_tasks()[dead_index]
            # add to completed_tasks
            self._completed_tasks.insert(0, marked_task)
            
            # delete task
            self._task_list_box.delete(dead_index)
            self.current_user.remove_task(marked_task)
            print(self.current_user.return_user_tasks())

    def _on_closing(self):
        self.current_user.write()
        self._root.destroy()

    def _add_to_list(self):
        """refreshes the shown tasks"""
        self._task_list_box.insert("end", \
                    self.current_user.return_user_tasks()[-1])
    
    def _check_status(self):
        task = self._task_text.get()
        quantity = self._quantity_text.get()
        self._check_attainment(task, quantity)
        
        
        self._frame.after(1000, self._check_status)
    
    def _check_attainment(self, task, quantity):
        if not task in ["Write your task here", ""] \
           and not quantity in\
           ["Write your quantity of the task here, or leave blank for no quantity"]:
            if len(self.current_user.return_user_tasks()) < 1:
                self._attained_button.config(state="normal", bg=self._good_colour)
#                 print('normal')
                return True
            else:
                if self._check_user_tasks(task, quantity) == False:
                    return False
                else:
                    return True
            
            
        else:
            self._attained_button.config(state="disabled", bg=self._bad_colour)
#             print('disabled')
            return False
        return True
    
    def _check_user_tasks(self, task, quantity):
        for i in range(len(self.current_user.return_user_tasks())):
            real_task = self.current_user.return_user_tasks()[i].return_task()
            real_quantity = self.current_user.return_user_tasks()[i].return_quantity()
            if task != real_task or quantity != real_quantity:
                self._attained_button.config(state="normal", bg=self._good_colour)
#                 print('normal')
            else:
                self._attained_button.config(state="disabled", bg=self._bad_colour)
#                 print('disabled')
                return False
        return True

    def change_user(self, new_user):
        """changes the user"""
        self.current_user = new_user
        

class Task:
    def __init__(self, whole_task):
        try:
            self._task, self._quantity = whole_task.split(",")
        except ValueError:
            print(self._task, self._quantity)
            raise Exception("Task is formatted incorrectly!")
    def __str__(self):
        if self._quantity != "":
            return(f"{self._task}: {self._quantity}")
        else:
            return(f"{self._task}")
    def return_task(self):
        return self._task
    def return_quantity(self):
        return self._quantity

class Tasks:
    def __init__(self, tasks):
        if isinstance(tasks, list):
            self._tasks = []
            for i in range(len(tasks)):
                self._tasks.append(Task(tasks[i]))
        else:
            if len(tasks) < 1:
                self._tasks = [Task('No tasks found, 0')]
            else:
                self._tasks = [Task(tasks)]

    def __str__(self):
        task_list = []
        for i in range(len(self._tasks)):
            task_list.append(str(self._tasks[i]))
        return(f"Tasks: {str(task_list)}")
    
    def __len__(self):
        return(len(self._tasks))
    
    def __getitem__(self, index):
        return self._tasks[index]
    
    def __add__(self, task_quantity):
        new_task, new_quantity = task_quantity
        exist = False
        for i in range(len(self._tasks)):
            if self._tasks[i].return_task() == new_task:
                if self._tasks[i].return_quantity() == new_quantity:
                    exist = True
        if not exist:
            well_done_task = new_task.strip() + ',' + new_quantity.strip()
            self._tasks.append(Task(well_done_task))

        return self
    
    def __sub__(self, task_obj):
        i = 0
        while i != len(self._tasks):
            if self._tasks[i] == task_obj:
                self._tasks.remove(self._tasks[i])
                i -= 1
            i += 1
        return self
    
    def return_tasks(self):
        return self._tasks

class File:
    def __init__(self, file):
        self._file_name = file

    def read(self):
        """reads the files"""
        try:
            with open(self._file_name) as f:
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
            with open(self._file_name, 'w') as f:
                f.write('')

            with open(self._file_name, 'a') as f:
                for i in range(len(tasks)):
                    f.write(f"{tasks[i].return_task()},{tasks[i].return_quantity()}\n")
                    print(f"Writing task '{tasks[i]}'.")
        else:
            with open(self._file_name, 'w') as f:
                f.write('')
class User:
    def __init__(self, username):
        self._user_file = File(f"{username}.txt")
        self._user_tasks = Tasks([])
        
    def read(self):
        self._user_tasks = self._user_file.read()
    
    def return_user_tasks(self):
        return self._user_tasks
    
    def write(self):
        if len(self._user_tasks) > 0:
            self._user_file.write(self._user_tasks)
        else:
            print('User has no tasks to write!')
            self._user_file.write('Write nothing')
    
    def new_task(self, task, quantity):
        """makes a new task"""
        self._user_tasks += (task.strip(), quantity.strip())
    
    def remove_task(self, task_obj):
        """removes a task"""
        self._user_tasks -= task_obj


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
