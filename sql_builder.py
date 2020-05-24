# -*- coding: utf-8 -*-

from  tkinter import messagebox
# import collections
import sqlite3 as lite
import time
import datetime

# ------- local imports
from   app_global import AppGlobal
import app_global
import file_writers


#   ------- pseudo columns -- if used typically in sql and in columns out
ROW_COUNT_CN         = "'*rc*'"     # just a running row count
TOTAL_WORD_RANK      = "'*twr*'"    # running total of word rank and average at end


#---------
indent             = "    "   # use for formatting

# ----------------------------------------
def transform_0_1( transform_in ):
    """
    actually transforms the truthyness of anything
    """
    if transform_in:
        return( "Yes!")
    else:
        return( "No?")

# ----------------------------------------
def transform_word_type( word_type_int ):
    """
    what it says ... currently list is manual make auto ?? auto now in test
    """
    #return( AppGlobal.transform_word_types[ word_type_int ] )
    return( AppGlobal.gui.decode_word_type_dict[ word_type_int ] )

# ----------------------------------------
def transform_is_ascii( is_ascii ):
    """
    what it says ... currently list is manual make auto ?? auto now in test
    """
    if is_ascii == 1:
        return "Yes"
    else:
        return "No"

# ----------------------------------------
def build_column_info():
    """
    a data dictionary like thing for selects
    right now more or less a literal
    !! still getting developed, and features added

    Returns:
        column_info

    column_info  dict of dicts outer key, column name ( and pseudo columns),
    inner key property of the column.  still working on the properties
    """
    column_info                             = {}   # dict of dicts ... outer dict

    # ------ # begin construction of inner dict one for each column
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:<20}"
    info_for_a_column["column_head"]        = "default"
    info_for_a_column["transform"]          = None        # function takes row item and returns a transformed item 0/1 to True/False......
    default_info_for_a_column               = info_for_a_column   # temp untill proper one is built

    # ----- concord.word
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:<20}"
    info_for_a_column["column_head"]        = "Concord Word"
    info_for_a_column["transform"]          = None
    column_info["concord.word"]             = info_for_a_column


    #  ------ concord.is_ascii
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:<5}"
    info_for_a_column["column_head"]        = "Ascii"
    info_for_a_column["transform"]          = transform_is_ascii
    column_info["concord.is_ascii"]         = info_for_a_column

    #  ------ concord.is_ascii
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:<5}"
    info_for_a_column["column_head"]        = "Type"
    info_for_a_column["transform"]          = None
    column_info["concord.word_type"]        = info_for_a_column


    #  ------ tweet_id
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:<20}"
    info_for_a_column["column_head"]        = "Words Word"
    info_for_a_column["transform"]          = None
    column_info["concord.tweet_id"]         = info_for_a_column
    column_info["tweets.tweet_id"]          = default_info_for_a_column

    #  ------ words.word
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:<20}"
    info_for_a_column["column_head"]        = "Words Word"
    info_for_a_column["transform"]          = None
    column_info["words.word"]               = info_for_a_column

    # ----- word_rank
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:<6}"
    info_for_a_column["column_head"]        = "Rank"
    info_for_a_column["transform"]          = None
    column_info["words.word_rank"]          = info_for_a_column

    # ----- tweet id
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:<20}"
    info_for_a_column["column_head"]        = "Tweet Id"
    info_for_a_column["transform"]          = None
    column_info["tweets.tweet_id"]          = info_for_a_column

    # ----- tweets_datetime
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:<20}"
    info_for_a_column["column_head"]        = "Date/Time"
    info_for_a_column["transform"]          = None
    column_info["tweets.tweet_datetime"]    = info_for_a_column

    # ----- tweets_is covid
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:<8}"
    info_for_a_column["column_head"]        = "Is Covid"
    info_for_a_column["transform"]          = transform_0_1    # need self no module
    column_info["tweets.is_covid"]          = info_for_a_column


    # ----- line number
    column_info["tweets.line_no"]           = default_info_for_a_column


    # # ----- xxx
    # info_for_a_column                       = {}
    # info_for_a_column["curly_format"]       = "{x:<10}"
    # info_for_a_column["column_head"]        = "Tweet Type"
    # column_info["tweets.tweet_type"]        = info_for_a_column


    # ----- tweet
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:<120}"
    info_for_a_column["column_head"]        = "Tweet"
    info_for_a_column["transform"]          = None
    column_info["tweets.tweet"]             = info_for_a_column


    column_info["tweets.raw_tweet"]         = default_info_for_a_column
    column_info["tweet.url_list"]           = default_info_for_a_column

    # ----- tweet type
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:<8}"
    info_for_a_column["column_head"]        = "Type"
    info_for_a_column["transform"]          = None
    column_info["tweets.tweet_type"]        = info_for_a_column

    # ----- concord word type
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:<6}"
    info_for_a_column["column_head"]        = "W Type"
    info_for_a_column["transform"]          = transform_word_type    # module level
    column_info["concord.word_type"]        = info_for_a_column

    # ------ my count
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:>10}"
    info_for_a_column["column_head"]        = "Count"
    info_for_a_column["transform"]          = None
    column_info["my_count"]                 = info_for_a_column   # this for a group count ...

    # ------ row count
    info_for_a_column                       = {}  # used for row count line in select  builder.add_row_count  = True ??
    info_for_a_column["column_head"]        = "Row#"
    info_for_a_column["curly_format"]       = "{x:<4}"
    info_for_a_column["transform"]          = None               # another function transforms entire row
    column_info[ ROW_COUNT_CN ]             = info_for_a_column


    # ------ TOTAL_WORD_RANK
    info_for_a_column                       = {}  # used for row count line in select  builder.add_row_count  = True ??
    info_for_a_column["column_head"]        = "WordRank"
    info_for_a_column["curly_format"]       = "{x:>5}"
    info_for_a_column["transform"]          = None
    column_info[TOTAL_WORD_RANK]            = default_info_for_a_column   # used for total word rank  builder.add_row_count        = True

    return column_info

