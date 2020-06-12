# -*- coding: utf-8 -*-
"""
define/load tweet data to populate tweets and concord


"""

#import sys
#import string
#import collections
import spacy          # linguistic module words to lemmas ( might not be correct explain )
import datetime
import sqlite3 as lite

from   app_global import AppGlobal
#import app_global

nlp             = spacy.load( 'en_core_web_sm'   )    # object to do spacy processing
                                                      # example used 'en' but throws error
                                                      # had fight installing
numerals        = set( "0123456789" )   # use to eliminate words that are not words words do not start with numerals so this will get them out

# also consider  other bad prefixes  like $  but maybe spacy does it all ?

datetime_fmt     = "%m-%d-%Y %H:%M:%S"           # use to convert strings to datetimes

people_words     = None

#------ covid words
covid_words      = set( [ "covid-19"
                         ,"covid"
                         ,"coronavirus"
                         ,"crisis"
                         ,"deaths"
                         ,"fatalities"
                         ,"ppp"
                         ,"paycheckprotectionprogram"
                         ,"social-distancing"
                         ,"coronavirus-ravaged"
                         ,"covid19"
                         ,"fauci"
                         ,"hydroxychloroquine"
                         ,"ppe"
                         ,"respiratory"
                         ,"sbagov"
                         ,"smallbiz"
                         ,"smallbusiness"
                         ,"transmission"
                         ,"transmitted"
                         ,"ventilators"
                         ,"virus"
                         ,"covid"
                         ,"covid"
                         ,"covid"
                         ,"covid"

                         ,
                         ]  )

# -------------------- replace list --------------------
"""
replace list is to get rid of non ascii stuff and convert to something
that may be parsed later
"we

"""
# this really should only be non ascii char
replace_list      = [  ( "’", "'"   )
                     , ( "”", '"'   )
                     , ( "“", '"'   )
                     , ( "…", "..." )
                     , ( ",", " "   )   # to white ... or iterate through punctuation
                     , ( "↓", " "   )   # to white ... or iterate through punctuation
                     , ( "‘", " "   )

                    ]

"""
also found
⚙️⛰️🇺🇸
""
"""

remove_ascii        = "\"!$%&'()*+,-./:;<=>?[\]^_`{|}~"   # removable ascii not @ #  not ' as may be a contraction
# for i_char in remove_ascii:
#     print( i_char )


# ----------------------------------------------
def is_ascii( string_like ):
    """
    what it says: is string_like ascii
    return bool
    """
    try:
        string_like.decode('ascii')
    except UnicodeDecodeError:
        #rint "it was not a ascii-encoded unicode string"
        return False
    else:
        #rint "It may have been an ascii-encoded unicode string"
        return True

# ----------------------------------------------
def define_table_concord( db_name, allow_drop = False ):
    """
    what it says
    """
    #rint( "  ============= define_table_concord() db {db_name} drop {allow_drop}========== " )

    try:
        sql_con = lite.connect( db_name )

        with sql_con:
            cur = sql_con.cursor()
            if allow_drop:
               cur.execute("DROP TABLE IF EXISTS concord")   # else error if table exists

            cur.execute(
                "CREATE TABLE concord( "
                "word      Text, "
                "tweet_id  Text, "  # , " on most ) on last
                "word_type Int, "     # word types in  AppGlobal.word_types[ "word" ]
                "is_ascii  BOOLEAN )"
                )

    except lite.Error as a_except:
     #except ( lite.Error, TypeError) as a_except:
         print( type(a_except), '::', a_except )
         msg   = "error util_create_table_concord, exception {a_except}"
         AppGlobal.logger.error( msg )
         print( msg )
         raise

    sql_con.close()

