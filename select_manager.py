# -*- coding: utf-8 -*-
"""
Overall management for each select more or less ABC
use instances or classes ??  now instances


"""
from   tkinter import messagebox
# import logging
# import sys
# import os
# import time
import datetime
# import traceback
# import psutil
# import queue
# import threading
# import importlib
# from   tkinter import messagebox
import collections

#----------- local imports --------------------------
# import parameters
# import gui
from   app_global import AppGlobal
# import app_global
# import sql_builder
# import load_tweet_data
# import load_word_data
import sql_builder

WidgetInfo               = collections.namedtuple( 'WidgetInfo', ['value', 'state', 'dd_list', ]) #

# ----- ========================== Begin Application Class ================================
class SelectManager( object ):
    """
    create one of these for each select, it currently:
        controls the gui
        sets up the first part of the select that is
        then passed to a SQLBuilder, which carries out the select

    pass something to gui to have it adjust the selects
    is we have dates  words -- with dropdown and dropdowns
    what we pass should be a dict keyed off the controls as in control dict
    what are the values
    another dict?  a named tuple ? just a tuple
    ColumnInfoTuple              = collections.namedtuple( 'ColumnInfoTuple', ['curly_format', 'xxx' ]) #
    print( ColumnInfoTuple )

    a_cit    = ColumnInfoTuple( curly_format = "joe", xxx = 3 )

    """
    def __init__(self ):
        """
        may be more doc in SM_Select_01
        """
        # WidgetInfo is created to control the widgets for a select
        #rint( WidgetInfo )

        # in the dict  enabled  valid selects ( choose from list ?? ) default selects ....
        # ---------- sample creation of a control_dict .. override in children
        # ---------- you cannot skip any part of the tuple
        # ---------------------
        self.control_dict    =  { }
        a_wi                 = WidgetInfo( value    = "Any",
                                          dd_list   = [ 1,2,3 ],   # if present configure ( else Noneleave as is )
                                          state     = "readonly",
                                )
        a_wi                 = WidgetInfo( value    = "Any",
                                          dd_list   = None,   # if present configure ( else None leave as is )
                                          state     = "readonly",
                                          )
        #rint( a_wi )
        self.control_dict[AppGlobal.gui.is_covid]     = a_wi
        self.control_dict[AppGlobal.gui.tweet_type]   = a_wi
        self.control_dict[AppGlobal.gui.max_count]    = a_wi

        self.control_dict[AppGlobal.gui.is_covid]     = a_wi
                                  # AppGlobal.gui.time_end: 1,
                                  # AppGlobal.gui.is_covid: a_wi,

                                  # AppGlobal.gui.is_ascii: 1,

                                  # AppGlobal.gui.tweet_type: 1,
                                  # AppGlobal.gui.word_type: 1,
                                  # AppGlobal.gui.tweet_type: 1,
                                  # AppGlobal.gui.max_count: 1,

                                  #   }


       # sort_order_dict            =  {    "Default":              "default",
        #                                         "Date":                 "tweets.tweet_datetime",
        #                                         "Date, Tweet Type":     "tweets.tweet_datetime, tweets.tweet_type",
        #                                         "Tweet Type, Date":     "tweets.tweet_type, tweets.tweet_datetime",
        #                                         "Word":        "word",
        #                                         "Word Count":  "words.word_count",
        #                                         "Word Rank":   "words.word_rank" }

        self.sort_order_dict      =  {
                                         "Date, Tweet Type":     "tweets.tweet_datetime, tweets.tweet_type",
                                         "Tweet Type, Date":     "tweets.tweet_type, tweets.tweet_datetime",
                                      }

    # --------------------------------------------------------
    def set_up_widgets( self ):
        """
        args: zip
        ret: mutate widgets in gui
        """
        #rint( "SelectManager set_up_widgets")
        #rint( f"SelectManager self.control_dict  {self.control_dict}" )

        AppGlobal.gui.deactivate_select_widgets(   )
        AppGlobal.gui.configure_select_widgets( self.control_dict )
        AppGlobal.gui.set_date_widget_state_normal( True )    # True  False
        #rint( f"SelectManager self.sort_order_dict  {self.sort_order_dict}" )
        AppGlobal.gui.set_sort_order_dict( self.sort_order_dict )

    # --------------------------------------------------------
    def run_sql_builderxxxxxxxxxx( self, select_name, help_mode ):
        """

        args: zip
        ret: zip ... all sided effects
        """
        print( "run_sql_builder")
        # print( f"{self.control_dict}" )
        # AppGlobal.gui.configure_select_widgets( self.control_dict )
        # # ----------------------------------------------
        # def select_05( self, select_name, help_mode ):
        # """
        # Experiment Tweet Select
        # first clean up Basic Tweet Select and test then try to add like, then perhaps migrate back
        # """
        print( "select_05" )
        builder                  = sql_builder.Select_05()
        builder.help_mode        = help_mode
        builder.select_name      = select_name
        builder.columns_out      = [ "tweets.tweet_datetime",
                                     "tweets.time_of_day",
                                     "tweets.tweet_type",
                                     "tweets.tweet",
                                     #"tweets.tweet_id",
                                     sql_builder.ROW_COUNT_CN,
                                     ]

        AppGlobal.controller.get_gui_into_builder( builder )   # move to here

        builder.help_file        = AppGlobal.parameters.help_path + "./select_05.txt"

        builder.go( )

    # --------------------------------------------------------
    def set_control_dict_tweet_type( self,  ):
        """
        stand gui contol dict setting for see final line ... this is really for the whole text tweets.tweet ....
        ret: zip ... all sided effects
        """

        # --------------------
        a_wi                 = WidgetInfo( value        = "Any",
                                           dd_list      = None,
                                            state       = "readonly",
                                          )
        self.control_dict[ AppGlobal.gui.tweet_type ]   = a_wi

    # --------------------------------------------------------
    def set_control_dict_tweets_word( self,  ):
        """
        stand gui control dict setting for see final line ... this is really for the whole text tweets.tweet ....
        ret: zip ... all sided effects
        """
        a_wi                 = WidgetInfo( value        = "Any",
                                            dd_list      = None,   # if present configure ( else leave as is )
                                            state        = "normal",
                                          )
        self.control_dict[AppGlobal.gui.tweets_word_widget]       = a_wi

        # set_up_widgets( )
    # --------------------------------------------------------
    def set_control_dict_is_covid( self,  ):
        """
        stand gui control dict setting for is_covid
        args: zip
        ret: zip ... all sided effects
        """
        a_wi                 = WidgetInfo( value        = "Any",
                                           dd_list       = None,   # if present configure ( else leave as is )
                                           state        = "readonly",
                                          )
        self.control_dict[AppGlobal.gui.is_covid]       = a_wi


    # --------------------------------------------------------
    def set_control_dict_concord_word( self,  ):
        """
        stand gui control dict setting for see last line or function name
        ret: zip ... all sided effects
        """
       # --------------------
        a_wi                 = WidgetInfo( value            = "Any",
                                           dd_list          = None,
                                            state           = "normal",
                                          )
        self.control_dict[ AppGlobal.gui.concord_word_widget ] = a_wi

    # --------------------------------------------------------
    def set_control_dict_concord_word_type( self,  ):
        """
        stand gui control dict setting for see last line or function name
        ret: zip ... all sided effects
        """
      # --------------------
        a_wi                 = WidgetInfo( value            = "Any",
                                           dd_list          = None,
                                            state           = "readonly",
                                          )
        self.control_dict[ AppGlobal.gui.concord_word_type_widget ] = a_wi


    # --------------------------------------------------------
    def set_control_dict_words_word( self,  ):
        """
        stand gui control dict setting for see final line
        ret: zip ... all sided effects
        """
        a_wi                 = WidgetInfo( value        = "Any",
                                            dd_list      = None,   # if present configure ( else leave as is )
                                            state        = "normal",
                                          )
        self.control_dict[AppGlobal.gui.words_word_widget]      = a_wi

    # --------------------------------------------------------
    def set_control_dict_is_ascii( self,  ):
        """
        stand gui control dict setting for see final line
        ret: zip ... all sided effects
        """
        a_wi                 = WidgetInfo( value    = "Any",
                                          dd_list   = None ,
                                           state    = "readonly",   #[ 1,2,3 ]   # if present configure ( else leave as is )
                                )
        #rint( a_wi )
        self.control_dict[AppGlobal.gui.is_ascii]    = a_wi

    # --------------------------------------------------------
    def set_control_dict_max_count( self,  ):
        """
        stand gui control dict setting for see final line
        ret: zip ... all sided effects
        """
        # --------------------
        a_wi                 = WidgetInfo( value            = "Any",
                                           dd_list          = None,
                                           state            = "readonly",
                                          )
        self.control_dict[ AppGlobal.gui.words_max_count_widget ] = a_wi

    # --------------------------------------------------------
    def set_control_dict_min_rank( self,  ):
        """
        stand gui control dict setting for see final line
        ret: .
        """
        # --------------------
        a_wi                 = WidgetInfo( value            = "Any",
                                           dd_list          = None,
                                           state            = "readonly",
                                          )
        self.control_dict[ AppGlobal.gui.words_min_rank_widget ] = a_wi

    # --------------------------------------------------------
    def set_control_dict_tod_min( self,  ):
        """
        stand gui control dict setting for see final line
        ret: ... mutates self
        """
        a_wi                 = WidgetInfo( value        = "",
                                           dd_list      = None,   # if present configure ( else leave as is )
                                           state        = "readonly",
                                          )
        self.control_dict[AppGlobal.gui.tod_min_widget]  = a_wi

    # --------------------------------------------------------
    def set_control_dict_min_group_by( self,  ):
        """
        stand gui control dict setting for see final line
        ret: ... mutates self
        """
        a_wi                 = WidgetInfo( value        = "",
                                           dd_list      = None,   # if present configure ( else leave as is )
                                           state        = "readonly",
                                          )
        self.control_dict[AppGlobal.gui.group_by_min_count_widget]  = a_wi

    # --------------------------------------------------------
    def set_control_dict_words_word_null( self,  ):
        """
        stand gui control dict setting for see final line
        ret: ... mutates self
        """
        a_wi                 = WidgetInfo( value        = "",
                                           dd_list      = None,   # if present configure ( else leave as is )
                                           state        = "readonly",
                                          )
        self.control_dict[AppGlobal.gui.words_word_null_widget]  = a_wi
