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
"""
to make one,
   make a constant here
   add to column info in self.build_column_info
   add a class
        then add to self.pseudo_columns  ( search for the place)

"""

# literals on right are more or less arbitrary, but all must be different
ROW_COUNT_CN         = "'*rc*'"     # just a running row count
TOTAL_WORD_RANK      = "'*twr*'"    # running total of word rank and average at end
RA_WORD_RANK         = "'*pc03*'"   # running average word rank with groupby on word.words
                                    # a replacement for TOTAL_WORD_RANK which will be retired
RA_WORD_LENGTH       = "'*rawl*'"   # see PseudoColumnRa_Word_Length
RA_WORD_NULL         = "'*rawn*'"   # see PseudoColumnRa_Word_Null
#---------
indent             = "    "   # use for formatting

# ----------------------------------------
def transform_0_1( transform_in ):
    """
    actually transforms the truthyness of anything
    # for is_covid probably
    """
    if transform_in:
        return( "Yes")
    else:
        return( "No")

# ----------------------------------------
def transform_word_type( word_type_int ):
    """
    what it says ... currently list is manual make auto ?? auto now in test
    """
    # msg    = f"transform_word_type index is {word_type_int}"
    #rint( msg )
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

    Returns:  column_info

    column_info  dict of dicts outer key, column name ( and pseudo columns),
    inner key property of the column.  still working on the properties
    """
    column_info                             = {}   # dict of dicts ... outer dict

    # ------ # begin construction of inner dict one for each column
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:<20}"
    info_for_a_column["text_format"]        = "{x:<20}"
    info_for_a_column["column_head"]        = "default"
    info_for_a_column["transform"]          = None        # function takes row item and returns a transformed item 0/1 to True/False......
    default_info_for_a_column               = info_for_a_column   # temp untill proper one is built

    # ----- concord.word
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:<20}"
    info_for_a_column["text_format"]        = "{x:<20}"
    info_for_a_column["column_head"]        = "Concord Word"
    info_for_a_column["transform"]          = None
    column_info["concord.word"]             = info_for_a_column

    #  ------ concord.is_ascii
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:<5}"
    info_for_a_column["text_format"]        = "{x:<5}"
    info_for_a_column["column_head"]        = "Ascii"
    info_for_a_column["transform"]          = transform_is_ascii
    column_info["concord.is_ascii"]         = info_for_a_column

    #  ------ concord.word_type
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:<12}"
    info_for_a_column["text_format"]        = "{x:<12}"
    info_for_a_column["column_head"]        = "Type"
    info_for_a_column["transform"]          = None
    column_info["concord.word_type"]        = info_for_a_column

    #  ------ tweet_id
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:<20}"
    info_for_a_column["text_format"]        = "{x:<20}"
    info_for_a_column["column_head"]        = "Tweet Id"
    info_for_a_column["transform"]          = None
    column_info["concord.tweet_id"]         = info_for_a_column
    column_info["tweets.tweet_id"]          = default_info_for_a_column

    #  ------ words.word
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:<20}"
    info_for_a_column["text_format"]        = "{x:>20}"
    info_for_a_column["column_head"]        = "Words Word"
    info_for_a_column["transform"]          = None
    column_info["words.word"]               = info_for_a_column

    # ----- words_rank
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:>8}"
    info_for_a_column["text_format"]        = "{x:>8}"
    info_for_a_column["column_head"]        = "Rank"
    info_for_a_column["transform"]          = None
    column_info["words.word_rank"]          = info_for_a_column

    # ----- words.count
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:>13}"
    info_for_a_column["text_format"]        = "{x:>13}"
    info_for_a_column["column_head"]        = "Count"
    info_for_a_column["transform"]          = None
    column_info["words.word_count"]         = info_for_a_column

    # ----- tweets.tweet id
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:<20}"
    info_for_a_column["text_format"]        = "{x:<20}"
    info_for_a_column["column_head"]        = "Tweet Id"
    info_for_a_column["transform"]          = None
    column_info["tweets.tweet_id"]          = info_for_a_column

    # ----- tweets.tweets_datetime
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:<20}"
    info_for_a_column["text_format"]        = "{x:<20}"
    info_for_a_column["column_head"]        = "Date/Time"
    info_for_a_column["transform"]          = None
    column_info["tweets.tweet_datetime"]    = info_for_a_column

    # ----- tweets.time_of_day
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:<6}"
    info_for_a_column["text_format"]        = "{x:<6}"
    info_for_a_column["column_head"]        = "TofDay"
    info_for_a_column["transform"]          = None
    column_info["tweets.time_of_day"]       = info_for_a_column

    # ----- tweets_is covid
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:<8}"
    info_for_a_column["text_format"]        = "{x:<8}"  #  =  info_for_a_column["curly_format"]
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
    info_for_a_column["curly_format"]       = "{x:<150}"
    info_for_a_column["text_format"]        = "{x:<150}"
    info_for_a_column["column_head"]        = "Tweet"
    info_for_a_column["transform"]          = None
    column_info["tweets.tweet"]             = info_for_a_column


    column_info["tweets.raw_tweet"]         = default_info_for_a_column
    column_info["tweet.url_list"]           = default_info_for_a_column

    # ----- tweet type
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:<8}"
    info_for_a_column["text_format"]        = "{x:<8}"
    info_for_a_column["column_head"]        = "Type"
    info_for_a_column["transform"]          = None
    column_info["tweets.tweet_type"]        = info_for_a_column

    # ----- concord word type
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:<6}"
    info_for_a_column["text_format"]        = "{x:>5}"
    info_for_a_column["column_head"]        = "W Type"
    info_for_a_column["transform"]          = transform_word_type    # module level
    column_info["concord.word_type"]        = info_for_a_column

    # ------ my count
    info_for_a_column                       = {}
    info_for_a_column["curly_format"]       = "{x:>10}"
    info_for_a_column["text_format"]        = info_for_a_column["curly_format"]
    info_for_a_column["column_head"]        = "Count"
    info_for_a_column["transform"]          = None
    column_info["my_count"]                 = info_for_a_column   # this for a group count ...

    # ------ row count
    info_for_a_column                       = {}  # used for row count line in select
    info_for_a_column["column_head"]        = "Row#"
    info_for_a_column["curly_format"]       = "{x:>5}"
    info_for_a_column["text_format"]        = info_for_a_column["curly_format"]
    info_for_a_column["transform"]          = None               # another function transforms entire row
    column_info[ ROW_COUNT_CN ]             = info_for_a_column


    # ------ TOTAL_WORD_RANK
    info_for_a_column                       = {}  # used for row count line in select
    info_for_a_column["column_head"]        = "TWRank"
    info_for_a_column["curly_format"]       = "{x:>5}"
    info_for_a_column["text_format"]        = info_for_a_column["curly_format"]
    info_for_a_column["transform"]          = None
    column_info[ TOTAL_WORD_RANK ]          = info_for_a_column   # used for total word rank  builder.add_row_count        = True

    # ------ RA_WORD_RANK
    info_for_a_column                       = {}
    info_for_a_column["column_head"]        = "RaRank"
    info_for_a_column["curly_format"]       = "{x:>10.0f}"
    info_for_a_column["text_format"]        = "{x:>10}"
    info_for_a_column["transform"]          = None
    column_info[ RA_WORD_RANK ]             = info_for_a_column

    # ------ RA_WORD_LENGTH
    info_for_a_column                       = {}
    info_for_a_column["column_head"]        = "RaWL"
    info_for_a_column["curly_format"]       = "{x:>10.2f}"
    info_for_a_column["text_format"]        = "{x:>10}"
    info_for_a_column["transform"]          = None        # not necessary for a pseodo column
    column_info[ RA_WORD_LENGTH ]           = info_for_a_column

    # ------ RA_WORD_NULL
    info_for_a_column                       = {}
    info_for_a_column["column_head"]        = "RaWN"
    info_for_a_column["curly_format"]       = "{x:>10.4f}"
    info_for_a_column["text_format"]        = "{x:>10}"
    info_for_a_column["transform"]          = None        # not necessary for a pseodo column
    column_info[ RA_WORD_NULL ]           = info_for_a_column

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
        self.builder.footer_functions.append( self.footer_function )

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
        based on builder columns_out configures its self and builder
        mutates self and builder
        TOTAL_WORD_RANK and we need my_count and words.word_rank
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

        try:
            self.ix_my_count     = self.builder.columns_out.index( "words.word_rank" )
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
        #rint( f"PseudoColumnRowCount config  --  {self.builder.row_functions}" )
        #self.builder.footer_function.append()   !! do me

# ----------------------------------------
class PseudoColumnRa_Word_Rank(   ):
    """
    supports adding of a running count/average of the word rank in tweets will replace  PseudoColumnTotalWordRank
    then add to self.pseudo_columns  ( search for the place)
    """
    def __init__( self, builder ):
        """
        what it says
        """
        #rint( "PseudoColumnRa_Word_Rank INIT" )
        self.builder   = builder

    # ----------------------------------------------
    def config( self,   ):   # or running word rank or ....
        """
        based on builder columns_out configures its self and builder
        mutates self and builder
        need columns RA_WORD_RANK and my_count and words.word_rank
        presume grouping is right
        """
        #rint( "PseudoColumnRa_Word_Rank config" )
        self.ix_col_out          = None   # ?? may not be needed function takes care of it

        try:
            self.ix_col_out      = self.builder.columns_out.index( RA_WORD_RANK )
        except ValueError:
            pass
            # self.row_to_list      = False no someone else may set to true
            #print( "PseudoColumnRowCount config  --  NOT" )
            return
        try:
            self.ix_word_rank     = self.builder.columns_out.index( "words.word_rank" )
        except ValueError:
            self.ix_word_rank          = None   # error condition ... manage this better
            msg  =  "config_for_total_word_rank configuration error no: words.word_rank"
            AppGlobal.logger.error( msg )
            print( msg )
            return

        try:
            self.ix_my_count     = self.builder.columns_out.index( "my_count" )
        except ValueError:
            self.ix_word_rank          = None   # error condition ... manage this better
            msg  =  "config_for_total_word_rank configuration error no: my_count "
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
        self.builder.footer_functions.append( self.footer_function )
        msg  = f"PseudoColumnRa_Word_Rank config complete  self.ix_my_count: {self.ix_my_count} "
        print( msg )
        AppGlobal.logger.debug( msg )
        #self.builder.footer_function.append()   !! do me

    # ----------------------------------------------
    def row_function( self, a_row  ):
        """
        called for each row
        note: possible early return
        return  mutates a_row and self
        """
        #rint( "self.builder.row_count"  )  # may need processing for none
        word_rank       = a_row[ self.ix_word_rank ]
        if word_rank is None:
            a_row[ self.ix_col_out  ]  = None
            return

        my_count   = a_row[ self.ix_my_count ]

        # if word_rank is None:                 # unranked concord.word's
        #     a_row[ self.ix_col_out  ]  = None
        # else:

        self.count_words           += my_count
        self.total_word_rank       += word_rank * my_count
        a_row[ self.ix_col_out  ]   = self.total_word_rank/self.count_words

    # ----------------------------------------------
    def footer_function( self,   ):
        """
        called for footer, for now have all return a string ??
        mutates a_row
        """
        if self.count_words > 0:
            msg   = f"final value of average word rank is {self.total_word_rank/self.count_words}"
        else:
             msg   = f"final value of average word rank is undefined"
        print( msg )
        return msg

# ----------------------------------------
class PseudoColumnRa_Word_Length(   ):
    """
    supports adding of a running count/average of the word lengths in tweets will replace


    """
    def __init__( self, builder ):
        """
        what it says
        """
        #rint( "PseudoColumnRa_Word_Length INIT" )
        self.builder   = builder

    # ----------------------------------------------
    def config( self,   ):   # or running word rank or ....
        """
        based on builder columns_out configures its self and builder
        mutates self and builder
        need columns RA_WORD_LENGTH and my_count and words.word_rank
        presume grouping is right
        """
        #rint( "PseudoColumnRa_Word_Rank config" )
        # self.ix_col_out          = None   # ?? may not be needed function takes care of it -- check others

        try:
            self.ix_col_out      = self.builder.columns_out.index( RA_WORD_LENGTH )
        except ValueError:
            pass
            # !! log error in this and other configs -- also below
            # self.row_to_list      = False no someone else may set to true
            #print( "PseudoColumnRowCount config  --  NOT" )
            return

        try:
            self.ix_concord_word     = self.builder.columns_out.index( "concord.word" )
        except ValueError:
            self.ix_concord_word          = None   # error condition ... manage this better
            msg  =  "config_  PseudoColumnRa_Word_Length configuration error no: concord.word"
            AppGlobal.logger.error( msg )
            print( msg )
            return

        try:
            self.ix_my_count     = self.builder.columns_out.index( "my_count" )
        except ValueError:
            self.ix_word_rank          = None   # error condition ... manage this better
            msg  =  "config_for_total_word_rank configuration error no: my_count "
            AppGlobal.logger.error( msg )
            print( msg )
            return

            # msg  =  "config_for_total_word_rank configuration error"
            # AppGlobal.display_info_string( msg )
            # return
        self.count_words              = 0  # count of words for this, not all parsed things are words
        self.total_word_length        = 0
        self.builder.row_to_list      = True
        self.builder.row_functions.append(    self.row_function )
        self.builder.footer_functions.append( self.footer_function )
        # print( f"PseudoColumnRowCount config  --  {self.builder.row_functions}" )

        msg  = ( f"PseudoColumnRa_Word_Length config complete:" +
                 f"\n    ix_concord_word :{self.ix_concord_word}" +
                 f"\n    ix_my_count:     {self.ix_my_count} " +
                 f"\n    ix_col_out:      { self.ix_col_out} " )
        print( msg )
        AppGlobal.logger.debug( msg )

   # ----------------------------------------------
    def row_function( self, a_row  ):
        """
        called for each row
        mutates a_row
        """
        # print( "self.builder.row_count"  )  # may need processing for none
        word       = a_row[ self.ix_concord_word ] # compress syntax
        #if word is None:  # should not happen
        word_len   = len( word )

        my_count   = a_row[ self.ix_my_count ]

        # if word_rank is None:                 # unranked concord.word's
        #     a_row[ self.ix_col_out  ]  = None
        # else:
        self.count_words          += my_count
        self.total_word_length    += word_len * my_count
        a_row[ self.ix_col_out  ]  = self.total_word_length/self.count_words

        #  this seems to work but might build another way and control from gui suppress
        # self.builder.write_row     = False  # perhaps in call and return would be better

    # ----------------------------------------------
    def footer_function( self,   ):
        """
        called for footer, for now have all return a string ??

        """
        msg   = f"final value of average word length is {self.total_word_length/self.count_words}"
        print( msg )
        return msg

# ----------------------------------------
class PseudoColumnRa_Word_Null(   ):
    """
    supports adding of a running count/average of the concord.words that are or not words.word

    """
    def __init__( self, builder ):
        """
        what it says
        """
        #rint( "PseudoColumnRa_Word_Length INIT" )
        self.builder   = builder

    # ----------------------------------------------
    def config( self,   ):   # or running word rank or ....
        """
        based on builder columns_out configures its self and builder
        mutates self and builder
        need columns RA_WORD_NULL and my_count and words.word
        presume grouping is right
        """
        #rint( "PseudoColumnRa_Word_Rank config" )
        # self.ix_col_out          = None   # ?? may not be needed function takes care of it -- check others

        try:
            self.ix_col_out      = self.builder.columns_out.index( RA_WORD_NULL )
        except ValueError:
            pass
            # !! log error in this and other configs -- also below
            # self.row_to_list      = False no someone else may set to true
            #print( "PseudoColumnRowCount config  --  NOT" )
            return

        try:
            self.ix_words_word     = self.builder.columns_out.index( "words.word" )
        except ValueError:
            self.ix_words_word          = None   # error condition ... manage this better
            msg  =  "config_  PseudoColumnRa_Word_Null configuration error no: words.word"
            AppGlobal.logger.error( msg )
            print( msg )
            return

        try:
            self.ix_my_count     = self.builder.columns_out.index( "my_count" )
        except ValueError:
            # self.ix_word_rank          = None   # error condition ... manage this better
            msg  =  "config_  PseudoColumnRa_Word_Null configuration error no: my_count "
            AppGlobal.logger.error( msg )
            print( msg )
            return

            # msg  =  "config_for_total_word_rank configuration error"
            # AppGlobal.display_info_string( msg )
            # return
        self.count_words              = 0  # count of words for this, not all parsed things are words
        self.count_words_null         = 0
        self.builder.row_to_list      = True
        self.builder.row_functions.append(    self.row_function    )
        self.builder.footer_functions.append( self.footer_function )
        # print( f"PseudoColumnRowCount config  --  {self.builder.row_functions}" )

        msg  = ( f"PseudoColumnRa_Word_Null config complete:" +
                 f"\n    ix_words_word :{self.ix_words_word}" +
                 f"\n    ix_my_count:  {self.ix_my_count} " +
                 f"\n    ix_col_out:   { self.ix_col_out} " )
        print( msg )
        AppGlobal.logger.debug( msg )

    # ----------------------------------------------
    def row_function( self, a_row  ):
        """
        called for each row
        mutates a_row
        """
        my_count         = a_row[ self.ix_my_count   ]
        words_word       = a_row[ self.ix_words_word ] # compress syntax
        if words_word is None:
            self.count_words_null       += my_count

        self.count_words          += my_count

        a_row[ self.ix_col_out  ]  = self.count_words_null/self.count_words

        # msg    = "PseudoColumnRa_Word_Null modifying row at {ix_col_out} setting to >{a_row[ self.ix_col_out  ]}<"
        # print( msg )
        #  this seems to work but might build another way and control from gui suppress row, ?? how to use
        # self.builder.write_row     = False  # perhaps in call and return would be better

    # ----------------------------------------------
    def footer_function( self,   ):
        """
        called for footer, for now have all return a string ??  later make a generator....
        if self.count_words > 0:
            msg   = f"final value of average word rank is {self.total_word_rank/self.count_words}"
        else:
             msg   = f"final value of average word rank is undefined"
        """
        msg   = f"final value of average words.word nullis {self.count_words_null/self.count_words}"
        print( msg )
        return msg

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
        what it says .. for now it seems subclasses should make super call
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
        try to define most instance var. here to eliminate reporting errors
        Return: mutates self
        """
        self.columns_info       = build_column_info()  # dict of dicts info on each column by fully qualified column name
        self.db_name            = ""
        self.output_format      = "tablexxx"  #  "html"......
        self.db_name            = ""
        self.output_name        = None
        self.columns_out        = None     # list of names in order for the column output
        self.help_file          = "./help/build_for_default.txt"  # change to generic

        self.help_mode          = True
        self.a_word             = ""    # word for select criteria, in some cases a string
        self.my_count           = None
        self.is_covid           = ""    # select criteria on tweet
        self.default_order_by   = ""
        self.gui_order_by       = ""
        self.word_type          = "get_error"

        self.tweets_word_select     = ""
        self.words_word_select      = ""

        self.begin_dt               = datetime.datetime( 1945, 5, 24, 17, 53, 59 )
        self.end_dt                 = datetime.datetime(   1945, 5, 24, 17, 53, 59 )

        self.select_name        = "A select- name not set "   # user oriented name, same as in dropdown -- can dropdown pass itself with lambda

        self.start_time         = 0    # probably time.time() start of select
        self.end_time           = 0

        self.select_msg         = ""    # a message generated during the select ... ?? may just be an idea
        
        # list to check may not be present in any given select
        self.pseudo_columns     = [   PseudoColumnRowCount(         self ),       
                                      PseudoColumnTotalWordRank(    self ),
                                      PseudoColumnRa_Word_Rank(     self ),
                                      PseudoColumnRa_Word_Length(   self ),
                                      PseudoColumnRa_Word_Null(     self ),
                                  ]

        self.row_functions      = []    # called for each row, used with pseudo columns
        self.footer_functions   = []    # called for the footer

        self.message_function   = None   # set to a function message_function( msg ) for progress messages ?? not implemented

        self.output_append      = None

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

        self.row_functions    = []    # functions called on each row, producing column dat
        self.prior_row        = None
        self.row_to_list      = False  # convert row to a list for manipulation

    # ----------------------------------------------
    def builder_vars_as_str( self,   ):
        """
        what it says ....
        for debug gathers instance var for select ... into a string
        return string
        """
        # add more as needed, setup in setup init to avoid errors
        msg     =  "builder vars for SQLBuilder( self.x ):\n"
        msg    += f"     db_name:                   {self.db_name}\n"
        msg    += f"     select_name:               {self.select_name}\n"
        msg    += f"     output_format:             {self.output_format}\n"

        msg    += f"     columns_out:               {self.columns_out}\n"

        # ---- tweets selects
        msg    += f"     begin_dt:                  {self.begin_dt}\n"
        msg    += f"     end_dt:                    {self.end_dt}\n"

        msg    += f"     tweet_type:                {self.tweet_type}\n"
        msg    += f"     max_count:                 {self.max_count}\n"
        msg    += f"     word_type:                 {self.word_type}\n"


        msg    += f"     tweets_word_select         {self.tweets_word_select}\n"
        msg    += f"     is_covid:                  {self.is_covid}\n"


        msg    += f"     a_word:                    {self.a_word}\n"

        # ---- concord selects
        msg    += f"     concord_word_select:       {self.concord_word_select}\n"
        msg    += f"     is_ascii:                  {self.is_ascii}\n"

        # ---- words selects
        msg    += f"     words_word_select          {self.words_word_select}\n"
        msg    += f"     min_group_by_count         {self.min_group_by_count}\n"
        msg    += f"     words_is_word_null         {self.words_is_word_null}\n"

        # ---- end selcts
        msg    += f"     default_order_by:          {self.default_order_by}\n"
        msg    += f"     gui_order_by:              {self.gui_order_by}\n"
       # msg    += f"     sort_order:        {self.sort_order}\n"   # why both of them is this default set where

        msg    += f"     my_count:                  {self.my_count}\n"

        msg    += f"     sql:                       {self.sql}\n"
        msg    += f"     sql_where:                 {self.sql_where}\n"
        msg    += f"     sql_having:                {self.sql_having}\n"
        msg    += f"     sql_data:                  {self.sql_data}\n"

        msg    += f"     output_append:             {self.output_append}\n"
        msg    += f"\n\n"

        return msg

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
    def confirm_continue_0( self,   ):   #  help_mode = False
        """
        adding more common code to confirm_continue, experimenting with factoring

        """

        # next is standard this is the refactor ??

        if self.help_mode or self.output_format != "msg":
            self.display_help()
            info_msg     =    f"sql is:\n{self.sql}\n"
            AppGlobal.gui.display_info_string( info_msg )
            info_msg     =    f"sql_data is:\n{self.sql_data}"

        info_msg     = ""
        self.confirm_continue( info_msg, self.check_title,   self.check_run_select, )

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

        if AppGlobal.parameters.confirm_selects:   #  !! may still need adjust for msg format

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
        ?? flag to see if any transforms used now seems to be automatic based on
        column names
        some mutation and file output in most cases
        """
        self.start_time     = time.time()

        # check transforms to see if we need to convert to list !! for speed, but is it worth it
        # for now force it
        self.row_to_list    = True

        columns_info        = self.columns_info
        #rint( f"columns_info{columns_info}")

        file_writer         = file_writers.make_file_writer( self  )
        file_writer.write_header()

        #msg     = f"Select and output; connect to {self.db_name}"
        #rint( msg )
        sql_con = lite.connect( self.db_name )

        with sql_con:
            cur           = sql_con.cursor()
            execute_args  = ( self.sql,  self.sql_data,  )
            msg           = f"select and output; execute_args {execute_args}"
            #rint(  msg )
            AppGlobal.logger.debug( msg )
            cur.execute( *execute_args )

            while True:  # get rows one at a time in loop
                row   = cur.fetchone()
                self.write_row   = True   # this allows pseodo columns to suppress output
                if row is None:
                    break
                self.row_count    += 1
                self.prior_row     = row    # save for later use, perhaps at footer ? -- save after transform
                if self.row_to_list:        # !! efficiency tweak ... probably not worth it
                    #print( "row_to_list"  )
                    row  = list( row )

                for i_function in self.row_functions:
                    i_function( row )   # mutates row
                #rint( f"_>>>>>{row}")

                for ix_col, i_col in enumerate( row ):
                    # better ?? to put functions in a list to simplify reference
                    # indexed double dict lookup
                    i_col_info    = columns_info[ self.columns_out[ ix_col ] ]
                    transform     = i_col_info["transform"]
                    #col_text     = i_col_info["column_head"]
                    if transform is not None:
                        row[ ix_col ]    = transform( i_col )

                if self.write_row:
                    file_writer.write_row( row )   # here may need to add row count.... breaking stuff what type is row?
                # else row is suppressed

        sql_con.commit()
        sql_con.close()
        self.end_time = time.time()

        # beware this is a mess
        footer_function_info  = ""
        footer_info           = ""
        # pseudo columns and perhaps others

        #rint( f"footer functions are {self.footer_functions}" )

        for i_function in self.footer_functions:
                 #rint( "calling footer function"  )
                 foot_msg                  =   i_function(  )   # returns string
                 footer_function_info     += "\n" + foot_msg

        footer_info    +=  f"Done: >\n"
        footer_info    +=  f"     total number of rows = {self.row_count}"

        msg             =  f"     select and file write took {self.end_time - self.start_time} seconds"
        footer_info  += f"\n{msg}"
        footer_info  += f"\n{footer_function_info}"

        file_writer.write_footer( footer_info )

        print(  footer_info )
        msg      =  f"select complete with footer info: {footer_info}"
        AppGlobal.logger.debug( msg )

        # os open file for user to view
        if   self.output_format  == "html":
            AppGlobal.os_open_html_file( self.output_name )

        elif self.output_format  == "zap":
            pass
        elif self.output_format  == "msg":
            pass
            # AppGlobal.gui.do_clear_button( "dummy_event")

            # with open( self.output_name, "r", encoding = "utf8", errors = 'replace' )  as a_file:
            #     lines = a_file.readlines()
            #     # print( lines )
            #     msg  = "".join( lines )
            #     AppGlobal.gui.display_info_string( msg )

        else:
            AppGlobal.os_open_txt_file(  self.output_name )

  # ----------------------------------------------
    def go( self,  ):
        """
        after all setup is done go and do the select
        arg:  which select in builder to run, later when sub-classed just go
        """
        AppGlobal.gui.do_clear_button( "ignored" ) # check this actually works in real time !!
        try:
            self.this_select()          # configured for one of self.  ... with sub-classing always the same
            self.select_and_output()    # help_mode ??

        except app_global.UserCancel as exception:   #

            pass  # Catch the  exception and swallow as user wants out not an error
            #rint( exception )

        msg   = f"Select Done, rows selected: {self.row_count} time = {self.end_time - self.start_time}"
        AppGlobal.gui.display_info_string( msg )
        AppGlobal.logger.debug(  msg  )

   # ----------------------------------------------
    def format_sql_for_user( self  ):
        """
        ?? finish me ... I go back and forth on this, now leaning towards
        mutate self
        """
        self.display_sql   = "not implemented"

# ----------- where methods
   # ----------------------------------------------
    def add_to_where( self,    add_where = None, add_data = None,   ):
        """
        add on to where clause ok if starts at 0.  assumes and between clauses
        return mutates self -- in particular  self.sql_where self.sql_data
        """
        if self.sql_where == "":
            self.sql_where  = "\n WHERE "
        else:
            self.sql_where += " AND  "

        if add_where is not None:
            self.sql_where   +=  add_where
            if add_data is not None:
                self.sql_data.append( add_data )

    # ----------------------------------------------
    def add_to_where_dates( self,   ):
        """
        what it says ....
        return mutates self -- in particular  self.sql_where self.sql_data
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
    def add_to_where_is_covid( self  ):
        """
        return mutates self -- in particular  self.sql_where self.sql_data
        """
        #  --------tweets is_covid
        is_covid   = self.is_covid
        if is_covid is not None:

            if is_covid:
                self.add_to_where( add_where = f"\n{indent}tweets.is_covid   ",
                                   add_data = None )

            else:
                self.add_to_where( add_where = f"\n{indent}NOT tweets.is_covid   ",
                                   add_data = None )

   # ----------------------------------------------
    def add_to_where_is_ascii( self  ):
        """
        return mutates self -- in particular  self.sql_where self.sql_data
        """
        #  --------concord is_ascii-- ok
        is_ascii   = self.is_ascii
        if is_ascii is not None:

            if is_ascii:
                self.add_to_where( add_where = f"\n{indent}concord.is_ascii   ",
                                   add_data = None )

            else:
                self.add_to_where( add_where = f"\n{indent}NOT concord.is_ascii   ",
                                   add_data = None )

   # ----------------------------------------------
    def add_to_where_word_like( self  ):
        """
        return mutates self -- in particular  self.sql_where self.sql_data
        """
        # --------- word  ... consider auto adding of wild char at both ends
        # --------- tweets.word   consider auto adding of wild char at both ends
        a_word    = self.tweets_word_select
        if a_word != "":
            a_word    = a_word.lower()
            self.add_to_where( add_where  = f'\n{indent}lower( tweets.tweet )  LIKE  "%{a_word}%"',     # sql inject
                               add_data   = None  )

   # ----------------------------------------------
    def add_to_where_tweet_type( self  ):
        """
        return mutates self -- in particular  self.sql_where self.sql_data
        """
        # ----- tweet_type
        tweet_type      =   self.tweet_type
        if tweet_type is not None:
             self.add_to_where( add_where = f"\n{indent}tweets.tweet_type = ? ",
                               add_data = tweet_type  )

   # ----------------------------------------------
    def add_to_where_concord_word_like( self  ):
        """
        return mutates self -- in particular  self.sql_where self.sql_data
        """
        # --------- word  ... consider auto adding of wild char at both ends
        # --------- tweets.word   consider auto adding of wild char at both ends
        a_word    = self.concord_word_select
        if a_word != "":
            self.add_to_where( add_where  = f'\n{indent}concord.word  LIKE  "{a_word}"  ',     # sql inject
                               add_data   = None  )
   # ----------------------------------------------
    def add_to_where_concord_word_type( self  ):
        """
        return mutates self -- in particular  self.sql_where self.sql_data
        """
        # ----- concord word_type
        word_type      =   self.concord_word_type_select
        if word_type is not None:
             self.add_to_where( add_where = f"\n{indent}concord.word_type = ? ",
                               add_data = word_type  )

   # ----------------------------------------------
    def add_to_where_words_word( self  ):
        """
        return mutates self -- in particular  self.sql_where self.sql_data
        """
        a_word    = self.words_word_select
        if a_word != "":
            a_word    = a_word.lower()
            self.add_to_where( add_where  = f'\n{indent}words.word LIKE  ? ',
                               add_data   = a_word  )

   # ----------------------------------------------
    def add_to_where_words_word_null( self  ):
        """
        return mutates self -- in particular  self.sql_where self.sql_data
        """
        is_null     = self.words_is_word_null
        if is_null is None:
            return
        if is_null:
            self.add_to_where( add_where  = f'\n{indent}words.word IS NULL ',
                               add_data   = None )
        else:
            self.add_to_where( add_where  = f'\n{indent}words.word IS NOT NULL ',
                               add_data   = None )

