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

replace_list      = [  ( "’", "'" )
                     , ( "”", '"' )
                     , ( "“", '"' )
                     , ( "…", "..." )
                     , ( ".", " " )   # to white space for word split
                     , ( ",", " " )   # to white ... or iterate through punctuation
                     , ( "↓", " " )   # to white ... oor iterate through punctuation

                    ]

"""
also found
⚙️⛰️🇺🇸
""
"""

remove_ascii        = "\"!$%&'()*+,-./:;<=>?[\]^_`{|}~"   # removable ascii not @ #
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
        #print "it was not a ascii-encoded unicode string"
        return False
    else:
        #print "It may have been an ascii-encoded unicode string"
        return True

# ----------------------------------------------
def define_table_concord( db_name, allow_drop = False ):
    """
    what it says
    """
    # print( "  ============= define_table_concord() db {db_name} drop {allow_drop}========== " )

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


# ==========================================
class ConcordanceWord( ):
    """
    basically a struct ( could put in parse functions here but not now )
    we will store words here prior to saving
    """
    def __init__( self, a_string, tweet_id ):
        pass
        self.reset_data( a_string, tweet_id )

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
    """
    def __init__( self, tweet, tweet_id ):
        pass
        self.reset_data( tweet, tweet_id )

    #------------------
    def reset_data( self, tweet, tweet_id ):
        """ most of this stuff will probably be mutated, partly here for doc """
        self.concordance_words    = []     # what do we put in the list concordance_word
        self.tweet_raw            = tweet
        self.tweet_cleaned        = tweet  # will be mutated # check we are doing this right
        #self.is_retweet           = False
        self.is_covid             = False
        self.tweet_id             = tweet_id
        self.tweet_datetime       = None    # next from where data line is split
        #self.tweet_id             = None
        self.line_no              = 0
        self.tweet_type           = "tweet"   # what are the types
        self.who_tweets           = "?"

    # ----------------------------------------
    def parse_me( self, ):
        self.clean_tweet(  )
        self.tweet_to_concordance_words()

    # ----------------------------------------
    def apply_replace_list( self,  ):
        """
        mutates self.tweet_cleaned
        mostly removes non ascii, not for punctuation
        """
        for i_replace in replace_list:
            a, b        = i_replace
            self.tweet_cleaned    = self.tweet_cleaned.replace( a, b )

    # ----------------------------------------
    def clean_tweet( self,    ):
        """
        mutates self.tweet_cleaned
        """
        self.tweet_cleaned   = self.tweet_raw.lower()
        self.apply_replace_list()

    # ----------------------------------------
    def tweet_to_concordance_words( self, use_spacy = False  ):
        """
        works with self.tweet_cleaned to break into words
        may reclassify self based on word content
        break line into clean words -- even lemmas
        return a list or list like thing -- no empty or illegal words should be returned
        after general character.... substutions
         word_types               = {   "word": 1, "url": 2,  "hashtag": 3, "at_ref": 4  }  # AppGlobal.word_types["word"]

        check for leading punctuation ** and numbers ?? ... add type leading nunmber or contains number really numeral
        """
        words                    = self.tweet_cleaned.split()
        self.concordance_words   = []
        for word  in words:
            # clean out punctuation to nothing

            # apply at word level for ends
            word = word.strip( remove_ascii )

            # maybe later check whole word as numeral/number ??
            concordance_word = ConcordanceWord( word, self.tweet_id )
            self.concordance_words.append(  concordance_word  )

            string_part    = concordance_word.string  # or just use word for speed ??

            # ?? need check here for empty
            # move this stuff into corcordanceWord ??

            if len( string_part ) and ( string_part[0].isdigit()):
                concordance_word.type    = AppGlobal.word_types["lead_num"]

            # if string_part.startswith( "@" ):
            #     concordance_word.type    = AppGlobal.word_types["at_ref"]

            # think all thees mutates work
            # remove at ref
            if string_part.startswith( "@" ):
                concordance_word.type    = AppGlobal.word_types["at_ref"]

            if string_part.startswith( "#" ):   # remove hastag
                concordance_word.type    = AppGlobal.word_types["hashtag"]

            if string_part.startswith( "http" ) or word.startswith( "https" ):
                concordance_word.type    = AppGlobal.word_types["url"]

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
        print( "---------- write tweet record ------------------" )

        try:
            #still needs fix up
            tweet_id       = a_parsed_tweet.tweet_id      #   8 dbcolumns
            #line_no        = self.data["line_no"]
            tweet_type     = a_parsed_tweet.tweet_type
            is_covid       = a_parsed_tweet.is_covid
            #url_list       = self.data["url_list"]
            line_no         = a_parsed_tweet.line_no

            tweet          = a_parsed_tweet.tweet_raw
            #tweet_raw      = a_parsed_tweet.raw_tweet

            tweet_datetime = a_parsed_tweet.tweet_datetime
            who            = a_parsed_tweet.who_tweets


            with self.sql_con:    # !! remember what
                cur  = self.sql_con.cursor()
                data = [(     tweet_id, line_no, tweet_datetime, is_covid, tweet, tweet_type, who )]     # 7   dbcolumns
                sql  = ( "INSERT INTO tweets "
                         " (  tweet_id, line_no, tweet_datetime, is_covid, tweet, tweet_type, who ) VALUES  "
                         " (         ?,       ?,              ?,        ?,     ?,         ?,        ?  )" )

                print( f"{sql}" )

                cur.executemany( sql, data )

                self.sql_con.commit()

        except Exception as a_except:  # !! be more specific

            print( type(a_except), '::', a_except )
            #return "error create_table_tweets, exception {a_except}"
            raise

        # self.reset_data()

    # #------------------
    # def read_line( self):

    #     while True:    # do until
    #         # note early returns and continues
    #         line   = self.file_src.readline()
    #         self.in_count   += 1
    #         #print( f"line{self.in_count} is {line}" )

    #         if not line:
    #             return -1  # eof
    #         line   = line.rstrip('\n')
    #         line   = line.strip( )       # may make above unnecessary

    #         if line == "": # blank after strip is empty line -- skip
    #             continue

    #         if line.startswith( "#" ):   # comment
    #             continue

    #         self.line   = line    # put in instance var

    #         print( f"line{self.in_count} is {line}" )

    #         return self.in_count  # line no, data in self.

    # #------------------
    # def parse_line( self ):
    #     """
    #     parse line and take appropriate action
    #         save data to dict
    #         save record to database
    #         exception if bad line
    #     return  None and self.mutate
    #     """
    #     if self.line.startswith( ":======" ):    # this is a record break -- do we have data ??
    #         if self.data  == {}:
    #             pass # no data
    #             return
    #         else:
    #             self.write_record( )
    #             return

    #     splits   = self.line.split( ":", 1 )
    #     if len( splits ) < 2:
    #         print( "bad line ")
    #         pass # bad line quit??

    #     data_name     = splits[0].strip()
    #     data_value    = splits[1].strip()
    #     print( f"data_name >{data_name}< data_value >>{data_value}<< ")
    #     self.data[data_name]   = data_value

    #     # print( self.data )

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
        #     print( msg )
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

        print( "---------- write db  concord record pass------------------" )

        """
        tweet_id
        words  = list of words, cleaned up in the tweet
        this really tries to use execute many
        """
                # "CREATE TABLE concord( "
                # "word      Text, "
                # "tweet_id  Text, "  # , " on most ) on last
                # "word_type Int, "     # word types in  AppGlobal.word_types[ "word" ]
                # "is_ascii  BOOLEAN )"


        concordance_words      = a_parsed_tweet.concordance_words
        data         = []
        for i_concordance_word  in concordance_words:
            data.append( ( i_concordance_word.tweet_id, i_concordance_word.type,
                           i_concordance_word.string,   i_concordance_word.is_ascii  ) )


        # print( f"tweet count* =  {self.tweet_count}" )
        try:

            with self.sql_con:
                cur  = self.sql_con.cursor()

                sql  = ( "INSERT INTO concord "
                         " (  tweet_id, word_type, word, is_ascii   ) VALUES  "
                         " (         ?,         ?,    ?,        ?  )" )

                print( f"{sql}  {data}" )
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

    # # ----------------------------------------
    # def apply_replace_list( self, a_string ):

    #     b_string   = a_string
    #     for i_replace in replace_list:
    #         a, b        = i_replace
    #         #b_string    = b_string.replace( "’", "'" )
    #         b_string    = b_string.replace( a, b )

    #     return b_string

    # # ----------------------------------------
    # def remove_urls( self, a_string ):
    #     """
    #     what it says
    #     most but not all at begin or end of line, location may mean something, some imbedded
    #     reassemble line without url's'
    #     need to do this befor other clean up migh split up  url
    #     mutate  TweetOutput
    #     return a cleaned string
    #     """
    #     words         = a_string.split()
    #     clean_words   = []
    #     for word  in words:

    #         # do this before more break up
    #         # clean words do not start witn http, it is a url not a word
    #         # things like https://t.co/2cfwNTvpNX are already split
    #         if word.startswith( "http" ) or word.startswith( "https" ):   # ?? right way to manage?  https:
    #             self.tweet_output.url_list.append( word )
    #             continue
    #         clean_words.append( word )

    #     return " ".join( clean_words )


    #  # ----------------------------------------
    # def is_ascii( self, a_string ):
    #     """
    #     what it says -- like remove urls ( may combine with it )
    #     need to enhance TweetTabel, concord write to have this
    #     """
    #     words         = a_string.split()
    #     clean_words   = []
    #     for word  in words:

    #         if not word.is_ascii(   ):   # ?? right way to manage?  https:
    #              print( f"word is not ascii {word}")

    #     return a_string

    # # ----------------------------------------
    # def remove_hashtags( self, a_string ):
    #     """
    #     what it says -- like remove urls ( may combine with it )
    #     most but not all at begin or end of line, location may mean something, some imbedded
    #     reassemble line without url's'
    #     need to do this befor other clean up migh split up  url
    #     mutate  TweetOutput
    #     return a cleaned string
    #     """
    #     words         = a_string.split()
    #     clean_words   = []
    #     for word  in words:

    #         if word.startswith( "#" ):   # remove hastag
    #             self.parsed_tweet.hashtag_list.append( word )
    #             continue
    #         clean_words.append( word )

    #     return " ".join( clean_words )

    # # ----------------------------------------
    # def remove_at_ref( self, a_string ):
    #     """
    #     what it says -- like remove urls ( may combine with it )
    #     most but not all at begin or end of line, location may mean something, some imbedded
    #     reassemble line without url's'
    #     need to do this befor other clean up migh split up  url
    #     mutate  TweetOutput
    #     return a cleaned string
    #     """
    #     words         = a_string.split()
    #     clean_words   = []
    #     for word  in words:

    #         if word.startswith( "@" ):   # ?? right way to manage?  https:
    #             self.parsed_tweet.at_references.append( word )
    #             continue
    #         clean_words.append( word )

    #     return " ".join( clean_words )

    # ----------------------------------------
    def leftovers( self, ):

    # !! remove_hashtags()  remove @references

        tweet         = apply_replace_list( tweet )  # some may cause a word break  problem in links
        words         = tweet.split()       # get word list from line -- this was all original code did
        clean_words   = []
        for i_word in words:
            j_word   = clean_word( i_word )
            if j_word == "":
                continue
            # since looping thru words check for covid words
            if j_word in covid_words:
               tweet_output.is_covid  = True

            if not j_word == "" and not j_word == "rt":   # change to a stop list, set
                # tweet_output.words.append( j_word )
                clean_words.append( j_word )

        if use_spacy:   # if using npl spacy....
            "rebuild line, then convert to list again "
            spacy_line  = " ".join( clean_words )
            doc         = nlp( spacy_line )
            """
            what is doc?
            """
            # clean_words = doc    # this is not array of words, may need to convert

            npl_words = []
            for token in doc:
                #print( token, token.lemma, token.lemma_)  # debug
                npl_words.append( (token.lemma_) )  # token   just messing with this
            #print( f"npl_words {npl_words}" )  # debug
            clean_words   = npl_words

        return clean_words


    # def clean_word( self, word ):
    #     """
    #     clean a word may change to "" if no other clean version --
    #           so dropping as a word.

    #     Note eary returns in code

    #     comments may help define what is 'clean'
    #     takes word and returns word
    #     """

    #     # clean words do not start with punctuation
    #     word = word.strip( string.punctuation ).lower()

    #     if len(word) == 0:
    #          return ""

    #     # clean words do not start witn http, it is a url not a word
    #     # things like https://t.co/2cfwNTvpNX are already split
    #     if word.startswith( "http" ):   # ?? right way to manage?  https:
    #         return ""

    #     #..... more "cleaning" is probably needed

    #     #print( f"word = {word}")
    #     return word

    # ----------------------------------------
    def line_to_tweet( self, a_line  ):
        """
        parse clean and classify the line, return
        classify:   see line_type, and code
        clean:  means clean the line ( some in this code some in function clean_word() )
        note that for the word ananysis we convert to lowere case

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
            parsed_tweet.tweet_datetime   = datetime.datetime.strptime( input_timestamp, datetime_fmt )
            # print( ">>>>", dt )
        except:
            print( f"bad datetime {input_timestamp}")
            parsed_tweet.tweet_datetime   = None

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
            print( f"input line {line_no}" )
            # self.tweet_output.reset_defaults()        # may be reduandant with open and write

            parsed_tweet                  =  self.line_to_tweet( line  )

            if parsed_tweet is not None:
                parsed_tweet.line_no      = line_no  # unless we want to pass some other way

                self.tweet_table_writer.write_record(   parsed_tweet )
                self.concord_table_writer.write_record( parsed_tweet )

        self.close()

        print( f"=========== TweetFileProcessor done at input line {line_no}" )

        return  line_no

# # ----------------------------------------
# def main(  ):
#     """
#     build concondance
#     write 'list' file and to db
#     sort and print
#     """
#     print( "\n\n----------------- start concordance ----------------------" )

