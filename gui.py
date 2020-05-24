# -*- coding: utf-8 -*-
"""
	gui    for Tweet App


"""

import logging
from   tkinter import *   # is added everywhere since a gui assume tkinter namespace
from   tkinter import ttk
import sys
from   tkcalendar import Calendar, DateEntry
import datetime
from   tkinter.filedialog import askopenfilename
#from   tkinter.filedialog import asksaveasfile
import pyperclip
import ctypes   # probably should be used to set icon.

#------- local imports
from   app_global import AppGlobal


# ======================= begin class ====================
class GUI:
    """
    gui for the application
    """
    def __init__( self,  ):
        """
        build the application GUI
        """
        AppGlobal.gui           = self
        self.controller         = AppGlobal.controller
        self.parameters         = AppGlobal.parameters

        self.root               = Tk()

        a_title   = self.controller.app_name + " version: " + self.controller.version + " Mode: " +self.parameters.mode
        if self.controller.parmeters_x    != "none":
            a_title  += " parameters=" +   self.controller.parmeters_x

        self.root.title( a_title )
        self.root.geometry( self.parameters.win_geometry )

        # if self.parameters.os_win:
            # from qt - How to set application's taskbar icon in Windows 7 - Stack Overflow
            # https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105

            # icon = self.parameters.icon_graph
            # if not( icon is None ):
            #     print( "set icon "  + str( icon ))
            #     ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(icon)
            #     self.root.iconbitmap( icon )
            # else:
            #     print( "no icon for you!"  + str( icon ))

        self.logger             = logging.getLogger( self.controller.logger_id + ".gui")
        self.logger.info( "in class gui_new GUI init" ) # logger not currently used by here

        # next leftover values may not be used
        self.save_redir          = None
        self.save_sys_stdout     = sys.stdout

        self.rb_var              = IntVar() #Tk.IntVar()

        #------ drop down dicts ( integrate into a calss ?? )  ------  concord_joined_select_1

        # key what displays in gui, value what program uses. constants
        self.select_type_dict     =  {
                                       "Basic Tweet Select":                     self.controller.tweet_select_1,       # #self.controller.cb_check_tweet_load,
                                       "Basic Concordance Select":               self.controller.concord_select_1,       #self.controller.cb_check_concord_load,
                                       "Three Way Join; Full Tweet Text":        self.controller.select_03,

                                       # "Tweet  joined to Concord 1":  self.controller.select_zip,     # self.controller.tweet_joined_select_1,    # was tweet

                                       # #"Basic Concordance Select":    self.controller.concord_select_1,       #self.controller.cb_check_concord_load,
                                       # "Concordance joined to Words": self.controller.concord_joined_select_1,

                                       # "Concordance":                self.controller.tweet_select_1,    # was concord
                                       # "concord 1":                  self.controller.tweet_select_1,    # was concord_1
                                       }

        self.select_word_type_dict  =  { "Any":           None,
                                         "Regular Word":  1,
                                         "Hashtag":       3,
                                         "Regular Word":  1,
                                         "Url":           2,
                                         "@...":          4,
                                         "Leading Num":   5,
                                         }

        self.decode_word_type_dict     = dict(map(reversed, self.select_word_type_dict.items()))  # invert the dict above


        self.select_tweet_type_dict =  { "Any":          None,
                                         "ReTweet":      "retweet",
                                         "Tweet":        "tweet",     }

        self.output_format_dict   =  { "text":      "txt",
                                       "csv":       "csv",
                                       "yaml": "yaml",
                                       "html":      "html",
                                        # "sql":    "sql",
                                        "msg":  "msg"
                                       }

        self.sort_order_dict      =  { "Default":     "default",
                                       "Date":        "date",
                                       "Word":        "word",
                                       "Word Count":  "word _count",
                                       "Word Rank":   "word_rank" }

        self.dd_zero              = [ "data_begin", "data_end",  "db_sql_begin",  "db_sql_end"  ]

        self.dd_units             = [ "seconds", "minutes", "hours", "days" ]

        self.dt_widgets           = []

        #------ constants for controlling layout and look  ------
        self.button_width         = 6

        self.button_padx          = "2m"
        self.button_pady          = "1m"

        self.btn_color            = self.parameters.btn_color
        self.bkg_color            = self.parameters.bkg_color

        self.root.grid_columnconfigure( 0, weight=1 ) # final missing bit of magic
#        self.root.grid_rowconfigure(    0, weight=1 )

        # ------------ start making frames
        next_frame                = 0      # index of frames and position row for frames

        a_frame = self._make_button_frame( self.root,  )
        a_frame.grid(row=next_frame, column=0, sticky=E + W + N)
        next_frame += 1

        a_frame  = self._make_other_select_frame( self.root,  )
        a_frame.grid( row=next_frame, column=0, sticky = E + W + N + S )   # + N + S  )  # actually only expands horiz
        next_frame += 1

        a_frame  = self._make_select_values_frame( self.root,  )
        a_frame.grid( row=next_frame, column=0, sticky = E + W + N + S )   # + N + S  )  # actually only expands horiz
        next_frame += 1


        if AppGlobal.parameters.show_db_def:
            a_frame  = self._make_input_frame( self.root,  )
            a_frame.grid( row=next_frame, column=0, sticky = E + W + N + S )
            next_frame += 1

            a_frame = self._make_load_frame( self.root,  )
            a_frame.grid(row=next_frame, column=0, sticky=E + W + N)
            next_frame += 1

        a_frame = self._make_message_frame( self.root,  )
        a_frame.grid(row=next_frame, column=0, sticky=E + W + N + S)
        next_frame += 1

        self.root.grid_columnconfigure( 0, weight=1 )
        self.root.grid_rowconfigure(    0, weight=0 )
        self.root.grid_rowconfigure( ( next_frame - 1 ), weight=1 )