# ----------------------------------------
class Select_01( SQLBuilder  ):
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
        #rint( "init Select_01")
        super().__init__(  )

    # ----------------------------------------------
    def this_select( self,  ):
        #rint( "this select TweetSelect1")
        # ----------------------------------------------
        msg   = f"tweet_select_1 builder vars: {self.builder_vars_as_str()}"
        print( msg  )
        AppGlobal.logger.debug(  msg  )

        # self.columns_out      = [ "tweets.tweet_datetime", "tweets.tweet_type",  "tweets.tweet", "tweets.tweet_id"    ]

        # --- not sure think sets up pseudo columns if in column list
        for i_pc in self.pseudo_columns:
            i_pc.config()
        self.sql           =  "SELECT  " + ", ".join( self.columns_out  ) + " FROM tweets "

        #  -------- dates
        self.add_to_where_dates(   )

        #  -------- tweet_type
        tweet_type   = self.tweet_type
        if tweet_type is not None:
               self.add_to_where( add_where = f"\n{indent}tweets.tweet_type = ?   ",
                                  add_data = tweet_type )

        # --------- word  ... consider auto adding of wild char at both ends
        # --------- tweets.word   consider auto adding of wild char at both ends
        a_word    = self.tweets_word_select
        if a_word != "":
            a_word    = a_word.lower()
            self.add_to_where( add_where  = f'\n{indent}lower( tweets.tweet )  LIKE  "%{a_word}%"',     # sql inject
                               add_data   = None  )

        self.add_to_where_is_covid()

        self.sql   += self.sql_where

        # still need to fix order by
        # self.sql   +=   f"\n{indent}ORDER BY tweets.tweet_datetime "
        self.sql   +=   f"\n{indent}ORDER BY {self.gui_order_by} "

        # next is standard refactor ??
        self.display_help()
        info_msg     =    f"sql is:\n{self.sql}\n"
        AppGlobal.gui.display_info_string( info_msg )
        info_msg     =    f"sql_data is:\n{self.sql_data}"

        self.confirm_continue( info_msg, self.check_title,   self.check_run_select, )

