import argparse
from .tasklist import TaskList
import os
import pickle

class CLI:
    def __init__(self, location):
        
        self.location = location
        try:
            task_dict = pickle.load(open(location, 'rb'))
        except:
            # if fails, assume there's no data stored and start fresh
            print("Creating a new task file.")
            task_dict = {}
        
        self.tasklist = TaskList(task_dict)
        
        self.parser = argparse.ArgumentParser(description='Tracks time spent on different tasks.')
    
        subparsers = self.parser.add_subparsers(title='commands')
        
        #add task
        add_parser = subparsers.add_parser('a', help='Add task')
        add_parser.add_argument('name', help='Task name')
        add_parser.set_defaults(func = lambda args: self.tasklist.add(args.name))
        
        #start
        start_parser = subparsers.add_parser('s', help='Start task')
        start_parser.add_argument('name', help='Task name')
        start_parser.set_defaults(func = lambda args: self.tasklist.start(args.name))
        
        #pause
        pause_parser = subparsers.add_parser('p', help='Pause task')
        pause_parser.add_argument('name', help='Task name')
        pause_parser.set_defaults(func = lambda args: self.tasklist.pause(args.name))
        
        #pause all
        pauseall_parser = subparsers.add_parser('pa', help='Pause all tasks')
        pauseall_parser.set_defaults(func = lambda args: self.tasklist.pause_all())
        
        #end
        end_parser = subparsers.add_parser('e', help='End task')
        end_parser.add_argument('name', help='Task name')
        end_parser.set_defaults(func = lambda args: self.tasklist.end(args.name))
        
        #unend
        unend_parser = subparsers.add_parser('u', help='Unend task')
        unend_parser.add_argument('name', help='Task name')
        unend_parser.set_defaults(func = lambda args: self.tasklist.unend(args.name))

        #delete
        delete_parser = subparsers.add_parser('d', help='Delete task')
        delete_parser.add_argument('name', help='Task name')
        delete_parser.set_defaults(func = lambda args: self.tasklist.delete(args.name))
        
        #rename
        rename_parser = subparsers.add_parser('r', help='Rename task')
        rename_parser.add_argument('name', help='Task name')
        rename_parser.add_argument('newname', help='New name')
        rename_parser.set_defaults(func = lambda args: self.tasklist.rename(args.name, args.newname))
        
        #query
        query_parser = subparsers.add_parser('q', help='Query task')
        query_parser.add_argument('name', help='Task name')
        query_parser.set_defaults(func = lambda args: self.tasklist.query(args.name))
        
        #list
        list_parser = subparsers.add_parser('l', help='List tasks')
        list_parser.set_defaults(func = lambda args: self.tasklist.print_all())
        
        #list active
        listactive_parser = subparsers.add_parser('la', help='List active tasks')
        listactive_parser.set_defaults(func = lambda args: self.tasklist.print_active())
        
        #erase file
        erase_parser = subparsers.add_parser('erase', help='Erase task file')
        erase_parser.set_defaults(func = lambda args: self.erase_taskfile())

    def store(self):
        pickle.dump(self.tasklist.tasks, open(self.location, 'wb'))

    def parse_command(self, args):
        args = self.parser.parse_args(args)
        args.func(args)
    
    def erase_taskfile(self):
        intext = input("Deleting ALL tasks. Are you sure? y/n")
        if intext.downcase().startswith('y'):
            os.remove(self.location)