# ---------------------------------------------
def define_table_tweets( db_name, allow_drop = False ):
    """
    what it says
    """
    print( f"  ====== define_table_tweets() db {db_name} drop {allow_drop}========== "  )
    try:
        sql_con = lite.connect( db_name )

        with sql_con:
            cur = sql_con.cursor()
            if allow_drop:
               cur.execute("DROP TABLE IF EXISTS tweets")   # else error if table exists

            # 8   dbcolumns
            cur.execute(
                "CREATE TABLE tweets( "
                "tweet_datetime DATETIME, "
                "time_of_day TEXT, "
                "is_covid   BOOLEAN, "
                "line_no    INT, "
                "tweet_type TEXT, "
                "tweet      TEXT, "
                "tweet_id   TEXT, "
                "who        TEXT, "
                "PRIMARY KEY (tweet_id ) ) "
                )

    except lite.Error as a_except:     #except ( lite.Error, TypeError) as a_except:
         print( type(a_except), '::', a_except )
         print( "error create_table_tweets, exception {a_except}" )
         raise

    sql_con.close()

    def __str__( self,  ):
        my_str    = "parsed_tweet = "
        my_str    = f"{my_str}\n  tweet_cleaned:        {self.tweet_cleaned}"
        #my_str    = f"{my_str}\n  concordance_words:    {info_about_list( self.concordance_words )}"
        #my_str    = f"{my_str}\n  concordance_words:    {self.concordance_words}"

# ----------------------------------------
def list_to_str( a_obj, msg = "for a list:" ):
    if  isinstance( a_obj, list ):
        my_str    = f"{msg} = "
        my_str    = f"{my_str}\n  length of list is: {len( a_obj )}"
        #my_str    = f"{my_str}\n  length of list is: {len( a_obj )}"
        for  i_list in a_obj:
             my_str    = f"{my_str}\n     ** {i_list}"

    else:
        my_str    = f"\nfor msg = {msg} object is not an instance of list but is a {type(a_obj)}"

    return my_str


# ==========================================
class ConcordanceWord( ):
    """
    basically a struct ( could put in parse functions here but not now )
    we will store words here prior to saving

    """
    def __init__( self, a_string, tweet_id ):
        """
        ?? change to create with type as well

        """
        pass
        self.reset_data( a_string, tweet_id )

    # ----------------------------------------
    def __str__( self,  ):
        my_str    = "ConcordanceWord = "
        my_str    = f"{my_str}\n  string:       {self.string}"
        my_str    = f"{my_str}\n  is_ascii:     {self.is_ascii}"
        my_str    = f"{my_str}\n  type:         {self.type}"

        return my_str
    #------------------
    def reset_data( self, a_string, tweet_id ):
        """
        """
        self.string     = a_string
        self.type       = AppGlobal.word_types["word"]
        #self.is_covid   = not used at this level, see tweets
        self.is_ascii   = True
        self.tweet_id   = tweet_id