# ----------------------------------------
class Select_Msg_01( SQLBuilder  ):
    """
    see parent SQLBuilder
    is this the same as Select_01 ??
    """
    def __init__( self,  ):
        """
        what it says
        """
        #print( "init Select_01")
        super().__init__(  )

    # ----------------------------------------------
    def this_select( self,  ):
        #rint( "this select TweetSelect1")
        # ----------------------------------------------
        msg   = f"tweet_select_1 builder vars: {self.builder_vars_as_str()}"
        print( msg  )
        AppGlobal.logger.debug(  msg  )

        # self.columns_out      = [ "tweets.tweet_datetime", "tweets.tweet_type",  "tweets.tweet", "tweets.tweet_id"    ]

        # --- not sure think sets up pseudo columns if in column list
        for i_pc in self.pseudo_columns:
            i_pc.config()
        self.sql           =  "SELECT  " + ", ".join( self.columns_out  ) + " FROM tweets "

        #  -------- dates
        self.add_to_where_dates(   )

        #  -------- tweet_type
        tweet_type   = self.tweet_type
        if tweet_type is not None:
               self.add_to_where( add_where = f"\n{indent}tweets.tweet_type = ?   ",
                                  add_data = tweet_type )

        # --------- word  ... consider auto adding of wild char at both ends
        # --------- tweets.word   consider auto adding of wild char at both ends
        a_word    = self.tweets_word_select
        if a_word != "":
            a_word    = a_word.lower()
            self.add_to_where( add_where  = f'\n{indent}lower( tweets.tweet )  LIKE  "%{a_word}%"',     # sql inject
                               add_data   = None  )

        self.add_to_where_is_covid()

        self.sql   += self.sql_where

        self.sql   +=   f"\n{indent}ORDER BY {self.gui_order_by} "

        self.confirm_continue_0()