# ------ build frames  ------------------------
    # ------------------------------------------
    def _make_input_frame( self, parent, ):
        """
        make a frame for input parameters  .....
        Return:  a frame with the controls in it
        """
        a_frame  = Frame( parent, width=600, height=200, bg =self.bkg_color, relief=RAISED, borderwidth=1 )

        # add some more for db, different style, which do I like best?
        lrow   =  0
        lcol   =  0
#        a_spacer  = Frame( a_frame, width=60, height=60, bg ="green", relief=RAISED, borderwidth=1 )
#        a_spacer.grid( row = 0, column = lcol, sticky = E + W + N + S, rowspan = 2 )

        bw_for_db      = FileBrowseWidget( a_frame )
        bw_for_db.grid( row = lrow, column = lcol, columnspan = 6, )
        bw_for_db.set_text( AppGlobal.parameters.database_name )
        self.bw_for_db = bw_for_db  # save reference

        lrow   =  2
        lcol   =  0

        return  a_frame

    # ------------------------------------------
    def _make_button_frame( self, parent, ):
            """
            buttons, mostly system level not app
            """
            a_frame  = Frame( parent, width=300, height=200, bg = self.parameters.id_color, relief=RAISED, borderwidth=1 )

            a_button = Button( a_frame , width=10, height=2, text = "Edit Log" )
            a_button.config( command = self.controller.os_open_logfile )
            a_button.pack( side = LEFT )

            a_button = Button( a_frame , width=10, height=2, text = "Edit Parms" )
            a_button.config( command = self.controller.os_open_parmfile )
            a_button.pack( side = LEFT )

            if self.controller.parmeters_x  != "none":
                a_button = Button( a_frame , width=10, height=2, text = "Edit ParmsX" )
                a_button.config( command = self.controller.os_open_parmxfile )
                a_button.pack( side = LEFT )

            # --- restart
            a_button = Button( a_frame , width=10, height=2, text = "Restart" )
            a_button.config( command = self.controller.restart )
            a_button.pack( side = LEFT )

            a_button = Button( a_frame , width=10, height=2, text = "Test" )
            a_button.config( command = self.controller.cb_test )
            a_button.pack( side = LEFT )

            # --- help
            a_button = Button( a_frame , width=10, height=2, text = "Help" )
            a_button.config( command = self.controller.os_open_helpfile )
            a_button.pack( side = LEFT )

            # --- about
            a_button = Button( a_frame , width=10, height=2, text = "About" )
            a_button.config( command = self.controller.cb_about )
            a_button.pack( side = LEFT )

            return a_frame

    # ------------------------------------------
    def _make_other_select_frame( self, parent, ):
        """
        make vale frame for selects = queries -- input from users

        Return: a frame with the widgets in it
        """
        a_frame  = Frame( parent, width=600, height=200,
                          bg = self.bkg_color, relief=RAISED, borderwidth=1 )

        lrow   =  0
        lcol   =  -1

        # ----- run select
        lcol   += 1
        a_widget = Button( a_frame , width=10, height=2, text = "Selection:" )
        #a_widget.config( command = self.controller.cb_gui_test_1 )
        a_widget.pack( side = LEFT )
        a_widget.grid( row = lrow, column = lcol,  sticky=E + W + N + S )

        # ----- select type
        lcol   += 1
        a_widget   = ( Label( a_frame, text = "Select Type:", width = 30, height=2, relief = RAISED,  )  )
        a_widget.grid( row = lrow, column = lcol, columnspan = 2,  sticky = E + W + N + S )

        lrow   += 1
        a_list     = list(self.select_type_dict.keys())
        a_widget   =  ttk.Combobox( a_frame,
                                values = a_list,
                                height = 20, state='readonly')

        #a_widget.pack( side = LEFT )
        a_widget.grid( row = lrow, column = lcol, columnspan = 2, rowspan = 1, sticky=E + W + N + S )
        #a_widget.set( AppGlobal.parameters.default_output_format )
        a_widget.set( a_list[1] )    # default not in parms ??
        self.select_type  = a_widget
        lrow   += -1

        lcol   += 2 # see above
        a_widget = Button( a_frame , width = 10, height=2, text = "About It" )
        a_widget.config( command = self.controller.cb_about_select )
        #a_widget.pack( side = LEFT )
        a_widget.grid( row = lrow, column = lcol,  sticky=E + W + N + S )

        lcol   += 1
        a_widget = Button( a_frame , width=10, height=2, text = "Run It" )
        a_widget.config( command = self.controller.cb_run_select )
        #a_widget.pack( side = LEFT )
        a_widget.grid( row = lrow, column = lcol,  sticky=E + W + N + S )

        lcol   += 1
        a_widget   = ( Label( a_frame, text = "Other Select\nInfo", height=2, relief = RAISED,  )  )
        #a_widget.grid( row = lrow, column = lcol,  sticky=E + W + N + S )
        a_widget.grid( row = lrow, column = lcol,  sticky=E + W + N + S )

        # ----- sort order
        lcol   += 1
        a_widget   = ( Label( a_frame, text = "Sort", relief = RAISED,  )  )
        a_widget.grid( row = lrow, column = lcol,  sticky=E + W + N + S )

        lrow   += 1
        a_list     = list(self.sort_order_dict.keys())
        a_widget   =  ttk.Combobox( a_frame, values = a_list,  state='readonly')
        a_widget.grid( row = lrow, column = lcol, rowspan = 1, sticky=E + W + N + S )
        a_widget.set( a_list[0] )
        self.sort_order = a_widget
        lrow   += -1

        # ----- output format
        lcol   += 1
        a_widget   = ( Label( a_frame, text = "Output Format:", height=2, relief = RAISED,  )  )
        a_widget.grid( row = lrow, column = lcol,  sticky=E + W + N + S )
        #a_widget.pack( side = LEFT )

        lrow   += 1
        a_widget   =  ttk.Combobox( a_frame,
                                values=list(self.output_format_dict.keys()),
                                height=10,  state='readonly')
        #_widget.configure( ""
        a_widget.grid( row = lrow, column = lcol, rowspan = 1, sticky=E + W + N + S )
        # a_widget.set( AppGlobal.parameters.default_output_format )
        self.output_format  = a_widget
        lrow   += -1

        return a_frame

    # ------------------------------------------
    def _set_active_date_widget( self, a_widget, ):
        """
        indicate the last active date widget used, detail in flux
        change to loop over list of date widgets
        """
        print( "_set_active_date_widget" )
        for i_widget in self.dt_widgets:
            #print( f"widgets: {a_widget} == ? {i_widget}")
            if i_widget == a_widget:
                #print( "_set_active_date_widget   this button" )  # we are not getting this
                i_widget.configure( background = self.parameters.bn_color_active )
            else:
                i_widget.configure( background = self.parameters.bn_color )

    # ----------------------------------------
    def _set_lambda_callback( self, a_widget, a_function ):
        """
        a_function to set the callback in case_dict for a_widget
        also adds to list to control color for active button _set_active_date_widget
        a bit indirect as this seems to 'hide' the parm a_widget and make it the "current" value
        perhaps a closure?
        """
        a_widget.config( command = lambda: a_function( a_widget ) )
        self.dt_widgets.append( a_widget )

    # ------------------------------------------
    def _make_select_values_frame( self, parent, ):
        """
        make value frame for selects values -- input from users
       reset_select_values -- for defaults not here called ate end
        Return: a frame with the widgets in it
        """
        a_frame  = Frame( parent, width=600, height=200,
                          bg = self.bkg_color, relief=RAISED, borderwidth=1 )

        lrow   =  0
        lcol   =  0

        # some spacers might be nice -- may put back as we play with the look