# ----------------------------------------
class PseudoColumnRowCount(   ):
    """
    supports adding of a row count pseudo column
    where to use, call in any setup that might use this
    """
    def __init__( self, builder ):
        """
        what it says
        """
        #print( "PseudoColumnRowCount INIT" )
        self.builder   = builder
        # call config reset from here?

    # ----------------------------------------------
    def config( self,   ):   # or running word rank or ....
        """
        based on builder columns out configures its self and builder
        mutates self and builder
        """
        #print( "PseudoColumnRowCount config" )
        self.ix_col_out          = None   # ?? may not be needed function takes care of it

        try:
            self.ix_col_out      = self.builder.columns_out.index( ROW_COUNT_CN )
        except:
            pass
            # self.row_to_list      = False no someone else may set to true
            #print( "PseudoColumnRowCount config  --  NOT" )
            return

            # msg  =  "config_for_total_word_rank configuration error"
            # AppGlobal.display_info_string( msg )
            # return

        self.builder.row_to_list      = True
        self.builder.row_functions.append( self.row_function )
        self.builder.footer_function.append( self.footer_function )


        print( f"PseudoColumnRowCount config  -- for column {self.ix_col_out}\n    row function = {self.builder.row_functions}" )
        #self.builder.footer_function.append()   !! do me

    # ----------------------------------------------
    def row_function( self, a_row  ):
        """
        called for each row fetch in select and output
        mutates a_row
        """
        #print( f"{self.builder.row_count}"  )
        a_row[ self.ix_col_out  ]  = self.builder.row_count
        #print( a_row )

    # ----------------------------------------------
    def footer_function( self,   ):
        """
        called for footer, for now have all return a string ??
        mutates a_row
        """
        msg   = "footer_function from row count"
        return msg