# ----------------------------------------
class Select_02( SQLBuilder  ):
#class Select_02( SQLBuilder  ):   # !! update
    """
    specialized descendant of SQLBuilder for a particular select see help doc
    """
    def __init__( self,  ):
        """
        what it says
        """
        #rint( "init ConcordSelect1")
        super().__init__(  )

    # ----------------------------------------------
    def this_select( self,  ):
        print( "Select_02")

        # debug
        msg    = self.builder_vars_as_str()
        AppGlobal.logger.debug( msg )
        print( msg )

        self.columns_out      = [
                                  ROW_COUNT_CN,
                                  "concord.word",
                                  "concord.word_type",
                                  "concord.is_ascii",
                                  "my_count",
                                 ]

        # --- not sure think sets up pseudo columns if in column list
        for i_pc in self.pseudo_columns:
            i_pc.config()

        # !! build from columns out -- but my count still an issue do a replace
        self.sql           =  ( "SELECT " + ", ".join( self.columns_out  ) + " " +
                                    "FROM concord " +
                                    "JOIN tweets  ON concord.tweet_id = tweets.tweet_id "
                                    )

        self.sql           = self.sql.replace( "my_count", " COUNT(*) AS my_count ")
        # # pseudo_columns after set up in both sql and columns out
        # for i_pc in self.pseudo_columns:
        #     i_pc.config()

        #  ---- tweets
        self.add_to_where_dates()
        self.add_to_where_tweet_type()
        self.add_to_where_word_like()

        # ---- concord
        self.add_to_where_concord_word_type()
        self.add_to_where_is_ascii()
        self.add_to_where_concord_word_like()

        # !! may still need more -- check it out

        self.sql   += self.sql_where

        self.sql   +=  (  f"GROUP BY concord.word " )

        if self.min_group_by_count is not None:
            self.sql_having   =   f"\n{indent}HAVING ( my_count > ? ) "
            self.sql_data.append( self.min_group_by_count )

        self.sql   +=  self.sql_having

        self.sql   +=   f"\n{indent}ORDER BY {self.gui_order_by} "

        #self.sql   +=  f"\n{indent}ORDER BY my_count Desc, concord.word "

        self.display_help()
        info_msg     =    f"sql is:\n{self.sql}\n"
        AppGlobal.gui.display_info_string( info_msg )
        info_msg     =    f"sql_data is:\n{self.sql_data}"

        self.confirm_continue( info_msg, self.check_title,   self.check_run_select, )