# ==========================================
class ParsedTweet( ):
    """
    basically a self parsing  structure
    ?? this should probably have internal method renamed with _xxx

    """
    def __init__( self, tweet, tweet_id ):
        pass
        self.reset_data( tweet, tweet_id )

    #------------------
    def reset_data( self, tweet, tweet_id ):
        """
        most of this stuff will probably be mutated, partly here for doc

        we build up the list  self.concordance_words and...

        pretty much all of these instance var
        """
        self.concordance_words    = []     # what do we put in the list concordance_word
        self.tweet_raw            = tweet
        self.tweet_cleaned        = tweet  # will be mutated # check we are doing this right
        #self.is_retweet           = False
        self.is_covid             = False
        self.tweet_id             = tweet_id
        self.tweet_datetime       = None    # next from where data line is split
        self.time_of_day          = None    # a 24 hr clock... as a string
        #self.tweet_id             = None
        self.line_no              = 0
        self.tweet_type           = "tweet"   # what are the types
        self.who_tweets           = "?"

    # ----------------------------------------
    def __str__( self,  ):
        my_str    = "parsed_tweet = "
        my_str    = f"{my_str}\n  tweet_cleaned:        {self.tweet_cleaned}"
        my_str    = f"{my_str}\n  concordance_words:    {list_to_str( self.concordance_words )}"
        #my_str    = f"{my_str}\n  concordance_words:    {self.concordance_words}"

        return my_str

    # ----------------------------------------
    def parse_me( self, ):
        """


        """
        self._clean_tweet(  )
        self._tweet_to_concordance_words()

    # ----------------------------------------
    def _apply_replace_list( self,  ):
        """
        mutates self.tweet_cleaned
        mostly removes non ascii, not for punctuation  look for it ....
        """
        for i_replace in replace_list:
            a, b        = i_replace
            self.tweet_cleaned    = self.tweet_cleaned.replace( a, b )

    # ----------------------------------------
    def _extract_urls( self,  ):
        """
        returns mutates self, self.tweet_cleaned and self.concordance_words
        """
        continue_flag  = True
        while continue_flag:
            continue_flag  = self._extract_a_url(  )

    # ----------------------------------------
    def _extract_a_url( self,  ):
        """
        look for one url at end of tweet and in tweet.
        watch for early return?
        returns  True if one extracted and  mutates self, self.tweet_cleaned and self.concordance_words

        better ?? use tuple unpack -- did second time... looks better -- slightly
        """
        a_rpartition    =  self.tweet_cleaned.rpartition( "http:"   )

        if a_rpartition[0] != "":

            self.tweet_cleaned   = a_rpartition[ 0 ]      # mutate with url removed
            word                 = a_rpartition[ 1 ] +  a_rpartition[ 2 ]
            #msg = f"found  http:  >{word}<  partition tuple >>>>>>  >{a_rpartition[ 0 ]}< >{a_rpartition[ 1 ]}< >{a_rpartition[ 2 ]}<"
            #rint( msg )
            # if we can then partition on a space ( any whitespace ?? )
            # put that peice back else put whole tail back
            partition_url_0, partition_url_1, partition_url_2     =  word.partition( " " )
            #rint( f">>>>>>partition tuple >>>>>>  {partition_url_0}< >{partition_url_1}< >{partition_url_2}<" )
            if partition_url_2 != "":
                word  = partition_url_0
                self.tweet_cleaned   += " " + partition_url_2
                #rint( f"**>>>>>>partition tuple >>>>>>  {partition_url_0}< >{partition_url_1}< >{partition_url_2}<" )

            concordance_word         = ConcordanceWord( word, self.tweet_id )
            concordance_word.type    = AppGlobal.word_types["url"]
            self.concordance_words.append(  concordance_word  )
            return True

        a_rpartition    =  self.tweet_cleaned.rpartition( "https:"   )

        if a_rpartition[0] != "":

            self.tweet_cleaned   = a_rpartition[ 0 ]      # mutate with url removed
            word                 = a_rpartition[ 1 ] +  a_rpartition[ 2 ]
            # msg = f"found  https:  >{word}<  partition tuple >>>>>>  >{a_rpartition[ 0 ]}< >{a_rpartition[ 1 ]}< >{a_rpartition[ 2 ]}<"
            #rint( msg )
            partition_url_0, partition_url_1, partition_url_2     =  word.partition( " " )
            #rint( f">>>>>>partition tuple >>>>>>  {partition_url_0}< >{partition_url_1}< >{partition_url_2}<" )
            if partition_url_2 != "":
                word  = partition_url_0
                self.tweet_cleaned   += " " + partition_url_2
                #rint( f"**>>>>>>partition tuple >>>>>>  {partition_url_0}< >{partition_url_1}< >{partition_url_2}<" )
            concordance_word         = ConcordanceWord( word, self.tweet_id )
            concordance_word.type    = AppGlobal.word_types["url"]
            self.concordance_words.append(  concordance_word  )
            return True

        return False

    # ----------------------------------------
    def _clean_tweet( self,    ):
        """
        right now lowers and removes replaces ( mostly non standard char with mostly spaces or equivalents )
        mutates self.tweet_cleaned
        ?? take urls out first
        """
        self.tweet_cleaned   = self.tweet_raw.lower()
        self._apply_replace_list()

    # ----------------------------------------
    def _tweet_to_concordance_words( self, use_spacy = False  ):
        """
        works with self.tweet_cleaned to break into words
        may reclassify self based on word content
        break line into clean words -- even lemmas
        return a list or list like thing -- no empty or illegal words should be returned
        after general character.... substutions
         word_types               = {   "word": 1, "url": 2,  "hashtag": 3, "at_ref": 4  }  # AppGlobal.word_types["word"]

        check for leading punctuation ** and numbers ?? ... add type leading nunmber or contains number really numeral
        """
        continue_flag  = True
        while continue_flag:
            continue_flag  = self._extract_urls(  )   # ?? apply befor lower back in clean tweet think that is better !!

        words                    = self.tweet_cleaned.split()

        for word  in words:
            # clean out punctuation to nothing

            # apply at word level for ends
            word = word.strip( remove_ascii )
            word  = word.strip( )     # skipping blanks for words
            if word == "":
                continue

            # maybe later check whole word as numeral/number ??
            concordance_word = ConcordanceWord( word, self.tweet_id )
            self.concordance_words.append(  concordance_word  )

            string_part    = concordance_word.string  # or just use word for speed ??

            # ?? need check here for empty
            # move this stuff into corcordanceWord ??

            if len( string_part ) and ( string_part[0].isdigit()):
                concordance_word.type    = AppGlobal.word_types["lead_num"]

            # think all thees mutates work
            # remove at ref
            if string_part.startswith( "@" ):
                concordance_word.type    = AppGlobal.word_types["at_ref"]

            if string_part.startswith( "#" ):   # remove hastag
                concordance_word.type    = AppGlobal.word_types["hashtag"]

            # note error look in py_log
            if string_part.startswith( "http" ) or word.startswith( "https" ):
                concordance_word.type    = AppGlobal.word_types["url"]
                # no longer an error this seems common
                # msg     = f"_tweet_to_concordance_words found a url where it should not be {string_part}"
                # AppGlobal.logger.error( msg )

            #if not is_ascii( string_part ):
            if not string_part.isascii():
                concordance_word.is_ascii    =  False

            # right place for spacy ??

            if string_part in covid_words:
               self.is_covid  = True

            if string_part == "rt":   # change to a stop list, set
                self.is_retweet = True