#        a_spacer  = Frame( a_frame, width=60, height=60, bg ="green", relief=RAISED, borderwidth=1 )
#        a_spacer.grid( row = 0, column = lcol, sticky = E + W + N + S, rowspan = 2 )

        # ---------------- buttons for datetimes
        lcol   += 1
        a_widget = Button( a_frame , width=10, height=2, text = "Set Today" )
        self._set_lambda_callback( a_widget, self.set_select_this_week )
        a_widget.grid( row = lrow, column = lcol, rowspan = 1, sticky=E + W + N + S )

        #lcol   += 1
        a_widget = Button( a_frame , width=10, height=2, text = "Set This\n Week" )
        self._set_lambda_callback( a_widget, self.set_select_this_week )
        a_widget.grid( row = lrow +1, column = lcol, rowspan = 1, sticky=E + W + N + S )
        self.dt_widgets.append( a_widget )

        lcol   += 1    # comment out for row 2 add 1 in row below
        a_widget = Button( a_frame , width=10, height=2, text = "Set This\n Month" )
        self._set_lambda_callback( a_widget, self.set_select_this_month )
        a_widget.grid( row = lrow, column = lcol, rowspan = 1, sticky = E + W + N + S )

        #lcol   += 1
        a_widget = Button( a_frame , width=10, height=2, text = "Set\nForever" )
        self._set_lambda_callback( a_widget, self.set_select_forever )
        a_widget.grid( row = lrow +1, column = lcol, rowspan = 1, sticky = E + W + N + S )

        # ------ date slider
        lrow    = 0
        lcol   += 1    # comment out for row 2 add 1 in row below
        a_widget =  Label( a_frame, text = "Set Weeks\nin Past", relief = RAISED,  )
        a_widget.grid( row = lrow, column = lcol, sticky = E + W + N + S )    # sticky=W+E+N+S  )
        #self.dt_widgets.append( a_widget )

        #lcol   += 1
        a_widget = Scale( a_frame, orient ='horizontal', from_= -52, to= 0, command = self.set_select_slier_datetimes )
        #a_widget.config( command = self.set_select_forever )
        a_widget.grid( row = lrow +1, column = lcol, rowspan = 1, sticky =E + W + N + S )
        self.date_slider = a_widget
        self.dt_widgets.append( a_widget )

        # ------------- calendars dates ---------------
        # !! do not need to save labels
        lrow    += 1  # next has some auto increment magic i think
        ( lrow, lcol, self.lbl_start )   = self._make_label( a_frame,
                                                             lrow, lcol, "Start date and hour:", )
        ( lrow, lcol, self.lbl_end   )   = self._make_label( a_frame,
                                                             lrow, lcol, "End date and hour:", )

        lrow    = 0
        #lcol    = 2
        cal     = DateEntry( a_frame, width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=2010,    bordercolor = "red",     )

        cal.grid( row=lrow, column=lcol, sticky=E + W + N + S )
        cal.configure( date_pattern = "yyyy/mm/dd" )
        # cal.set_date( self.parameters.select_begin_date  )
        self.cal_begin = cal

        cal     = DateEntry( a_frame, width=12, background='darkblue',
                             foreground='white',
                             borderwidth=2, year=2010,    bordercolor = "red",     )
        cal.grid( row = lrow +1, column=lcol, sticky=E + W + N + S )
        cal.configure( date_pattern = "yyyy/mm/dd" )
        # cal.set_date( self.parameters.select_end_date  )
        self.cal_end     = cal

        #-------------------- drop down for hours
        lrow    = 0
        lcol    += 1

        a_widget   =  ttk.Combobox( a_frame, values = AppGlobal.dd_hours, state='readonly')
        a_widget.grid( row = lrow, column = lcol,
                       rowspan = 1, sticky=E + W + N + S )
        a_widget.set( self.parameters.select_begin_hr )
        self.time_begin  = a_widget

        a_widget   =  ttk.Combobox( a_frame, values=AppGlobal.dd_hours, state='readonly')
        a_widget.grid( row = lrow + 1, column = lcol, rowspan = 1, sticky=E + W + N + S )
        # a_widget.set( self.parameters.select_end_hr )
        self.time_end  = a_widget

        # ------ text word input -- ?? check default
        lcol   += 3
        a_widget   = ( Label( a_frame, text = "Word Search: ", relief = RAISED,  )  )
        a_widget.grid( row = lrow, column = lcol,  sticky=E + W + N + S )

        lrow   += 1
        self.a_word_search       = StringVar()

        a_widget               = ttk.Combobox( a_frame, values = self.parameters.combo_box_words, textvariable = self.a_word_search )
        a_widget.configure(  height = 50 )   # height of what --- dropdown size on down arrow

        #a_widget               = Entry( a_frame , width=30,  text = "bound", textvariable = self.a_word_search )
        a_widget.grid( row = lrow, column = lcol,  sticky = E + W + N + S )
        # self.a_word_search.set( AppGlobal.parameters.default_word   )
        #print(  "set    ", AppGlobal.parameters.default_word )
        lrow   += -1

        # ----- is covid
        lcol   += 1
        a_widget   = ( Label( a_frame, text = "Is Covid:", relief = RAISED,  )  )
        a_widget.grid( row = lrow, column = lcol,  sticky=E + W + N + S )

        lrow   += 1
        a_widget   =  ttk.Combobox( a_frame, values=[ "Any", "Yes", "No",  ], state='readonly')
        a_widget.grid( row = lrow, column = lcol, rowspan = 1, sticky=E + W + N + S )
        a_widget.set( "Any" )
        self.is_covid  = a_widget
        lrow   += -1

        # ----- max_count
        lcol   += 1
        a_widget   = ( Label( a_frame, text = "Max Count", relief = RAISED,  )  )
        a_widget.grid( row = lrow, column = lcol,  sticky=E + W + N + S )

        lrow   += 1
        a_widget   =  ttk.Combobox( a_frame, values=[ "Any", "100", "100,000",  ], state='readonly')
        a_widget.grid( row = lrow, column = lcol, rowspan = 1, sticky=E + W + N + S )
        a_widget.set( "Any" )
        self.max_count  = a_widget
        lrow   += -1

        # ----- min_rank
        lcol   += 1
        a_widget   = ( Label( a_frame, text = "Min Rank", relief = RAISED,  )  )
        a_widget.grid( row = lrow, column = lcol,  sticky=E + W + N + S )

        lrow   += 1
        a_widget   =  ttk.Combobox( a_frame, values=[ "Any", "100", "500", "1000", "2000", "5000", "10000", ], state='readonly')
        a_widget.grid( row = lrow, column = lcol, rowspan = 1, sticky=E + W + N + S )
        a_widget.set( "Any" )
        self.min_rank  = a_widget
        lrow   += -1

        # ----- tweet_type
        lcol   += 1
        a_widget   = ( Label( a_frame, text = "Tweet Type", relief = RAISED,  )  )
        a_widget.grid( row = lrow, column = lcol,  sticky=E + W + N + S )

        lrow   += 1
        a_widget   =  ttk.Combobox( a_frame, values=[ "Any", "ReTweet", "Tweet",  ], state='readonly')
        a_widget.grid( row = lrow, column = lcol, rowspan = 1, sticky=E + W + N + S )
        a_widget.set( "Any" )
        self.tweet_type = a_widget

        lrow   += -1

        # ----- word_type  !! got get and reset
        lcol   += 1

        a_widget   = ( Label( a_frame, text = "Word Type", relief = RAISED,  )  )
        a_widget.grid( row = lrow, column = lcol,  sticky=E + W + N + S )
        lrow   += 1

        a_list     = list( self.select_word_type_dict.keys())  #  ?? convert iter to list?
        a_widget   =  ttk.Combobox( a_frame, values = a_list, state='readonly')
        a_widget.grid( row = lrow, column = lcol, rowspan = 1, sticky=E + W + N + S )
        a_widget.set( "Any" )
        self.word_type = a_widget
        lcol   += 1   # !! change style to setup for next

        # ----- reset

        a_widget = Button( a_frame , width=10, height=2, text = "Reset" )
        a_widget.config( command = self.reset_select_values )
        # self._set_lambda_callback( a_widget, self.set_select_this_month )
        # a_widget.
        # a_widget   = ( Label( a_frame, text = "Tweet Type", relief = RAISED,  )  )
        a_widget.grid( row = lrow, column = lcol,  sticky=E + W + N + S )

        # lrow   += 1
        # a_widget   =  ttk.Combobox( a_frame, values=[ "Any", "ReTweet", "Tweet",  ], state='readonly')
        # a_widget.grid( row = lrow, column = lcol, rowspan = 1, sticky=E + W + N + S )
        # a_widget.set( "Any" )
        # self.tweet_type = a_widget

        lrow   += -1

        self.reset_select_values()

        return  a_frame

    # ------------------------------------------
    def _make_load_frame( self, parent, ):
            """
            this frame for loading from input files
            make a frame in parent and
            return frame for placement by caller
            """
            a_frame  = Frame( parent, width=300, height=200,
                              bg = self.parameters.id_color, relief=RAISED, borderwidth=1 )

            buttonOpen = Button( a_frame , width=10, height=2, text = "Show Load\nParameters" )
            buttonOpen.config( command = self.controller.cb_show_load_parms )
            buttonOpen.pack( side = LEFT )

            a_button = Button( a_frame , width=10, height=2, text = "Spacer" )
            a_button.config( command = self.controller.cb_gui_test_1 )
            a_button.pack( side = LEFT )

            buttonOpen = Button( a_frame , width=10, height=2, text = "Define Tweets\nConcord" )
            buttonOpen.config( command = self.controller.cb_define_tweets_concord )
            buttonOpen.pack( side = LEFT )


            buttonOpen = Button( a_frame , width=10, height=2, text = "Load Tweets\n(Concord)" )
            buttonOpen.config( command = self.controller.cb_load_tweets )
            buttonOpen.pack( side = LEFT )

            a_button = Button( a_frame , width=10, height=2, text = "Spacer" )
            a_button.config( command = self.controller.cb_gui_test_1 )
            a_button.pack( side = LEFT )

            buttonOpen = Button( a_frame , width=10, height=2, text = "Define\nWords" )
            buttonOpen.config( command = self.controller.cb_define_words )
            buttonOpen.pack( side = LEFT )

            buttonOpen = Button( a_frame , width=10, height=2, text = "Load\nWords" )
            buttonOpen.config( command = self.controller.cb_load_words )
            buttonOpen.pack( side = LEFT )

            buttonOpen = Button( a_frame , width=10, height=2, text = "Rank\nWords" )
            buttonOpen.config( command = self.controller.cb_rank_words )
            buttonOpen.pack( side = LEFT )

            # a_button = Button( a_frame , width=10, height=2, text = "Spacer" )
            # a_button.config( command = self.controller.cb_gui_test_1 )
            # a_button.pack( side = LEFT )

            # buttonOpen = Button( a_frame , width=10, height=2, text = "Check Select\nCWords" )
            # buttonOpen.config( command = self.controller.cb_check_concord_load )
            # buttonOpen.pack( side = LEFT )


            # buttonOpen = Button( a_frame , width=10, height=2, text = "Check Select\nTweets" )
            # buttonOpen.config( command = self.controller.cb_check_tweet_load )
            # buttonOpen.pack( side = LEFT )

            # a_button = Button( a_frame , width=10, height=2, text = "Define/load\n concord DB" )
            # a_button.config( command = self.controller.cb_define_db )
            # a_button.pack( side = LEFT )

            return a_frame

    # ------------------------------------------
    def _make_message_frame( self, parent,  ):
        """
        a frame with scrolling text area and controls for it
        -- there is a scrolled_text control, not currently using it --- why??
        """
        self.max_lines      = 500
        self.cb_scroll_var  = IntVar()  # for check box in reciev frame
        color   = "red"
        iframe  = Frame( parent, width=300, height=800, bg ="blue", relief=RAISED, borderwidth=1,  )

        bframe  = Frame( iframe, bg ="black", width=30  )
        # width=300, height=800, bg ="blue", relief=RAISED, borderwidth=1,  )
        bframe.grid( row=0, column=0, sticky = N + S )

        text0 = Text( iframe , width=50, height=20 )
        #text0.configure( bg = "red" )