# ----------------------------------------
class Select_03( SQLBuilder  ):
    """
    see SQLBuilder
    this select is specialized as describe in this_select
    """
    def __init__( self,  ):
        """
        what it says
        """
        #rint( "init Select_03")
        super().__init__(  )

    # ----------------------------------------------
    def this_select( self,  ):
        """
        see SQLBuilder
        three way join
        select pretty much uses all gui criteria, and should be good on most sort orders !! check
        """
        self.select_name   = "select_name = select_03"
        # self.tweet_joined_select_1( select_name,   )

        # debug
        msg    = self.builder_vars_as_str()
        AppGlobal.logger.debug( msg )
        print( msg )

        # --- not sure think sets up pseudo columns if in column list
        for i_pc in self.pseudo_columns:
            i_pc.config()

        self.sql           = "SELECT DISTINCT " + ", ".join( self.columns_out  ) + " "

        self.sql           += f"\n{indent}FROM concord "

        self.sql           += f"\n{indent}JOIN tweets  ON concord.tweet_id = tweets.tweet_id  "

        self.sql           += f"\n{indent}LEFT OUTER JOIN words  ON concord.word = words.word  "

        #---- where self.sql_where

        # ---------tweets.word
        if self.tweets_word_select != "":
            self.add_to_where( add_where  = f'\n{indent}tweets.tweet  LIKE     "{self.tweets_word_select}"',     # need quotes ??
                               add_data   = None  )

        #  -------- tweets dates
        self.add_to_where_dates(   )

        #  --------tweets is_covid
        is_covid   = self.is_covid
        if is_covid is not None:

            if is_covid:
                self.add_to_where( add_where = f"\n{indent}tweets.is_covid   ",
                                   add_data = None )

            else:
                self.add_to_where( add_where = f"\n{indent}NOT tweets.is_covid   ",
                                   add_data = None )

        #  -------- tweet_type
        tweet_type   = self.tweet_type
        if tweet_type is not None:
               self.add_to_where( add_where = f"\n{indent}tweets.tweet_type = ?   ",
                                  add_data = tweet_type )

        #  --------concord
        self.add_to_where_is_ascii()

        # ----- concord word_type
        self.add_to_where_concord_word_type()
        self.add_to_where_concord_word_like()

        # ---- words ?? still need more
        self.add_to_where_words_word()

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

        self.confirm_continue( info_msg, self.check_title,   self.check_run_select, )
        