# ----------------------------------------
class SM_Select_01( SelectManager  ):
    """
    see SelectManager
    this SM is specialized as describe in .....
    """
    def __init__( self,  ):
        """
        what it says -- parent may have more doc
        """
        #rint( "init SM_Select_01")
        #super().__init__(  )     # probably should use, but right now does nothing useful

        self.sort_order_dict      =  {
                                         "Date, Tweet Type":     "tweets.tweet_datetime, tweets.tweet_type",
                                          "Tweet Type, Date":     "tweets.tweet_type, tweets.tweet_datetime",
                                      }

        #------------------------------ for use of this see gui.configure_select_widgets()   ---
        self.control_dict    =  { }

        self.set_control_dict_is_covid()
        self.set_control_dict_tweet_type()
        self.set_control_dict_tweets_word( )
        self.set_control_dict_tod_min( )

    # --------------------------------------------------------
    def run_sql_builder( self, select_name, help_mode ):
        """
        -- see base class for doc
        args: zip
        ret: zip ... all sided effects
        """
        #rint( "SM_Select_01  run_sql_builder")

        builder                  = sql_builder.Select_01()
        builder.help_file        = AppGlobal.parameters.help_path + "./select_01.txt"
        builder.help_mode        = help_mode
        builder.select_name      = select_name

        AppGlobal.controller.get_gui_into_builder( builder )

        builder.columns_out      = [  sql_builder.ROW_COUNT_CN,
                                     "tweets.tweet_datetime", "tweets.time_of_day",
                                     "tweets.tweet_type",     "tweets.tweet",           "tweets.tweet_id"    ]
        builder.go( )