#        self.save_redir = RedirectText( text0 )

        s_text0 = Scrollbar( iframe  )  # LEFT left
        s_text0.grid( row=0, column=2, sticky = N + S )

        s_text0.config( command=text0.yview )
        text0.config( yscrollcommand=s_text0.set )

        text0.grid( row=0, column=1, sticky = N + S + E + W  )

        self.rec_text  = text0

        iframe.grid_columnconfigure( 1, weight=1 )
        iframe.grid_rowconfigure(    0, weight=1 )

        # spacer
        s_frame = Frame( bframe, bg ="green", height=20 ) # width=30  )
        s_frame.grid( row=0, column=0  )
        row_ix   = 0

        # --------------------
        b_clear = Button( bframe , width=10, height=2, text = "Clear" )
        b_clear.bind( "<Button-1>", self.do_clear_button )
        b_clear.grid( row=row_ix, column=0   )
        row_ix   += 1

        #-----
        b_copy = Button( bframe , width=10, height=2, text = "copy all" )
        b_copy.bind( "<Button-1>", self.do_copy_button )
        b_copy.grid( row=row_ix, column=0   )
        row_ix += 1

        # -------------
        a_widget = Checkbutton( bframe,  width=7, height=2, text="A Scroll",
                                variable=self.cb_scroll_var,  command=self.do_auto_scroll )
        a_widget.grid( row=row_ix, column=0   )
        row_ix += 1

        self.cb_scroll_var.set( self.parameters.default_scroll )

        return iframe

    # ------------------------------------------
    def _make_label( self, a_frame, a_row, a_col, a_text, ):
        """
        make a label and auto place in grid, return new value for a_row, a_col for
        use next time.
        placement goes down a row then up to the next column, intended for
        pairs of labels ( more or less assumes we do not need ref to label )
        return tuple -- or by ref do not need to , test this in templates
        return label
        increment row col
        """
        a_row    += 1
        if a_row >= 2:
                a_row   =  0
                a_col   += 1

        a_label   = ( Label( a_frame, text = a_text, relief = RAISED,  )  )
        a_label.grid( row=a_row, column=a_col, sticky=E + W + N + S )    # sticky=W+E+N+S  )

        # set weight??
        return ( a_row, a_col, a_label )