# ----------------------------------------
class Select_04( SQLBuilder  ):
    """
    see SQLBuilder
    this select is specialized as describe in this_select
    """
    def __init__( self,  ):
        """
        what it says
        """
        #rint( "init Select_03")
        super().__init__(  )

    # ----------------------------------------------
    def this_select( self,  ):
        """
        see SQLBuilder
        three way join
        select pretty much uses all gui criteria, and should be good on most sort orders !! check
        """
        self.select_name   = "select_name = select_04"
        # self.tweet_joined_select_1( select_name,   )

        # debug
        msg    = self.builder_vars_as_str()
        AppGlobal.logger.debug( msg )
        print( msg )

        # --- not sure think sets up pseudo columns if in column list
        for i_pc in self.pseudo_columns:
            i_pc.config()

        self.sql           = "SELECT DISTINCT " + ", ".join( self.columns_out  ) + " "

        self.sql           += f"\n{indent}FROM concord "

        self.sql           += f"\n{indent}JOIN tweets  ON concord.tweet_id = tweets.tweet_id  "

        self.sql           += f"\n{indent}LEFT OUTER JOIN words  ON concord.word = words.word  "

        #LEFT   JOIN effects e2 ON e2.id = i.effect2

        #-------------------- where self.sql_where

        # ---------tweets.word
        if self.tweets_word_select != "":
            self.add_to_where( add_where  = f'\n{indent}tweets.tweet  LIKE     "{self.tweets_word_select}"',     # need quotes ??
                               add_data   = None  )

        #  -------- tweets dates
        self.add_to_where_dates(   )

        #  --------tweets is_covid
        is_covid   = self.is_covid
        if is_covid is not None:

            if is_covid:
                self.add_to_where( add_where = f"\n{indent}tweets.is_covid   ",
                                   add_data = None )

            else:
                self.add_to_where( add_where = f"\n{indent}NOT tweets.is_covid   ",
                                   add_data = None )

        #  --------concord is_ascii-- ok
        is_ascii   = self.is_ascii
        if is_ascii is not None:

            if is_ascii:
                self.add_to_where( add_where = f"\n{indent}concord.is_ascii   ",
                                   add_data = None )

            else:
                self.add_to_where( add_where = f"\n{indent}NOT concord.is_ascii   ",
                                   add_data = None )

        # ----- concord word_type
        word_type      =   self.concord_word_type_select
        if word_type is not None:
             self.add_to_where( add_where = f"\n{indent}concord.word_type = ? ",
                               add_data = word_type  )

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

        self.confirm_continue( info_msg, self.check_title,   self.check_run_select, )