# ----------------------------------------
class PseudoColumnTotalWordRank(   ):
    """
    supports adding of a running count/average of the word rank in tweets
    """
    def __init__( self, builder ):
        """
        what it says
        """
        #print( "PseudoColumnTotalWordRank INIT" )
        self.builder   = builder

    # ----------------------------------------------
    def config( self,   ):   # or running word rank or ....
        """
        based on builder columns out configures its self and builder
        mutates self and builder
        """
        #print( "PseudoColumnTotalWordRank config" )
        self.ix_col_out          = None   # ?? may not be needed function takes care of it

        try:
            self.ix_col_out      = self.builder.columns_out.index( TOTAL_WORD_RANK )
        except ValueError:
            pass
            # self.row_to_list      = False no someone else may set to true
            #print( "PseudoColumnRowCount config  --  NOT" )
            return
        try:
            self.ix_word_rank     = self.builder.columns_out.index( "words.word_rank" )
        except ValueError:
            self.ix_word_rank          = None   # error condition ... manage this better
            msg  =  "config_for_total_word_rank configuration error"
            AppGlobal.logger.error( msg )
            print( msg )
            return

            # msg  =  "config_for_total_word_rank configuration error"
            # AppGlobal.display_info_string( msg )
            # return
        self.count_words              = 0  # count of words for this, not all parsed things are words
        self.total_word_rank          = 0
        self.builder.row_to_list      = True
        self.builder.row_functions.append( self.row_function )
        # print( f"PseudoColumnRowCount config  --  {self.builder.row_functions}" )
        #self.builder.footer_function.append()   !! do me

    # ----------------------------------------------
    def row_function( self, a_row  ):
        """
        called for each row
        mutates a_row
        """
        # print( "self.builder.row_count"  )
        word_rank      = a_row[ self.ix_word_rank ]
        if word_rank is None:                 # unranked concord.word's
            a_row[ self.ix_col_out  ]  = None
        else:
            self.count_words          += 1
            self.total_word_rank      += word_rank
            a_row[ self.ix_col_out  ]  = self.total_word_rank/self.count_words

# # ----------------------------------------
# class PseudoColumnWORDCOUNTSOMETHING_FINISH_ME(   ):
#     """
#     .....
#     """


#         self.ix_twr          = None
#         self.ix_word_rank    = None

#         try:
#             self.ix_twr     = self.columns_out.index( "'twr'" )
#         except ValueError:
#             pass
#             # self.row_to_list      = False no someone else may set to true
#             return

#         try:
#             self.ix_word_rank     = self.columns_out.index( "words.word_rank" )
#         except ValueError:
#             self.ix_twr          = None   # error condition ... manage this better
#             msg  =  "config_for_total_word_rank configuration error"
#             AppGlobal.display_info_string( msg )
#             return

#         self.row_to_list      = True

#         # have both so we are good to go

