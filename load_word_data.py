# -*- coding: utf-8 -*-
"""

loads word data from a file, also a little test select


"""

import sys
import string
import collections
import spacy          # linguistic module words to lemmas ( might not be correct explain )
import datetime
import sqlite3 as lite
import os


# ----------------------------------------------
def define_table_word( db_file_name, allow_drop = False ):
    """  ============= util_create_table_words() =====================
    return  -- none
    """
    try:
        sql_con = lite.connect( db_file_name )

        with sql_con:
            cur = sql_con.cursor()
            if allow_drop:
               cur.execute("DROP TABLE IF EXISTS words")   # else error if table exists

            cur.execute(
                "CREATE TABLE words ( "
                "word       Text, "
                "word_count INT, "
                "word_rank INT, "
                "PRIMARY KEY ( word ) ) "   # think about index later
                )

    except lite.Error as a_except:
     #except ( lite.Error, TypeError) as a_except:
         print( type(a_except), '::', a_except )
         print( "error util_create_table_words, exception {a_except}" )
         raise


    sql_con.close()

# ==========================================
class FileReadDBWrite( ):
    """
    read a file and write a db file
    """
    def __init__( self, fn_src, db_name ):

        self.fn_src     = fn_src
        self.db_name    = db_name
        self.file_src   = None
        self.sql_con    = None    # should we keep open
        self.data       = None   # keep in a dict
        #self.data_req   = [ "tweet", ".........."  ]
        self.in_count   = -1
        self.line       = ""
        self.reset_data()

    #------------------
    def reset_data( self):
        """
        after we write a record -- get ready for next
        """
        self.data    = {}     # or clean out some other way

    #------------------
    def open( self   ):
        self.file_src   = open( self.fn_src , 'r', encoding = "utf8", errors = 'ignore' )
        self.sql_con    = lite.connect( self.db_name )

    #------------------
    def write_record( self):
        #print( "---------- write word record ------------------" )

        try:
            word             = self.data["word"]      #   2 dbcolumns
            word_count       = self.data["word_count"]

            with self.sql_con:    # !! remember what
                cur  = self.sql_con.cursor()
                data = [(     word,  word_count )]     # 2   dbcolumns
                sql  = ( "INSERT INTO words "
                         " (  word, word_count   ) VALUES  "
                         " (     ?,         ?  )" )

                #print( f"{sql}" )
                cur.executemany( sql, data )
                self.sql_con.commit()

        except Exception as a_except:  # !! be more specific
            print( type(a_except), '>>', a_except )
            raise

        self.reset_data()

    #------------------
    def read_line( self):
        """
        read a data line ( not comment or blank ) return 1 line or eof condition
        better written as some sort of itterator
        return  line#, mutates self
        """
        while True:    # do until
            # note early returns and continues
            line   = self.file_src.readline()
            self.in_count   += 1
            #print( f"line{self.in_count} is {line}" )

            if not line:
                return -1  # eof

            line   = line.rstrip('\n')
            line   = line.strip( )       # may make above unnecessary

            if line == "": # blank after strip is empty line -- skip
                continue

            if line.startswith( "#" ):   # comment line skiip
                continue

            self.line   = line
            print( f"line: {self.in_count} is >>{line}<<" )

            return self.in_count  # line no, data in self.

    #------------------
    def parse_line( self ):
        """
        parse line and take appropriate action
            save data to dict
            save record to database
            exception if bad line
        return  None and self.mutate
        """
        splits   = self.line.split( ",", 1 )
        if len( splits ) < 2:
            print( "bad line ")
            pass # bad line quit?? -- lets log these

        word           = splits[0].strip()
        word_count     = splits[1].strip()
        #print( f"word >{word}< word_count >>{word_count}<< ")
        # we could be more direct, but for now stick with the pattern ??
        self.data["word"]         = word
        self.data["word_count"]   = word_count
        self.write_record( )
        # print( self.data )

    #------------------
    def close( self   ):
        self.file_src.close()
        self.sql_con.close()

# ----------------------------------------------
def load_table_word( name_db,  fn_src ): # db_file_name, input_file_name ):
    """  ============= util_insert_words_from_file() into db =====================
    a csv file
    #fn_src    = parameters.word_input_file_name   !! fix call
    #name_db   = set_db_file_name
    """
    print( f"os.getcwd(): {os.getcwd()}"  )  #

    file_read_write   = FileReadDBWrite( fn_src, name_db )

    file_read_write.open()
    file_read_write.read_line()
    file_read_write.parse_line()

    while True:
        ret    = file_read_write.read_line()
        if ret == -1:
            break
        file_read_write.parse_line()

    file_read_write.close()


# ----------------------------------------------
def update_rank( db_file_name ):
    """
    update the rank column in word table using word_count sort
    just refactored to gui test ??
    """

    sql_con = lite.connect( db_file_name )

    # --------- are 2 cursors the same -- they are not use one to fetch one to update

    with sql_con:
        cur_1 = sql_con.cursor()
        cur_2 = sql_con.cursor()
        # select all with cur_1 and use cur_2 for update on the row

        sql         = "SELECT rowid, word, word_count FROM words  order by word_count desc, word asc"
        sql_data    = []
        row_count   = 0

        execute_args  = ( sql,  sql_data,  )
        # print( f"{"for f sake"}  execute {execute_args}")
        cur_1.execute( *execute_args )

        while True:  # get rows one at a time in loop
            row   = cur_1.fetchone()

            if row is None:
                break

            row_count += 1
            #print( row )
            row_id   = row[ 0 ]
            word     = row[ 1 ]

            sql_2 = ( f"UPDATE words SET word_rank = {row_count}  WHERE rowid = '{row_id}' " )
            print( sql_2 )
            cur_2.execute( sql_2 )

        return row_count


# ==============================================
if __name__ == '__main__':
    """
    run the app here for convenience of launching
    """
    # import smart_plug
    # a_app = smart_plug.SmartPlug(  )
    #sys.path.append( r"D:\Russ\0000\python00\python3\_examples"  )
    #import ex_helpers       # ex_helpers.info_about_obj()
    import tweet_app
    a_app = tweet_app.TweetApp(  )
# ======================== eof ======================


