# -*- coding: utf-8 -*-

#  running_on.py master in smart plug for now  2019 12 17

"""

---- template header example -----
What:   introspection type stuff
Status: draft, ok draft but possibly useful
Refs:

Code introspection in Python - GeeksforGeeks
    *>url  https://www.geeksforgeeks.org/code-introspection-in-python/

home-assistant/home-assistant: Open source home automation that puts local control and privacy first
    *>url  https://github.com/home-assistant/home-assistant


view.View Python Example
    *>url  https://www.programcreek.com/python/example/15897/view.View

What are Python dictionary view objects?
    *>url  https://www.tutorialspoint.com/What-are-Python-dictionary-view-objects

python - What are dictionary view objects? - Stack Overflow
    *>url  https://stackoverflow.com/questions/8957750/what-are-dictionary-view-objects

Python reflection: how to list modules and inspect functions - Federico Tomassetti - Software Architect
    *>url  https://tomassetti.me/python-reflection-how-to-list-modules-and-inspect-functions/


Notes:



    ** memory
    ** disassemble
    types              ex_type.py
    is instance
    issubclass()	Checks if a specific class is a derived class of another class.
    isinstance()	Checks if an objects is an instance of a specific class.


    ** help()	It is used it to find what other functions do
    hasattr()	Checks if an object has an attribute
    getattr()	Returns the contents of an attribute if there are some.
    repr()	Return string representation of object
    callable()	Checks if an object is a callable object (a function)or not.

    sys()	Give access to system specific variables and functions
    __doc__	Return some documentation about an object
    __name__	Return the name of the object.
    ** which version of python
    ** which version of os

    inspect — Inspect live objects — Python 3.8.0 documentation
    *>url  https://docs.python.org/3/library/inspect.html

    platform — Access to underlying platform’s identifying data — Python 3.8.0 documentation
    https://docs.python.org/3.8/library/platform.html

"""


import sys
import os
import psutil
import platform
import socket;
from   platform import python_version


# --------------------------------------
class RunningOn( object ):
    """
    Provides information on the system..... we are running on
    now including some directory stuff
    i decided to make all available as class variables
    """

    def __init__(self,   ):
        """
        this is meant to be a singleton use class level only do not instantiated
        throw a exception if instantiated 1/0
        """
        y = 1/0

    # ----------------------------------------------
    @classmethod
    def gather_data( cls,  ):
        """
        what it says
        add flag for how much ??

        """
        our_os           = sys.platform       #testing if our_os == "linux" or our_os == "linux2"  "darwin"  "win32"
        cls.our_os       = our_os
        if our_os == "win32":
            os_win = True     # the OS is windows any version
        else:
            os_win = False    # the OS is not windows
        cls.os_win         = os_win

        if  os_win:
            cls.computername       = os.getenv( "COMPUTERNAME" ).lower() # at least in windows the lower case name of your computer.  what in linux?
        else:
            cls.computername       = ""

        process               = psutil.Process(os.getpid())
        cls.memory_mega       = process.memory_info().rss / 1e6   # mega bytes seem better

        cls.platform_system   = platform.system()
        cls.sys_version       = sys.version
        cls.sys_version_info  = sys.version_info
        cls.python_version    = python_version()

        # --- environment does not seem too useful but make sure defined
        cls.environments       = {"what": "not collected"}
#        cls.environments        = os.environ     # not sure of type, dict like

        host_name              = socket.gethostname()
        cls.host_name          = host_name
        cls.host_tcpip         = socket.gethostbyname( host_name )

        # try to make computer id, and host_tcpid the best indicators of our box
        if cls.computername == "":
            cls.computer_id    = cls.host_name.lower()
        else:
            cls.computer_id    = cls.computername

        cls.platform_machine   = platform.machine()

        cls.opening_dir        = os.getcwd()    # name of the directory that the application is started in. Probably "....../smart_plug

        cls.program_py_fn      = sys.argv[ 0 ]
        cls.py_path            = os.path.dirname(  cls.program_py_fn  )

        # os.chdir( desired_path )
        # logger.log( fll,  "current directory now " +  os.getcwd() )

#       ...... as needed

    # ----------------------------------------------
    @classmethod
    def linux_distribution( cls ):
        """
        may use later
        """
        try:
            return platform.linux_distribution()
        except:
            return "N/A"

    # ----------------------------------------------
    @classmethod
    def log_msg(cls, msg, logger, logger_level = 10, print_flag = False  ):
        """
        for debugging

        """
        if logger is None:
            pass
        else:
            logger.log( logger_level, msg )
        if print_flag:
            print( msg )

    # ----------------------------------------------
    @classmethod
    def log_me(cls, logger, logger_level, print_flag  ):
        """
        for debugging
        log and/or print info
        add log level, and default
        """
        cls.log_msg( f">>>>>>>>>>> running_on() log_me() <<<<<<<<<<<<<",     logger, logger_level, print_flag )
        cls.log_msg( f"platform_system    >{cls.platform_system}<",     logger, logger_level, print_flag )
        cls.log_msg( f"sys_version        >{cls.sys_version}<",         logger, logger_level, print_flag )
        cls.log_msg( f"sys_version_info   >{cls.sys_version_info}<",    logger, logger_level, print_flag )
        cls.log_msg( f"memory_mega        >{cls.memory_mega}<",         logger, logger_level, print_flag )
        cls.log_msg( f"python_version     >{cls.python_version}<",      logger, logger_level, print_flag )

        cls.log_msg( f"environments       >{cls.environments}<",        logger, logger_level, print_flag )

        cls.log_msg( f"host_name          >{cls.host_name}<",           logger, logger_level, print_flag )
        cls.log_msg( f"host_tcpip         >{cls.host_tcpip}<",          logger, logger_level, print_flag )
        cls.log_msg( f"computername       >{cls.computername}<",        logger, logger_level, print_flag )
        cls.log_msg( f"computer_id        >{cls.computer_id}<",         logger, logger_level, print_flag )
        cls.log_msg( f"platform_machine   >{cls.platform_machine}<",    logger, logger_level, print_flag )
        cls.log_msg( f"os_win             >{cls.os_win}<",              logger, logger_level, print_flag )
        cls.log_msg( f"program_py_fn      >{cls.program_py_fn}<",       logger, logger_level, print_flag )

        cls.log_msg( f"cls.py_path        >{cls.py_path }<",             logger, logger_level, print_flag )

        cls.log_msg( f"---------------- end running on --------------",          logger, print_flag )


# ==============================================
if __name__ == '__main__':
    """
    do not run the app here for convenience of launching
    """

#    print("")
#    print("================= do not run me ( app_global.py ) please, I have nothing to say  ===================")


    the_class   =  RunningOn
    the_class.gather_data()
    the_class.log_me( logger = None, logger_level = 20, print_flag = True )