# ==========================================
class TweetTableWriter( ):
    """
    was   class FileReadDBWrite( ):

    old code for ref
    """
    def __init__( self,  db_name ):

        self.db_name    = db_name
        self.open(  )

    # #------------------
    # def reset_data( self):
    #     self.data    = {}     # or clean out some other way

    #------------------
    def open( self   ):
        # self.file_src   = open( self.fn_src , 'r', encoding = "utf8", errors = 'ignore' )
        self.sql_con    = lite.connect( self.db_name )

    #------------------
    def write_record( self, a_parsed_tweet ):
        #rint( "---------- write tweet record ------------------" )

        try:
            #still needs fix up
            tweet_id       = a_parsed_tweet.tweet_id
            #line_no        = self.data["line_no"]
            tweet_type     = a_parsed_tweet.tweet_type
            is_covid       = a_parsed_tweet.is_covid
            #url_list       = self.data["url_list"]
            line_no         = a_parsed_tweet.line_no

            tweet          = a_parsed_tweet.tweet_raw
            #tweet_raw      = a_parsed_tweet.raw_tweet

            tweet_datetime = a_parsed_tweet.tweet_datetime
            time_of_day    = a_parsed_tweet.time_of_day
            who            = a_parsed_tweet.who_tweets


            with self.sql_con:    # !! remember what
                cur  = self.sql_con.cursor()
                data = [(     tweet_id, line_no, tweet_datetime, time_of_day, is_covid, tweet, tweet_type, who )]     # 7   dbcolumns
                sql  = ( "INSERT INTO tweets "
                         " (  tweet_id, line_no, tweet_datetime, time_of_day,  is_covid, tweet, tweet_type, who ) VALUES  "
                         " (         ?,       ?,              ?,           ?,         ?,     ?,          ?,   ?  )" )

                #rint( f"{sql}" )   # but it is always the same, so only for debug

                cur.executemany( sql, data )

                self.sql_con.commit()

        except Exception as a_except:  # !! be more specific
            msg     = f" {type(a_except)} :: {a_except}"
            AppGlobal.logger.debug( msg )
            print( msg )

            msg  = f"record dropped data was {data}"
            AppGlobal.logger.debug( msg )
            print( msg )
            # so after dropping record lets try to continue


            #return "error create_table_tweets, exception {a_except}"
            # raise

        # self.reset_data()

    #------------------
    def close( self   ):
        #self.file_src.close()
        self.sql_con.close()