# ----------------------------------------
class SQLBuilder(   ):
    """
    build sql based on criteria ( all should be in reset )
    then pushed in by external methods setting values
    not all criteria used by all methods ?
    always use fully qualified table names
    """
    def __init__( self,  ):
        """
        what it says
        """
        print( "init SQLBuilder")
        self.reset()
        self.check_title       = "Check Select"
        self.check_run_select  = "Would you like still continue ?"

    # ------ helpers
    # ----------------------------------------------
    def reset( self,  ):
        """
        reset criteria
        None = criteria not being used
        """
        # set up a little report for this difference in attributs over run ??
        # !! default for datetimes

        self.columns_info      = build_column_info()  # dict of dicts info on each column by fully qualified column name
        self.db_name          = ""
        self.output_format    = "tablexxx"  #  "html"......
        self.db_name          = ""
        self.output_name      = None
        self.columns_out      = None     # list of names in order for the column output
        self.help_file        = "./help/build_for_default.txt"  # change to generic

        self.help_mode        = True
        self.a_word           = ""    # word for select criteria, in some cases a string
        self.my_count         = None
        self.is_covid         = ""    # select criteria on tweet
        self.default_order_by = ""
        self.gui_order_by     = ""
        self.word_type        = "get_error"

        self.begin_dt              = datetime.datetime( 1945, 5, 24, 17, 53, 59 )
        self.end_dt              = datetime.datetime(   1945, 5, 24, 17, 53, 59 )
        self.select_name      = "A select- name not set "   # user oriented name, same as in dropdown -- can dropdown pass itself with lambda

        self.start_time       = 0    # probably time.time() start of select
        self.end_time         = 0

        self.pseudo_columns   = [   PseudoColumnRowCount( self ),       # list to check may not be present
                                    PseudoColumnTotalWordRank( self ),
                                 ]

        self.row_functions    = []    # called for each row, used with pseudo columns
        self.footer_functions = []    # called for the footer

        self.message_function = None   # set to a function message_function( msg ) for progress messages ?? not implemented

        self.reset_sql()

    # ----------------------------------------------
    def reset_sql( self,  ):
        """
        what it says
        return mutate self  --- not sure it should differ from reset
        """
        # use these when building so little mutating routines  like add_to_where work
        self.sql              = ""
        self.sql_where        = ""
        self.sql_having       = ""
        self.sql_from         = ""
        self.sql_data         = []    # parameters passed to sql
        self.row_count        = 0

        self.row_functions    = []    # functions called on each row, producing column data
        self.footer_function  = []    # functions called at end of fetch, data for footer
        self.prior_row        = None
        self.row_to_list      = False  # convert row to a list for manipulation

    # ----------------------------------------------
    def builder_vars_as_str( self,   ):
        """
        what it says ....
        for debug gathers instance var for select into a string
        return string
        """
        # add more as needed, setup in setup init to avoid errors
        msg     =  "builder vars ( self.x ):\n"
        msg    += f"     db_name:            {self.db_name}\n"
        msg    += f"     select_name:        {self.select_name}\n"
        msg    += f"     output_format:      {self.output_format}\n"

        msg    += f"     columns_out:        {self.columns_out}\n"

        msg    += f"     a_word:             {self.a_word}\n"
        msg    += f"     is_covid:           {self.is_covid}\n"
        msg    += f"     default_order_by:   {self.default_order_by}\n"
        msg    += f"     gui_order_by:       {self.gui_order_by}\n"
       # msg    += f"     sort_order:        {self.sort_order}\n"   # why both of them is this default set where
        msg    += f"     begin_dt:           {self.begin_dt}\n"
        msg    += f"     end_dt:             {self.end_dt}\n"
        msg    += f"     tweet_type:         {self.tweet_type}\n"
        msg    += f"     max_count:          {self.max_count}\n"
        msg    += f"     word_type:          {self.word_type}\n"
        msg    += f"     my_count:           {self.my_count}\n"

        msg    += f"     sql:                {self.sql}\n"
        msg    += f"     sql_where:          {self.sql_where}\n"
        msg    += f"     sql_having:         {self.sql_having}\n"
        msg    += f"     sql_data:           {self.sql_data}\n"
        msg    += f"\n\n"

        return msg

   # ----------------------------------------------
    def add_to_where( self,    add_where = None, add_data = None,   ):
        """
        add on to where clause ok if starts at 0.  assumes and between clauses
        return    mutates self
        """
        if self.sql_where == "":
            self.sql_where  = "\n WHERE "
        else:
            self.sql_where += " AND  "

        if add_where is not None:

            #sql_where   +=  f" tweets.tweet_datetime  >= {begin_dt} "
            self.sql_where   +=  add_where
            if add_data is not None:
                self.sql_data.append( add_data )

    # ----------------------------------------------
    def add_to_where_dates( self,   ):
        """
        what it says ....
        return mutates self, sqlwhere in particular
        """
        #  -------- dates
        begin_dt      =   self.begin_dt
        if begin_dt is not None:
            self.add_to_where( add_where = f"\n{indent}tweets.tweet_datetime  >= ? ",
                               add_data  = begin_dt  )

        end_dt        =   self.end_dt
        if end_dt is not None:
            self.add_to_where( add_where  = f"\n{indent}tweets.tweet_datetime <= ? ",
                               add_data   = end_dt  )

   # ----------------------------------------------
    def display_help( self  ):
        """
        user interaction:
        display help for this report
        """
        AppGlobal.gui.do_clear_button( "dummy_event")
        with open( self.help_file, "r" ) as a_file:
            lines = a_file.readlines()
            # print( lines )
            msg  = "".join( lines )
            AppGlobal.gui.display_info_string( msg )
        return

   # ----------------------------------------------
    def confirm_continue( self, info_msg,  a_title, msg, ):   #  help_mode = False
        """
        user interaction:
        display and perhaps throw exception
        app_global.UserCancel
        exceptions: raise app_global.UserCancel if user does not want to continue
        return: zip or exception
        argument in builder  ..... help_mode = True aborts the actual select
        """
        help_mode    = self.help_mode

        print( f"builder confirm_continue {help_mode}")

        AppGlobal.gui.display_info_string( info_msg )

        if help_mode:
            raise app_global.UserCancel( "Mode: Help only, query not run" )

        if AppGlobal.parameters.confirm_selects:

            continue_flag  = messagebox.askokcancel( a_title, msg )

            if continue_flag is not True:
                AppGlobal.gui.display_info_string( "Operation canceled" )
                raise app_global.UserCancel( "user: Operation canceled" )

    # ----------------------------------------------
    def select_and_output( self,  ):
        """
        what it says
        now does pseudo cols ....
        !! update for col transforms
        ?? would bringing references local help anything
        !! flag to se if any transforms used ... tie them up in the f strings ??
        some mutation and file output in most cases
        """
        self.start_time     = time.time()

        # check transforms to see if we need to convert to list !! for speed, but is it worth it
        # for now force it
        self.row_to_list    = True

        columns_info        = self.columns_info
        # print( f"columns_info{columns_info}")

        file_writer         = file_writers.make_file_writer( self  )
        file_writer.write_header()

        msg     = f"Select and output connect to {self.db_name}"
        print( msg )
        sql_con = lite.connect( self.db_name )

        with sql_con:
            cur           = sql_con.cursor()
            execute_args  = ( self.sql,  self.sql_data,  )
            msg           = f"selet and output execute_args {execute_args}"
            print(  msg )
            AppGlobal.logger.debug( msg )
            cur.execute( *execute_args )

            while True:  # get rows one at a time in loop
                row   = cur.fetchone()

                if row is None:
                    break
                self.row_count    += 1
                self.prior_row     = row    # save for later use, perhaps at footer ? -- save after transform
                if self.row_to_list:        # !! efficency tweak
                    #print( "row_to_list"  )
                    row  = list( row )

                for i_function in self.row_functions:
                    i_function( row )   # mutates row
                # print( f"_>>>>>{row}")

                for ix_col, i_col in enumerate( row ):
                    # better to put functions in a list to simplify reference
                    # indexed double dict lookup
                    i_col_info    = columns_info[ self.columns_out[ ix_col ] ]
                    transform     = i_col_info["transform"]
                    #col_text     = i_col_info["column_head"]
                    if transform is not None:
                        row[ ix_col ]    = transform( i_col )

                file_writer.write_row( row )   # here may need to add row count.... breaking stuff what type is row?

        sql_con.commit()
        sql_con.close()
        self.end_time = time.time()

        footer_info  = ""
        # pseudo columns and perhaps others
        for i_function in self.footer_functions:
                 foot_msg  =   i_function(  )   # returns string
                 footer_info     += "\n" + foot_msg

        footer_info    +=  f"Done: >\n"
        footer_info    +=  f"     total number of rows = {self.row_count}"

        msg             =  f"     select and file write took {self.end_time - self.start_time} seconds"
        footer_info  += f"\n{msg}"

        file_writer.write_footer( footer_info )

        print(  msg )
        msg      =  f"select complete with footer info: {footer_info}"
        AppGlobal.logger.debug( msg )

        # open file for user to read
        if   self.output_format  == "html":
            AppGlobal.os_open_html_file( self.output_name )

        elif self.output_format  == "msg":
            AppGlobal.gui.do_clear_button( "dummy_event")

            with open( self.output_name, "r", encoding = "utf8", errors = 'replace' )  as a_file:
                lines = a_file.readlines()
                # print( lines )
                msg  = "".join( lines )
                AppGlobal.gui.display_info_string( msg )

        else:
            AppGlobal.os_open_txt_file(  self.output_name )

  # ----------------------------------------------
    def go( self,  ):
        """
        move back to parent
        after all setup is done go
        arg:  which select in builder to run, later when sub-classed just go
        """
        try:
            self.this_select()   # configured for one of self.  ... with subclassing always the same
            self.select_and_output()    # help_mode ??

        except app_global.UserCancel as exception:   #

            pass  # Catch the  exception and swallow as user wants out
            #print( exception )

        msg   = f"Select Done, rows selected: {self.row_count} time = {self.end_time - self.start_time}"
        AppGlobal.gui.display_info_string( msg )
        AppGlobal.logger.debug(  msg  )

   # # ----------------------------------------------
   #  def go( self, which_select  ):
   #      """
   #      after all setup is done go
   #      arg:  which select in builder to run, later when sub-classed just go
   #      """
   #      try:
   #          which_select()   # configured for one of self.  ... with subclassing always the same
   #          self.select_and_output()    # help_mode ??

   #      except app_global.UserCancel as exception:   #

   #          pass  # Catch the  exception and swallow as user wants out
   #          #print( exception )

   #      msg   = f"Select Done, rows selected: {self.row_count} time = {self.end_time - self.start_time}"
   #      AppGlobal.gui.display_info_string( msg )
   #      AppGlobal.logger.debug(  msg  )

   # ----------------------------------------------
    def format_sql_for_user( self  ):
        """
        !! finish me
        mutate self
        """
        self.display_sql   = "not implemented"

    # ------ a- now all obsolete, use sub classes now

    # ----------------------------------------------
    def build_for_select_1( self,  ):
        """
        seems to be 3 way join work on next
        select 1 is a concordance query with the
            columns
                concord.word word_type word_rank, word_count
            select
                dates is_covid  concond.word like / word_count  /word_rank
        argument  help_mode = True, give help and sql but doed not run

        """
        help_mode =self.help_mode
        print( f"builder build_for_select_1 help_mode = {help_mode}")
        msg    = self.builder_vars_as_str()
        print( msg )
        AppGlobal.logger.info( msg )

        self.display_help()
        print( f"builder actual build done here, complete me = {''}")

        #  -------- dates
        self.add_to_where_dates(   )

        #  -------- tweet_type
        tweet_type   = self.tweet_type
        if tweet_type is not None:
               self.add_to_where( add_where = f"\n{indent}tweets.tweet_type = ?   ",
                                  add_data = tweet_type )

        info_msg     =    f"sql is:  {self.sql}"                # refactor into confirm continue ??
        print( info_msg )
        AppGlobal.gui.display_info_string( info_msg )

        info_msg     =    f"sql_data is:  {self.sql_data}"
        print( info_msg )
        AppGlobal.gui.display_info_string( info_msg )

        self.confirm_continue( info_msg, self.check_title,   self.check_run_select, help_mode = help_mode )



    # ----------------------------------------------
    # def build_for_word_count( self,   ):
    def concord_joined_select_1( self,   ):
        """
        cb_select_concord
        build base on criteria already in instance var
        return   self mutated
        instance var may be used differently by different build routines

        """
        columns            =  self.columns_out       # may need adjust for my count..... or not
        self.sql          = "SELECT " + ", ".join( columns  ) + " "

        self.count          = True       # should be in select_dict ??
        self.group_by       = "concord.word"

        # now add the sort of phony column my_count
        columns.append( "my_count" )   # does this mutate back to select_dict, i think so -- will be used by file writer

        if self.count:
            self.sql       += ", COUNT( * ) as my_count  "

        self.sql           += "\n    FROM concord "

        self.sql           += "\n    LEFT JOIN words  ON concord.word = words.word  "

        self.sql_data         = []   # probaly should have reset_sql()
        #-------------------- where self.sql_where
        self.sql_where     = ""

        if self.max_word_rank is not None:
            self.add_to_where( add_where = f" words.word_rank  <  {self.max_word_rank}  ",
                               add_data = None  )

        if self.word_rank_null is not None:
            if self.word_rank_null == "is":
                a_add_to_where       = " words.word_rank is NULL "

            else:
                a_add_to_where       = " words.word_rank is not NULL "

            self.add_to_where( add_where = a_add_to_where ,
                           add_data = None  )

        # if self.sql_where != ""
        self.sql   += self.sql_where         # if now where adds ""

        # ----------------- having
        self.sql           += "\n    GROUP BY concord.word  "

        sql_having          = ""
        min_word_count      = self.min_word_count
        if  min_word_count is not None:
            if sql_having == "":
                sql_having = "\n HAVING "
            else:
                sql_having += " AND  "

            sql_having   +=  f"( my_count > {min_word_count} )"

        if sql_having != "":
            self.sql           += sql_having

        # ----------------- order_by
        order_by    = self.order_by
        if order_by is not None:   # change to tuples
            self.sql           += "\n ORDER BY " + order_by

        # done  ( put in an assemble method ?? )
        self.display_help()
        info_msg     =    f"\n\n-------------sql is:  {self.sql}"
        AppGlobal.gui.display_info_string( info_msg )
        info_msg     =    f"sql_data is:  {self.sql_data}"

        self.confirm_continue( info_msg, "Check SQL", "Would you like still continue ?" )


