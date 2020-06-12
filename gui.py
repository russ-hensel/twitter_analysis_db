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
import select_manager

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

        #------ drop down dicts ( integrate into a class ?? )

        # use constructor name
        self.select_type_dict     =  {  # connot lay out in columns easily if font not proportional
                                       "Tweets ( tweets ) - 01":           select_manager.SM_Select_01,
                                       "Concordance Word Count ( concord:tweets ) - 02":  select_manager.SM_Select_02,
                                       "Three Way Join; Full Tweet Text -              03": select_manager.SM_Select_03,
                                       "Experimental Select - 04": select_manager.SM_Select_04,
                                       "Experimental Tweet Select -                    05": select_manager.SM_Select_05,
                                       "Word rank average - ( words:concord:tweets ) - 06": select_manager.SM_Select_06,
                                       "Select Words Like ( words )  07": select_manager.SM_Select_07,
                                       "Concordance with Tweet ( concord:tweets ) - X1": select_manager.SM_Select_X1,
                                       }

        self.select_word_type_dict  =  { "Any":           None,
                                         "Regular":       1,
                                         "Hashtag":       3,
                                         "Url":           2,
                                         "@...":          4,
                                         "Num...":        5,
                                         }

        self.decode_word_type_dict      = dict(map(reversed, self.select_word_type_dict.items()))  # invert the dict above

        self.select_tweet_type_dict     = {    "Any":              None,
                                               "ReTweet":          "retweet",
                                               "Tweet":            "tweet",
                                          }

        self.output_format_dict         = {    "text":      "txt",
                                                "csv":      "csv",
                                                "yaml":     "yaml",
                                                "html":     "html",
                                                # "sql":    "sql",
                                                "msg":      "msg"
                                          }

        # some seem to be litterally what you sort on other key words....decide ... need one for_my count??
        # !! I may have broken some by using full columnname
        self.sort_order_dict            = {    "Default":              "default",
                                                "Date":                 "tweets.tweet_datetime",
                                                "Date, Tweet Type":     "tweets.tweet_datetime, tweets.tweet_type",
                                                "Tweet Type, Date":     "tweets.tweet_type, tweets.tweet_datetime",
                                                "Word":        "word",
                                                "Word Count":  "words.word_count",
                                                "Word Rank":   "words.word_rank" }

        self.dd_zero              = [ "data_begin", "data_end",  "db_sql_begin",  "db_sql_end"  ]

        self.dd_units             = [ "seconds", "minutes", "hours", "days" ]

        self.dt_widgets           = []

        #------ constants for controlling layout and look  ------
        self.button_width         = 6

        self.button_padx          = "2m"
        self.button_pady          = "1m"

        self.btn_color            = self.parameters.btn_color
        self.bkg_color            = self.parameters.bkg_color

        # get widget names into existance
        #widgets    = [ self.tweets_word_widget, self.is_covid,  self.tweet_type, self.word_type ]
        self.tweets_word_widget   = None    # need to define now so....
        self.is_covid             = None    # need to define now so....
        self.tweet_type           = None    # need to define now so....
        self.word_type            = None    # need to define now so....

        # instead of above lets try
        self.select_widget_list   = []      # and controls will add themselves

        self.root.grid_columnconfigure( 0, weight=1 ) # final missing bit of magic
#        self.root.grid_rowconfigure(    0, weight=1 )
        self._master_frame_maker( )

# ------ frame building helpers  ------------------------
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
    def _set_active_date_widget( self, a_widget, ):
        """
        indicate the last active date widget used, detail in flux
        change to loop over list of date widgets
        """
        #rint( "_set_active_date_widget" )
        for i_widget in self.dt_widgets:
            #rint( f"widgets: {a_widget} == ? {i_widget}")
            if i_widget == a_widget:
                #rint( "_set_active_date_widget   this button" )  # we are not getting this
                i_widget.configure( background = self.parameters.bn_color_active )
            else:
                i_widget.configure( background = self.parameters.bn_color )

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

        # set weight seems not to be needed ??
        return ( a_row, a_col, a_label )

