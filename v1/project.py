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

class Tasks:
    def __init__(self, tasks):
        self.tasks = tasks
    def __str__(self):
        return(f"Tasks: {self.tasks}")

class File:
    def __init__(self):
        pass
    def write(self, tasks, user):
        """writes tasks to the to-do list"""

class User:
    def __init__(self, username):
        self.user_name = username
        try:
            with open(self.user_name +".txt") as f:
                

def main():
    """The main project loop"""
    