# ----------------------------------------
class Select_03( SQLBuilder  ):
    """
    build sql based on criteria ( all should be in reset )
    then pushed in by external methods setting values
    not all criteria used by all methods ?
    always use fully qualified table names
    """
    def __init__( self,  ):
        """
        what it says
        """
        #print( "init Select_03")
        super().__init__(  )

    # ----------------------------------------------
    def this_select( self,  ):
        """
        build base on criteria already in instance var
        return   self mutated
        instance var may be used differently by different build routines

        hardcoded, no user select, can select output
        !! fix
        """
        print( "this_select Select_03")
        select_name = "joe"

        self.select_name   = "joe select_03"
        # self.tweet_joined_select_1( select_name,   )

        msg    = self.builder_vars_as_str()
        print( msg )

        columns            =  self.columns_out

        # --- not sure think sets up pseudo columns if in column list
        for i_pc in self.pseudo_columns:
            i_pc.config()

        self.sql           = "SELECT DISTINCT " + ", ".join( columns  ) + " "

        self.sql           += f"\n{indent}FROM concord "

        self.sql           += f"\n{indent}JOIN tweets  ON concord.tweet_id = tweets.tweet_id  "

        self.sql           += f"\n{indent}LEFT OUTER JOIN words  ON concord.word = words.word  "

        #LEFT   JOIN effects e2 ON e2.id = i.effect2

        #-------------------- where self.sql_where
        # --------- word
        if self.a_word != "":
            self.add_to_where( add_where  = f'\n{indent}concord.word  LIKE     "{self.a_word}"',     # need quotes ??
                               add_data   = None  )

        #  -------- dates
        self.add_to_where_dates(   )

        #  --------is_covid -- ok
        is_covid   = self.is_covid
        if is_covid is not None:

            if is_covid:
                self.add_to_where( add_where = f"\n{indent}tweets.is_covid   ",
                                   add_data = None )

            else:
                self.add_to_where( add_where = f"\n{indent}NOT tweets.is_covid   ",
                                   add_data = None )

        #  -------- max_count
        max_count   = self.max_count
        if max_count is not None:
               self.add_to_where( add_where = f"\n{indent}words.word_count < ?   ",
                                  add_data = max_count )

        #  -------- builder.min_rank
        min_rank   = self.min_rank
        if min_rank is not None:
               self.add_to_where( add_where = f"\n{indent}words.word_rank > ?   ",
                                  add_data = min_rank )

        #  -------- tweet_type
        tweet_type   = self.tweet_type
        if tweet_type is not None:
               self.add_to_where( add_where = f"\n{indent}tweets.tweet_type = ?   ",
                                  add_data = tweet_type )

        # ---------- final where ....wrap it up -- if no where's adds ""
        self.sql   += self.sql_where         # wrap it up -- if now where adds ""

        # ----------------- order by
        gui_order_by    = self.gui_order_by
        if gui_order_by == "default":
            self.sql           +=  f"\n{indent}ORDER BY " + self.default_order_by
        else:
            self.sql           +=  f"\n{indent}ORDER BY " + gui_order_by

        self.display_help()   # move more to confirm and continue ??

        info_msg     =    f"sql is:  {self.sql}"
        print( info_msg )
        AppGlobal.gui.display_info_string( info_msg )

        info_msg     =    f"sql_data is:  {self.sql_data}"
        print( info_msg )
        AppGlobal.gui.display_info_string( info_msg )

        self.confirm_continue( info_msg, "Check SQL", "Would you like still continue ?" )

