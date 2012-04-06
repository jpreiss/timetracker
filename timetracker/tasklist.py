import task
import pickle

class TaskList:
    """Stores a set of tasks, accessible by name, and allows basic operations."""
    
    def __init__(self):
        """Create an empty list of tasks."""
        self.tasks = {}
        pass
    
    def add(self, name):
        """Create a new task in the paused state.
        If a task with this name already exists, does nothing."""
        if name not in self.tasks:
            self.tasks[name] = task.Task(name)
    
    def start(self, name):
        """Start or unpause a task, while pausing all other tasks.
        Raises a KeyError if the task name is not found.
        """
        self.tasks[name].start()
        
        for taskname, task in self.tasks.iteritems():
            if taskname != name:
                task.pause()
        
    
    def pause(self, name):
        """Pause a task.  Raises a KeyError if the task name is not found."""
        self.tasks[name].pause()
    
    def pause_all(self):
        """Pauses every task in the list."""
        for task in self.tasks.itervalues():
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
#    def addtime(self, name, days=0, hours=0, minutes=0):
#        """Add time to a task if you forgot to start it."""
#        self.tasks[name].add(days=days, hours=hours, minutes=minutes)
#        
#    def subtracttime(self, name, days=0, hours=0, minutes=0):
#        """Remove time from a task if you forgot to pause it."""
#        self.tasks[name].subtract
    
    def rename(self, name, newname):
        """Rename a task. Raises a KeyError if the task name is not found."""
        before = self.tasks[name]
        before.rename(newname)
        del self.tasks[name]
        self.tasks[newname] = before
    
    def print_all(self):
        """Print information about all tasks to the console."""
        for taskname in self.tasks.iterkeys():
            self.prettyprint(taskname)
        print #blank line
    
    def print_active(self):
        """Print information about tasks which are not ended."""
        for name, task in self.tasks.iteritems():
            if not task.isended():
                self.prettyprint(name)
        print #blank line
    
    def query(self, name):
        """Print information about a single task to the console.
        Raises a KeyError if the task name is not found.
        """
        self.prettyprint(name)
    
    def store(self, path):
        """Store the TaskList to a file.
        Currently uses Pickle, but I'd like to use a human-readable format in the future.
        """
        pickle.dump(self.tasks, open(path, 'w'))
    
    def load(self, path):
        """Load the TaskList from a file.
        Currently uses Pickle, but I'd like to use a human-readable format in the future.
        """
        self.tasks = pickle.load(open(path, 'r'))
        
    def prettyprint(self, taskname):
        """Print information about a task to the console."""

        task = self.tasks[taskname]
        
        # helper method - print appropriate info depending on whether task
        # is active, paused, or ended
        def task_end_string(task):
            if task.isended():
                return "Ended " + str(task.lastworked().date())
            elif task.ispaused():
                return "Paused " + str(task.lastworked().date())
            else:
                return "Currently working"

        def length_format(delta):
            SECS_PER_HOUR = 60 * 60
            SECS_PER_MINUTE = 60
            hours, remainder = divmod(delta.seconds, SECS_PER_HOUR)
            minutes, seconds = divmod(remainder, SECS_PER_MINUTE)
            
            fmt = ""
            if delta.days > 0:
                fmt += str(delta.days) + " days "
            fmt += str(hours) + ':' + str(minutes)

            return fmt

        #TODO: return a string instead of printing directly 
        print task.name() + ':',
        if task.isstarted():
            print "Started", str(task.starttime().date()) + ",",
            print task_end_string(task) + ",",
            print "Duration", length_format(task.length()),
        else:
            print "Not started yet" 
