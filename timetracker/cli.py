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
        add_parser = subparsers.add_parser('add', help='Add task')
        add_parser.add_argument('name', help='Task name')
        add_parser.set_defaults(func = lambda args: self.tasklist.add(args.name))
        
        #start
        start_parser = subparsers.add_parser('start', help='Start task')
        start_parser.add_argument('name', help='Task name')
        start_parser.set_defaults(func = lambda args: self.tasklist.start(args.name))
        
        #pause
        pause_parser = subparsers.add_parser('pause', help='Pause task')
        pause_parser.add_argument('name', help='Task name')
        pause_parser.set_defaults(func = lambda args: self.tasklist.pause(args.name))
        
        #pause all
        pauseall_parser = subparsers.add_parser('pauseall', help='Pause all tasks')
        pauseall_parser.set_defaults(func = lambda args: self.tasklist.pause_all())
        
        #end
        end_parser = subparsers.add_parser('end', help='End task')
        end_parser.add_argument('name', help='Task name')
        end_parser.set_defaults(func = lambda args: self.tasklist.end(args.name))
        
        #unend
        unend_parser = subparsers.add_parser('unend', help='Unend task')
        unend_parser.add_argument('name', help='Task name')
        unend_parser.set_defaults(func = lambda args: self.tasklist.unend(args.name))

        #reset
        reset_parser = subparsers.add_parser('reset', help='Reset task')
        reset_parser.add_argument('name', help='Task name')
        reset_parser.set_defaults(func = lambda args: self.tasklist.reset(args.name))

        #reset all
        resetall_parser = subparsers.add_parser('resetall', help='Reset all tasks')
        resetall_parser.set_defaults(func = lambda args: self.tasklist.reset_all())

        #delete
        delete_parser = subparsers.add_parser('delete', help='Delete task')
        delete_parser.add_argument('name', help='Task name')
        delete_parser.set_defaults(func = lambda args: self.tasklist.delete(args.name))
        
        #rename
        rename_parser = subparsers.add_parser('rename', help='Rename task')
        rename_parser.add_argument('name', help='Task name')
        rename_parser.add_argument('newname', help='New name')
        rename_parser.set_defaults(func = lambda args: self.tasklist.rename(args.name, args.newname))
        
        #query
        query_parser = subparsers.add_parser('query', help='Query task')
        query_parser.add_argument('name', help='Task name')
        query_parser.set_defaults(func = lambda args: self.tasklist.query(args.name))
        
        #list
        list_parser = subparsers.add_parser('list', help='List tasks')
        list_parser.set_defaults(func = lambda args: self.tasklist.print_all())
        
        #list active
        listactive_parser = subparsers.add_parser('listactive', help='List active tasks')
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