# ----------------------------------------
class SM_Select_Msg_01( SelectManager  ):
    """
    see SelectManager
    this SM is specialized as describe in .....
    """
    def __init__( self,  ):
        """
        what it says -- parent may have more doc
        """
        #rint( "init SM_Select_01")
        #super().__init__(  )

        self.sort_order_dict      =  {
                                         "Date, Tweet Type":     "tweets.tweet_datetime, tweets.tweet_type",
                                         "Tweet Type, Date":     "tweets.tweet_type, tweets.tweet_datetime",
                                      }

        #------------------------------ for use of this see gui.configure_select_widgets()   ---
        self.control_dict    =  { }

        self.set_control_dict_is_covid()
        self.set_control_dict_tweet_type()
        self.set_control_dict_tweets_word( )
        self.set_control_dict_tod_min( )

    # --------------------------------------------------------
    def run_sql_builder( self, select_name, help_mode ):
        """
        -- see base class for doc
        args: zip
        ret: zip ... all sided effects
        """
        #rint( "SM_Select_01  run_sql_builder")

        builder                  = sql_builder.Select_Msg_01()
        builder.help_file        = AppGlobal.parameters.help_path + "./select_msg_01.txt"
        builder.help_mode        = help_mode
        builder.select_name      = select_name

        AppGlobal.controller.get_gui_into_builder( builder )

        builder.columns_out      = [  sql_builder.ROW_COUNT_CN,

                                     "tweets.tweet_type",
                                     "tweets.tweet",
                                     "tweets.tweet_datetime",
                                     ]
        builder.go( )

