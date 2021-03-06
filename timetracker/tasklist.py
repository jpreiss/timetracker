from .task import Task
import pickle

class TaskList:
    """Wraps a Dictionary of tasks and provides a few extra behaviors"""
    
    def __init__(self, tasks):
        """tasks: a dictionary of Task objects"""
        self.tasks = tasks
        pass
    
    def add(self, name):
        """Create a new task in the paused state.
        If a task with this name already exists, does nothing."""
        if name not in self.tasks:
            self.tasks[name] = Task(name)
    
    def start(self, name):
        """Start or unpause a task, while pausing all other tasks.
        If task is not found, creates it.
        """
        if not name in self.tasks:
            self.add(name)

        for taskname, task in self.tasks.items():
            if taskname != name:
                task.pause()

        self.tasks[name].start()
        
    
    def pause(self, name):
        """Pause a task.  Raises a KeyError if the task name is not found."""
        self.tasks[name].pause()
    
    def pause_all(self):
        """Pauses every task in the list."""
        for task in self.tasks.values():
            task.pause()
    
    def end(self, name):
        """End a task. Raises a KeyError if the task name is not found."""
        self.tasks[name].end()
    
    def unend(self, name):
        """Unend a task. Raises a KeyError if the task name is not found."""
        self.tasks[name].unend()

    def delete(self, name):
        """Removes task completely. Does nothing if the task name is not found."""
        if name in self.tasks:
            del self.tasks[name]

# Currently disabled - see task.py for comments
#      
#   def addtime(self, name, days=0, hours=0, minutes=0):
#       """Add time to a task if you forgot to start it."""
#       self.tasks[name].add(days=days, hours=hours, minutes=minutes)
#       
#   def subtracttime(self, name, days=0, hours=0, minutes=0):
#       """Remove time from a task if you forgot to pause it."""
#       self.tasks[name].subtract
    
    def rename(self, name, newname):
        """Rename a task. Raises a KeyError if the task name is not found."""
        before = self.tasks[name]
        before.rename(newname)
        del self.tasks[name]
        self.tasks[newname] = before
    
    def print_all(self):
        """Print information about all tasks to the console."""
        #TODO: columnize
        for name, task in sorted(self.tasks.items()):
            print(task.prettyprint())
        print #blank line
    
    def print_active(self):
        """Print information about tasks which are not ended."""
        for task in self.tasks.values():
            if not task.isended():
                print(task.prettyprint())
        print #blank line
    
    def query(self, name):
        """Print information about a single task to the console.
        Raises a KeyError if the task name is not found.
        """
        print(self.tasks[taskname].prettyprint())

    def reset(self, name):
        """Reset a task to unstarted with 0 time logged."""
        if name in self.tasks:
            self.delete(name)
            self.add(name)

    def reset_all(self):
        """Resets all tasks to unstarted with 0 time logged."""
        for name in self.tasks.keys():
            self.reset(name)