# ----------------------------------------
class Select_04_old_new_from_03( SQLBuilder  ):
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
        print( "this_select Select_04")
        select_name = "joe"

        self.select_name   = "joe select_04"
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

        self.confirm_continue( info_msg, self.check_title,   self.check_run_select, )

# ----------------------------------------
class Select_05( SQLBuilder  ):
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
        #rint( "init TweetSelect1")
        super().__init__(  )

    # ----------------------------------------------
    def this_select( self,  ):
        #rint( "this select TweetSelect1")
        # ----------------------------------------------
        msg   = f"tweet_select_1 builder vars: {self.builder_vars_as_str()}"
        #rint( msg  )
        AppGlobal.logger.debug(  msg  )

        self.sql           = "SELECT  " +  ", ".join( self.columns_out  ) + " "

        self.sql           += f"\n{indent}FROM tweets "

        # pseudo_columns after set up in both sql and columns out
        for i_pc in self.pseudo_columns:
            i_pc.config()

        #  -------- dates
        self.add_to_where_dates(   )

        #  -------- tweet_type
        tweet_type   = self.tweet_type
        if tweet_type is not None:
               self.add_to_where( add_where = f"\n{indent}tweets.tweet_type = ?   ",
                                  add_data = tweet_type )

        # --------- word  ... consider auto adding of wild char at both ends
        if self.a_word != "":
            self.a_word    = self.a_word.lower()
            self.add_to_where( add_where  = f'\n{indent}lower( tweets.tweet )  LIKE  "%{self.a_word}%"',     # sql inject
                               add_data   = None  )

        self.sql   += self.sql_where

        sort_order      = self.sort_order
        if  sort_order  in   [ "tweets.tweet_datetime, tweets.tweet_type",
                               "tweets.tweet_type, tweets.tweet_datetime" ]:
            pass
        else:
            sort_order = "tweets.tweet_datetime, tweets.tweet_type"

        self.sql   +=   f"\n{indent}ORDER BY {sort_order} "

        # next is standard refactor    see confirm_...._0
        self.display_help()
        info_msg     =    f"sql is:\n{self.sql}\n"
        AppGlobal.gui.display_info_string( info_msg )
        info_msg     =    f"sql_data is:\n{self.sql_data}"

        self.confirm_continue( info_msg, self.check_title,   self.check_run_select, )

# ----------------------------------------
class Select_06( SQLBuilder  ):
    """
    see SQLBuilder
    this select is specialized as describe in this_select
    """
    def __init__( self,  ):
        """
        what it says
        """
        #rint( "init Select_06")
        super().__init__(  )

    # ----------------------------------------------
    def this_select( self,  ):
        """
        see SQLBuilder
        three way join
        lets try to make this a word rank average ... run the average against the row data
        select pretty much uses all gui criteria, and should be good on most sort orders !! check
        """
        # should be set in tweet_app self.select_name   = "select_name = select_06"
        #rint( f"this_select {self.select_name}")

        msg    = self.builder_vars_as_str()
        AppGlobal.logger.debug( msg )
        #rint( msg )   # debug

        # perhaps move back to controller   !! show why want columms_select and colums_out
        self.columns_out      = [
                                 ROW_COUNT_CN,
                                 "my_count",      # see replace below
                                 "concord.word",
                                 "concord.word_type",
                                 "concord.is_ascii",
                                 "words.word",
                                 "words.word_rank",
                                 RA_WORD_RANK,
                                 RA_WORD_LENGTH,
                                 RA_WORD_NULL,
                                 ]

        # --- sets up pseudo columns if in column list
        for i_pc in self.pseudo_columns:
            i_pc.config()

        self.sql           = "SELECT DISTINCT " + ", ".join( self.columns_out  ) + " "

        self.sql           = self.sql.replace( "my_count", " COUNT(*) AS my_count ")

        self.sql           += f"\n{indent}FROM concord "

        self.sql           += f"\n{indent}JOIN tweets  ON concord.tweet_id = tweets.tweet_id  "

        self.sql           += f"\n{indent}LEFT OUTER JOIN words  ON concord.word = words.word  "

        #LEFT   JOIN effects e2 ON e2.id = i.effect2

        #-------------------- where self.sql_where  --- note these are old style, change to function calls !!
        # ----- word
        if self.a_word != "":
            self.add_to_where( add_where  = f'\n{indent}concord.word  LIKE     "{self.a_word}"',     # need quotes ??
                               add_data   = None  )

        #  ----- dates
        self.add_to_where_dates()

        self.add_to_where_is_ascii()

        #  -----is_covid -- ok
        is_covid   = self.is_covid
        if is_covid is not None:

            if is_covid:
                self.add_to_where( add_where = f"\n{indent}tweets.is_covid   ",  # syntax for boolean
                                   add_data = None )

            else:
                self.add_to_where( add_where = f"\n{indent}NOT tweets.is_covid   ",
                                   add_data = None )

        #  ----- max_count
        max_count   = self.max_count
        if max_count is not None:
               self.add_to_where( add_where = f"\n{indent}words.word_count < ?   ",
                                  add_data = max_count )

        #  ----- builder.min_rank
        min_rank   = self.min_rank
        if min_rank is not None:
               self.add_to_where( add_where = f"\n{indent}words.word_rank > ?   ",
                                  add_data = min_rank )

        #  ----- tweet_type
        tweet_type   = self.tweet_type
        if tweet_type is not None:
               self.add_to_where( add_where = f"\n{indent}tweets.tweet_type = ?   ",
                                  add_data = tweet_type )

        # ----- word_type
        word_type      =   self.word_type
        if word_type is not None:
             self.add_to_where( add_where = f"\n{indent}concord.word_type = ? ",
                               add_data = word_type  )
        # -----
        self.add_to_where_words_word_null()

        # ---------- final where ....wrap it up -- if no where's adds ""
        self.sql   += self.sql_where         # wrap it up -- if now where adds ""

        # ----- group by
        self.sql   +=  (  f"\n{indent}GROUP BY concord.word " )

        # ----- order by
        gui_order_by    = self.gui_order_by
        if gui_order_by == "default":
            #self.sql           +=  f"\n{indent}ORDER BY " + self.default_order_by
            self.sql           +=  f"\n{indent}ORDER BY words.word_rank "
        else:
            self.sql           +=  f"\n{indent}ORDER BY " + gui_order_by

        self.display_help()   # move more to confirm and continue ??

        info_msg     =    f"sql is:  {self.sql}"
        AppGlobal.gui.display_info_string( info_msg )
        print( info_msg )

        info_msg     =    f"sql_data is:  {self.sql_data}"
        AppGlobal.gui.display_info_string( info_msg )
        print( info_msg )

        self.confirm_continue( info_msg, self.check_title,   self.check_run_select, )