# ----------------------------------------
class SM_Select_02( SelectManager  ):
    """
    see parent SelectManager
    this SM is specialized as describe in help file: builder.help_file
    """
    def __init__( self,  ):
        """
        what it says

        """
        #rint( "init SM_Select_02")
        # super().__init__(  )   # need to eliminate this

        self.sort_order_dict      =  {
                                          "Word ( concord )":       "concord.word",
                                          "Word Type, Word":        "concord.word_type, concord.word",
                                          "Is Ascii, Word":         "concord.is_ascii, concord.word",
                                          "Count, Word":            "my_count, concord.word",
                                          "Word Type, Count, Word": "concord.word_type, my_count, concord.word",
                                      }

        #---------------------------------
        self.control_dict    =  { }

        a_wi                 = WidgetInfo( value        = "Any",
                                          dd_list       = None,   # if present configure ( else leave as is )
                                           state        = "readonly",
                                          )
        #rint( a_wi )
        self.control_dict[AppGlobal.gui.is_covid]       = a_wi
        # --------------------
        self.set_control_dict_tweet_type()
        # --------------------
        a_wi                 = WidgetInfo( value         = "Any",
                                          dd_list        = None,   # if present configure ( else leave as is )
                                           state         = "normal",
                                          )
        self.control_dict[ AppGlobal.gui.tweets_word_widget ] = a_wi

        # # --------------------
        a_wi                 = WidgetInfo( value         = "Any",
                                            dd_list       = None,
                                             state        = "readonly",
                                          )
        self.control_dict[ AppGlobal.gui.concord_word_type_widget ] = a_wi

        # --------------------
        self.set_control_dict_concord_word()
        self.set_control_dict_is_ascii()
        self.set_control_dict_min_group_by()

    # --------------------------------------------------------
    def run_sql_builder( self, select_name, help_mode ):
        """
        args: zip
        ret: zip ... all sided effects
        """
        #rint( "SM_Select_02  run_sql_builder")

        builder                  = sql_builder.Select_02()
        builder.help_file        = AppGlobal.parameters.help_path + "./select_02.txt"

        builder.help_mode        = help_mode
        builder.select_name      = select_name

        builder.tweet_type       = AppGlobal.gui.get_tweet_type()  # should be in next line
        AppGlobal.controller.get_gui_into_builder( builder )

        # my count is dynamic to group by and count * as my_count  !! wrong should come from gui
        # !! need gui element for this  .. still need development for now treat as a minimum
        builder.my_count           = 0   # if using a groupby with count  !! this is a min needs rename

        builder.go( )

# ----------------------------------------
class SM_Select_03( SelectManager  ):
    """
    see SelectManager
    this SM is specialized as describe in its help text
    look at 04 which is close to this init
    """
    def __init__( self,  ):
        """
        what it says
        """
        #rint( "init SM_Select_03")
        # super().__init__(  )

        self.sort_order_dict      =  {
                                         "Date, Tweet Type":       "tweets.tweet_datetime, tweets.tweet_type",
                                         "Tweet Type, Date":       "tweets.tweet_type, tweets.tweet_datetime",
                                          "Word ( concord )":      "concord.word",
                                          "Word Type, Word":       "concord.word_type, concord.word",
                                          "Is Ascii, Word":        "concord.is_ascii, concord.word",
                                          #"Count, Word":             "my_count, concord.word",
                                          #"Word Type, Count, Word":        "concord.word_type, my_count, concord.word",
                                      }

        #---------------------------------
        self.control_dict    =  { }

        a_wi                 = WidgetInfo( value    = "Any",
                                          dd_list   = None,    #[ 1,2,3 ]   # if present configure ( else leave as is )
                                           state    = "readonly",
                                )
        #rint( a_wi )
        self.control_dict[AppGlobal.gui.is_covid]   = a_wi

        # #---------------------------------
        # a_wi                 = WidgetInfo( value    = "Any",
        #                                   dd_list   = None ,
        #                                    state    = "readonly",   #[ 1,2,3 ]   # if present configure ( else leave as is )
        #                         )
        # #rint( a_wi )
        # self.control_dict[AppGlobal.gui.is_ascii]    = a_wi
        self.set_control_dict_is_ascii()

        # --------------------
        a_wi                 = WidgetInfo( value        = "Any",
                                           dd_list      = None,
                                            state       = "readonly",
                                          )
        self.control_dict[ AppGlobal.gui.tweet_type ]   = a_wi

      # --------------------
        a_wi                 = WidgetInfo( value        = "Any",
                                           dd_list      = None,
                                            state       = "normal",
                                          )
        self.control_dict[ AppGlobal.gui.tweets_word_widget ] = a_wi

      # --------------------
        a_wi                 = WidgetInfo( value            = "Any",
                                           dd_list          = None,
                                            state           = "readonly",
                                          )
        self.control_dict[ AppGlobal.gui.concord_word_type_widget ] = a_wi

        self.set_control_dict_concord_word()
        self.set_control_dict_words_word()

        # --------------------
        a_wi                 = WidgetInfo( value            = "Any",
                                           dd_list          = None,
                                           state            = "readonly",
                                          )
        self.control_dict[ AppGlobal.gui.words_max_count_widget ] = a_wi

        # --------------------
        a_wi                 = WidgetInfo( value            = "Any",
                                           dd_list          = None,
                                           state            = "readonly",
                                          )
        self.control_dict[ AppGlobal.gui.words_min_rank_widget ] = a_wi

    # --------------------------------------------------------
    def run_sql_builder( self, select_name, help_mode ):
        """
        args: zip
        ret: zip ... all sided effects
        """
        print( "SM_Select_03  run_sql_builder")

        builder                  = sql_builder.Select_03()
        builder.help_file        = AppGlobal.parameters.help_path + "./select_03.txt"

        builder.help_mode        = help_mode
        builder.select_name      = select_name

        builder.tweet_type       = AppGlobal.gui.get_tweet_type()  # should be in next line
        AppGlobal.controller.get_gui_into_builder( builder )

        builder.columns_out      = [ "tweets.tweet_datetime",

                                      "tweets.tweet",
                                      "tweets.tweet_type",
                                      "tweets.is_covid",
                                      "concord.word",
                                      "concord.word_type",
                                      "concord.is_ascii",
                                      "words.word_rank",
                                      "words.word_count",

                                       "tweets.tweet_id",
                                         #"SUM( 1 ) ",
                                        sql_builder.ROW_COUNT_CN,      # pseudo column for row count
                                        #sql_builder.TOTAL_WORD_RANK    # pseudo column for word rank, in flux
                                         ]

        builder.go( )

