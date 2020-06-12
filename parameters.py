# -*- coding: utf-8 -*-

"""

for tweet analysis db


"""

import logging
import sys
import os
import datetime
#import collections

# --------- local
from app_global import AppGlobal
from running_on import RunningOn

# ------------------------------------
class Parameters( object ):
    """
    manages parameter values use like ini file
    much like a structure but with a few smarts
    """
   # -------
    def choose_mode( self,  ):
        """
        choose your mode, typically only one line is uncommented, or just pass to stay in default mode
        note addition "mode_plus_tests" set up for some testing, keep for that purpose
        """
        # ===========  add your  modes as desired starting here ========
        # ---------->> call modes here; I comment out ones I am not using.
        # Makes it really easy to switch modes

        #----------------- begin pick a mode -------------->>
        """
        modes set here override values in the default mode ( and in self.os_tweaks() self.computer_name_tweaks()   )

        """
        pass                              # if everything else is commented out
        self.mode_build_tables_on_ram_drive()
        self.mode_2020_test()
        #self.mode_tiny_test()
        #self.mode_db_in_code_dir()
        # --- probably obsolete, save for ref
        #self.mode_tiny_trump()
        #self.mode_2Ktrump()

        #self.mode_db_in_code_dir()
        #self.mode_big_test()
        #self.mode_add_2019()
        #self.mode_db_in_code_dir()

        # ---- additional stuff only for testing -- in addition to another mode
        #self.mode_plus_tests()                # used only for testing

    # -------
    def mode_plus_tests( self ):
        """
        add change some parameters just for testing
        """
        self.mode               += " + tests"
        self.logging_level      = logging.DEBUG     #INFO

  # ------------------------
    def mode_build_tables_on_ram_drive( self,  ):
        """
        for building on ram drive, one table or time period at a time
        do not add other data to this db without a copy/rename
        """
        self.mode                    = "mode_build_tables_on_ram_drive"

        self.show_db_def             = True    # True or False  normally false so you do not trash db by mistake
        self.database_name           = r"R:/Temp./all_words.db"
        self.database_name           = r"R:/Temp./2019_to_dec2019.db"
        self.database_name           = r"R:/Temp./2018_thru_may_2020.db"
        self.database_name           = r"R:/Temp./2017_thru_may_2020.db"
        self.database_name           = r"R:/Temp./2016_thru_may_2020.db"


        self.tweet_input_file_name   = r"./input/all_tweets_2019.csv"
        self.tweet_input_file_name   = r"./input/all_tweets_2020_thru_may.csv"
        self.tweet_input_file_name   = r"./input/all_tweets_2018.csv"
        self.tweet_input_file_name   = r"./input/all_tweets_2017.csv"
        self.tweet_input_file_name   = r"./input/all_tweets_2016.csv"

        self.word_input_file_name    = r"./input/english-word-frequency/unigram_freq.csv"
        self.logging_level           = logging.DEBUG     #INFO

  # ------------------------
    def mode_db_in_code_dir( self,  ):
        """
        mode for first use, database in directory with code, not best for performance, but no special setup
        from github download
        """
        self.mode                    = "db_in_code_dir"                        # mode for db in same dir as code
        self.database_name           = r"./all_words_tweets_to_all2019.db"     # location of the sqlite db, file name
                                                                               # move to ram drive for fasted response
        self.database_name           = r"R:/Temp./all_words.db"
        # ------------- data load
        self.show_db_def             = False    # True or False  show db def features in the gui
                                               # normally False so you do not trash db by mistake

        self.tweet_input_file_name   = r"./input/all_tweets_2019.txt"   # input data for tweets




        self.who_tweets              = "djt"   # not really used yet -- perhaps later
        self.use_spacy               = True    # use the spacy processor on input words
        self.confirm_selects         = False   # if true use message box to confirm selects prior to running

        self.word_input_file_name    = r"./input/english-word-frequency/unigram_freq.csv"   # input to the words table, reference word data

        self.default_word_list       = []  # probably proper name for combo_box_words... now being renamed again ... put in defaults

        self.default_word            = ""
        self.combo_box_words         = [ "fake", "fraud", "outraged", "dem%", "republican",  "immigration",
                                         "sam", "joe", "warren", "barr", "more", "bad", "best", "faith", "god", "love", "hate" ]
    # -------
    def mode_2020_test( self,  ):
        """
        test with small file size ... good for testing, run on ram drive, everything runs fast
        """
        self.mode                    = "mode_2020_test"

        self.database_name           = "all_words_plus_tiny_test.db"  # starting from all words first
        self.database_name           = r"R:/Temp./2020_test.db"  # copy up fill words, rename

        # ------------- data load
        self.show_db_def             = True    # True or False  normally false so you do not trash db by mistake

        self.tweet_input_file_name   = r"./input/all_tweets_2020_thru_may.csv"
        self.tweet_input_file_name   = r"./input/all_tweets_2019.csv"
        self.tweet_input_file_name   = r"./input/all_tweets_2018.csv"
        self.tweet_input_file_name   = r"./input/all_tweets_2017.csv"
        self.tweet_input_file_name   = r"./input/all_tweets_2016.csv"

        #self.tweet_input_file_name   =  os.path.join( dir_name, base_fn  + os.extsep + ext )

        self.who_tweets              = "djt"    # not really used yet
        self.use_spacy               = True
        self.confirm_selects         = False      # if true use message box to confirm selects
        self.word_input_file_name    = r"./input/english-word-frequency/tiny_unigram_freq.csv"

   # ------------------------
    def mode_big_test( self,  ):
        """
        test with large db size
        """
        self.mode                    = "big_test"

        self.database_name           = "big_test.db"
        self.database_name           = r"R:/big_test.db"            # ram disk version
        self.database_name           = r"R:/big_test_with_tweets.db"    # on both r and C:  working version

        # ------------- data load
        self.show_db_def             = True   # True or False  show db def features in the gui
                                               # normally False so you do not trash db by mistake

        self.tweet_input_file_name   = r"./input/tiny_in.txt"   # just for now redo
        #self.tweet_input_file_name   =  os.path.join( dir_name, base_fn  + os.extsep + ext )
        self.tweet_input_file_name   = r"./input/all_tweets_may_16_for_2020.txt"

        self.who_tweets              = "djt"    # not really used yet
        self.use_spacy               = True
        self.confirm_selects         = False      # if true use message box to confirm selects

        self.word_input_file_name    = r"./input/english-word-frequency/tiny_unigram_freq.csv"
        self.word_input_file_name    = r"./input/english-word-frequency/unigram_freq.csv"

        self.default_word_list       = []  # not implemented

        self.default_word            = "joe"
        self.combo_box_words         = [ "fake", "fraud", "outraged", "dem", "republican",  "immigration",
                                         "sam", "joe", "warren", "barr", "more", "bad", "best", "faith", "god", "love", "hate" ]
   # ------------------------
    def mode_add_2019( self,  ):
        """
        test with large db size
        """
        self.mode                    = "add_2019"

        #self.database_name           = "big_test.db"
        #self.database_name           = r"R:/big_test.db"            # ram disk version
        self.database_name           = r"R:/all_words_tweets_to_all2019.db"    # on both r and C:  working version

        # ------------- data load
        self.show_db_def             = True   #True   # True or False  show db def features in the gui
                                               # normally False so you do not trash db by mistake

        #self.tweet_input_file_name   = r"./input/tiny_in.txt"   # just for now redo
        #self.tweet_input_file_name   =  os.path.join( dir_name, base_fn  + os.extsep + ext )
        #self.tweet_input_file_name   = r"./input/all_tweets_may_16_for_2020.txt"
        self.tweet_input_file_name   = r"./input/all_tweets_2019.txt"

        self.who_tweets              = "djt"    # not really used yet
        self.use_spacy               = True
        self.confirm_selects         = False      # if true use message box to confirm selects

        self.word_input_file_name    = r"./input/english-word-frequency/tiny_unigram_freq.csv"
        self.word_input_file_name    = r"./input/english-word-frequency/unigram_freq.csv"


        self.default_word            = "joe"
        self.combo_box_words         = [ "fake", "fraud", "outraged", "dem", "republican",  "immigration",
                                        "sam", "joe", "warren", "barr", "more", "bad", "best", "faith", "god", "love", "hate" ]

    # -------
    def mode_2Ktrump(self,  ):
        """
        changes not much -- may not be in default this may be ok as we may not want to run
        """
        self.word_input_file_name    = r".\english-word-frequency\unigram_freq.csv"
        #self.word_input_file_name    = r".\english-word-frequency\tiny_unigram_freq.csv"

        self.use_db                  = True      # if false then no output to db

        self.database_name           = "tweet_2.db"
        self.database_name           = "tweet_big_words.db"

        self.use_spacy               = True

        self.tweet_input_file_name   = r"tiny_in.txt"
        self.tweet_input_file_name   = r"twoKTweets.csv"

        # where does tweet output go ... direct to db? and a file
        self.tweet_out_file_name     = r"twoKTweets_out.txt"   # out for concor.py input for util
        self.tweet_out_file_name     = r"twoK_out.txt"   # out for concor.py input for util

        print( "====================={self.database_name }============================" )

    # -------
    def __init__(self,    ):

        AppGlobal.parameters   = self
        self.default_mode()
        self.running_on_tweaks()
        self.choose_mode()
        AppGlobal.parameter_tweaks()  # including restart

    # -------
    def running_on_tweaks(self,  ):
        """
        use running on tweaks as a more sophisticated  version of os_tweaks and computer name tweaks,
        """
        computer_id              =   self.running_on.computer_id

        self.os_tweaks()  # general for os, later for more specific

        if computer_id == "smithers":
            self.win_geometry       = '1450x700+20+20'      # width x height position
            self.ex_editor          =  r"D:\apps\Notepad++\notepad++.exe"
            #self.db_file_name       =  "smithers_db.db"

        elif computer_id == "millhouse":
            self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"
            #self.ex_editor          =  r"notepad"
            #self.win_geometry   = '1300x600+20+20'
            #self.db_file_name       =  "millhouse_db.db"

        elif computer_id == "theprof":
            #self.win_geometry       = '1450x700+20+20'      # width x height position
            self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"
            #self.db_file_name       =  "the_prof_db.db"

        elif computer_id == "bulldog":    # may be gone
            self.ex_editor          =  r"gedit"            # ubuntu
            #self.db_file_name       =  "bulldog_db.db"

        elif computer_id == "bulldog-mint-russ":
            self.ex_editor          =  r"xed"
            #self.db_file_name       =  "bulldog_db.db"

        else:
            print( f"In parameters: no special settings for computer_id {computer_id}" )
            if self.running_on.os_is_win:
                self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"
            else:
                self.ex_editor          =  r"leafpad"    # linux raspberry pi maybe

    # -------
    def os_tweaks( self, ):
        """
        this is an subroutine to tweak the default settings of "default_ _mode"
        for particular operating systems
        you may need to mess with this based on your os setup
        """
        if  self.os_win:
            pass
            #self.icon               = r"./clipboard_b.ico"    #  greenhouse this has issues on rasPi
            #self.icon              = None                    #  default gui icon

        else:
            pass

    # -------
    def computer_name_tweaks( self ):
        """
        this is an subroutine to tweak the default settings of "default_mode"
        for particular computers.  Put in settings for you computer if you wish
        these are for my computers, add what you want ( or nothing ) for your computes
        """
        if self.computername == "smithers":
            self.win_geometry       = '1250x700+20+20'      # width x height position
            self.ex_editor          =  r"D:\apps\Notepad++\notepad++.exe"    # russ win 10 smithers

        elif self.computername == "millhouse":
            self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"    # russ win 10 millhouse
            self.win_geometry       = '1000x500+20+20'          # width x height position
            #self.pylogging_fn       = "millhouse_clipboard.py_log"   # file name for the python logging

        elif self.computername == "theprof":
            self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"    # russ win 10 millhouse
            #self.win_geometry       = '1800x800+20+20'          # width x height position
            #self.pylogging_fn       = "millhouse_clipboard.py_log"   # file name for the python logging

        else:
            print( f"no tweaks for {self.computername}" )

    # ------->> Subroutines:  one for each mode alpha order - except tutorial
    # -------
    def default_mode( self ):
        #print( "\n ======== default_config =========" )
        self.mode               = "default_mode"

        # ------------- file and path names -------------------

        # this is the name of a program: its excutable with path inof.
        # to be used in opening an exteranl editor
        self.ex_editor          = r"D:\apps\Notepad++\notepad++.exe"    # russ win 10

        self.help_file          = r"http://www.opencircuits.com/Twitter_Analysis_DB_GUI"

        self.output_path        = f".{os.sep}output"     # may need to fix for linux vs win
        self.input_path         = ".\input"
        self.help_path          = f".{os.sep}help"

        #self.db_path            = None     # if we do not want db in the default ignore if None

        # ------------- Application
        #--------------- automatic settings -----------------
        self.running_on   = RunningOn
        self.running_on.gather_data()

        self.py_path                = self.running_on.py_path

        self.tweet_input_file_name  = r"./input/all_tweets_2019.txt"

        our_os = sys.platform