#     my_parameters      = parameters

#     """
#     # fn = file name -- may be come table or database name
#     fn_src          = r"D:\Russ\0000\python00\python3\_projects\covid_data\trump\tiny_tweet_download.txt"
#     #fn_src         = r"D:\Russ\0000\python00\python3\_projects\covid_data\trump\tweet_download.csv"
#     fn_src          = r"tiny_tweet_download.txt"
#     fn_src          = r"tiny_in.txt"
#     """

#     fn_list         = r"D:\Russ\0000\python00\python3\_projects\covid_data\trump\tiny_list.txt"
#     fn_list         = r"tiny_out.txt"

#     fn_tweet_out    =  parameters.tweet_out_file_name
#     fn_concordance  = "tiny_concordance.txt"

#     concordance     = concord_from_file( parameters.tweet_input_file_name, fn_list )

#     # print without sorting
#     #info_about_dict( c )

#     # try with better names
#     # a_dict   = c

#     # this is the old style
#     # sort on key and output to file whole concordance in the dict
#     if True:
#         a_ordered_dict    = collections.OrderedDict( sorted( concordance.items(), key=lambda a_item: a_item[0])) # items makes dict to tuples
#         info_about_dict( a_ordered_dict, max_lines = 10 )
#         concordance_output   = ConcordanceDictOutput( fn_concordance )
#         concordance_output.write( a_ordered_dict )
#         concordance_output.close()

#     print( "\n---------------- end concordance ----------------------\n\n" )

#     #print ( string.punctuation )

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