# ----------------------------------------
class SM_Select_04( SelectManager  ):
    """
    see SelectManager
    this SM is specialized as describe in .....
    """
    def __init__( self,  ):
        """
        what it says
        """
        print( "init SM_Select_04")
        #super().__init__(  )

        self.sort_order_dict      =  {
                                         "Date, Tweet Type":       "tweets.tweet_datetime, tweets.tweet_type",
                                         "Tweet Type, Date":       "tweets.tweet_type, tweets.tweet_datetime",
                                          "Word ( concord )":      "concord.word",
                                          "Word Type, Word":       "concord.word_type, concord.word",
                                          "Is Ascii, Word":        "concord.is_ascii, concord.word",
                                          #"Count, Word":             "my_count, concord.word",
                                          #"Word Type, Count, Word":        "concord.word_type, my_count, concord.word",
                                      }

        #---------------------------------
        self.control_dict    =  { }

        a_wi                 = WidgetInfo( value    = "Any",
                                          dd_list   = None,    #[ 1,2,3 ]   # if present configure ( else leave as is )
                                           state     = "readonly",
                                )
        #rint( a_wi )
        self.control_dict[AppGlobal.gui.is_covid]    = a_wi

        a_wi                 = WidgetInfo( value    = "Any",
                                          dd_list   = None,    #[ 1,2,3 ]   # if present configure ( else leave as is )
                                           state     = "readonly",
                                )
        #rint( a_wi )
        self.control_dict[AppGlobal.gui.is_ascii]    = a_wi

        # # --------------------
        # a_wi                 = WidgetInfo( value    = "Any",
        #                                   dd_list   = [ "Any" , "Yes", "No",  ]   # if present configure ( else leave as is )
        #                                   )
        # self.control_dict[ AppGlobal.gui.is_ascii ] = a_wi

        # --------------------
        a_wi                 = WidgetInfo( value    = "Any",
                                           dd_list   = None,   # if present configure ( else leave as is )
                                            state     = "readonly",
                                          )
        self.control_dict[ AppGlobal.gui.tweet_type ] = a_wi

      # --------------------
        a_wi                 = WidgetInfo( value    = "Any",
                                           dd_list   = None,   # if present configure ( else leave as is )
                                            state     = "readonly",
                                          )
        self.control_dict[ AppGlobal.gui.tweets_word_widget ] = a_wi

      # --------------------
        a_wi                 = WidgetInfo( value    = "Any",
                                           dd_list   = None,   # if present configure ( else leave as is )
                                            state     = "readonly",
                                          )
        self.control_dict[ AppGlobal.gui.concord_word_type_widget ] = a_wi

      # --------------------
        a_wi                 = WidgetInfo( value    = "Any",
                                           dd_list   = None,   # if present configure ( else leave as is )
                                            state     = "readonly",
                                          )
        self.control_dict[ AppGlobal.gui.concord_word_widget ] = a_wi

        # ---- words
        self.set_control_dict_words_word()

        # --------------------
        a_wi                 = WidgetInfo( value    = "Any",
                                           dd_list   = None,   # if present configure ( else leave as is )
                                           state     = "readonly",
                                          )
        self.control_dict[ AppGlobal.gui.words_min_rank_widget ] = a_wi

        # --------------------
        a_wi                 = WidgetInfo( value    = "Any",
                                           dd_list   = None,   # if present configure ( else leave as is )
                                            state     = "readonly",
                                          )
        self.control_dict[ AppGlobal.gui.words_max_count_widget ] = a_wi

    # --------------------------------------------------------
    def run_sql_builder( self, select_name, help_mode ):
        """
        args: zip
        ret: zip ... all sided effects
        """
        #rint( "SM_Select_04  run_sql_builder")


        builder                  = sql_builder.Select_04()
        builder.help_file        = AppGlobal.parameters.help_path + "./select_04.txt"

        builder.help_mode        = help_mode
        builder.select_name      = select_name

        builder.tweet_type       = AppGlobal.gui.get_tweet_type()  # should be in next line
        AppGlobal.controller.get_gui_into_builder( builder )

        builder.columns_out      = [ "tweets.tweet_datetime",
                                      "concord.word",
                                      "tweets.tweet",
                                      "tweets.tweet_type",
                                      "tweets.is_covid",
                                      "words.word_rank",

                                      "tweets.tweet_id",
                                         #"SUM( 1 ) ",
                                         sql_builder.ROW_COUNT_CN,      # pseodo column for row count
                                   #      sql_builder.TOTAL_WORD_RANK    # pseodo column for word rank, in flux
                                         ]

        builder.go( )