#        print( "our_os is ", our_os )

        if our_os == "win32":
            self.os_win = True     # right now windows and everything else
        else:
            self.os_win = False

        self.platform               = our_os    # sometimes it matters which os

        self.computername           = ( str( os.getenv( "COMPUTERNAME" ) ) ).lower()

        # ------------ manual settings
        self.icon                   = r"clipboard_c.ico"
        self.icon                   = r"CHIP.ICO"

        self.id_color               = "red"                # ?? not implemented

        self.win_geometry           = '1500x800+20+20'     # width x height position
        self.win_geometry           = '900x600+700+230'    # width x height position  x, y  --- find code for maximize
        self.win_geometry           = '1900x1000+2+2'    # width x height position  x, y  --- find code for maximize  good for the prof

        self.id_color               = "red"    # the application may have color to help identify the gui. think dead code  "blue"   "green"  and lots of other work
        self.id_height              = 20       # if there is an id pane, height of id pane, 0 for no pane

        # tkinter uses bg for background so I should probably make a global change
        self.bkg_color              = "blue"   # color for the background, you can match the id color or use a neutral color like gray
        self.bkg_color              = "gray"   # override of above because I could
        self.bkg_color              = "dark slate gray"
        self.bn_color               = "light gray"    # color for buttons -- may not be implemented -- use bn to match tkinter api
        self.btn_color              = self.bn_color
        self.bn_color_active        = "gray"

        self.log_gui_text           = False  # True log all the stuff put in the message area -- may be issues with unicode??

        self.log_gui_text_level     = logging.DEBUG
        self.pylogging_fn           = "tweet_app.py_log"      # file name for the python logging

        self.logging_level          = logging.DEBUG        # .DEBUG  .INFO   logging level

        self.logger_id              = "tweet"                # id in logging file
        self.who_tweets             = "djt"

        # ---- next 4 parms are for the select clause -- may be changed in the GUI
        self.select_begin_date      = datetime.date( 1981, 6,  16 )    # default beginning date for the sql select  ( year, month, day)
        self.select_begin_date      = datetime.date( 2019, 10, 10 )    # override of above for no particular reason
        self.select_end_date        = datetime.date( 2020, 11, 20 )    # default end date for the sql select  ( year, month, day)

        self.select_begin_hr        = AppGlobal.dd_hours[0]            # default begin time for the sql select  (  index on 24 hr clock )
        self.select_end_hr          = AppGlobal.dd_hours[0]            # default end time for the sql select    (  index on 24 hr clock )
        self.slider_datetime_width  = datetime.timedelta( days = 9  )

        self.default_word           = "dem%" #  default word for tweet selects president truth fake failing
        self.confirm_selects        = False      # if true use message box to confirm selects
        self.show_db_def            = True       #  or False

        self.default_scroll         = True
        self.default_output_format  = "html"     # default format for selects  html yaml csv text  see gui..

        self.default_select_type     = ""

        # take these: as possible suggestions
        self.combo_box_words        = [ "fake", "fraud", "outraged", "dem", "republican",  "immigration",
                                        "sam", "joe", "warren", "barr", "more", "bad", "best", "faith", "god", "love", "hate" ]

        self.polling_delta         = 200    # units ms # set to 0 for no polling

# ==============================================
if __name__ == '__main__':
    """
    run the app here for convenience of launching
    """
    import tweet_app
    a_app = tweet_app.TweetApp(  )

# ======================== eof ======================