# ----------------------------------------
class TweetSelect1( SQLBuilder  ):
    """
    build sql based on criteria ( all should be in reset )
    then pushed in by external methods setting values
    not all criteria used by all methods ?
    always use fully qualified table names
    """
    def __init__( self,  ):
        """
        what it says
        """
        #print( "init TweetSelect1")
        super().__init__(  )

    # ----------------------------------------------
    def this_select( self,  ):
        print( "this select TweetSelect1")
        # ----------------------------------------------

        msg   = f"tweet_select_1 builder vars: {self.builder_vars_as_str()}"
        print( msg  )
        AppGlobal.logger.debug(  msg  )

        self.columns_out      = [ "tweets.tweet_datetime", "tweets.tweet_type",  "tweets.tweet", "tweets.tweet_id"    ]
        self.sql              = (
            "\n SELECT tweets.tweet_datetime, tweets.tweet_type, tweets.tweet, tweets.tweet_id  "
            "FROM tweets "
            )

        #  -------- dates
        self.add_to_where_dates(   )

        #  -------- tweet_type
        tweet_type   = self.tweet_type
        if tweet_type is not None:
               self.add_to_where( add_where = f"\n{indent}tweets.tweet_type = ?   ",
                                  add_data = tweet_type )

        self.sql   += self.sql_where

        # still need to fix order by
        self.sql   +=   "ORDER BY tweets.tweet_datetime "

        # next is standard refactor ??
        self.display_help()
        info_msg     =    f"sql is:\n{self.sql}\n"
        AppGlobal.gui.display_info_string( info_msg )
        info_msg     =    f"sql_data is:\n{self.sql_data}"

        self.confirm_continue( info_msg, self.check_title,   self.check_run_select, )