# -----  functions mostly for controller to call  sets and gets ------------------------

    # ------------------------------------------
    def reset_select_values( self, ):
        """
        reset the select values
        """
        # maybe "Basic Tweet Select"
        a_list     = list(self.select_type_dict.keys())   # probably a method to get list from dropdown ??
        self.select_type.set(a_list[ 0 ] )
        # old could use # on list  self.select_type.set( AppGlobal.parameters.default_select_type  )

        self.output_format.set( AppGlobal.parameters.default_output_format  )

        self.a_word_search.set( AppGlobal.parameters.default_word   )

        self.tweet_type.set( "Tweet" )

        self.min_rank.set(  "Any" )

        self.max_count.set( "Any" )

        self.is_covid.set(  "Any" )

        self.word_type.set( "Any" )

        # need shading of date button -- actually set default by "pressing a button" !!

        self.time_end.set(       self.parameters.select_end_hr )
        self.cal_end.set_date(   self.parameters.select_end_date  )
        self.time_begin.set(     self.parameters.select_begin_hr )
        self.cal_begin.set_date( self.parameters.select_begin_date  )

    # ------------------------------------------
    def get_units( self, ):
        """
        get units for the graph as a string
        """
        return self.units_widget.get()

    # ------------------------------------------
    def get_word_type( self ):
        """
        what it says:
        return function to be run for the select
        """
        cb_text    = self.word_type.get()  # compact syntax ??
        return self.select_word_type_dict[cb_text]

    # ------------------------------------------
    def get_select_type( self ):
        """
        what it says:
        return function to be run for the select
        """
        cb_text    = self.select_type.get()  # compact syntax ??
        return self.select_type_dict[cb_text]

    # ------------------------------------------
    def get_select_type_text_function( self ):
        """
        what it says:
        return
        """
        cb_text    = self.select_type.get()  # compact syntax ??
        return ( cb_text, self.select_type_dict[cb_text] )

    # ------------------------------------------
    def get_max_count( self ):
        """
        what it says:
        return string for file_writers
        """
        cb_text    = self.max_count.get().replace( ",", "" )  # compact syntax ??
        #print( cb_text )
        if cb_text == "Any":
            return None
        else:
            return int( cb_text )

    # ------------------------------------------
    def get_min_rank( self ):
        """
        what it says:
        """
        cb_text    = self.min_rank.get().replace( ",", "" )
        if cb_text == "Any":
            return None
        else:
            return int( cb_text )

    # ------------------------------------------
    def get_tweet_type( self ):
        """
        what it says:
        """
        cb_text    = self.tweet_type.get()  # compact syntax ??
        return self.select_tweet_type_dict[cb_text]   # this is where adapt to butto

    # ------------------------------------------
    def get_output_format( self ):
        """
        what it says:
        """
        cb_text    = self.output_format.get( )
        return self.output_format_dict[cb_text]

    # ------------------------------------------
    def get_is_covid( self ):
        """
        what it says:
        return tuple ( text, sql_text, data )
        cut/paste text, sql_text, data   =  gui.get_is_covid()
        cut/paste    cb_text, cb_sql_text, cb_sql_value  =  self.gui.
        """
        return self.get_logic_values_combobox( self.is_covid )

    # ------------------------------------------
    def get_sort_order( self ):
        """
        what it says:
        return tuple ( text, sql_text, data )  -
        cut/paste text, sql_text, data   =  gui.get_is_covid()
        cut/paste    cb_text, cb_sql_text, cb_sql_value  =  self.gui.
        """
        pass
        #self.sort_order
        return   self.sort_order_dict[self.sort_order.get()]
        #return self.get_logic_values_combobox( self.is_covid )

    # ------------------------------------------
    def get_begin_end( self ):
        """
        what it says:
        get begin end times from the gui -- combine dates and hours
        may need to extend to date times
        return tuple (begin, end )  -- types may vary as I mess about
        """
        hour         = AppGlobal.dd_hours.index( self.time_begin.get() )
        time_begin   = datetime.time(hour = hour )
        hour         = AppGlobal.dd_hours.index( self.time_end.get() )
        time_end     = datetime.time(hour = hour )