# ----------------------------------------
class SM_Select_05( SelectManager  ):
    """
    see SelectManager
    this SMis specialized as describe in .....   select_05.txt
    in init        customize self.control.dict
    implement run_sql_builder
    """
    def __init__( self,  ):
        """
        what it says

        """
        #print( "init SM_Select_03")
        #super().__init__(  )

        #----------- override parent
        self.control_dict    =  { }
        # --------------------

        a_wi                 = WidgetInfo( value        = "Any",
                                           dd_list      = None,   # if present configure ( else None leave as is )
                                           state        = "readonly",
                                )

        print( a_wi )
        self.control_dict[AppGlobal.gui.is_covid]    = a_wi

    # --------------------------------------------------------
    def run_sql_builder( self, select_name, help_mode ):
        """
        args: zip
        ret: zip ... all sided effects
        """
        print( "SM_Select_05  run_sql_builder")
        # print( f"{self.control_dict}" )
        # AppGlobal.gui.configure_select_widgets( self.control_dict )
        # # ----------------------------------------------
        # def select_05( self, select_name, help_mode ):
        # """
        # Experiment Tweet Select
        # first clean up Basic Tweet Select and test then try to add like, then perhaps migrate back
        # """
        print( "select_05" )

        builder                  = sql_builder.Select_05()
        builder.help_file        = AppGlobal.parameters.help_path + "./select_05.txt"

        builder.help_mode        = help_mode
        builder.select_name      = select_name
        builder.columns_out      = [ "tweets.tweet_datetime",
                                     "tweets.tweet_type",
                                     "tweets.tweet",
                                     #"tweets.tweet_id",
                                     sql_builder.ROW_COUNT_CN,
                                     ]

        AppGlobal.controller.get_gui_into_builder( builder )   # move to here

        builder.go( )

# ----------------------------------------
class SM_Select_06( SelectManager  ):
    """
    see SelectManager
    this SM is specialized as describe in .....
    """
    def __init__( self,  ):
        """
        what it says
        !! do select name here perhaps even more
        """
        #rint( "init SM_Select_06")
        #super().__init__(  )
        self.sort_order_dict      =  {
                                         "Date, Tweet Type":       "tweets.tweet_datetime, tweets.tweet_type",
                                         "Tweet Type, Date":       "tweets.tweet_type, tweets.tweet_datetime",
                                          "Word ( concord )":      "concord.word",
                                          "Word Type, Word":       "concord.word_type, concord.word",
                                          "Is Ascii, Word":        "concord.is_ascii, concord.word",
                                          "Word Count Word":       "my_count, concord.word"
                                          #"Count, Word":             "my_count, concord.word",
                                          #"Word Type, Count, Word":        "concord.word_type, my_count, concord.word",
                                      }

        #---------------------------------
        self.control_dict    =  { }

        self.set_control_dict_is_covid()     # tweets
        self.set_control_dict_tweet_type()
        self.set_control_dict_tweets_word()

        # ---- concord
        self.set_control_dict_concord_word_type()
        self.set_control_dict_is_ascii()     # concord
        self.set_control_dict_concord_word()

        # ---- words
        self.set_control_dict_words_word()
        self.set_control_dict_words_word_null()
        self.set_control_dict_min_rank()
        self.set_control_dict_max_count()

        # ---- group by and other
        #  !!self.set_control_dict_word_words_is_null() needs implementation

        self.set_control_dict_min_group_by()
    # --------------------------------------------------------
    def run_sql_builder( self, select_name, help_mode ):
        """
        args: zip
        ret: zip ... all sided effects
        """
        print( "SM_Select_06  run_sql_builder")

        builder                     = sql_builder.Select_06()
        builder.help_file           = AppGlobal.parameters.help_path + "./select_06.txt"

        builder.help_mode           = help_mode
        builder.select_name         = select_name

        builder.tweet_type          = AppGlobal.gui.get_tweet_type()  # should be in next line
        AppGlobal.controller.get_gui_into_builder( builder )

        # my count is dynamic to group by and count * as my_count  !! wrong should come from gui
        # !! need gui element for this  .. still need development for now treat as a minimum
        builder.my_count            = 0   # if using a groupby with count  !! this is a min needs rename

        # builder.columns_out         = [    "concord.word",
        #                                    "concord.word_type",
        #                                    "concord.is_ascii",
        #                                    "tweets.tweet",
        #                                    "tweets.tweet_type",
        #                                    "tweets.tweet_datetime",
        #                                    "tweets.time_of_day",
        #                                    sql_builder.ROW_COUNT_CN,
        #                                    #  "my_count",  this will call a count(*) and if not used with group by .....
        #                               ]

        builder.go( )