# ----------------------------------------
class ConcordTableWriter(   ):
    """
    was

      class TweetFileConcordDBWriter(   ):

    """
    # -------------
    def __init__( self,  db_name ):
        """
        what it says
        """
        self.db_name              = db_name

        # counts may not be implemented ??
        self.record_count         = -1

        self.open()

    #------------------
    def open( self   ):
        """
        open file and db
        mutates self

        """
        # if not( os.path.isfile( db_file_name  )):      # already checked in caller but move whole connect back there
        #     msg   =  f"Error: db file does not exist: {db_file_name}"
        #     #rint( msg )
        #     raise FileNotFoundError( f"could not find {db_file_name}" )
        #     #AppGlobal.gui.display_info_string( msg )
        #     return

        self.sql_con    = lite.connect( self.db_name )

    # -------------
    def write_record( self, a_parsed_tweet ):
        """
        write output to both file and db
        may drop file output
        """
        #self.tweet_count   += 1

        #rint( "---------- write db  concord record pass------------------" )

        """
        tweet_id
        words  = list of words, cleaned up in the tweet
        this really tries to use execute many
        """

        concordance_words      = a_parsed_tweet.concordance_words
        data         = []
        for i_concordance_word  in concordance_words:
            data.append( ( i_concordance_word.tweet_id, i_concordance_word.type,
                           i_concordance_word.string,   i_concordance_word.is_ascii  ) )

        #rint( f"tweet count* =  {self.tweet_count}" )
        try:

            with self.sql_con:
                cur  = self.sql_con.cursor()

                sql  = ( "INSERT INTO concord "
                         " (  tweet_id, word_type, word, is_ascii   ) VALUES  "
                         " (         ?,         ?,    ?,        ?  )" )

                #rint( f"{sql}  {data}" )
                cur.executemany( sql, data )
            self.sql_con.commit()

        except Exception as a_except:  # !! be more specific
            print( type(a_except), '>>', a_except )
            raise

    # -------------
    def close( self, ):
        """
        close the output
        """
        self.sql_con.close()

