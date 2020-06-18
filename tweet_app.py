# -*- coding: utf-8 -*-
#!/usr/bin/env python3

"""
Purpose:
    now the tweet app code modified from
    smart_plug.py  ( tp link ) app with a gui
    this is the main program, start it
    see readme_rsh.txt

Environment:
        Spyder 3.3.6
        Python 3.6
        Tkinker
        .....
        tested in Win 10 should work in all os's

See Also:
        smart_plug_help.txt
        readme.txt
        readme_rsh.txt
#!python3


=========================
"""

import logging
import sys
import os
import time
import datetime
#import traceback
import psutil
#import queue
import threading
import importlib
from   tkinter import messagebox

#----------- local imports --------------------------
import parameters
import gui
from   app_global import AppGlobal
import app_global
import sql_builder
import load_tweet_data
import load_word_data
import select_manager


# ----- ========================== Begin Application Class ================================
class TweetApp( object ):
    """
    main and controller class for the application
    """
    def __init__(self ):
        """
        mostly instance variables are declared here or in restart
        """
        # ------------------- basic setup --------------------------------
        print( "" )
        print( "=============== starting TweetApp ========================= " )
        print( "" )
        print( "     -----> prints may be sent to log file !" )
        print( "" )

        AppGlobal.controller        = self
        AppGlobal.main_thread_id    = threading.get_ident()
        self.app_name               = "TweetApp"
        self.version                = "Ver: Alpha 15 - 2020 06 17.1"   # most of structure for traditional
                                                                       # select in place, more cleanup
                                                                       # build multi year db, and perhaps for others

        self.gui                    =  None  # the gui created later
        self.no_restarts            =  -1    # counter for the number of times the application is restarted

        self.restart( )

    # --------------------------------------------------------
    def restart( self ):
        """
        use to restart the app without ending it - also extend init
        parameters will be reloaded and the gui rebuilt
        args: zip
        ret: zip ... all sided effects
        """
        #rint( "===================restart===========================" )
        self.no_restarts    += 1
        if self.gui is not None:

            self.logger.info( self.app_name + ": restart" )

            # self.post_to_queue( "stop", None  , (  ) ) # need to shut down other thread
            # self.helper_thread.join()

            self.gui.close()

            importlib.reload( parameters )    #
        self.polling_mode = "off"
        #self._polling_fail        = False   # flag set if _polling in gui thread fails

