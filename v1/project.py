"""A family to-do list"""
import tkinter as tk
import tkinter.font as tkFont
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
        self.root.geometry("400x400")
        
        std_font = tkFont.Font(family="Arial", size=14, weight="normal")
 
        # sets up frame
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill = "both", expand = True)

        # sets up tkvars
        self.task_text = tk.StringVar()
        self.task_text.set("Write your task here")

        # sets up inputs
        self.task_input = tk.Entry(self.frame, textvariable = self.task_text,\
                                   font=std_font)
        self.task_input.pack()

        # sets up buttons
        self.attained = tk.Button(self.frame, text = "✓", font=std_font,\
                                  command = self._attainment)
        self.attained.pack()
        self.kill = tk.Button(self.frame, text = "KILL TASK", font=std_font,\
                              command = self._kill)
        self.kill.pack()
        self.edit = tk.Button(self.frame, text = "Edit", font=std_font,\
                              command = self._edit)
        self.edit.pack()
        
        # sets up list box
        self.task_list_box = tk.Listbox(self.root)
        self.task_list_box.pack()
        #print(self.user_tasks)
        try:
            for i in range(len(self.current_user.return_user_tasks())):
                print(self.current_user.return_user_tasks()[i].return_task_and_quantity())
                self.task_list_box.insert("end", \
                    self.current_user.return_user_tasks()[i].return_task_and_quantity())
                
        except TypeError:
            self.task_list_box.insert(0, "Try adding a task!")
        
#         self.current_user.remove_task(\
#                 self.current_user.return_user_tasks()[0].return_task_and_quantity())
        
    
    def start(self):
        self.root.mainloop()
    
    def _attainment(self):
        """make the task"""
        task_text_str = self.task_text.get()
        if not task_text_str in ["Write your task here", ""]:
            initial_len = len(self.current_user.return_user_tasks())
            self.current_user.new_task(task_text_str)
            if initial_len != len(self.current_user.return_user_tasks()):
                self._update_list()
                self.task_text.set("")
    
    def _edit(self):
        """edits a task"""
        edit_index = self.task_list_box.curselection()
        if len(edit_index) >= 1:
            edit_index = edit_index[0]
            temp_task = self.current_user.return_user_tasks()[edit_index]
            self._kill()
            self.task_text.set(temp_task.return_task_and_quantity())
    
    def _kill(self):
        dead_index = self.task_list_box.curselection()
        if len(dead_index) >= 1:
            dead_index = dead_index[0]
        if isinstance(dead_index, int):
            self.task_list_box.delete(dead_index)
            self.current_user.remove_task(\
                self.current_user.return_user_tasks()[dead_index].return_task_and_quantity())

    def _on_closing(self):
        self.current_user.write()
        self.root.destroy()

    def _update_list(self):
        """refreshes the shown tasks"""
        self.task_list_box.insert("end", \
                    self.current_user.return_user_tasks()[-1].return_task_and_quantity())

    def change_user(self, new_user):
        """changes the user"""
        self.current_user = new_user
        
        

class Task:
    def __init__(self, task):
        try:
            self.task, self.quantity = task.split(",")
        except ValueError:
            raise Exception("Task is formatted incorrectly!")
    def __str__(self):
        return(f"Task: {self.task}: {self.quantity}.")
    def return_task_and_quantity(self):
        return self.task +": " + self.quantity
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
        return(f"Tasks: {self.tasks}")
    
    def __len__(self):
        return(len(self.tasks))
    
    def __getitem__(self, index):
        return self.tasks[index]
    
    def __add__(self, new_task):
        if new_task in self.raw_tasks:
            return self
        if isinstance(new_task, list):
            for i in range(len(new_task)):
                # raw
                self.raw_tasks.append(new_task[i])
                # obj
                self.tasks.append(Task(new_task[i]))
                
        else:
            # raw
            self.raw_tasks.append(new_task)
            # obj
            self.tasks.append(Task(new_task))
            
        return self
    
    def __sub__(self, target_task):
        i = 0
        while i != len(self.tasks):
            if self.tasks[i].return_task_and_quantity() == target_task:
                self.raw_tasks.remove(target_task)
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
                    f.write(f"{tasks[i].return_task()}, {tasks[i].return_quantity()}\n")
                    print(f"Writing {tasks[i]}")
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
    
    def new_task(self, task):
        """makes a new task"""
        self.tasks += task
    
    def remove_task(self, task):
        """removes a task"""
        self.tasks -= task


def main():
    """The main project loop"""
    kid1 = User('kid1')
    gui = GUI(kid1)
    kid1.read()
    task = 'go, 3'
    while not task.lower() in ['quit','q']:
        task = input('whats ur task: ')
        if not task.lower() in ['quit', 'q']:
            kid1.new_task(task)
    kid1.write()
    task = input('What task do you want to remove? ')
    kid1.remove_task(task)
    kid1.write()
    gui.start()

main()