# ----------------------------------------
class TweetFileProcessor(   ):
    """
    """
    # -------------
    def __init__( self,  fn_src, db_name, who_tweets,  fn_list = None ):
        """
        initialize the class, with a name for the output
        at first name will be the file name, later perhaps the database name....
        will also open the file/conection......
        serves as open()
        currently file and db based
        file_output_name
        db_name         currently sqllite file name
        create a_tweet_file_processor   =  TweetFileProcessor( fn_src, db_name  )
        run it with
        a_tweet_file_processor.read_process_lines()


        """
        self.who_tweets  = who_tweets
        self.fn_src      = fn_src
        self.db_name     = db_name
        self.fn_list     = fn_list     # think all of this is gone

        # will do open here
        self.line_no                = 0

        self.file_src               = open( fn_src, 'r', encoding = "utf8", errors = 'ignore' )   #encoding='utf8'

        #self.parsed_tweet           = ParsedTweet()  # maybe later reuse, for now recreate
        self.tweet_table_writer     = TweetTableWriter(   db_name  )
        self.concord_table_writer   = ConcordTableWriter( db_name  )

    # -------------
    def close( self, ):
        """
        close the optput
        """
        self.tweet_table_writer.close()
        self.concord_table_writer.close()
        self.file_src.close

    # ----------------------------------------
    def line_to_tweet( self, a_line  ):
        """
        parse clean and classify the line, return
        classify:   see line_type, and code
        clean:  means clean the line ( some in this code some in function clean_word() )
        note that for the word ananysis we convert to lower case

        Return:
            ParsedTweet or None --
        """
        # header line
        # 0     1    2           3            4              5          6
        #source,text,created_at,retweet_count,favorite_count,is_retweet,id_str
        # datetime_fmt     = "%m-%d-%Y %H:%M:%S"
        a_line     = a_line.rstrip(  )   # remove trailing junk on file input

        # this is the parse for the csv
        line_parts  = a_line.split( ",")  # , delimited file

        # if we do not get the required no of parts we "reject" the line
        if len( line_parts )  < 7 :
            tweet_type  = "bad"
            return( None )

        tweet                   = line_parts[1]
        tweet_id                = line_parts[6]
        parsed_tweet            = ParsedTweet( tweet, tweet_id )

        input_timestamp         = line_parts[2]
        try:

            dt_data    = datetime.datetime.strptime( input_timestamp, datetime_fmt )  # move into parsed tweet ??
            parsed_tweet.tweet_datetime     = dt_data
            str_hr                          = ("0" + str( dt_data.hour   ))[ -2 : ]   # may be number formatting that puts on missing leading 0
            str_min                         = ("0" + str( dt_data.minute ))[ -2 : ]
            parsed_tweet.time_of_day        = str_hr + ":" + str_min

        except:
            print( f"bad datetime {input_timestamp}")
            parsed_tweet.tweet_datetime   = None
            parsed_tweet.time_of_day      = None


        parsed_tweet.who_tweets  = self.who_tweets

        if tweet.startswith( "RT"):  # be careful where we lower case
            parsed_tweet.tweet_type  = "retweet"
            # get rid of the RT from tweet ??

        # self.parsed_tweet.tweet_cleaned  = tweet    # think use only to continue to clean
        # self.parsed_tweet.tweet_id       = tweet_id
        # self.parsed_tweet.tweet_type     = tweet_type
        parsed_tweet.parse_me( )

        return  parsed_tweet

    # ----------------------------------------
    def read_process_lines( self, ):
        """
        read lines then output process all of open file

        """
        line_no   = 0
        for line in self.file_src: # process source file line by line

            line_no               += 1
            # self.tweet_output.line_no   = line_no
            #rint( f"input line {line_no}" )
            # self.tweet_output.reset_defaults()        # may be reduandant with open and write

            parsed_tweet                  =  self.line_to_tweet( line  )

            if parsed_tweet is not None:
                parsed_tweet.line_no      = line_no  # unless we want to pass some other way

                self.tweet_table_writer.write_record(   parsed_tweet )
                self.concord_table_writer.write_record( parsed_tweet )

        self.close()

        print( f"=========== TweetFileProcessor done at input line {line_no}" )

        return  line_no

# ==============================================
if __name__ == '__main__':
    """
    run the app, here for convenience of launching
    """
#    sys.path.append( r"D:\Russ\0000\python00\python3\_examples"  )
 #   import ex_helpers       # ex_helpers.info_about_obj()
    import tweet_app
    a_app = tweet_app.TweetApp(  )
# ======================== eof ======================









