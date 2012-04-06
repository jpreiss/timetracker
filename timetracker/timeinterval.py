import datetime

class TimeInterval:
    """Represents an interval of time with a beginning and end."""
    
    def __init__(self):
        """Create a new time interval. Time intervals begin when they are created."""
        self.began = datetime.datetime.now()
        self.ended = None
    
    def end(self):
        """End the time interval. If it is already ended, nothing happens."""
        if not self.ended:
            self.ended = datetime.datetime.now()

    def isended(self):
        """Query if the interval has ended yet."""
        return self.ended
    
    def length(self):
        """Returns a datetime.timedelta object containing
        the elapsed time between the interval's beginning and end.
        
        If the interval that has not yet ended,
        The length is the time since the interval was created.
        """
        if self.ended:
            return self.ended - self.began
        else:
            return datetime.datetime.now() - self.began
    
    def length_today(self):
        """Returns a datetime.timedelta object containing
        the elapsed time spent working on the task today.
        
        If the interval was started yesterday and ran overnight,
        only the portion since midnight will be included.
        """
        
        # helper method...
        def midnight():
            now = datetime.datetime.now()
            return now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # negative timedelta means that we began before midnight of today
        if self.began - midnight() < datetime.timedelta():
            begantime = midnight()
        else:
            begantime = self.began
        
        if self.ended:
            return self.ended - begantime
        else:
            return datetime.datetime.now() - begantime
            
        
    def empty():
        """Class method to create a TimeInterval of zero length."""
        notime = TimeInterval()
        notime.ended = notime.began
        return notime