#        my_date    = datetime.date.today()
        min_time      = datetime.time.min   # means midnight
        dt_begin      = datetime.datetime.combine(self.cal_begin.get_date(), time_begin )
        dt_end        = datetime.datetime.combine(self.cal_end.get_date(),   time_end )

        ts_begin      = dt_begin.timestamp()
        ts_end        = dt_end.timestamp()

#        a_datetime_begin     = datetime.datetime.fromtimestamp( ts_begin )
#        print( f"a_datetime_begin = { type(a_datetime_begin)}  {a_datetime_begin} " )
#
#        a_datetime_end     = datetime.datetime.fromtimestamp( ts_end )
#        print( f"a_datetime_end = { type(a_datetime_end)}  {a_datetime_end} " )

        return( ts_begin , ts_end  )

    #   -----  functions mostly for controller to call ------------------------
    def get_db_file_name( self, ):
        """
        what it says
        return a string
        """
        #bw_for_db.set_text     = AppGlobal.parameters.db_file_name
        # x = 1/0   # think should get directly from AppGlobal
        return( self.bw_for_db.get_text() )

    #   xxx-----  functions mostly for controller to call ------------------------
    def get_logic_values_combobox( self, cbox_widget ):
        """
        what it says
        decode a value from combobox for use in sql
        return:
            tuple (           )
        ?? not sure these are the correct values  ...convert to dict ??

        """
        cb_text    = cbox_widget.get( )
        if   cb_text == "Any":
             cb_sql_text        = ""
             cb_sql_value       = None
        elif cb_text == "Yes":
             cb_sql_text        = "is"
             cb_sql_value       = True
        else:                                 #cb_text == "No":
             cb_sql_text        = "isnot"
             cb_sql_value       = False

        return( cb_text, cb_sql_text, cb_sql_value )

    # ------------------------------------------
    def get_numeric_values_combobox( self, cbox_widget ):
        """
        what it says
        decode a value from combobox for use in sql
        return:
            tuple (           )
        ?? not sure these are the correct values
        """
        cb_text    = cbox_widget.get( )
        if   cb_text == "Any":
             cb_sql_text      = ""
             cb_sql_value     = None
        elif cb_text == "Yes":
             cb_sql_text      = "is"
             cb_sql_value     = True
        else:                                 #cb_text == "No":
             cb_sql_text      = "isnot"
             cb_sql_value     = False

        return( cb_text, cb_sql_text, cb_sql_value )

    # ------------------------------------------
    def display_info_string( self, data, update_now = False ):
        """
        add info prefix and new line suffix and show in message area
        data expected to be a string, but other stuff has str applied to it
        consider adding auto log
        """
        tab_char   = "\t"
        new_line   = "\n"
        sdata      = f">>{data}{new_line}...."
        self.display_string( sdata, update_now = update_now )
        return

    # ---------------------------------------
    def display_string( self, a_string, update_now = False ):
        """
        print to receive area, with scrolling and
        delete if there are too many lines in the area
        logging here !!  looks done test
        """
        if  AppGlobal.parameters.log_gui_text:
            AppGlobal.logger.log( AppGlobal.parameters.log_gui_text_level, a_string, )
             #AppGlobal.logger.info( a_string )     # not sure about this level

        self.rec_text.insert( END, a_string, )      # this is going wrong, why how
        try:
             numlines = int( self.rec_text.index( 'end - 1 line' ).split('.')[0] )
        except Exception as exception:
            self.logger.error( str( exception ) )
            print( exception )
            numlines = 0
        if numlines > self.max_lines:
            cut  = int( numlines/2  )   # lines to keep/remove py3 new make int
            # remove excess text
            self.rec_text.delete( 1.0, str( cut ) + ".0" )
