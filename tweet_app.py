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
import traceback
import psutil
import queue
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
        self.version                = "Ver: Alpha 11 - 2020 05 24.1"   # code cleanup by delete -- use sql_builder as super

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
#        print( "===================restart===========================" )
        self.no_restarts    += 1
        if self.gui is not None:

            self.logger.info( self.app_name + ": restart" )

            # self.post_to_queue( "stop", None  , (  ) ) # need to shut down other thread
            # self.helper_thread.join()

            self.gui.close()

            importlib.reload( parameters )    # should work on python 3 but sometimes if not

        #self._polling_fail        = False   # flag set if _polling in gui thread fails

#        self.is_first_gui_loop    = True
        #self.ext_processing       = None    # built later from parameters if specified
        self.logger               = None    # set later none value protects against call against nothing

        # ----- parameters
        self.parmeters_x          = "none"        # name without .py for parameters
                                                  #extension may ?? be replaced by command line args
        #self.__get_args__( )
        # command line might look like this
        # python smart_plug.py    parameters=gh_paramaters

        self.parameters         = parameters.Parameters( )
        self.starting_dir       = os.getcwd()

        # # get parm extensions  ?? for now drop -- will this work on a reload ??
        # if self.parmeters_x != "none":
        #     self.parmeters_xx   =  self.create_class_from_strings( self.parmeters_x, "ParmetersXx" )
        #     self.parmeters_xx.modify( self.parameters )

        self.logger_id          = self.parameters.logger_id       # std name
        self.logger             = self.config_logger()            # std name

        AppGlobal.logger        = self.logger
        AppGlobal.logger_id     = self.logger_id

        self.prog_info()

        self.gui                = gui.GUI(  )

        # now most of setup memory has been allocated -- may want to chekc in again later, save this value ??
        process      = psutil.Process(os.getpid())    #  import psutil
        mem          = process.memory_info().rss
        # convert to mega and format
        mem_mega     = mem/( 1e6 )
        msg          = f"process memory = {mem_mega:10,.2f} mega bytes "
        print( msg )
        self.logger.log( AppGlobal.force_log_level,      msg )

        self.gui.run()

        self.logger.info( self.app_name + ": all done" )

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
        print( msg )
        logger.info( msg ) #  .debug   .info    .warn    .error
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
        used as callback from gui button -- rename cb ??
        path addition here because parameters.py is not itself a parameter
        """
        a_filename = self.parameters.py_path + os.path.sep + "parameters.py"
        AppGlobal.os_open_txt_file( a_filename )

    # ----------------------------------------------
    def os_open_logfile( self,  ):
        """
        used as/by callback from gui button.  Can be called form gt
        """
        # a_filename = self.parameters.py_path + os.path.sep + self.parameters.pylogging_fn

        AppGlobal.os_open_txt_file( self.parameters.pylogging_fn )

    # ----------------------------------------------
    def os_open_helpfile( self,  ):
        """
        used as callback from gui button
        ?? still need to decide how to manage path if not a url
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

   # # ----------------------------------------------
   #  def cb_define_db( self,  ):
   #      """
   #      call back for gui button
   #      """
   #      print("cb_define_db not implemented")
   #      pass

   # ----------------------------------------------
    def cb_show_load_parms ( self,  ):
        """
        call back for gui button

        """
        msg     = (   f"Load parameters ..... "
                    + f"\nDatabase Name:  {self.parameters.database_name}"
                    + f"\nTweet Input:    {self.parameters.tweet_input_file_name}"
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
        pass
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
        msg        = "Loading tweets from {input_fn}..... "
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

        #self.gui.root.withdraw()
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
        print( "cb_gui_test_1" )


    # # ----------------------------------------------
    # def cb_tweet_select_1( self,  ):
    #     """
    #     call back for gui button
    #     -- moved to cb_select_word_count
    #     """
    #     print("cb_tweet_select_1")
    #     builder                     = sql_builder.SQLBuilder()
    #     builder.help_file           = self.parameters.help_path + "/build_for_tweets.txt"

    #     a_format                    =  self.gui.get_output_format()
    #     builder.output_format       = a_format

    #     builder.db_name             = self.parameters.database_name

    #     begin_ts, end_ts            = self.gui.get_begin_end()   # return( ts_begin , ts_end  )
    #     builder.begin_dt            = datetime.datetime.fromtimestamp( begin_ts )
    #     builder.end_dt              = datetime.datetime.fromtimestamp( end_ts )

    #     ___text, ___sql_text, data  = self.gui.get_is_covid()
    #     print( "is_covid",  ___text, ___sql_text, data  )
    #     builder.is_covid            = data # true false none

    #     builder.columns_out         = [ "tweets.tweet_datetime", "tweets.is_covid", "tweets.tweet", ]    # also need my_count? for now have builder add it at end
    #     builder.order_by            = "tweets.tweet_datetime"  # or "my_count DESC"
    #     builder.min_word_count      = 5

    #     try:
    #         builder.build_for_tweets()
    #         builder.select_and_output()

    #     except app_global.UserCancel as exception:
    #         # Catch the custom exception but just drop as this is the point
    #         pass
    #         print( exception )
    # ------------------ select helpers
    # ----------------------------------------------
    def gui_to_builder( self, builder  ):
        """
        what it says, get gui info for select into builder
        !! looks to overlap with get_gui_into_builder clarify this
        """
        a_format                    =  self.gui.get_output_format()
        builder.output_format       = a_format

        builder.a_word              = self.gui.a_word_search.get().strip()

        begin_ts, end_ts            = self.gui.get_begin_end()   # return( ts_begin , ts_end  )
        builder.begin_dt            = datetime.datetime.fromtimestamp( begin_ts )
        builder.end_dt              = datetime.datetime.fromtimestamp( end_ts )

        ___text, ___sql_text, data  = self.gui.get_is_covid()
        print( "is_covid",  ___text, ___sql_text, data  )
        builder.is_covid            = data # true false none should have any = none

        # ------------------tweet_type
        builder.tweet_type           = self.gui.get_tweet_type()
        #print( f">>>>>>>>>>>>>>>>>from gui is this right ..............{builder.tweet_type}" )

        builder.max_count            = self.gui.get_max_count()
        builder.min_rank             = self.gui.get_min_rank()

        builder.add_row_count        = True   # True or false adds "'rc'"

        builder.gui_order_by         = self.gui.get_sort_order()

        builder.word_type            = self.gui.get_word_type()

    # ----------------------------------------------
    def get_gui_into_builder( self, builder  ):
        """
        populate builder with user options for select
        mutate builder based on gui ( and parameters )
        return zip but builder mutated
        """
        print( "....................get_gui_into_builder")

        builder.db_name          = self.parameters.database_name
        builder.help_file        = self.parameters.help_path + "./build_for_word_count.txt"  #?? fix with pathlib

        # text, sql_text, data     =  self.gui.get_is_covid()
        # builder.is_covid         = data                # true false none should have any = none

        a_format                 =  self.gui.get_output_format()
        builder.output_format    = a_format

        begin_ts, end_ts            = self.gui.get_begin_end()   # return( ts_begin , ts_end  )
        builder.begin_dt            = datetime.datetime.fromtimestamp( begin_ts )
        builder.end_dt              = datetime.datetime.fromtimestamp( end_ts )

        ___text, ___sql_text, data  = self.gui.get_is_covid()
        print( "is_covid",  ___text, ___sql_text, data  )
        builder.is_covid            = data # true false none should have any = none

        # ------------------tweet_type
        builder.tweet_type           = self.gui.get_tweet_type()
        #print( f">>>>>>>>>>>>>>>>>from gui is this right ..............{builder.tweet_type}" )

        builder.max_count            = self.gui.get_max_count()
        builder.min_rank             = self.gui.get_min_rank()


        # # surprise have some mix up on min mas  count rank .... probably a bug to fix
        # builder.min_word_count   = self.gui.get_max_count()

        # # builder.max_word_rank    = 100_000    # keep above 100_000 or do not expect results
        # builder.max_word_rank    = self.gui.get_min_rank()

        builder.word_rank_null      = "is"     #or isnot  # put in gui

        # x   = self.gui.get_sort_order()
        # print( "sort order",  x  )
        # builder.sort_order       = self.gui.get_sort_order()
        builder.sort_order       = self.gui.get_sort_order()
        builder.gui_order_by     = self.gui.get_sort_order()
        #builder.order_by         = "words.word_rank"  #   or "my_count"

    # ----------------------------------------------
    def cb_run_select( self,  ):
        """
        run the select specified for the gui
        """
        text, foo            = self.gui.get_select_type_text_function( )
        foo( text, help_mode = False )

    # ----------------------------------------------
    def cb_about_select( self,  ):
        """
        run the help for select specified for the gui -- the select itself is not run
        """
        text, foo            = self.gui.get_select_type_text_function( )
        foo( text, help_mode = True )     # text in control is the select name

    # ------------------ select helpers
    # ----------------------------------------------
    def tweet_select_1( self, select_name, help_mode ):
        """
        Basic Tweet Select
        mostly fixed query for tweet load
        but changing that just use reset select and run
        """

        builder                  = sql_builder.TweetSelect1()
        builder.help_mode        = help_mode
        builder.select_name      = select_name

        #self.gui_to_builder( builder )   # ?? which one
        self.get_gui_into_builder( builder )
        # !! wrong here probably self.get_gui_into_buildeself.confirm_continue( info_msg, self.check_title,   self.check_run_select, ) #   r( builder )

        builder.help_file        = self.parameters.help_path + "./tweet_select_1.txt"

        builder.go( )

        # try:
        #     #db_util_concord.util_select_concord( builder  )
        #     #builder.build_for_check_tweet_load(   )       # mutates select_dict
        #     builder.tweet_select_1()
        #     builder.select_and_output( )    # help_mode ??

        # except app_global.UserCancel as exception:
        #     # let user cancel or help_mode = True
        #     print( exception )

        # msg   = f"Select Done, rows selected: {builder.row_count}"   # ?? add time
        # AppGlobal.gui.display_info_string( msg )
        # # self.print_info_string_now( msg )
        # AppGlobal.logger.debug(  msg  )

    # ----------------------------------------------
    def concord_select_1( self, select_name, help_mode  ):
        """
        concord joined to tweet with counts on each word
        concord_select_1.txt
        """
        # builder                  = sql_builder.SQLBuilder()

        builder                  = sql_builder.ConcordSelect1()
        self.get_gui_into_builder( builder )
        builder.help_mode        = help_mode
        builder.select_name      = select_name

        builder.help_file        = self.parameters.help_path + "./concord_select_1.txt"

        builder.tweet_type       = self.gui.get_tweet_type()

        self.gui_to_builder( builder )

        # my count is dynamic to group by and count * as my_count
        # !! need gui element for this  .. still need developmen for now treat as a minimum
        builder.my_count           = 3   # if using a groupby with count  !! this is a min needs rename

        #builder.go( which_select = builder.concord_select_1 )
        builder.go( )

    # ----------------------------------------------
    def select_03( self, select_name, help_mode ):
    # def tweet_joined_select_1( self, select_name, help_mode ):
        """
        call back for gui button  this is a tweet for a selected word -- date range?
        this is the part of the sql that may come from the gui and passed to the engine
        think now route thru cb_run_select
            # three way join work on next  lets just call select_03   and later will
        """
        # print( "cb_select_tweet_word" )

        builder                     = sql_builder.Select_03()
        builder.help_mode           = help_mode
        builder.select_name         = select_name

        builder.help_file           = self.parameters.help_path + "/build_for_select_tweet_word.txt"
        builder.help_file           = self.parameters.help_path + "/tweet_joined_select_1.txt"
        builder.help_file           = self.parameters.help_path + "/select_03.txt"   #

        # !! think better  get from gui here

        a_format                    = self.gui.get_output_format()
        builder.output_format       = a_format

        builder.db_name             = self.parameters.database_name

        builder.a_word              = self.gui.a_word_search.get().strip()

        begin_ts, end_ts            = self.gui.get_begin_end()   # return( ts_begin , ts_end  )
        builder.begin_dt            = datetime.datetime.fromtimestamp( begin_ts )
        builder.end_dt              = datetime.datetime.fromtimestamp( end_ts )

        ___text, ___sql_text, data  = self.gui.get_is_covid()
        print( "is_covid",  ___text, ___sql_text, data  )
        builder.is_covid            = data # true false none should have any = none

        # ------------------tweet_type
        builder.tweet_type           = self.gui.get_tweet_type()
        #print( f">>>>>>>>>>>>>>>>>from gui is this right ..............{builder.tweet_type}" )

        builder.max_count            = self.gui.get_max_count()
        builder.min_rank             = self.gui.get_min_rank()

        builder.add_row_count        = True   # True or false adds "'rc'"

        builder.default_order_by            = "tweets.tweet_datetime"
        builder.gui_order_by                = self.gui.get_sort_order()

        # if  builder.a_word == "zzzzzzzzzzz":   # !! decide and then fix
        #     builder.columns_out      = [ "tweets.tweet_type", "'joe'", "tweets.tweet", "tweets.tweet_id", "tweets.tweet_datetime", ]    # also need my_count? for now have builder add it at end
        # else:
        builder.columns_out      = [ "tweets.tweet_datetime",
                                      "concord.word",
                                         "tweets.tweet",
                                         "tweets.tweet_type",
                                         "tweets.is_covid",
                                         "words.word_rank",

                                         "tweets.tweet_id",
                                         #"SUM( 1 ) ",
                                         sql_builder.ROW_COUNT_CN,      # pseodo column for row count
                                         sql_builder.TOTAL_WORD_RANK    # pseodo column for word rank, in flux
                                         ]

        builder.go( )

# ------------------ old selects -- for code salvage -- no longer consisten with builder

    # ----------------------------------------------
    # xxxxnext to work on   not sure rename  db_select_3    join all select ... no looks like a 2 way join
    # concord joined to words, thus cannot do dates .... so do not work on
    # def cb_select_concord( self,  ):
    def concord_joined_select_1( self, select_name, help_mode ):
        """
        call back for gui button  this is a word or concordance selection
        set up for select ... most from user or parameters
        """
        builder                  = sql_builder.SQLBuilder()
        # builder.help_file        = self.parameters.help_path + "./build_for_word_count.txt"  #?? fix with pathlib
        builder.help_mode        = help_mode
        builder.select_name      = select_name

        builder.help_file        = self.parameters.help_path + "./concord_joined_select_1.txt"
        a_format                 = self.gui.get_output_format()
        builder.output_format    = a_format

        builder.db_name          = self.parameters.database_name

        builder.min_word_count   = 5

        builder.max_word_rank    = 100_000    # keep above 100_000 or do not expect results
        builder.max_word_rank    = None       # put in gui

        builder.word_rank_null   = "is"     #or isnot  # put in gui

        # x   = self.gui.get_sort_order()
        # print( "sort order",  x  )
        builder.sort_order       = self.gui.get_sort_order()

        builder.order_by         = "words.word_rank"  #   or "my_count"

        builder.columns_out      = [ "concord.word", "words.word", "words.word_rank",  ]    # also need my_count? for now have builder add it at end
        builder.columns_out      = [ "concord.word", "words.word_rank",  ]

        # consider ?? move to builder
        try:
            #db_util_concord.util_select_concord( builder  )
            # builder.build_for_word_count(   )   # mutates select_dict

            builder.concord_joined_select_1()
            builder.select_and_output()

        except app_global.UserCancel as exception:   #
            # Catch the custom exception
            print( exception )

        msg   = f"Select Done, rows selected: {builder.row_count}"   # ?? add time
        AppGlobal.gui.display_info_string( msg )
        # self.print_info_string_now( msg )
        AppGlobal.logger.debug(  msg  )

    # ----------------------------------------------
    def select_zip( self, select_name, help_mode = True ):   # lets just go to select_number
        """
        concordance select 1
        arguments   help_mode ......
        """
        print( "!! select zip error ")

    # ----------------------------------------------
    def select_concord_1( self, select_name, help_mode = True ):   # lets just go to select_number
        """
        concordance select 1
        arguments   help_mode ......
        """
        print( f"tweet_app select_concord_1 {help_mode}")
        builder                     = sql_builder.SQLBuilder()
        builder.help_mode           = help_mode
        builder.select_name         = select_name

        self.gui_to_builder( builder )

        builder.db_name               = self.parameters.database_name
        builder.help_file             = self.parameters.help_path + "/concord_1.txt"

        builder.default_order_by      = "tweets.tweet_datetime"

        builder.columns_out           = [   "tweets.tweet_datetime",
                                             "concord.word",
                                             "tweets.tweet",
                                             "tweets.tweet_type",
                                             "tweets.is_covid",
                                             "words.word_rank",
                                             "tweets.tweet_id",
                                              sql_builder.ROW_COUNT_CN,      # pseudo column for row count
                                              sql_builder.TOTAL_WORD_RANK ,   # pseudo column for word rank, in flux
                                           ]

        builder.sql_from                =  ""

        #.....................

        self.group_by       = "concord.word"

        if self.count:
            self.sql_from       += ", COUNT( * ) as my_count  "

        self.sql_from           += "\n    FROM concord "

        self.sql_from           += "\n    LEFT JOIN words  ON concord.word = words.word  "

        # consider ?? move to builder
        try:
            #db_util_concord.util_select_concord( builder  )
            builder.build_for_select_1( help_mode = help_mode  )   # pass in builder instead ??
            builder.select_and_output()

        except app_global.UserCancel as exception:
            # user has canceled
            pass
            print( exception )
        # start_time = time.time()
        # end_time = time.time()
        # print( f"for {loop_max} itterations code took {end - start} seconds")

        msg   = "Select Done"
        self.print_info_string_now( msg )






# ==============================================
if __name__ == '__main__':
    """
    run the app here for convenience of launching
    """
    a_app = TweetApp(  )