#        self.is_first_gui_loop    = True
        #self.ext_processing       = None    # built later from parameters if specified
        self.logger             = None    # set later none value protects against call against nothing

        # ----- parameters
        self.parmeters_x        = "none"        # name without .py for parameters
                                                #extension may ?? be replaced by command line args

        self.select_manager     = None          # populate in cb_change_select_type
        self.parameters         = parameters.Parameters( )
        self.starting_dir       = os.getcwd()

        self.logger_id          = self.parameters.logger_id       # std name
        self.logger             = self.config_logger()            # std name

        AppGlobal.logger        = self.logger
        AppGlobal.logger_id     = self.logger_id

        self.prog_info()

        self.gui                = gui.GUI(  )
        self.last_begin_dt,  self.last_end_dt  = self.gui.get_dt_begin_end() # after gui is built

        # now most of setup memory has been allocated -- may want to check in again later, save this value ??
        process      = psutil.Process(os.getpid())    #  import psutil
        mem          = process.memory_info().rss
        # convert to mega and format
        mem_mega     = mem/( 1e6 )
        msg          = f"process memory = {mem_mega:10,.2f} mega bytes "
        print( msg )
        # set up gui thread polling if delta > 0
        self.logger.log( AppGlobal.force_log_level, msg )
        self.polling_delta  = self.parameters.polling_delta
        if self.polling_delta > 0:
            self.gui.root.after( self.polling_delta, self.polling_0 )
        self.gui.run()

        self.logger.info( self.app_name + ": all done" )

    # --------------------------------------------------------
    def polling_0( self, ):
        """
        for first round(s) of polling, then use polling
        """
        self.polling_count   = 0

        self.gui.root.after( self.polling_delta, self.polling )  # reschedule event

    # --------------------------------------------------------
    def polling( self, ):
        """
        for usual rounds of polling, then use polling
        """
        self.polling_count   += 1
        pass
        if self.polling_count > 10:
            #print( "hi" )
            self.polling_count = 0

        if self.polling_mode == "on":
            #print( "checking date...")
            begin_dt,  end_dt  = self.gui.get_dt_begin_end() # after gui is built
            if ( begin_dt != self.last_begin_dt ) or ( end_dt != self.last_end_dt ):
                self.last_begin_dt   = begin_dt
                self.last_end_dt     = end_dt
                print( "dt change in polling"   )
                self.slider_select_1("slider_select", help_mode = False )

        self.gui.root.after( self.polling_delta, self.polling )  # reschedule event

    # --------------------------------------------------------
    def config_logger( self, ):
        """
        configure the logger in usual way using the current parameters
        ?? move to app global or in that direction
        args: zip
        ret:  the logger and side effects
              including adding logger to AppGlobal
        """
        logger = logging.getLogger( self.logger_id  )

        logger.handlers = []
        logger.setLevel( self.parameters.logging_level )     # DEBUG , INFO    WARNING    ERROR    CRITICAL

        # create the logging file handler.....
        fh = logging.FileHandler(   self.parameters.pylogging_fn )
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter( formatter )
        logger.addHandler( fh )

        msg   = "Done config_logger"
        #rint( msg )
        logger.debug( msg ) #  .debug   .info    .warn    .error
        AppGlobal.set_logger( logger )

        return logger

   # -------------------------------------------------------
    def prog_info( self ):
        """
        log info about program and its argument/environment to the logger
        of course wait until after logger is set up -- now can use pre logger
        args: zip
        ret:  zip
        """
        fll         = AppGlobal.force_log_level
        logger      = self.logger

        a_str = ""
        if ( self.no_restarts == 0 ) :
            a_str = f"{a_str}\n"
            a_str = f"{a_str}\n"
            a_str = f"{a_str}\n============================"
            a_str = f"{a_str}\n"

            a_str = f"{a_str}\nRunning {self.app_name} version = {self.version} mode = {self.parameters.mode}"
            a_str = f"{a_str}\n"
            logger.log( fll,  a_str )

        else:
            #a_str = ""
            a_str = f"{a_str}\n======"
            a_str = f"{a_str}\nRestarting {self.app_name} version = {self.version} mode = {self.parameters.mode}"
            a_str = f"{a_str}\n======"

        if len( sys.argv ) == 0:
            a_str = f"{a_str}\nno command line arg "
        else:
            for ix_arg, i_arg in enumerate( sys.argv ):
                a_str = f"{a_str}\ncommand line arg { ix_arg } =  {sys.argv[ix_arg]}"

        a_str = f"{a_str}\ncurrent directory {os.getcwd()}"
        # a_str = f"{a_str}\nCOMPUTERNAME {os.getenv( 'COMPUTERNAME' )}"   # may not exist in now in running on
        logger.log( fll,  a_str )

        logger.log( fll, f"{self.parameters}" )

        # a_str    = self.parameters.running_on.get_str()
        # logger.log( fll, a_str )
        # next may not be best way or place
        # self.parameters.running_on.log_me( logger, logger_level = AppGlobal.force_log_level,  print_flag = True )

        start_ts     = time.time()
        dt_obj       = datetime.datetime.utcfromtimestamp( start_ts )
        string_rep   = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
        logger.log( fll, f"Time now: {string_rep}" )  # but logging includes this in some format

    # ----------------------------------------------
    def os_open_parmfile( self,  ):
        """
        parameter file is opened in the configured system editor for the user to view and edit
        may be used as callback from gui button
        path addition here because parameters.py is not itself a parameter
        """
        a_filename = self.parameters.py_path + os.path.sep + "parameters.py"
        AppGlobal.os_open_txt_file( a_filename )

    # ----------------------------------------------
    def os_open_logfile( self,  ):
        """
        py_log file is opened in the configured system editor for the user to view and edit
        may be used as/by callback from gui button.  Can be called form gt
        """
        # a_filename = self.parameters.py_path + os.path.sep + self.parameters.pylogging_fn
        AppGlobal.os_open_txt_file( self.parameters.pylogging_fn )

    # ----------------------------------------------
    def os_open_helpfile( self,  ):
        """
        help "file" is opened in the os configured application for the file type:
        file set in parameters may be txt, pdf, or a url
        method may be used as callback from gui button
        """
        help_file            = self.parameters.help_file
        AppGlobal.os_open_help_file( help_file )

    # ----------------------------------------------
    def print_info_string_now( self, msg ):
        """
        object to pass in cb_probe
        """
        print( f"print_info_string_now {msg}" )
        self.gui.display_string( msg, update_now = True )

   # ----------------------------------------------
    def cb_rb_select( self,  ):
        """
        call back for gui button
        """
        pass

       # ----------------------------------------------
    def toggle_ds_mode ( self,  ):
        """
        call back for gui button

        """
        print( f"polling_mode {self.polling_mode}" )
        if self.polling_mode == "on":
            self.polling_mode = "off"
            self.gui.widget_slider.config( text  = "Turn Date\nSlider Mode\nOn"  )
        else:
            self.polling_mode = "on"
            self.gui.widget_slider.config( text  = "Turn Date\nSlider Mode\nOff" )

   # ----------------------------------------------
    def cb_show_load_parms ( self,  ):
        """
        call back for gui button

        """
        msg     = (   f"Load parameters ..... "
                    + f"\nDatabase Name:  {self.parameters.database_name}"
                    + f"\nTweet Input:    {self.parameters.tweet_input_file_name}"
                    + f"\nTweet For:      {self.parameters.who_tweets}"
                    + f"\nWord Input:     {self.parameters.word_input_file_name}"
                   )

        self.print_info_string_now( msg )
        AppGlobal.logger.debug(  msg  )

    # ----------------------------------------------
    def cb_define_tweets_concord( self,  ):
        """
        call back for gui button
        might want to do individually ??
        """
        print( f"cb_define_tweets_concord {self.parameters.database_name}")

        #confirm ?
        msg            = "This operation will delete any current data from the teeets and concord tables, continue?"
        continue_flag  = messagebox.askokcancel( "Continue?", msg )
        if continue_flag is not True:
            AppGlobal.gui.display_info_string( "Operation canceled" )
            return
        allow_drop   = True
        load_tweet_data.define_table_concord( self.parameters.database_name, allow_drop = allow_drop )
        load_tweet_data.define_table_tweets(  self.parameters.database_name, allow_drop = allow_drop )

        AppGlobal.gui.display_info_string( "Tables tweets and concord defined and  empty" )
        # fix up for any failure in the process -- error message, a except perhaps

   # ----------------------------------------------
    def cb_define_words( self,  ):
        """
        call back for gui button
        populates words table
        """
        msg   = "Defining words table... "
        print( msg )
        #self.print_info_string_now( msg )
        AppGlobal.gui.display_info_string( msg )

        msg            = "This operation will erase any current words table, continue?"
        continue_flag  = messagebox.askokcancel( "Continue?", msg )
        if continue_flag is not True:
            AppGlobal.gui.display_info_string( "Operation canceled" )
            return

        load_word_data.define_table_word( self.parameters.database_name, allow_drop = True )
        msg      = f"Done word table defined."
        print( msg )
        AppGlobal.gui.display_info_string( msg )
        #self.print_info_string_now( msg )

  # ----------------------------------------------
    def cb_load_words( self,  ):
        """
        call back for gui button
        populates words table
        """
        msg   = "Loading words table... "
        print( msg )
        #self.print_info_string_now( msg )
        AppGlobal.gui.display_info_string( msg )

        msg            = "This adds data to the current words table, continue?"
        continue_flag  = messagebox.askokcancel( "Continue?", msg )
        if continue_flag is not True:
            AppGlobal.gui.display_info_string( "Operation canceled" )
            return

        load_word_data.load_table_word( name_db   = self.parameters.database_name,
                                        fn_src    = self.parameters.word_input_file_name )
        line_count  = "implement me "
        msg      = f"done ... word lines processed {line_count}"
        print( msg )
        AppGlobal.gui.display_info_string( msg )
        # self.print_info_string_now( msg )

  # ----------------------------------------------
    def cb_rank_words( self,  ):
        """
        call back for gui button
        populates rank colum of words table by sorting on word_count
        """
        msg   = "Populating word rank in words table... "
        print( msg )
        #self.print_info_string_now( msg )
        AppGlobal.gui.display_info_string( msg )

        msg            = "This populates word rank in words table, continue?"
        continue_flag  = messagebox.askokcancel( "Continue?", msg )
        if continue_flag is not True:
            AppGlobal.gui.display_info_string( "Operation canceled" )
            return

        row_count   = load_word_data.update_rank( db_file_name  = self.parameters.database_name, )

        msg         = f"Done ... word rows processed {row_count}"
        print( msg )
        AppGlobal.gui.display_info_string( msg )
        AppGlobal.logger.info( msg )

  # ----------------------------------------------
    def cb_load_tweets( self,  ):
        """
        call back for gui button
        populates both tweets and concord tables
        !! catch exceptions
        """
        input_fn   =  self.parameters.tweet_input_file_name
        msg        = f"Loading tweets from {input_fn}..... "
        print( msg )
        # self.print_info_string_now( msg )
        AppGlobal.gui.display_info_string( msg )

        msg            = "This operation will add data to the current tweet and concord tables, continue?"
        continue_flag  = messagebox.askokcancel( "Continue?", msg )
        if continue_flag is not True:
            AppGlobal.gui.display_info_string( "Operation canceled" )
            return

        AppGlobal.gui.set_cursor( "wait" )

        a_tweet_file_processor   =  load_tweet_data.TweetFileProcessor( fn_src     = input_fn,
                                                                        db_name    = self.parameters.database_name,
                                                                        who_tweets = self.parameters.who_tweets )
        line_count  = a_tweet_file_processor.read_process_lines( )
        msg  = f"done ... tweet lines processed {line_count}"
        print( msg )
        self.print_info_string_now( msg )
        AppGlobal.gui.set_cursor( "" )

   # ----------------------------------------------
    def cb_graph( self,  ):
        """
        call back for gui button
        """
        pass

      # ----------------------------------------------
    def cb_test( self,  ):
        """
        call back for gui button
        """
        pass

        continue_flag  = messagebox.askokcancel( "Python", "Would you like to test again ?" )
        msg   = f"continue flag = {continue_flag}"
        self.gui.display_info_string( msg )

    # ----------------------------------------------
    def cb_about( self,  ):
        """
        call back for gui button
        """
        AppGlobal.about()

   # ----------------------------------------------
    def cb_gui_test_1( self,  ):
        """
        call back for gui button
        """
        print( "tweet_app.cb_gui_test_1" )

    # ------------------ select helpers
    # ----------------------------------------------
    def gui_to_builder( self, builder  ):
        """
        what it says, get gui info for select into builder
        !! looks to overlap with get_gui_into_builder clarify this
        """
        pass
        y = 1/0

    # ----------------------------------------------
    def get_gui_into_builder( self, builder  ):
        """
        !! look over and select_manager think needs more fields and some tweaks
        populate builder with user options for select
        mutate builder based on gui ( and parameters )
        return zip but builder mutated
        """
        #rint( "....................get_gui_into_builder")

        # think this is obsolete !! check it out
        #builder.a_word              = AppGlobal.gui.a_word_search.get().strip()   # should be in gui get....

        # logically next should not be here but is convientient
        builder.db_name             = self.parameters.database_name

        a_format                    =  self.gui.get_output_format()
        builder.output_format       = a_format

        builder.tweets_word_select   = self.gui.get_tweets_word_select()
        # builder.a_word              = self.gui.a_word_search.get().strip()

        builder.words_word_select   = self.gui.get_words_word_select()

        builder.begin_dt,  builder.end_dt  = self.gui.get_dt_begin_end()

        ___text, ___sql_text, data  = self.gui.get_is_covid()
        builder.is_covid            = data # true false none should have any = none
        #rint( "is_covid tuple ish ",  ___text, ___sql_text, data  )

        ___text, ___sql_text, data  = self.gui.get_is_ascii()
        builder.is_ascii            = data # true false none should have any = none
        #rint( "is_ascii tuple ish",  ___text, ___sql_text, data  )

        # ------------------tweet_type
        builder.tweet_type           = self.gui.get_tweet_type()
        #rint( f">>>>>>>>>>>>>>>>>from gui is this right ..............{builder.tweet_type}" )

        builder.words_word_select    = self.gui.get_words_word_select()

        builder.concord_word_type_select  = self.gui.get_concord_word_type_select()

        builder.concord_word_select       = self.gui.get_concord_word_select()

        # msg    = f"zzz getting max count:  {self.gui.get_words_max_count_select()}"
        # #rint( msg )

        builder.max_count           = self.gui.get_words_max_count_select()

        builder.min_rank            = self.gui.get_min_rank()

        builder.word_type           = self.gui.get_word_type()

        builder.group_by_min_count  = self.gui.get_group_by_min_count()   # ?? check if implemented

        builder.word_rank_null      = "is"     #or isnot  # put in gui  think obsolute

        ___text, ___sql_text, data  = self.gui.get_words_is_word_null_select()
        builder.words_is_word_null  = data # true false none should have any = none

        builder.output_append       =  self.gui.get_output_append_select()

        # !! eliminate dupe
        builder.sort_order          = self.gui.get_sort_order()
        builder.gui_order_by        = self.gui.get_sort_order()

        builder.min_group_by_count  = self.gui.get_group_by_min_count()

        #builder.order_by         = "words.word_rank"  #   or "my_count"

        builder.add_row_count        = True   # True or false adds "'rc'"  # think obsolute

    # ----------------------------------------------
    def cb_run_select( self,  ):
        """
        run the select specified for the gui
        # text, foo            = self.gui.get_select_type_text_function( )
        # foo( text, help_mode = False )
        """
        self.gui.set_cursor( "wait" )
        a_title, foo               = self.gui.get_select_type_constructor()

        #rint( a_title, foo  )
        a_manager      = foo()
        #rint( a_manager )

        a_manager.run_sql_builder( a_title, help_mode = False )
        self.gui.set_cursor( "" )

    # ----------------------------------------------
    def cb_about_select( self,  ):
        """
        run the help for select specified for the gui -- the select itself is not run
        """
        a_title, foo               = self.gui.get_select_type_constructor()
        #rint( a_title, foo  )
        a_manager      = foo()
        #rint( a_manager )
        a_manager.run_sql_builder( a_title, help_mode = True )

    # ----------------------------------------------
    def cb_change_select_type( self, event ):
        """
        Basic Tweet Select
        mostly fixed query for tweet load
        but changing that just use reset select and run
        args  event   ignored
        """
        a_title, foo               = self.gui.get_select_type_constructor()
        #rint( a_title, foo  )
        self.select_manager       = foo()
        self.select_manager.set_up_widgets()

    # ----------------------------------------------
    def slider_select_1( self, select_name, help_mode ):
        """
        Slider Select ... not yet optimized for speed
        problems with unicode may have to "convert"
        write number of tweets
        work on way to suppress header
        might be good time to change versions
        fix sql generation of column part in other selects
        """
        builder                  = sql_builder.SliderSelect1()
        builder.help_mode        = help_mode
        builder.select_name      = select_name
        builder.columns_out      = [ "tweets.tweet_datetime",

                                  "tweets.tweet",
                                ]   # add datetime ??

        self.get_gui_into_builder( builder )
        # then override some -- set into gui
        builder.tweet_type          = "tweet"       #self.gui.get_tweet_type()
        builder.output_format       = "msg"
        #builder.help_mode        = help_mode

        # ?? not right
        builder.help_file        = self.parameters.help_path + "./slider_select_1.txt"
        builder.help_file        = self.parameters.help_path + "./slider_select_1.txt"
        builder.go( )

    # ----------------------------------------------
    def select_zip( self, select_name, help_mode = True ):   # lets just go to select_number
        """
        concordance select 1
        arguments   help_mode ......
        """
        print( "!! select zip error not implemented")

# ==============================================
if __name__ == '__main__':
    """
    run the app here for convenience of launching
    """
    a_app = TweetApp(  )






