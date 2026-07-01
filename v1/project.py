"""A family to-do list"""
import tkinter as tk
import tkinter.font as tkFont
import os

class GUI:
    def __init__(self, current_user):
        self.current_user = current_user
        
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
        self.task_text = tk.IntVar()
        self.task_text.set("Write your task here")

        # sets up inputs
        self.task_input = tk.Entry(self.frame, textvariable = self.task_text, \
                                   font=std_font)
        self.task_input.pack()

        # sets up buttons
        self.attained = tk.Button(self.frame, text = "✓", font=std_font, \
                                  command = self._attainment)
        self.attained.pack()
        
    
    def start(self):
        self.root.mainloop()
    
    def _attainment(self):
        """make the task"""
        tast_text_str = self.task_text.get()
        self.current_user.new_task(tast_text_str)
        self.task_text.set("Write your task here")
        self._update_list()

    def _on_closing(self):
        self.current_user.write()
        self.root.destroy()

    def _update_list(self):
        """refreshes the shown tasks"""
        pass

    def change_user(self, new_user):
        """changes the user"""
        self.current_user = new_user
        
        

class Task:
    def __init__(self, task):
        self.task = task
    def __str__(self):
        return(f"Task: {self.task}.")
    def return_task(self):
        return self.task

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
                self.tasks = [Task('No tasks found')]
            else:
                self.tasks = [Task(tasks)]

    def __str__(self):
        return(f"Tasks: {self.tasks}")
    
    def __len__(self):
        return(len(self.tasks))
    
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
            if self.tasks[i].return_task() == target_task:
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
        tasks = tasks_obj.return_tasks()
        with open(self.file_name, 'w') as f:
            f.write('')

        with open(self.file_name, 'a') as f:
            for i in range(len(tasks)):
                f.write(f"{tasks[i]}\n")
                print(f"Writing {tasks[i]}")
class User:
    def __init__(self, username):
        self.user_file = File(f"{username}.txt")
        self.tasks = Tasks([])
        
    def read(self):
        self.tasks = self.user_file.read()
    
    def write(self):
        if len(self.tasks) > 0:
            self.user_file.write(self.tasks)
        else:
            print('User has no tasks to write!')
    
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
    task = 'go'
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