# ----------------------------------------
class ConcordSelect1( SQLBuilder  ):
    """
    specilized decendant of SQLBuilder for a particular select
    """
    def __init__( self,  ):
        """
        what it says
        """
        #print( "init ConcordSelect1")
        super().__init__(  )

    # ----------------------------------------------
    def this_select( self,  ):
        print( "this select TweetSelect1")


        self.columns_out      = [ "concord.word",
                                  "concord.word_type",
                                  "concord.is_ascii",
                                  ROW_COUNT_CN,
                                  "my_count",
                                 ]

        # !! build from columns out
        self.sql              = (
            f"\n SELECT concord.word, concord.word_type, concord.is_ascii, {ROW_COUNT_CN}, COUNT( * ) as my_count "
            "FROM concord "
            "JOIN tweets  ON concord.tweet_id = tweets.tweet_id "
            )

        # pseudo_columns after set up in both sql and columns out
        for i_pc in self.pseudo_columns:
            i_pc.config()

        #  -------- dates
        self.add_to_where_dates(   )

        # ----- tweet_type
        tweet_type      =   self.tweet_type
        if tweet_type is not None:
             self.add_to_where( add_where = f"\n{indent}tweets.tweet_type = ? ",
                               add_data = tweet_type  )

        # ----- word_type
        word_type      =   self.word_type
        if word_type is not None:
             self.add_to_where( add_where = f"\n{indent}concord.word_type = ? ",
                               add_data = word_type  )

        self.sql   += self.sql_where

        self.sql   +=  (  f"GROUP BY concord.word " )

        if self.my_count is not None:
            self.sql_having   =   f"\n{indent}HAVING ( my_count > ? ) "
            self.sql_data.append( self.my_count )

        self.sql   +=  self.sql_having

        self.sql   +=  f"\n{indent}ORDER BY my_count Desc, concord.word "

        self.display_help()
        info_msg     =    f"sql is:\n{self.sql}\n"
        AppGlobal.gui.display_info_string( info_msg )
        info_msg     =    f"sql_data is:\n{self.sql_data}"

        self.confirm_continue( info_msg, self.check_title,   self.check_run_select, )


# ==============================================
if __name__ == '__main__':
    """
    run the app here for convenience of launching
    """

    # import sys
    # sys.path.append( r"D:\Russ\0000\python00\python3\_examples"  )
    # import ex_helpers       # ex_helpers.info_about_obj()
    import tweet_app
    a_app = tweet_app.TweetApp(  )
# ======================== eof ======================