# ----------------------------------------
class SM_Select_07( SelectManager  ):
    """
    see SelectManager
    this SM is specialized as describe in .....
    """
    def __init__( self,  ):
        """
        what it says
        !! do select name here perhaps even more

        gui.words_word_widget
        gui.words_word_select
        get_gui_into_builder    -->   builder.words_word_select
        """
        print( "init SM_Select_07")
        #super().__init__(  )

        #---------------------------------
        self.control_dict    =  { }

        self.set_control_dict_words_word()

        # a_wi                 = WidgetInfo( value     = "Any",   # think not used
        #                                    dd_list   = None   # if present configure ( else leave as is )
        #                                   )
        # print( a_wi )
        # self.control_dict[AppGlobal.gui.words_word_widget]    = a_wi


       # self.sort_order_dict      =  {
       #                                    "Date, Tweet Type":     "tweets.tweet_datetime, tweets.tweet_type",
       #                                    "Tweet Type, Date":     "tweets.tweet_type, tweets.tweet_datetime",
       #                                    "Word ( concord )":      "concord.word",
       #                                    "Word Type, Word":        "concord.word_type, concord.word",
       #                                    "Is Ascii, Word":          "concord.is_ascii, concord.word",

       #                                    "Word ( concord )":      "concord.word",
       #                                    "Word Type, Word":        "concord.word_type, concord.word",
       #                                    "Is Ascii, Word":          "concord.is_ascii, concord.word",
       #                                    "Count, Word":             "my_count, concord.word",
       #                                    "Word Type, Count, Word":        "concord.word_type, my_count, concord.word",
       #                                    "Word ( word )":             "words.word",

       #                                }

        self.sort_order_dict      =  {
                                        "Word ( words )":          "words.word",
                                        "Word Rank, Word":         "words.word_rank, words.word",
                                        "Word Count, Word":        "words.word_count, words.word",
                                      }

    # --------------------------------------------------------
    def set_up_widgets_not_sure ( self ):
        """
        args: zip
        ret: zip ... all sided effects
        AppGlobal.gui.deactivate_select_widgets
        !! need to have my own control dict
        """
        #rint( "set_up_widgets")
        #rint( f"{self.control_dict}" )
        AppGlobal.gui.deactivate_select_widgets(   )
        AppGlobal.gui.configure_select_widgets( self.control_dict )
        AppGlobal.gui.set_date_widget_state_normal( False )    # True  False

    # --------------------------------------------------------
    def run_sql_builder( self, select_name, help_mode ):
        """
        args: zip
        ret: zip ... all sided effects
        """
        #rint( "SM_Select_07  run_sql_builder")

        builder                  = sql_builder.Select_07()
        builder.help_file        = AppGlobal.parameters.help_path + "./select_07.txt"

        builder.help_mode        = help_mode
        builder.select_name      = select_name
        builder.columns_out      = [ "words.word",
                                     "words.word_count",
                                     "words.word_rank",
                                     sql_builder.ROW_COUNT_CN,
                                     ]

        AppGlobal.controller.get_gui_into_builder( builder )   # move to here
        #msg = f">>>>>>>>>>>>>>>>>>>>>>>>>>>builder.words_word_select{builder.words_word_select}"
        #rint( msg )
        if  builder.words_word_select  == "":
            msg  = "There are so many words that the words like select must not be blank."
            # !! change to correct message box and put in gui
            print( msg )
            #messagebox.askokcancel( "Continue?", msg )
            messagebox.showinfo( "Cannot Run Select", msg )
            return

        builder.go( )