#            msg     = "Delete from test area at " + str( cut )
#            self.logger.info( msg )

        if self.cb_scroll_var.get():   # so no function on box needed !! remove later
            self.rec_text.see( END )

        if update_now:
            self.root.update()
        return

    # ------------------------------------------
    def set_cursor( self, cursor_type ):
        """
        what it says
        arg:   now: "" or "wait"  else ??

        """
        self.root.config( cursor = cursor_type )
        self.root.update()

# ----- button actions - this may be too indirect
    # ------------------------------------------
    def do_restart_button( self, event):
        self.controller.restart()
        return

    # ------------------------------------------
    def do_clear_button( self, event):
        """
        for the clear button
        clear the receive area
        """
        self.rec_text.delete( 1.0, END )
        return

    # ------------------------------------------
    def do_copy_button( self, event ):
        """
        copy all text to the clipboard
        """
        data  = self.rec_text.get( 1.0, END )
        pyperclip.copy( data )
        return

    # ------------------------------------------
    def do_auto_scroll( self,  ):
        """
        still configured so needed, but will not work ??
        pass, not needed, place holder see
        """
        print( "do_auto_scroll fix !!" )
        # not going to involve controller
        pass
        return

# ---- Set datetimes ------------------------------------
    #-------------------------------------------
    def set_select_slier_datetimes( self, val  ):
        """
        what it says"

        """
        #print( val )

        big_delta     = datetime.timedelta( weeks = int(val) )
        plus_delta    = AppGlobal.parameters.slider_datetime_width

        dt_now         = datetime.datetime.now()
        dt_begin       = dt_now      + big_delta
        dt_end         = dt_begin    + plus_delta

        self.set_select_datetimes( dt_begin, dt_end )

    #-------------------------------------------
    def set_select_datetimes( self, dt_begin, dt_end ):
        """
        what it says
        currently hours to 0
        put values into gui --- make a sub for all sets
        """
        self.cal_begin.set_date( dt_begin.date() )
        self.time_begin.set( AppGlobal.dd_hours[0] )

        self.cal_end.set_date( dt_end.date() )
        self.time_end.set( AppGlobal.dd_hours[0] )

    #-------------------------------------------
    def set_select_this_month( self, my_widget ):
        """
        what it says
        put values into gui
        """
        self._set_active_date_widget( my_widget )
        #self._set_active_date_widget( self.set_select_this_month )  # make easier by having as arg ??
        # continue to simplify
        dt_now         = datetime.datetime.now()
        dt_begin       = dt_now + datetime.timedelta(weeks=-4)
        #date_begin     = dt_begin.date()

        dt_end         = dt_now + datetime.timedelta( days=1 )

        self.set_select_datetimes( dt_begin, dt_end )

    #-------------------------------------------
    def set_select_this_week( self, my_widget ):
        """
        what it says
        put values into gui
        """
        self._set_active_date_widget( my_widget )  # make easier by having as arg ??
        # continue to simplify
        dt_now         = datetime.datetime.now()
        dt_begin       = dt_now + datetime.timedelta(weeks=-1)

        dt_end         = dt_now + datetime.timedelta( days=1 )

        self.set_select_datetimes( dt_begin, dt_end )

    #-------------------------------------------
    def set_select_forever( self, my_widget ):
        """
        what it says
        put values into gui
        """
        self._set_active_date_widget( my_widget )

        dt_now         = datetime.datetime.now()
        #tt_now         = dt_now.timetuple( )
        dt_now         = datetime.datetime.now()

        # March 2006 by Jack Dorsey, Noah Glass, Biz Ston
        self.cal_begin.set_date( datetime.date( 2006,3, 1 ) )
        self.time_begin.set( AppGlobal.dd_hours[0] )

        # set to begin tomorrow, end today
        date_end     =  ( dt_now + datetime.timedelta( days = 1 ) ).date()  #
        self.cal_end.set_date( date_end )
        self.time_end.set( AppGlobal.dd_hours[0] )

    #-------------------------------------------
    def set_select_today( self, my_widget ):
        """
        what it says
        put values into gui
        """