# ----------------------------------------
class Select_07( SQLBuilder  ):
    """
    see SQLBuilder
    this select is specialized as describe in this_select
    """
    def __init__( self,  ):
        """
        what it says
        """
        #print( "init Select_07")
        super().__init__(  )

    # ----------------------------------------------
    def this_select( self,  ):
        """
        see SQLBuilder
        just words
        lets try to make this a word rank average ... run the avearge against the row data
        select pretty much uses all gui criteria, and should be good on most sort orders !! check
        """
        # should be set in tweet_app self.select_name   = "select_name = select_06"
        #rint( f"this_select {self.select_name}")

        # debug
        msg    = self.builder_vars_as_str()
        AppGlobal.logger.debug( msg )
        #rint( msg )


        # --- not sure think sets up pseudo columns if in column list
        for i_pc in self.pseudo_columns:
            i_pc.config()

        self.sql           = "SELECT  " + ", ".join( self.columns_out  ) + " "
        self.sql           = self.sql.replace( "my_count", " COUNT(*) AS F ")  # if using the psudo column

        self.sql           += f"\n{indent}FROM words "

        #-------------------- where self.sql_where
        # ----- word
        if self.words_word_select != "":
            self.add_to_where( add_where  = f'\n{indent}words.word  LIKE   ?',
                               add_data   = self.words_word_select  )

        #  ----- max_count
        max_count   = self.max_count
        if max_count is not None:
               self.add_to_where( add_where = f"\n{indent}words.word_count < ?   ",
                                  add_data = max_count )

        #  ----- builder.min_rank
        min_rank   = self.min_rank
        if min_rank is not None:
               self.add_to_where( add_where = f"\n{indent}words.word_rank > ?   ",
                                  add_data = min_rank )

        # ---------- final where ....wrap it up -- if no where's adds ""
        self.sql   += self.sql_where         # wrap it up -- if now where adds ""

        # ----- order by  !! need to look at some more
        gui_order_by    = self.gui_order_by
        # gui_order_by    = "default"           #   !! fix me
        # if gui_order_by == "default":
        #     #self.sql           +=  f"\n{indent}ORDER BY " + self.default_order_by
        #     self.sql           +=  f"\n{indent}ORDER BY words.word_rank "
        # else:
        self.sql           +=  f"\n{indent}ORDER BY " + gui_order_by

        self.display_help()   # move more to confirm and continue ??

        info_msg     =    f"sql is:  {self.sql}"
        AppGlobal.gui.display_info_string( info_msg )
        print( info_msg )

        info_msg     =    f"sql_data is:  {self.sql_data}"
        AppGlobal.gui.display_info_string( info_msg )
        print( info_msg )

        self.confirm_continue( info_msg, self.check_title,   self.check_run_select, )

# ----------------------------------------
class SliderSelect1( SQLBuilder  ):
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
        #rint( "init SliderSelect1")
        super().__init__(  )

    # ----------------------------------------------
    def this_select( self,  ):
        print( "this select SliderSelect1")
        # ----------------------------------------------

        msg   = f"tweet_select_1 builder vars: {self.builder_vars_as_str()}"
        print( msg  )
        AppGlobal.logger.debug(  msg  )

        columns            = self.columns_out
        self.sql           = "SELECT  " + ", ".join( columns  ) + " "
        self.sql           += f"\n{indent} FROM tweets "

        # self.sql              = (
        #     "\n SELECT tweets.tweet_datetime, tweets.tweet_type, tweets.tweet, tweets.tweet_id  "
        #     "FROM tweets "
        #     )

        #  -------- dates
        self.add_to_where_dates(   )

        #  -------- tweet_type  -- may hardcode later or not
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
class Select_X1( SQLBuilder  ):
# from Select_02( SQLBuilder  ):
    """
    specilized decendant of SQLBuilder for a particular select see help doc
    """
    def __init__( self,  ):
        """
        what it says
        """
        #rint( "init ConcordSelect1")
        super().__init__(  )

    # ----------------------------------------------
    def this_select( self,  ):
        print( "Select_X1")

        # !! build from columns out -- but my count still an issue do a replace
        self.sql           = "SELECT  " +  ", ".join( self.columns_out  ) + " "
        self.sql           = self.sql.replace( "my_count", " COUNT(*) AS my_count ")

        self.sql          += (
            "\nFROM concord "
            "\nJOIN tweets  ON concord.tweet_id = tweets.tweet_id "
            )

        # pseudo_columns after set up in both sql and columns out
        for i_pc in self.pseudo_columns:
            i_pc.config()

        #  -------- dates
        self.add_to_where_dates(   )

        # ----- tweet_type
        self.add_to_where_tweet_type()
        # tweet_type      =   self.tweet_type
        # if tweet_type is not None:
        #      self.add_to_where( add_where = f"\n{indent}tweets.tweet_type = ? ",
        #                        add_data = tweet_type  )

        # # ----- word_type
        # word_type      =   self.word_type
        # if word_type is not None:
        #      self.add_to_where( add_where = f"\n{indent}concord.word_type = ? ",
        #                        add_data = word_type  )

        #  --------concord is_ascii-- ok
        self.add_to_where_is_ascii()

        # is_ascii   = self.is_ascii
        # if is_ascii is not None:

        #     if is_ascii:
        #         self.add_to_where( add_where = f"\n{indent}concord.is_ascii   ",
        #                            add_data = None )

        #     else:
        #         self.add_to_where( add_where = f"\n{indent}NOT concord.is_ascii   ",
        #                            add_data = None )

        # --------- tweets.word   consider auto adding of wild char at both ends

        self.add_to_where_word_like()

        # concord_word
        self.add_to_where_concord_word_like()
        self.add_to_where_concord_word_type()

        # a_word    = self.tweets_word_select
        # if a_word != "":
        #     a_word    = a_word.lower()
        #     self.add_to_where( add_where  = f'\n{indent}lower( tweets.tweet )  LIKE  "{a_word}"',     # sql inject
        #                        add_data   = None  )

        self.sql   += self.sql_where

        # might switch on off this from gui
        # self.sql   +=  (  f"GROUP BY concord.word " )

        # !! not clear what is up here
        # if self.my_count is not None:
        #     self.sql_having   =   f"\n{indent}HAVING ( my_count > ? ) "
        #     self.sql_data.append( self.my_count )

        self.sql   +=  self.sql_having

        self.sql   +=   f"\n{indent}ORDER BY {self.gui_order_by} "

        #self.sql   +=  f"\n{indent}ORDER BY my_count Desc, concord.word "

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






