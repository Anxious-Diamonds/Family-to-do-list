"""A family to-do list"""
import tkinter
import os

class GUI:
    def __init__(self):
        pass

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
            self.tasks = []
            for i in range(len(tasks)):
                self.tasks.append(Task(tasks[i]))
        else:
            if len(tasks) > 0:
                self.tasks = [Task('No tasks found')]
            else:
                self.tasks = [Task(tasks)]

    def __str__(self):
        return(f"Tasks: {self.tasks}")
    
    def __len__(self):
        return(len(self.tasks))
    
    def __add__(self, new_task):
        if isinstance(new_task, list):
            for i in range(len(new_task)):
                self.tasks.append(Task(new_task[i]))
        else:
            self.tasks.append(Tasks(new_task))
        return self.tasks
    
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

    def write(self, tasks):
        """writes tasks to the to-do list"""
        with open(self.file_name, 'w') as f:
            f.write('')

        with open(self.file_name, 'a') as f:
            for i in range(len(tasks)):
                f.write(f"{tasks[i].return_task()}\n")
                print(f"Writing {tasks[i]}")
class User:
    def __init__(self, username):
        self.user_file = File(f"{username}.txt")
        self.tasks = []
        
    def read(self):
        self.tasks = self.user_file.read()
    
    def write(self):
        if len(self.tasks) > 0:
            self.user_file.write(self.tasks.return_tasks())
        else:
            print('User has no tasks to write!')
    
    def new_task(self, task):
        """makes a new task"""
        self.tasks += task
  

def main():
    """The main project loop"""
    kid1 = User('kid1')
    kid1.read()
    task = input('whats ur task: ')
    kid1.new_task(task)
    kid1.write()

main()