# ------ frame building methods  ---------  should be from top to bottom on the window

    # ------------------------------------------
    def _master_frame_maker( self,  ):
        """
        make a frame for generic system level functions  .....
        Return:  a frame with the widgets placed in it
        buttons, mostly  ?? fix name
        """
        next_frame                = 0      # index of frames and position row for frames

        a_frame = self._make_button_frame( self.root,  )
        a_frame.grid(row=next_frame, column=0, sticky=E + W + N)
        next_frame += 1

        a_frame  = self._make_other_select_frame( self.root,  )
        a_frame.grid( row=next_frame, column=0, sticky = E + W + N + S )   # + N + S  )
        next_frame += 1

        a_frame  = self._make_select_datetime_frame( self.root,  )
        a_frame.grid( row=next_frame, column=0, sticky = E + W + N + S )   # + N + S  )
        next_frame += 1

        a_frame  = self._make_select_values_frame( self.root,  )
        a_frame.grid( row=next_frame, column=0, sticky = E + W + N + S )   # + N + S  )
        next_frame += 1

        a_frame  = self._make_select_values_frame_2( self.root,  )
        a_frame.grid( row=next_frame, column=0, sticky = E + W + N + S )   # + N + S  )
        next_frame += 1

        if AppGlobal.parameters.show_db_def:
            a_frame = self._make_load_frame( self.root,  )
            a_frame.grid(row=next_frame, column=0, sticky=E + W + N)
            next_frame += 1

        a_frame = self._make_message_frame( self.root,  )
        a_frame.grid(row=next_frame, column=0, sticky=E + W + N + S)
        next_frame += 1

        self.root.grid_columnconfigure( 0, weight=1 )
        self.root.grid_rowconfigure(    0, weight=0 )
        self.root.grid_rowconfigure( ( next_frame - 1 ), weight=1 )
        self.reset_select_values()

    # ------------------------------------------
    def _make_button_frame( self, parent, ):
            """
            make a frame for generic system level functions  .....
            Return:  a frame with the widgets placed in it
            buttons, mostly  ?? fix name
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

            # --- help
            a_button = Button( a_frame , width=10, height=2, text = "Help" )
            a_button.config( command = self.controller.os_open_helpfile )
            a_button.pack( side = LEFT )

            # --- about
            a_button = Button( a_frame , width=10, height=2, text = "About" )
            a_button.config( command = self.controller.cb_about )
            a_button.pack( side = LEFT )

            # --- test  -- comment out when not testing
            a_button = Button( a_frame , width=10, height=2, text = "Test" )
            a_button.config( command = self.cb_test )
            a_button.pack( side = LEFT )

            return a_frame

    # ------------------------------------------
    def _make_other_select_frame( self, parent, ):
        """
        this is the frame that kicks off the select and
        specified general features of the select
        Return:  a frame with the widgets placed in it
        """
        a_frame  = Frame( parent, width=600, height=200,
                          bg = self.bkg_color, relief=RAISED, borderwidth=1 )

        lrow   =  0
        lcol   =  -1

        # ----- run select
        lcol   += 1
        a_widget = Label( a_frame , width=10, height=2, text = "General\nSelect:" )
        #a_widget.config( command = self.controller.cb_xxxx)
        a_widget.pack( side = LEFT )
        a_widget.grid( row = lrow, column = lcol, rowspan = 2, sticky=E + W + N + S )
        lcol   += 1

        # ----- select type
        a_widget   = ( Label( a_frame, text = "Select Type:", width = 40, height=2, relief = RAISED,  )  )
        a_widget.grid( row = lrow, column = lcol, columnspan = 3,  sticky = E + W + N + S )
        lrow   += 1

        a_list     = list(self.select_type_dict.keys())
        a_widget   =  ttk.Combobox( a_frame,
                                    values = a_list,
                                    height = 20, state = 'readonly')

        a_widget.bind("<<ComboboxSelected>>", self.controller.cb_change_select_type  )

        a_widget.grid( row = lrow, column = lcol, columnspan = 3, rowspan = 1, sticky=E + W + N + S )
        #a_widget.set( AppGlobal.parameters.default_output_format )
        a_widget.set( a_list[1] )    # default not in parms ??
        self.select_type  = a_widget
        lrow   += -1
        lcol   += 3 # see above

        a_widget = Button( a_frame , width = 10, height=2, text = "About It" )
        a_widget.config( command = self.controller.cb_about_select )
        a_widget.grid( row = lrow, column = lcol, rowspan = 2, sticky=E + W + N + S )

        lcol   += 1
        a_widget = Button( a_frame , width=10, height=2, text = "Run It" )
        a_widget.config( command = self.controller.cb_run_select )
        a_widget.grid( row = lrow, column = lcol, rowspan = 2, sticky=E + W + N + S )
        lcol   += 1

        # ---------------
        a_widget   = ( Label( a_frame, text = "Other Select\nInfo:", height=2, relief = RAISED,  )  )
        a_widget.grid( row = lrow, column = lcol, rowspan = 2, sticky=E + W + N + S )
        lcol   += 1

        # ----- sort order  -- !! why not span
        a_widget   = ( Label( a_frame, text = "Sort", relief = RAISED,  )  )
        a_widget.grid( row = lrow, column = lcol, columnspan = 3, sticky = E + W + N + S )

        a_list     = list(self.sort_order_dict.keys())
        a_widget   =  ttk.Combobox( a_frame, values = a_list,  state='readonly')
        a_widget.grid( row = lrow + 1, column = lcol, rowspan = 1, columnspan = 3,  sticky = E + W + N + S )
        a_widget.set( a_list[0] )
        self.sort_order = a_widget
        lcol   += 3

        # ----- output format
        a_widget   = ( Label( a_frame, text = "Output Format:", height = 2, relief = RAISED,  )  )
        a_widget.grid( row = lrow, column = lcol,  sticky = E + W + N + S )

        a_widget   =  ttk.Combobox( a_frame,
                                values = list(self.output_format_dict.keys()),
                                height = 10,  state='readonly')
        a_widget.grid( row = lrow + 1, column = lcol, rowspan = 1, sticky = E + W + N + S )
        self.output_format  = a_widget

        lcol   += 1

        # ----- output append
        a_widget   = ( Label( a_frame, text = "Append to Output:", height = 2, relief = RAISED,  )  )
        a_widget.grid( row = lrow, column = lcol,  sticky = E + W + N + S )

        a_widget   =  ttk.Combobox( a_frame,
                                values = [ "No Append", "Append" ],
                                height = 10,  state='readonly')
        a_widget.grid( row = lrow + 1, column = lcol, rowspan = 1, sticky = E + W + N + S )
        a_widget.set( "No Append" )
        self.output_append_widget  = a_widget
        lcol   += 1
        # zz

        # ----- reset
        a_widget = Button( a_frame , width = 10, height = 4, text = "Turn Date\nSlider Mode\nOn" )
        a_widget.config( command = self.controller.toggle_ds_mode )
        # self._set_lambda_callback( a_widget, self.set_select_this_month )
        a_widget.grid( row = lrow, column = lcol,  rowspan = 2, sticky=E + W + N + S )
        self.widget_slider   = a_widget
        lcol   += 1

        return a_frame

    # ------------------------------------------
    def _make_select_datetime_frame( self, parent, ):
        """
        make value frame for selects values that control data selected -- input from users
        reset_select_values -- for defaults not here called at end
        Return:  a frame with the widgets placed in it
        """
        # msg   = f"_make_select_datetime_frame{''}"
        #rint( msg )
        a_frame  = Frame( parent, width=600, height=200,
                          bg = self.bkg_color, relief=RAISED, borderwidth=1 )

        lrow   =  0
        lcol   =  0

        # some spacers might be nice -- may put back as we play with the look
#        a_spacer  = Frame( a_frame, width=60, height=60, bg ="green", relief=RAISED, borderwidth=1 )
#        a_spacer.grid( row = 0, column = lcol, sticky = E + W + N + S, rowspan = 2 )
        # ----------------Label band of buttons
        lcol   += 1

        # a_widget = Label( a_frame , width=10, height=2, text = "Selection\nCriteria:" )
        # #self._set_lambda_callback( a_widget, self.set_select_this_week )
        # a_widget.grid( row = lrow, column = lcol, rowspan = 2, columnspan = 1, sticky=E + W + N + S )
        # lcol   += 1

        a_widget = Label( a_frame , width=10, height=2, text = "Date Selection:\n(tweets)" )
        #self._set_lambda_callback( a_widget, self.set_select_this_week )
        a_widget.grid( row = lrow, column = lcol, rowspan = 2, columnspan = 1, sticky=E + W + N + S )
        lcol   += 1

        # ---------------- buttons for datetimes !! next two need appropriate functions not ones in place

        # ----- years ago today
        a_widget = Button( a_frame , width=10, height=2, text = "1 Year Ago\nToday" )
        self._set_lambda_callback( a_widget, self.set_1_year_ago  )
        #a_widget.config( command = self.set_1_year_ago )
        a_widget.grid( row = lrow, column = lcol, rowspan = 1, sticky=E + W + N + S )
        self.dt_widgets.append( a_widget )

        a_widget = Button( a_frame , width=10, height=2, text = "2 Years Ago\nToday" )
        self._set_lambda_callback( a_widget, self.set_2_year_ago  )
        a_widget.grid( row = lrow +1, column = lcol, rowspan = 1, sticky=E + W + N + S )
        self.dt_widgets.append( a_widget )
        lcol   += 1

        # ----- years ago today
        a_widget = Button( a_frame , width=10, height=2, text = "3 Year Ago\nToday" )
        self._set_lambda_callback( a_widget, self.set_3_year_ago )
        a_widget.grid( row = lrow, column = lcol, rowspan = 1, sticky=E + W + N + S )
        self.dt_widgets.append( a_widget )

        a_widget = Button( a_frame , width=10, height=2, text = "4 Years Ago\nToday" )
        self._set_lambda_callback( a_widget, self.set_4_year_ago )
        a_widget.grid( row = lrow + 1, column = lcol, rowspan = 1, sticky=E + W + N + S )
        self.dt_widgets.append( a_widget )   # !! chdek all widgets some seem to be missing
        lcol   += 1

        # ----- both dates back
        a_widget = Button( a_frame , width=10, height=2, text = "Dates Back\nA Week" )
        self._set_lambda_callback( a_widget, self.set_dates_back_a_week )
        a_widget.grid( row = lrow, column = lcol, rowspan = 1, sticky=E + W + N + S )
        self.dt_widgets.append( a_widget )

        a_widget = Button( a_frame , width=10, height=2, text = "Dates Back\nA Month" )
        self._set_lambda_callback( a_widget, self.set_dates_back_a_month )
        a_widget.grid( row = lrow + 1, column = lcol, rowspan = 1, sticky=E + W + N + S )
        self.dt_widgets.append( a_widget )
        lcol   += 1

        # ---- this day and week
        a_widget = Button( a_frame , width = 10, height = 2, text = "Set Today" )
        self._set_lambda_callback( a_widget, self.set_select_today )    # may blow out silently if function does not exist
        a_widget.grid( row = lrow, column = lcol, rowspan = 1, sticky=E + W + N + S )
        self.dt_widgets.append( a_widget )

        a_widget = Button( a_frame , width=10, height=2, text = "Set This\n Week" )
        self._set_lambda_callback( a_widget, self.set_select_this_week )
        a_widget.grid( row = lrow +1, column = lcol, rowspan = 1, sticky=E + W + N + S )
        self.dt_widgets.append( a_widget )
        lcol   += 1    # comment out for row 2 add 1 in row below

        a_widget = Button( a_frame , width=10, height=2, text = "Set This\n Month" )
        self._set_lambda_callback( a_widget, self.set_select_this_month )
        a_widget.grid( row = lrow, column = lcol, rowspan = 1, sticky = E + W + N + S )

        a_widget = Button( a_frame , width=10, height=2, text = "Set\nForever" )
        self._set_lambda_callback( a_widget, self.set_select_forever )
        a_widget.grid( row = lrow + 1, column = lcol, rowspan = 1, sticky = E + W + N + S )
        #lrow    = 0
        lcol   += 1    # comment out for row 2 add 1 in row below

        # ------ date slider
        a_widget =  Label( a_frame, text = "Set Weeks\nin Past", relief = RAISED,  )
        a_widget.grid( row = lrow, column = lcol, sticky = E + W + N + S )    # sticky=W+E+N+S  )

        #lcol   += 1
        a_widget = Scale( a_frame, orient ='horizontal', from_= -52, to= 0, command = self.set_select_slier_datetimes )
        #a_widget.config( command = self.set_select_forever )
        a_widget.grid( row = lrow + 1, column = lcol, rowspan = 1, sticky =E + W + N + S )
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
        cal     = DateEntry( a_frame, width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=2010,    bordercolor = "red",     )

        cal.grid( row=lrow, column=lcol, sticky=E + W + N + S )
        cal.configure( date_pattern = "yyyy/mm/dd" )
        # cal.set_date( self.parameters.select_begin_date  )
        self.cal_begin = cal

        # msg   = f"_make_select_datetime_frame self.cal_begin{ self.cal_begin }"
        # print( msg )

        cal     = DateEntry( a_frame, width=12, background='darkblue',
                             foreground='white',
                             borderwidth=2, year=2010,    bordercolor = "red",     )
        cal.grid( row = lrow +1, column=lcol, sticky=E + W + N + S )
        cal.configure( date_pattern = "yyyy/mm/dd" )
        # cal.set_date( self.parameters.select_end_date  )
        self.cal_end     = cal

        #-------------------- drop downs for hours
        lrow    = 0
        lcol    += 1

        a_widget   =  ttk.Combobox( a_frame, values = AppGlobal.dd_hours, state='readonly')
        a_widget.grid( row = lrow, column = lcol,
                       rowspan = 1, sticky=E + W + N + S )
        a_widget.set( self.parameters.select_begin_hr )
        self.time_begin  = a_widget

        a_widget   =  ttk.Combobox( a_frame, values=AppGlobal.dd_hours, state='readonly')
        a_widget.grid( row = lrow + 1, column = lcol, rowspan = 1, sticky=E + W + N + S )
        self.time_end  = a_widget

        #msg   = f"_make_select_datetime_frame returning frame self.cal_begin{ self.cal_begin }"
        #rint( msg )

        return  a_frame

    # ------------------------------------------
    def _make_select_values_frame( self, parent, ):
        """
        make value frame for selects values that control data selected -- input from users
        reset_select_values -- for defaults not here called at end
        Return: a frame with the widgets in it
        Return:  a frame with the widgets placed in it
        """
        a_frame  = Frame( parent, width=600, height=200,
                          bg = self.bkg_color, relief=RAISED, borderwidth=1 )

        lrow   =  0
        lcol   =  0

        # some spacers might be nice -- may put back as we play with the look
#        a_spacer  = Frame( a_frame, width=60, height=60, bg ="green", relief=RAISED, borderwidth=1 )
#        a_spacer.grid( row = 0, column = lcol, sticky = E + W + N + S, rowspan = 2 )

        # ----- start band of buttons
        lcol   += 1

        a_widget = Label( a_frame , width=10, height=2, text = "Selection\nCriteria:" )
        #self._set_lambda_callback( a_widget, self.set_select_this_week )
        a_widget.grid( row = lrow, column = lcol, rowspan = 2, columnspan = 1, sticky=E + W + N + S )
        lcol   += 1

        # ----- is_covid tweets
        a_widget   = ( Label( a_frame, text = "Is Covid:\n(tweets)", relief = RAISED,  )  )
        a_widget.grid( row = lrow, column = lcol,  sticky=E + W + N + S )

        a_widget   =  ttk.Combobox( a_frame, values=[ "Any", "Yes", "No",  ], state='readonly')  # move to dict approach ?
        a_widget.grid( row = lrow + 1, column = lcol, rowspan = 1, sticky=E + W + N + S )
        self.select_widget_list.append( a_widget )
        self.is_covid               = a_widget   # phase out
        self.tweets_is_covid_widget = a_widget
        #lrow   += -1
        lcol  += 1

        # ------ tweets_word !! still need to do default reset
        a_widget   = ( Label( a_frame, text = "Word Like:\n(tweets)", relief = RAISED,  )  )
        a_widget.grid( row = lrow, column = lcol,  sticky=E + W + N + S )

        self.tweets_word_var      = StringVar()
        a_widget               = ttk.Combobox( a_frame, values = self.parameters.combo_box_words, textvariable = self.tweets_word_var )
        a_widget.configure(  height = 50 )   # height of what --- dropdown size on down arrow
        a_widget.grid( row = lrow + 1, column = lcol,  sticky = E + W + N + S )
        self.tweets_word_widget    = a_widget
        self.select_widget_list.append( a_widget )
        lcol   += 1

        # ----- tweets_type tweets
        a_widget   = ( Label( a_frame, text = "Tweet Type:\n(tweets)", relief = RAISED,  )  )
        a_widget.grid( row = lrow, column = lcol,  sticky=E + W + N + S )
        lrow   += 1

        a_widget   =  ttk.Combobox( a_frame, values=[ "Any", "ReTweet", "Tweet",  ], state='readonly')
        a_widget.grid( row = lrow, column = lcol, rowspan = 1, sticky=E + W + N + S )
        a_widget.set( "Any" )
        self.select_widget_list.append( a_widget )
        self.tweet_type               = a_widget
        self.tweets_tweet_type_widget = a_widget
        lrow   += -1
        lcol    += 3   # why 3

        # ----- min_time_of_day
        a_widget   = ( Label( a_frame, text = "Min Time of:\nDay (tweets)", relief = RAISED,  )  )
        a_widget.grid( row = lrow, column = lcol,  sticky=E + W + N + S )

        a_widget   =  ttk.Combobox( a_frame, values=[ "Any", "00:00", "01:00", "02:00", "03:00", "04:00", "05:00",
                                                             "06:00", "07:00", "08:00", "09:00",
                                                             "10:00", "11:00", "12:00", "13:00", "14:00", "15:00",
                                                             "16:00", "17:00", "18:00", "19:00",
                                                             "20:00", "21:00", "22:00", "23:00", "24:00",
                                                          ], state='readonly')
        a_widget.grid( row = lrow + 1, column = lcol, rowspan = 1, sticky = E + W + N + S )
        a_widget.set( "Any" )
        self.select_widget_list.append( a_widget )
        self.min_rank               = a_widget
        self.tod_min_widget  = a_widget
        lcol   += 1

        # ----- concord_word_type  concord !! got get and reset
        a_widget   = ( Label( a_frame, text = "Word Type:\n(concord)", relief = RAISED,  )  )
        a_widget.grid( row = lrow, column = lcol,  sticky=E + W + N + S )
        lrow   += 1

        a_list     = list( self.select_word_type_dict.keys())  #  ?? convert iter to list?
        a_widget   =  ttk.Combobox( a_frame, values = a_list, state='readonly')
        a_widget.grid( row = lrow, column = lcol, rowspan = 1, sticky=E + W + N + S )
        a_widget.set( "Any" )
        self.select_widget_list.append( a_widget )
        self.word_type                = a_widget  # phase out
        self.concord_word_type_widget = a_widget
        lcol   += 1
        lrow    = 0

        # ----- is_ascii concord
        a_widget   = ( Label( a_frame, text = "Is Ascii:\n(concord)", relief = RAISED,  )  )
        a_widget.grid( row = lrow, column = lcol,  sticky=E + W + N + S )
        lrow   += 1

        a_widget   =  ttk.Combobox( a_frame, values=[ "Any", "Yes", "No",  ], state='readonly')
        a_widget.grid( row = lrow, column = lcol, rowspan = 1, sticky=E + W + N + S )
        self.is_ascii  = a_widget
        self.select_widget_list.append( a_widget )
        lrow  += -1
        lcol  += 1

        # ------ concord_word !! still need to do default reset
        lcol   += 3
        a_widget   = ( Label( a_frame, text = "Word Search:\n(concord %)", relief = RAISED,  )  )
        a_widget.grid( row = lrow, column = lcol,  sticky=E + W + N + S )
        lrow   += 1

        self.concord_word_var      = StringVar()
        a_widget               = ttk.Combobox( a_frame, values = self.parameters.combo_box_words, textvariable = self.concord_word_var )
        a_widget.configure(  height = 50 )   # height of what --- dropdown size on down arrow
        a_widget.grid( row = lrow, column = lcol,  sticky = E + W + N + S )

        self.select_widget_list.append( a_widget )
        self.concord_word_widget   = a_widget
        lrow   += -1
        lcol   += 3   # think +1 would do it , check


        # ----- reset
        a_widget = Button( a_frame , width=10, height=4, text = "Reset\nCriteria" )
        a_widget.config( command = self.reset_select_values )
        a_widget.grid( row = lrow, column = lcol,  rowspan = 2, sticky=E + W + N + S )
        lrow   += -1

        #self.reset_select_values()

        return  a_frame

    # ------------------------------------------
    def _make_select_values_frame_2( self, parent, ):
        """
        make value frame for selects values that control data selected -- input from users
        reset_select_values -- for defaults not here called at end
        Return: a frame with the widgets in it
        Return:  a frame with the widgets placed in it
        """
        a_frame  = Frame( parent, width=600, height=200,
                          bg = self.bkg_color, relief=RAISED, borderwidth=1 )

        lrow   =  0
        lcol   =  0

        # some spacers might be nice -- may put back as we play with the look
#        a_spacer  = Frame( a_frame, width=60, height=60, bg ="green", relief=RAISED, borderwidth=1 )
#        a_spacer.grid( row = 0, column = lcol, sticky = E + W + N + S, rowspan = 2 )

        # ----- start band of buttons
        lcol   += 1

        a_widget = Label( a_frame , width=10, height=2, text = "More\nCriteria:" )
        #self._set_lambda_callback( a_widget, self.set_select_this_week )
        a_widget.grid( row = lrow, column = lcol, rowspan = 2, columnspan = 1, sticky=E + W + N + S )
        lcol   += 1

        # ------ words_word
        a_widget   = ( Label( a_frame, text = "Word Like:\n(words)", relief = RAISED,  )  )
        a_widget.grid( row = lrow, column = lcol,  sticky=E + W + N + S )

        self.words_word_var    = StringVar()
        a_widget               = ttk.Combobox( a_frame, values = self.parameters.combo_box_words, textvariable = self.words_word_var )
        a_widget.configure(  height = 50 )
        a_widget.grid( row = lrow + 1, column = lcol,  sticky = E + W + N + S )
        self.select_widget_list.append( a_widget )
        self.words_word_widget = a_widget
        lcol   += 1

        # ----- min_rank words
        a_widget   = ( Label( a_frame, text = "Min Rank:\n(words)", relief = RAISED,  )  )
        a_widget.grid( row = lrow, column = lcol,  sticky=E + W + N + S )
        lrow   += 1

        a_widget   =  ttk.Combobox( a_frame, values=[ "Any", "100", "500", "1000", "2000", "5000", "10000", ], state='readonly')
        a_widget.grid( row = lrow, column = lcol, rowspan = 1, sticky = E + W + N + S )
        a_widget.set( "Any" )
        self.select_widget_list.append( a_widget )
        self.min_rank               = a_widget
        self.words_min_rank_widget  = a_widget
        lrow   += -1
        lcol   += 1

        # ----- words_null  !! can we embed the where in the control, with a new class ??
        a_widget   = ( Label( a_frame, text = "Word Null:\n(words)", relief = RAISED,  )  )
        a_widget.grid( row = lrow, column = lcol,  sticky=E + W + N + S )

        a_widget   =  ttk.Combobox( a_frame, values=[ "Any", "Yes", "No",  ], state='readonly')
        a_widget.grid( row = lrow + 1, column = lcol, rowspan = 1, sticky=E + W + N + S )
        a_widget.set( "Any" )
        self.select_widget_list.append( a_widget )
        self.words_word_null_widget  = a_widget
        lcol   += 1

        # ----- words_max_count words
        a_widget   = ( Label( a_frame, text = "Max Count:\n(words)", relief = RAISED,  )  )
        a_widget.grid( row = lrow, column = lcol,  sticky=E + W + N + S )

        a_widget   =  ttk.Combobox( a_frame, values=[ "Any", "100", "100,000",  ], state='readonly')
        a_widget.grid( row = lrow + 1, column = lcol, rowspan = 1, sticky=E + W + N + S )
        a_widget.set( "Any" )
        self.select_widget_list.append( a_widget )
        self.max_count               = a_widget
        self.words_max_count_widget  = a_widget
        lcol   += 1

        # ----- min_group_by_count
        a_widget   = ( Label( a_frame, text = "Min Group By:\nCount", relief = RAISED,  )  )
        a_widget.grid( row = lrow, column = lcol,  sticky=E + W + N + S )

        a_widget   =  ttk.Combobox( a_frame, values=[ "0", "100", "100", "100,000",  ], state='readonly')
        a_widget.grid( row = lrow + 1, column = lcol, rowspan = 1, sticky=E + W + N + S )
        a_widget.set( "0" )
        self.select_widget_list.append( a_widget )
        self.group_by_min_count_widget  = a_widget
        lcol   += 1

        # ----- reset
        a_widget = Button( a_frame , width=10, height=4, text = "Reset\nCriteria" )
        a_widget.config( command = self.reset_select_values )
        a_widget.grid( row = lrow, column = lcol,  rowspan = 2, sticky=E + W + N + S )
        lrow   += -1

        # self.reset_select_values()

        return  a_frame

    # ------------------------------------------
    def _make_load_frame( self, parent, ):
            """
            this frame for loading from input files
            make a frame in parent and return frame for placement by caller
            """
            a_frame  = Frame( parent, width=300, height=200,
                              bg = self.parameters.id_color, relief=RAISED, borderwidth=1 )

            a_widget = Label( a_frame , width=10, height=2, text = "Database\nTable Load:" )
            #buttonOpen.config( command = self.controller.cb_show_load_parms )
            a_widget.pack( side = LEFT )

            a_widget = Button( a_frame , width=10, height=2, text = "Show Load\nParameters" )
            a_widget.config( command = self.controller.cb_show_load_parms )
            a_widget.pack( side = LEFT )

            a_widget = Label( a_frame , width=10, height=2, text = "Spacer" )
            # a_widget.config( command = self.controller.cb_gui_test_1 )
            a_widget.pack( side = LEFT )

            a_widget = Button( a_frame , width=10, height=2, text = "Define Tweets\nConcord" )
            a_widget.config( command = self.controller.cb_define_tweets_concord )
            a_widget.pack( side = LEFT )

            a_widget = Button( a_frame , width=10, height=2, text = "Load Tweets\n(Concord)" )
            a_widget.config( command = self.controller.cb_load_tweets )
            a_widget.pack( side = LEFT )

            a_widget = Label( a_frame , width=10, height=2, text = "Spacer" )
            # a_widget.config( command = self.controller.cb_gui_test_1 )
            a_widget.pack( side = LEFT )

            a_widget = Button( a_frame , width=10, height=2, text = "Define\nWords" )
            a_widget.config( command = self.controller.cb_define_words )
            a_widget.pack( side = LEFT )

            a_widget = Button( a_frame , width=10, height=2, text = "Load\nWords" )
            a_widget.config( command = self.controller.cb_load_words )
            a_widget.pack( side = LEFT )

            a_widget = Button( a_frame , width=10, height=2, text = "Rank\nWords" )
            a_widget.config( command = self.controller.cb_rank_words )
            a_widget.pack( side = LEFT )

            return a_frame

    # ------------------------------------------
    def _make_message_frame( self, parent,  ):
        """
        a frame with scrolling text area and controls for it
        -- there is a scrolled_text control, not currently using it --- why??
        """
        self.max_lines      = 500
        self.cb_scroll_var  = IntVar()  # for check box in reciev frame
        color               = "red"

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

        #----- copy selection, moving to my new coding standards
        a_widget = Button( bframe , width=10, height=2, text = "Copy/Sel." )
        # a_widget.bind( "<Button-1>", self.do_copy_button )
        a_widget.config( command = self.cb_copy_selection )
        a_widget.grid( row=row_ix, column=0   )
        row_ix += 1

        #----- copy selection, moving to my new coding standards
        a_widget = Button( bframe , width=10, height=2, text = "Copy/All" )
        # a_widget.bind( "<Button-1>", self.do_copy_button )
        a_widget.config( command = self.cb_copy_all )
        a_widget.grid( row=row_ix, column=0   )
        row_ix += 1
        # #-----
        # b_temp = Button( bframe , width=10, height=2, text = self.BN_CP_SELECTION )
        # b_temp.bind( "<Button-1>", self.doButtonText )
        # b_temp.grid( row=row_ix, column=0   )
        # row_ix   += 1

        # -------------
        a_widget = Checkbutton( bframe,  width=7, height=2, text="A Scroll",
                                variable=self.cb_scroll_var,  command=self.do_auto_scroll )
        a_widget.grid( row=row_ix, column=0   )
        row_ix += 1

        self.cb_scroll_var.set( self.parameters.default_scroll )

        return iframe

   # ------------------------------------------
    def _make_input_frame( self, parent, ):
        """
        apparently dead
        is this still used ?? for what !!
        Return:  a frame with the widgets placed in it
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

        #self.a_word_search.set( AppGlobal.parameters.default_word   )

        self.tweet_type.set( "Tweet" )

        self.min_rank.set(  "Any" )

        self.max_count.set( "Any" )

        self.is_covid.set(  "Any" )

        self.is_ascii.set(  "Yes"  )

        self.word_type.set( "Any" )

        # need shading of date button -- actually set default by "pressing a button" !!

        self.time_end.set(       self.parameters.select_end_hr )
        self.cal_end.set_date(   self.parameters.select_end_date  )
        self.time_begin.set(     self.parameters.select_begin_hr )
        self.cal_begin.set_date( self.parameters.select_begin_date  )

    # ------------------------------------------
    def set_sort_order_dict( self, sort_order_dict ):
        """
        what it says
        gui.set_sort_order_dict( self.sort_order_dict )
        """
        a_widget               = self.sort_order
        self.sort_order_dict   = sort_order_dict
        a_list                 = list(self.sort_order_dict.keys())
        a_widget.configure( values = a_list, )
        a_widget.set( a_list[0] )

    # ------------------------------------------
    def configure_select_widgets( self, a_control_dict ):
        """
        deactivate all
        for dates separate function
        change name to disable  ?? think comment ng
        """
        for  key_widget, i_widget_tuple in a_control_dict.items():
             #rint( f"in configure_select_widgets {key_widget}: {i_widget_tuple}" )

             dd_list  = i_widget_tuple.dd_list
             if dd_list is not None:
                 key_widget.configure( values = dd_list )
             # need to set state after changing list values or state will be normal
             key_widget.configure( state = i_widget_tuple.state  )      # =Tk.DISABLED   = Tk.NORMAL   "readonly"

    # ------------------------------------------
    def deactivate_select_widgets( self,  ):
        """
        deactivate all
        special for dates list for rest ??
        change name to disable
        """
        #rint( "deactivate_select_widgets ")
        # need to pass in so can be defined after widgets are constructed
        #bn_color_inactive               = "dark gray"
        # widgets    = [ self.tweets_word_widget, self.is_covid,  self.tweet_type, self.word_type ]
        widgets    = self.select_widget_list
        for i_widget in widgets:
            #i_widget.configure( bn_color = bn_color )
            #rint( i_widget )
            i_widget.config( state = DISABLED )      # =Tk.DISABLED   = Tk.NORMAL ......

    # ------------------------------------------
    def set_date_widget_state_normal( self, state ):  #    Normal
        """
        what it says
        arg True for N else....
        """
        if state:
            set_to  = NORMAL
        else:
            set_to  = DISABLED

        for i_widget in self.dt_widgets:
            i_widget.config( state = set_to )

        # above not include the calenders so:
        self.cal_begin.config(  state = set_to )
        self.cal_end.config(    state = set_to )
        self.time_begin.config( state = set_to )
        self.time_end.config(   state = set_to )