#        print( "db_select_today" )
        #self._set_active_date_widget( self.          )
        self._set_active_date_widget( my_widget )

        dt_now         = datetime.datetime.now()
        #tt_now         = dt_now.timetuple( )
        dt_now         = datetime.datetime.now()

        date_begin     =  dt_now.date()  # today
        self.cal_begin.set_date( date_begin )
        self.time_begin.set( AppGlobal.dd_hours[0] )

        # set to begin tomorrow, end today
        date_end     =  ( dt_now + datetime.timedelta( days=1 ) ).date()
        self.cal_end.set_date( date_end )
        self.time_end.set( AppGlobal.dd_hours[0] )

    # ---------------  end of button actions
    # ------------------------------------------
    def run( self,  ):
        """
        run the gui

        """
        # move from controller to decouple type of gui
        self.gui_running        = True
#        self.root.after( self.parameters.gt_delta_t, self.controller.polling )
        self.root.mainloop()
        self.gui_running        = False

    # ------------------------------------------
    def close( self, ):
        if self.gui_running:
             self.root.destroy()
        else:
            pass

# ------------------------------------------
class ComboboxDecodexxx( ttk.Combobox ):
    """
    ?? some sort of idea, think junk
    lrow   += 1
        a_list  = list(self.sort_order_dict.keys())
        a_widget   =  ttk.Combobox( a_frame, values = a_list,  state='readonly')
        a_widget.grid( row = lrow, column = lcol, rowspan = 1, sticky=E + W + N + S )
        a_widget.set( a_list[0] )
        self.sort_order = a_widget
        lrow   += -1
    """

    # ------------------------------------------
    def __init__(self, parent ):
        """
                Arguments:
            consider additions
        """
        pass
        #super( BrowseWidget, self ).__init__( parent, width=60, height=20, bg ="red")
        super(  ).__init__( parent, width=60, height=20, bg ="red")
        self.label_1      = Label( self, text="Input File: ").grid(row=1, column=0)


    # ------------------------------------------
    def foo(self, ) :
        pass


# -----------------------------------------
class FileBrowseWidget( Frame ):
    """
    let user pick a file name on their computer
    not sure why making it into a widget is a good idea but here goes
    this is a widget that both holds a filename
    and lets you browse to a file
    how is it different from just a couple of widgets
    in your frame ... more reusable ?
    better looking or what
    see graph_smart_plug gui for a use

    right now linking to app global,
    this is really bad, should have a way to control at runtime
    """
    def __init__(self, parent ):
        """
        what it says
        """
        #super( BrowseWidget, self ).__init__( parent, width=60, height=20, bg ="red")
        super(  ).__init__( parent, width=60, height=20, bg ="red")
        self.label_1      = Label( self, text="Input File: ").grid(row=1, column=0)

        self.a_string_var = StringVar()

        self.entry_1      = Entry( self , width=100,   text = "bound", textvariable = self.a_string_var )
        self.entry_1.grid( row=1, column=1 )

        self.button_2 = Button( self, text="Browse...", command = self.browse )
        self.button_2.grid( row=1, column=3 )

    # ------------------------------------------
    def browse( self ):
        """
        browse for a file name
        return full path or "" if no file chosen

        from tkinter import filedialog
        from tkinter import *

        root = Tk()
        root.filename =  filedialog.askopenfilename( initialdir = "/",
                                            title = "Select file",
                                            filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        print (root.filename)
        or use asksaveasfilename
        filedialog.asksaveasfile
        import tkinter.filedialog
        --  have not found docs ... do an ex_ file
        tkinter.filedialog.asksaveasfilename()
        tkinter.filedialog.asksaveasfile()
        tkinter.filedialog.askopenfilename()
        tkinter.filedialog.askopenfile()
        tkinter.filedialog.askdirectory()
        tkinter.filedialog.askopenfilenames()
        tkinter.filedialog.askopenfiles()

        """
        Tk().withdraw()
        #self.root.withdraw() # not part of gui so out of scope !! would it be better to get a gui reference
#        filename     = asksaveasfile(  initialdir   = "./",
#                                         title        = "Select file for db",
#                                         filetypes    = (("database files","*.db"),("all files","*.*")))

        filename     = askopenfilename(  initialdir   = "./",
                                         title        = "Input file",
                                         filetypes    = (("text files","*.txt"), ("csv","*.csv"), ("all files","*.*")))
        if filename == "":
            return

        self.set_text( filename )
        #print( f"get_text = {self.get_text()}", flush = True )

    # ------------------------------------------
    def set_text( self, a_string ):
        """
        get the text from the entry
        """
        self.a_string_var.set( a_string )

    # ------------------------------------------
    def get_text( self, ):
        """
        get the text from the entry -- this is how to get db name at all times
        """
        a_string   =  self.a_string_var.get(  )
        return( a_string )

# =======================================

# --------------------------------------
if __name__ == '__main__':
        """
        run the app
        """
        import tweet_app
        a_app = tweet_app.TweetApp(  )

# ===================== eof ==================






