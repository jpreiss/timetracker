import sys
import os
import timetracker

# Utility function, cross platform - from Douglas Mayle
def app_folder():
    APPNAME = "TimeTracker1.0"
    if sys.platform == 'darwin':
        from AppKit import NSSearchPathForDirectoriesInDomains
        return os.path.join(NSSearchPathForDirectoriesInDomains(14, 1, True)[0], APPNAME)
    elif sys.platform == 'win32':
        return os.path.join(os.environ['APPDATA'], APPNAME)
    else:
        return os.path.expanduser(path.join("~", "." + APPNAME))


# main

print #blank line
cli = timetracker.CLI(app_folder())
cli.parse_command(sys.argv[1:])
cli.store()