# ----- gets ------------------------

    # ------------------------------------------
    def get_select_type( self ):
        """
        what it says:
        return function to be run for the select
        """
        cb_text    = self.select_type.get()  # compact syntax ??
        return self.select_type_dict[cb_text]

    # ------------------------------------------
    def get_select_type_constructor( self ):
        """
        what it says:
        return  tuple ( name of the select, constructor )
        """
        cb_text    = self.select_type.get()  # compact syntax ??
        return ( cb_text, self.select_type_dict[cb_text] )

    # ------------------------------------------
    def get_select_type_text_function( self ):
        """
        may be dead
        what it says:
        return
        """
        cb_text    = self.select_type.get()  # compact syntax ??
        return ( cb_text, self.select_type_dict[cb_text] )

    # -------------------- gets by table tweets ... concord   words
    # ------------------------------------------
    def get_begin_end( self ):
        """
        !! is all this stuff right do we go back and forth between controls -- think is ok check later
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
        # min_time      = datetime.time.min   # means midnight
        dt_begin      = datetime.datetime.combine(self.cal_begin.get_date(), time_begin )
        dt_end        = datetime.datetime.combine(self.cal_end.get_date(),   time_end )

        ts_begin      = dt_begin.timestamp()
        ts_end        = dt_end.timestamp()

        return( ts_begin , ts_end  )

    # ------------------------------------------
    def get_dt_begin_end( self ):
        """
        what it says:   zz
        get begin end times from the gui -- combine dates and hours into a datetime
        return tuple (begin, end )
        """
        hour         = AppGlobal.dd_hours.index( self.time_begin.get() )
        time_begin   = datetime.time( hour = hour )
        hour         = AppGlobal.dd_hours.index( self.time_end.get() )
        time_end     = datetime.time( hour = hour )

#        my_date    = datetime.date.today()
        # min_time      = datetime.time.min   # means midnight
        dt_begin      = datetime.datetime.combine( self.cal_begin.get_date(), time_begin )
        dt_end        = datetime.datetime.combine( self.cal_end.get_date(),   time_end )

        return( dt_begin , dt_end  )

    # ------------------------------------------
    def get_tweets_word_select( self ):
        """
        what it says:
        return function to be run for the select
        """
        ret = self.tweets_word_widget.get().strip()    # or the var
        return ret

    # ------------------------------------------
    def get_tweets_is_covid_select( self ):
        """
        what it says:
        return tuple ( text, sql_text, data )
        cut/paste text, sql_text, data   =  gui.get_is_covid()
        cut/paste    cb_text, cb_sql_text, cb_sql_value  =  self.gui.
        """
        # unpack done elsewhere
        #  _1, _2, tf  =  self.get_logic_values_combobox( self.is_covid )
        # return  tf
        return self.get_logic_values_combobox( self.is_covid )

    # ------------------------------------------
    def get_is_covid( self ):
        """
        return  True False, None ??

        """
        msg   =  f" self.get_tweets_is_covid_select()   {self.get_tweets_is_covid_select()}"
        #rint( msg )
        return self.get_tweets_is_covid_select()

    # ------------------------------------------
    def get_words_is_word_null_select( self ):
        """
        what it says:  zz
        return tuple ( text, sql_text, data )  !! change to dict approach
        cut/paste text, sql_text, data   =  gui.get_is_covid()
        cut/paste    cb_text, cb_sql_text, cb_sql_value  =  self.gui.
        """
        # unpack done elsewhere
        #  _1, _2, tf  =  self.get_logic_values_combobox( self.is_covid )
        # return  tf
        return self.get_logic_values_combobox( self.words_word_null_widget )


    # ------------------------------------------
    def get_output_append_select( self ):
        """
        what it says:
        return function to be run for the select
        """
        ret = self.output_append_widget.get()
        return ret

    # ------------------------------------------
    def get_tweets_tweet_type_select( self ):
        """
        what it says:
        """
        cb_text    = self.tweet_type.get()
        return self.select_tweet_type_dict[cb_text]

    # ------------------------------------------
    def get_tweet_type( self ):
        """
        what it says:
        """
        return self.get_tweets_tweet_type_select()

    # ------------------------------------------
    def get_concord_is_ascii_select( self ):
        """
        what it says:
        return tuple ( text, sql_text, data )
        cut/paste text, sql_text, data   =  gui.get_is_covid()
        cut/paste    cb_text, cb_sql_text, cb_sql_value  =  self.gui.
        """
        return self.get_logic_values_combobox( self.is_ascii )

    # ------------------------------------------
    def get_is_ascii( self ):
        """
        what it says:
        return tuple ( text, sql_text, data )
        cut/paste text, sql_text, data   =  gui.get_is_covid()
        cut/paste    cb_text, cb_sql_text, cb_sql_value  =  self.gui.
        """
        return self.get_concord_is_ascii_select()

    # ------------------------------------------
    def get_concord_word_type_select( self ):
        """
        what it says:
        return function to be run for the select
        """
        cb_text    = self.word_type.get()  # compact syntax ??
        return self.select_word_type_dict[cb_text]

    # ------------------------------------------
    def get_concord_word_select( self ):
        """
        what it says:
        return function to be run for the select
        """
        return self.concord_word_widget.get()

    # ------------------------------------------
    def get_word_type( self ):
        """
        what it says:
        return function to be run for the select --- looks like old funct forwarede to new
        """
        return self.get_concord_word_type_select(  )

    # ------------------------------------------
    def get_words_min_rank_select( self ):
        """
        what it says:
        """
        cb_text    = self.min_rank.get().replace( ",", "" )
        if cb_text == "Any":
            return None
        else:
            return int( cb_text )

    # ------------------------------------------
    def get_min_rank( self ):
        """
        what it says:
        """
        return self.get_words_min_rank_select()

    # ------------------------------------------
    def get_words_word_select( self ):
        """
        what it says:
        return function to be run for the select
        """
        ret = self.words_word_widget.get().strip()
        return ret

    # ------------------------------------------
    def get_words_max_count_select( self ):
        """
        what it says:
        return string for file_writers
        """
        cb_text    = self.max_count.get().replace( ",", "" )  # compact syntax ?? -- changing widget name??
        # msg        = f"cb_text for max_count {cb_text}"
        # #rint( cb_text )
        if cb_text == "Any":
            return None
        else:
            return int( cb_text )

    # ------------------------------------------
    def get_group_by_min_count( self ):
        """
        what it says:

        """
        cb_text    = self.group_by_min_count_widget.get().replace( ",", "" )
        if cb_text == "Any":
            return None
        else:
            return int( cb_text )

    # ------------------------------------------
    def get_max_countxxx( self ):
        """
        what it says:    for words.word_count
        return string for file_writers
        """
        self.get_words_max_count_select()

# ----------- end gets by table
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
    def get_output_format( self ):
        """
        what it says:
        """
        cb_text    = self.output_format.get( )
        return self.output_format_dict[cb_text]

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
        p rint to receive area, with scrolling and
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

# ----- button actions - some may be too indirect, so recode ?? low priority  may be too indirect
    # ------------------------------------------
    def cb_test( self, ):
        """
        for test button, but only if so configured, may go to controller instead
        """
        pass
        # widgets   = [ self.tweets_word_widget, self.is_covid,  self.tweet_type, self.word_type ]
        # # do we want to reset
        # self.deactivate_select_widgets( widgets )

        # a_select_manager   = select_manager.SM_Select_03()
        # a_select_manager.set_up_widgets()

    # ---------------------------------------
    def paste_string( self, a_string, update_now = False ):
        """
        will mess up uses copy paste -- could save and put back would loose formatting I thik
        will this get aroung unicode issues up pyperclip
        data  = self.rec_text.get( 1.0, END )
        pyperclip.copy( data )
        new_clip  = pyperclip.paste()
        looks like will not work can we try to put in a ctrl-v ??
        need to search  send keystroke to tk text control
        """
        pass

    # ------------------------------------------
    def set_cursor( self, cursor_type ):
        """
        what it says
        arg:   now: "" or "wait"  else ?? !! is this working do we need
        something more a repaint....

        """
        self.root.config( cursor = cursor_type )
        self.root.update()

    # ------------------------------------------
    def do_restart_button( self, event):
        self.controller.restart()
        return

    # ------------------------------------------
    def do_clear_button( self, event):
        """
        for the clear button
        arguments:  event, ignored can be anything
        clear the receive area
        """
        self.rec_text.delete( 1.0, END )
        # !! may need refresh here is next any good
        self.root.update()
        return

    # ------------------------------------------
    def do_copy_button( self, event ):
        """
        copy all text to the clipboard
        """
        data  = self.rec_text.get( 1.0, END )
        pyperclip.copy( data )

    # # ------------------------------------------
    # def cb_copy_selection( self, event ):
    #     """
    #     copy selected text in the receive/message area

    #     """
    #     try:
    #         data  = self.rec_text.get( "sel.first", "sel.last" )
    #         pyperclip.copy( data )
    #     except Exception as exception:  # if no selection -- this is too broad and exception !!
    #         pass

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

    # ------------------------------------------
    def cb_copy_selection( self,  ):
        """
        copy selected text in the message/receive area
        """
        try:
            data  = self.rec_text.get( "sel.first", "sel.last" )
            pyperclip.copy( data )
        except Exception as exception:  # if no selection -- this is too broad and exception !!
            pass

    # ------------------------------------------
    def cb_copy_all( self,  ):
        """
        copy all from message/receive area
        new from terminal implementation
        """
        # pass
        #rint("implemen me cb_copy_all")
        data  = self.rec_text.get( 1.0, END )
        pyperclip.copy( data )

    # ---- Set datetimes ------------------------------------

    #-------------------------------------------
    def set_1_year_ago( self,  my_widget,  ):
        """
        what it says

        """
        self._set_active_date_widget( my_widget )
        self.set_years_ago_datetimes( 1, 1 )    # second arg, no of days ?

    #-------------------------------------------
    def set_2_year_ago( self,  my_widget, ):
        """
        what it says

        """
        self._set_active_date_widget( my_widget )
        self.set_years_ago_datetimes( 2, 1 )

    #-------------------------------------------
    def set_3_year_ago( self,  my_widget,  ):
        """
        what it says
        """
        self._set_active_date_widget( my_widget )
        self.set_years_ago_datetimes( 3, 1 )

    #-------------------------------------------
    def set_4_year_ago( self,   my_widget,  ):
        """
        what it says
        """
        self._set_active_date_widget( my_widget )
        self.set_years_ago_datetimes( 4, 1 )

    #-------------------------------------------
    def set_years_ago_datetimes( self, a_year_delta, a_day_delta   ):
        """
        what it says
        args    a_year_delta int, normally positive, a_day_delta  int usually 1
        returns  changed state of date elements
        """
        year_delta    = datetime.timedelta( weeks  = a_year_delta * 52 )  # no years argument
        day_delta     = datetime.timedelta( days   = a_day_delta   )

        dt_now         = datetime.datetime.now()
        dt_begin       = dt_now      - year_delta
        dt_end         = dt_begin    + day_delta

        self.set_select_datetimes( dt_begin, dt_end )

    #-------------------------------------------
    def set_dates_back_a_month( self, my_widget ):
        """
        what it say
        returns  changed state of gui date elements
        """
        self._set_active_date_widget( my_widget )
        self.set_both_datetimes_ahead( a_year_delta = 0, a_day_delta = - ( 7 * 4 ) )

    #-------------------------------------------
    def set_dates_back_a_week( self, my_widget ):
        """
        what it say
        returns  changed state of gui date elements
        """
        #rint( "set_dates_back_a_week")
        self._set_active_date_widget( my_widget )
        self.set_both_datetimes_ahead( a_year_delta = 0, a_day_delta = - 7 )

    #-------------------------------------------
    def set_both_datetimes_ahead( self, a_year_delta, a_day_delta   ):
        """
        what it says
        args    a_year_delta int, neg for back in time, a_day_delta
        returns  changed state of gui date elements
        """
        dt_begin, dt_end    = self.get_dt_begin_end()

        year_delta          = datetime.timedelta( weeks  = a_year_delta * 52 )  # no years argument
        day_delta           = datetime.timedelta( days   = a_day_delta   )

        dt_begin            += ( year_delta + day_delta )
        dt_end              += ( year_delta + day_delta )

        #rint( f">>>> date_begin  {dt_begin}"  )

        self.set_select_datetimes( dt_begin, dt_end )

    #-------------------------------------------
    def set_select_slier_datetimes( self, val  ):
        """
        what it says"
        """
        #rint( val )

        big_delta      = datetime.timedelta( weeks = int( val) )
        plus_delta     = AppGlobal.parameters.slider_datetime_width

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
        dt_begin       = dt_now + datetime.timedelta( weeks=-4 )

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
        dt_begin       = dt_now + datetime.timedelta( weeks=-1 )

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

        # March 2006 by Jack Dorsey, Noah Glass, Biz Ston
        self.cal_begin.set_date( datetime.date( 2006,3, 1 ) )
        self.time_begin.set( AppGlobal.dd_hours[0] )

        # set to begin tomorrow, end today
        date_end     =  ( dt_now + datetime.timedelta( days = 1 ) ).date()
        self.cal_end.set_date( date_end )
        self.time_end.set( AppGlobal.dd_hours[0] )

    #-------------------------------------------
    def set_select_today( self, my_widget ):
        """
        what it says
        put values into gui
        """
        #rint( "db_select_today" )
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
        # move from controller to decouple type of gui ??
        AppGlobal.controller.cb_change_select_type( None ) # so right options out of the shute
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
        #rint (root.filename)
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
        #rint( f"get_text = {self.get_text()}", flush = True )

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






