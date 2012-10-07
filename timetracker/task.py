from .timeinterval import TimeInterval
import datetime

class Task:
    """A task object keeps track of when you have been working on it."""
    def __init__(self, thename):
        self._name = thename
        self.intervals = []
        self.ended = False

    def start(self):
        """You have started working on the task.
        If you have already ended the task, a ValueError is raised.
        You must unend() the task first."""
        if self.ended:
            raise ValueError("Cannot restart a task that is ended.  You must unend it first.")
        # if the most recent time interval is still in progress, do nothing
        if not self.isstarted() or self.intervals[-1].isended():
            self.intervals.append(TimeInterval())

    def pause(self):
        """You are not working the task, but you are not done yet."""
        if self.intervals: #if empty, then task hasn't started
            self.intervals[-1].end()

    def end(self):
        """You are done with the task."""
        self.pause()
        self.ended = True
        pass

    def unend(self):
        """Reopens the task for calling start() - but the task is still paused."""
        self.ended = False
        pass

# I have chosen to comment out add and subtract for now because they make the
# program structure a lot more complicated.
# I think it's better to force users to make manual corrections if they forget.
#
# need to add in self.manuals = [] to __init__() if re-enabling
#
#    def subtract(self, days=0, hours=0, minutes=0):
#        """If you forgot to pause the task - subtract some time.
#        
#        The subtraction is stored as a separate entity --
#        the sequence of start and pause commands is left undisturbed.
#        """
#        delta = datetime.timedelta(days=days, hours=hours, minutes=minutes)
#        if delta < datetime.timedelta():
#            raise ValueError("You cannot subtract a negative amount of time.")
#        
#        total = self.length()
#        if delta > total:
#            raise ValueError("You cannot subtract more time than you have spent so far on the task.")
#        
#        negversion = datetime.timedelta(days=-days, hours=-hours, minutes=-minutes)    
#        self.manual.append(negversion)
#    
#    def add(self, days=0, hours=0, minutes=0):
#        """If you worked on the task but forgot to start it - add some time.
#        
#        The addition is stored as a separate entity --
#        the sequence of start and pause commands is left undisturbed.
#        """
#        delta = datetime.timedelta(days=days, hours=hours, minutes=minutes)
#        if delta < datetime.timedelta():
#            raise ValueError("You cannot add a negative amount of time.")
#        
#        self.manual.append(delta)
        
    def isstarted(self):
        """Evaluates to True if the task has ever been started,
        even if it is currently paused."""
        return self.intervals
    
    def ispaused(self):
        """Evaluates to True if the task is currently paused,
        or has never been started.
        """
        if self.intervals:
            return self.intervals[-1].isended()
        else:
            return True
    
    def isended(self):
        """Evaluates to True if the task is ended."""
        return self.ended

    def name(self):
        """The task's name, as set by the constructor or rename() method."""
        return self._name

    def rename(self, thename):
        """Change the task's name."""
        self._name = thename
    
    def length(self):
        """Returns a datetime.timedelta object containing
        the total amount of time you have spent on the task so far."""
        lengths = [i.length() for i in self.intervals]
        total = sum(lengths, datetime.timedelta(0))
        return total

    def length_today(self):
        """Returns a datetime.timedelta object containing
        the amount of time spent on the task since Midnight of today.
        
        This will not be very useful for people who work through Midnight.
        """
        lengths = [i.length_today() for i in self.intervals]
        total = sum(lengths, datetime.timedelta(0))
        return total
    
    def starttime(self):
        """Returns a datetime.datetime object containing
        the time when the task was first started.
        
        Raises a ValueError if the task has not yet started."""
        if not self.isstarted():
            raise ValueError("Task has not started yet.")
        else:
            return self.intervals[0].began
    
    def lastworked(self):
        """Returns a datetime.datetime object containing 
        the time the task was most recently paused.
        If the task is currently active, returns the present time."""
        if not self.isstarted():
            raise ValueError("Task has not started yet.")
        else:
            last = self.intervals[-1]
            if last.isended():
                return last.ended
            else:
                return datetime.datetime.now()

    def prettyprint(self):
        """Print information about a task to the console."""

        # helper method to print a useful representation of duration
        def length_format(delta):
            SECS_PER_HOUR = 60 * 60
            SECS_PER_MINUTE = 60
            hours, remainder = divmod(delta.seconds, SECS_PER_HOUR)
            minutes, seconds = divmod(remainder, SECS_PER_MINUTE)
            
            fmt = "{0}:{1:02d}:{2:02d}s".format(hours, minutes, seconds)
            if delta.days > 0:
                fmt = str(delta.days) + " days " + fmt

            return fmt

        # helper method - print appropriate info depending on whether task
        # is active, paused, or ended
        def end_string():
            if self.isended():
                return "Ended " + str(self.lastworked().date())
            elif self.ispaused():
                return "Paused " + self.lastworked().strftime("%m-%d %H:%M")
            else:
                return "Currently working"

        def start_and_end():
            if self.isstarted():
                return "Started {0}, {1}, Duration {2}".format(
                    self.starttime().strftime("%Y-%m-%d %H:%M"),
                    end_string(),
                    length_format(self.length()))
            else:
                return "Not started yet" 

        return "{0}: {1}".format(self.name(), start_and_end())