# ----------------------------------------
class SM_Select_X1( SelectManager  ):
# from  class SM_Select_02( SelectManager  ):
    """
    see SelectManager
    this SM is specialized as describe in .....
    """
    def __init__( self,  ):
        """
        what it says

        """
        #rint( "init SM_Select_02")
        # super().__init__(  )   # need to eliminate this

        self.sort_order_dict      =  {
                                          "Word ( concord )":                   "concord.word",
                                          "Word Type, Word ( concord )":        "concord.word_type, concord.word",
                                          "Is Ascii, Word ( concord )":         "concord.is_ascii, concord.word",
                                          "DateTime, Word ( concord )":         "tweets.tweet_datetime, concord.word",
                                          #"Count, Word":            "my_count, concord.word",
                                          #"Word Type, Count, Word": "concord.word_type, my_count, concord.word",
                                      }

        #---------------------------------
        self.control_dict    =  { }
        # --------------------
        self.set_control_dict_is_covid()
 
        # --------------------
        a_wi                 = WidgetInfo( value        = "Any",
                                          dd_list       = None ,  # if present configure ( else leave as is )
                                           state        = "readonly",
                                          )
        self.control_dict[ AppGlobal.gui.tweet_type ]   = a_wi
        
        # --------------------
        a_wi                 = WidgetInfo( value         = "Any",
                                          dd_list        = None,   # if present configure ( else leave as is )
                                           state         = "normal",
                                          )
        self.control_dict[ AppGlobal.gui.tweets_word_widget ] = a_wi
        # --------------------
        a_wi                 = WidgetInfo( value         = "Any",
                                           dd_list       = None,
                                            state        = "readonly",
                                          )
        self.control_dict[ AppGlobal.gui.concord_word_type_widget ] = a_wi
        # --------------------
      
        self.set_control_dict_is_ascii()
        self.set_control_dict_concord_word()

    # --------------------------------------------------------
    def run_sql_builder( self, select_name, help_mode ):
        """
        args: zip
        ret: zip ... all sided effects
        """
        #rint( "SM_Select_02  run_sql_builder")

        builder                     = sql_builder.Select_X1()
        builder.help_file           = AppGlobal.parameters.help_path + "./select_X1.txt"

        builder.help_mode           = help_mode
        builder.select_name         = select_name

        builder.tweet_type          = AppGlobal.gui.get_tweet_type()  # should be in next line
        AppGlobal.controller.get_gui_into_builder( builder )

        # my count is dynamic to group by and count * as my_count  !! wrong should come from gui
        # !! need gui element for this  .. still need development for now treat as a minimum
        builder.my_count            = 0   # if using a groupby with count  !! this is a min needs rename

        builder.columns_out         = [    "concord.word",
                                           "concord.word_type",
                                           "concord.is_ascii",
                                           "tweets.tweet",
                                           "tweets.tweet_type",
                                           "tweets.tweet_datetime",
                                           "tweets.time_of_day",
                                           sql_builder.ROW_COUNT_CN,
                                           #  "my_count",  this will call a count(*) and if not used with group by .....
                                      ]

        builder.go( )

# ----------------------------------------
class SM_Select_01_Old_for_code_ref_delete( SelectManager  ):
    """
    see SelectManager
    this SM is specialized as describe in .....
    """
    def __init__( self,  ):
        """
        what it says
        """
        print( "init SM_Select_01")
        #super().__init__(  )
        #print( WidgetInfo )


       # sort_order_dict            =  {    "Default":              "default",
        #                                         "Date":                 "tweets.tweet_datetime",
        #
        #
        #
        #                                         "Word Count":  "words.word_count",
        #                                         "Word Rank":   "words.word_rank" }


        self.sort_order_dict      =  {    # may be useful for other managers
                                          "Date, Tweet Type":       "tweets.tweet_datetime, tweets.tweet_type",
                                          "Tweet Type, Date":       "tweets.tweet_type, tweets.tweet_datetime",
                                          "Word ( concord )":       "concord.word",
                                          "Word Type, Word":        "concord.word_type, concord.word",
                                          "Is Ascii, Word":         "concord.is_ascii, concord.word",
                                      }

        self.sort_order_dict      =  {



                                          "Count, Word":            "my_count, concord.word",
                                          "Word Type, Count, Word": "concord.word_type, my_count, concord.word",

                                      }




        a_wi    = WidgetInfo( value = "Any",
                              dd_list   = [ 1,2,3 ],
                               state     = "readonly",
                                )
        print( a_wi )
        #


        #---------------------------------
        self.control_dict    =  { }

        a_wi                 = WidgetInfo( value    = "Any",
                                          dd_list   = [ 1,2,3 ],
                                           state     = "readonly",

                                )
        print( a_wi )
        self.control_dict[AppGlobal.gui.is_covid]    = a_wi

        # # --------------------
        # a_wi                 = WidgetInfo( value    = "Any",
        #                                   dd_list   = [ "Any" , "Yes", "No",  ]   # if present configure ( else leave as is )
        #                                   )
        # self.control_dict[ AppGlobal.gui.is_ascii ] = a_wi

        # --------------------
        a_wi                 = WidgetInfo( value    = "Any",
                                           dd_list   = None,   # if present configure ( else leave as is )
                                            state     = "readonly",
                                          )
        self.control_dict[ AppGlobal.gui.tweet_type ] = a_wi

      # --------------------
        a_wi                 = WidgetInfo( value    = "Any",
                                           dd_list   = None,   # if present configure ( else leave as is )
                                            state     = "readonly",
                                          )
        self.control_dict[ AppGlobal.gui.tweets_word_widget ] = a_wi


    # --------------------------------------------------------
    def run_sql_builder( self, select_name, help_mode ):
        """

        args: zip
        ret: zip ... all sided effects
        """
        print( "SM_Select_01  run_sql_builder")

        builder                  = sql_builder.Select_01()
        # builder                  = sql_builder.TweetSelect1()
        builder.help_file        = AppGlobal.parameters.help_path + "./select_01.txt"
        builder.help_mode        = help_mode
        builder.select_name      = select_name

        AppGlobal.controller.get_gui_into_builder( builder )

        builder.go( )

# --------------------------------------
if __name__ == '__main__':
        """
        run the app
        """
        import tweet_app
        a_app = tweet_app.TweetApp(  )

# ===================== eof ==================



