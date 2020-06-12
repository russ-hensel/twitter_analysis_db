# -*- coding: utf-8 -*-


"""
these objects write the results of a select in
various formats
more or less implement an abstract base class
but without the formalism

"""

import HTML

import os
from   app_global import AppGlobal


BREAK_LINE      =  ":===================="    # break in "input files"

# ----------------------------------------------
def add_data_path(  file_name ):
    """
    complete short path names by adding data_dir part  ... remove instance funct of same name
    from another app may not be used here
    """
    ret  = ""  # why, will fail unless changed, just not well though out
    try:     # in case of config errors log
        ret = os.path.join( AppGlobal.parameters.data_dir, file_name )
    except Exception as exception:   # should not really catch all
        AppGlobal.print_debug(       exception.msg )
        AppGlobal.gui_write_error(   exception.msg )
        #self.os_open_text_file( self.parameters.pylogging_fn )
        msg     = "Exception building file name {AppGlobal.parameters.data_dir} and {file_name} see py_log"
        #AppGlobal.print_debug(       msg )
        AppGlobal.gui_write_error(   msg )

    return ret

 # -------------------------------
def make_file_writer(  builder,  ):
    """
    Purpose:
        what it says -- make a file_writer of the correct format output_format
    Args: builder -- amoung other things uses output_format to determine type of
          writer and file name

    Returns: a fileWriter, mutates builder
    Issues:  could use a thougful refactoring  --- conside dict version
    """
    output_format   = builder.output_format

    # msg     = f"make_file_writer: for format {output_format}"
    #rint( msg )

    # some are left over and need to be changed

    # AppGlobal.print_debug( msg )
    # AppGlobal.gui_write_progress( msg )

    if  output_format == "py_log":
        # fileout_name           = add_data_path( AppGlobal.parameters.pylogging_fn  )
        builder.output_name    = "not used"
        select_writer          = SelectLogWriter(  builder )

        # our use os.path.join( rpath, "temp", "zxqq.txt" ) ))

    elif output_format == "csv":
        # fileout_name      = add_data_path( "output_select.csv"  )
        builder.output_name    = AppGlobal.parameters.output_path  + f"{os.sep}output_select.csv"

        #AppGlobal.parameters.output_path
        select_writer          = SelectCSVWriter( builder )

    elif output_format == "txt":
        builder.output_name    = AppGlobal.parameters.output_path  + f"{os.sep}output_select.txt"
        select_writer          = SelectTxtWriter( builder )

    elif output_format == "yaml":  # still need to do

        builder.output_name    = AppGlobal.parameters.output_path  + f"{os.sep}output_select.yaml"
        select_writer          = SelectYamlWriter( builder )

    elif output_format == "html":
        #fileout_name      = add_data_path( "output_select.html"  )
        builder.output_name    = AppGlobal.parameters.output_path  +  f"{os.sep}output_select.html"
        select_writer          = SelectHTMLWriter( builder )

    elif output_format == "msg":
        #fileout_name      = add_data_path( "output_select.html"  )
        builder.output_name    = AppGlobal.parameters.output_path  +  f"{os.sep}output_select.msg"
        select_writer          = SelectMessageWriter( builder )

    elif output_format == "zap":
        #fileout_name      = add_data_path( "output_select.html"  )
        builder.output_name    = AppGlobal.parameters.output_path  +  f"{os.sep}output_select.msg"
        select_writer          = SelectZapWriter( builder )

    else:
        msg   =  f"invalid output_format = {output_format}"
        AppGlobal.gui.display_info_string( msg )
        AppGlobal.print_debug( msg )
        raise  Exception( msg )

#    msg     = f"make_file_writer: return {( select_writer, fileout_name )}"
#    AppGlobal.print_debug( msg )

    return ( select_writer )



#====================================
class SelectWriter( object ):
    """
    Purpose: base class for all writers
    """
    #----------- init -----------
    def __init__(self, builder ):
        """
        what it says
        """
        self.builder                = builder
        self.file_name              = builder.output_name
        self.columns_out            = builder.columns_out
        self.columns_info           = builder.columns_info

    #----------- init -----------
    def open_output_file(self,  ):
        """
        what it says
        arguments:  from builder
        mutates to give self.fileout for output
        """
        #rint( f"append to output {self.builder.output_append} " )

        if self.builder.output_append == "Append":
            mode    = "a"

        else:
            mode    = "w"

        self.fileout                = open( self.file_name, mode, encoding = "utf8", errors = 'replace' )

    #----------- init -----------
    def format_row( self, row_object ):
        """
        what i says
        take row, return line_parts, row formatted ( all parts a string ?? )
        """
        columns_info  = self.columns_info   # believe it is also a dict like a data dict
        columns_out   = self.columns_out
        line_parts    = []
        for  ix, i_col in enumerate( columns_out ):

            i_col_info   = columns_info[i_col]
            i_col_data   = row_object[ix]
            fmt          = i_col_info["curly_format"]

            if i_col_data is None:
                fmt          = i_col_info["text_format"]
                line_parts.append( fmt.format( x = ".n." ) )

            else:
                fmt          = i_col_info["curly_format"]
                # print( f"formatting:  >{fmt}< >{i_col_data}<")   # surround try except
                line_parts.append( fmt.format( x = i_col_data ) )

        return line_parts

#====================================
class SelectLogWriter( object ):
    """
    obsolete not sure if will being back
    this writes output in compact form to the logger
    not working but would not be hard fix first
    """
    #----------- init -----------
    def __init__(self, file_name, table_info ):
        """
        all have the same init signature, may allow nulls in some cases, see code
        this guy does not need file_name
        """
        self.file_name       = file_name
        self.table_info      = table_info
        # more def in other functions

    #----------- init -----------
    def write_header(self,  ):
        """
        what is says
        Args: Return: state change, output
        Raises: none planned
        """
        lines                       = []

        # will use in other methods
        self.col_names              =  [ i_format[0] for i_format in self.table_info.format_list ]
        msg   = f"write_header()  self.col_names  {self.col_names}"
        AppGlobal.print_debug( msg )

        i_line    = f"#---------- SelectLogWriter output from {AppGlobal.controller.app_name} {AppGlobal.controller.app_version}"
        lines.append( i_line  )

        lines.append( f" self.table_info.sql = {self.table_info.sql}"  )

        i_line    = f"use_table:{self.table_info.table_name}"
        lines.append( i_line  )

        msg       = "\n".join( lines )
        AppGlobal.logger.log( AppGlobal.force_log_level, msg )

    #----------------------
    def write_row(self, row_object ):
        """
        could have a write row_col function to eliminate the row object  -- but might forget column name unless tricky
        """
        msg   =  str( row_object )   #.ix_db_value
        AppGlobal.logger.log( AppGlobal.force_log_level, msg )

    #---------------------
    def write_footer(self, footer_info ):
        """
        what is says
        Args: Return: state change, output
        Raises: none planned
        """
        AppGlobal.logger.log( AppGlobal.force_log_level, footer_info )

#        i_line    =  ":======== eof footer ============"
##        self.fileout.write( i_line   + "\n" )
#
##        msg       = "\n".join( lines )
#        AppGlobal.logger.log( AppGlobal.force_log_level, i_line )



#====================================
class SelectCSVWriter( object ):
    """
    Purpose: write a tab separated file
    """
    #----------- init -----------
    def __init__(self, builder ):
        """
        what it says
        """
        super().__init__( builder )
        # self.builder                = builder
        # self.file_name              = builder.output_name
        # self.columns                = builder.columns_out

  #----------------------
    def write_header(self, ):
        """
        what is says
        Args: Return: state change, output
        Raises: none planned, file open could fail
        """
        msg   = "write header...."
        AppGlobal.print_debug( msg )
        self.open_output_file()

        #self.fileout                = open( self.file_name, "w", encoding = "utf8", errors = 'replace' )

        columns_info  = self.builder.columns_info   # believe it is also a dict like a data dict
        columns_out   = self.builder.columns_out
        line_parts    = []
        for  ix, i_col in enumerate( columns_out ):

            i_col_info   = columns_info[i_col]
            fmt          = i_col_info["text_format"]
            col_text     = i_col_info["column_head"]


            line_parts.append( fmt.format( x =  col_text  ) )

        line    = "\t".join( line_parts )

        #rint( line, flush = True )

        self.fileout.write( line   + "\n" )

    #----------------------
    def write_row(self, row_object ):
        """
        Purpose: what it says
        Args: Return: state change, output
        Raises: none planned
        """
        columns_info  = self.builder.columns_info   # believe it is also a dict like a data dict
        columns_out   = self.builder.columns_out
        line_parts    = []
        for  ix, i_col in enumerate( columns_out ):

            i_col_info   = columns_info[i_col]
            fmt          = i_col_info["curly_format"]

            line_parts.append( fmt.format( x = str( row_object[ix] ) ) )

        line    = "\t".join( line_parts )

        #rint( line, flush = True )

        self.fileout.write( line   + "\n" )

    #---------------------
    def write_footer(self, footer_info,  ):
        """
        what it says
        ?? add args for sql time date blank lines .... perhaps a dict or a footer object
        Args: Return: mutate self, output
        """
        if footer_info != "":
            self.fileout.write( footer_info   + "\n" )

        i_line    =  ":========  footer eof  ============"
        self.fileout.write( i_line   + "\n" )

        self.fileout.close( )

#====================================
class SelectTxtWriter( SelectWriter ):

    """
    Tabular output with justification to a .txt file

    """
    #----------- init -----------
    def __init__(self, builder ):
        """
        what it says
        all have the same init signature, may allow nulls in some cases, see code
        """
        #rint( "init SM_Select_02")
        super().__init__( builder )

        # self.builder                = builder
        # self.file_name              = builder.output_name
        # self.columns                = builder.columns_out

    #----------- init -----------
    def write_header(self, ):
        """
        what it says
        Args: Return: state change, output
        Raises: none planned, file open could fail
        """
        msg   = "write header...."
        #AppGlobal.print_debug( msg )

        # if builder.output_append == "Append":
        #     mode    = "a"
        # else:
        #     mode    = "w"

        # self.fileout                = open( self.file_name, mode, encoding = "utf8", errors = 'replace' )

        self.open_output_file()

        self.fileout.write( f"Output for: {self.builder.select_name}\n" )

        columns_info  = self.builder.columns_info   # believe it is also a dict like a data dict
        columns_out   = self.builder.columns_out
        line_parts    = []
        for  ix, i_col in enumerate( columns_out ):

            i_col_info   = columns_info[i_col]
            fmt          = i_col_info["text_format"]
            col_text     = i_col_info["column_head"]

            line_parts.append( fmt.format( x =  col_text  ) )

        line    = "".join( line_parts )
        #rint( line, flush = True )

        self.fileout.write( line   + "\n" )

    #----------------------
    def _format_list(self, a_list ):
        """
        take a list of strings and format according to col_just and col_width
        return the line a string
        """
#        msg     = f"_format_list self.col_names>> {self.col_names}"
#        AppGlobal.print_debug( msg )

        out_columns    = []
        for ix_col, i_col in enumerate( self.col_names ):
            item       = self.table_info.format_list[ ix_col ]
            col_name   = item[ 0 ]   # should be i_col  self.col_names ???

            align      = item[ self.ix_format_just   ]
            length     = item[ self.ix_format_len    ]

            # or the second way
            align      = self.col_just[  ix_col ]
            length     = self.col_width[ ix_col ]      # slide between length and width.  width would be better

            #i_data    = self.fix_null( row[ ix_col ] )
            #i_data    = row_object.get_value( i_col,  row_object.ix_db_value )
            i_data     = a_list[ ix_col ]    # ROWID comes back as an int

            if isinstance( i_data, int):
                i_data = str( i_data )
#            msg     = f"_format_list i_data>>{i_data} i_data>>{i_data}<<length>>{length}<<"
#            AppGlobal.print_debug( msg )

            i_data         = i_data[0:length ]
            data_length    = len( i_data )

            if data_length < length:   # need allignment
                if   align  == "c":
                    i_data  =  ( int( ( length - data_length )/2 ) * " " ) + i_data  + ( length * " " )
                    i_data    = i_data[0:length ]

                elif align  == "r":
                    i_data  =  ( ( length - data_length ) * " " ) + i_data

                else: # assume l
                    i_data  = i_data + ( ( length - data_length ) * " " )

            out_columns.append( i_data )
        i_line   = " | ".join( out_columns )
        return i_line

   #----------------------
    def write_row(self, row_object ):
        """
        Purpose: what it says --  5 th ver .... think build a col at a time
        Args:
            row_object, for now just a row which is list like one data item for each column

            should use self. perhaps set up in header
        self.sql_builder            = sql_builder

        self.columns                = sql_builder.columns
        self.sql_builder.column_info which currently has {} format whatever
        """
        # probably could zip columns and row_object


        line_parts   = self.format_row( row_object )    # apply formatting to exch item in row

        # columns_info  = self.builder.columns_info   # believe it is also a dict like a data dict
        # columns_out   = self.builder.columns_out
        # line_parts    = []
        # for  ix, i_col in enumerate( columns_out ):

        #     i_col_info   = columns_info[i_col]
        #     i_col_data   = row_object[ix]
        #     fmt          = i_col_info["curly_format"]

        #     if i_col_data is None:
        #         fmt          = i_col_info["text_format"]
        #         line_parts.append( fmt.format( x = ".n." ) )
        #         line_parts.append( ".none." )
        #     else:
        #         fmt          = i_col_info["curly_format"]
        #         line_parts.append( fmt.format( x = i_col_data ) )

        line    = "".join( line_parts )

        # rint( line, flush = True )

        self.fileout.write( line   + "\n" )

    #---------------------
    def write_footer(self, footer_info,  ):
        """
        what it says
        ?? add args for sql time date blank lines .... perhaps a dict or a footer object
        Args:
        Return: None,  output
        """

        if footer_info != "":
            self.fileout.write( footer_info   + "\n" )

        i_line    =  ":========  footer eof  ============"
        self.fileout.write( i_line   + "\n" )

        self.fileout.close( )

#====================================
class SelectYamlWriter( object ):

    """
    yamal like output, may make more official later
    """
    #----------- init -----------
    def __init__(self, builder ):
        """
        what is says
        """
        super().__init__( builder )
        # self.builder               = builder
        # #self.select_dict            = select_dict
        # self.file_name              = builder.output_name
        # self.columns                = builder.columns_out


    #----------- init -----------
    def write_header(self, ):
        """
        what is says
        Args: Return: state change, output
        Raises: none planned, file open could fail
        """
        #msg   = "write header...."
        #AppGlobal.print_debug( msg )
        self.open_output_file()

        #self.fileout                = open( self.file_name, "w", encoding = "utf8", errors = 'replace' )

        columns_info  = self.builder.columns_info   # believe it is also a dict like a data dict
        columns_out   = self.builder.columns_out
        line_parts    = []
        for  ix, i_col in enumerate( columns_out ):

            i_col_info   = columns_info[i_col]
            fmt          = i_col_info["text_format"]
            col_text     = i_col_info["column_head"]

            line_parts.append( fmt.format( x =  col_text  ) )

        line    = "".join( line_parts )

        #rint( line, flush = True )

        self.fileout.write( line   + "\n" )

   #----------------------
    def write_row(self, row_object ):
        """
        what is says  --  5 th ver .... think build a col at a time
        Args:
            row_object, for now just a row which is list like one data item for each column

            should use self. perhaps set up in header
        self.sql_builder            = sql_builder

        self.columns                = sql_builder.columns
        self.sql_builder.column_info which currently has {} format whatever

        Raises: none planned
        """
        # probably could zip columns and row_object
        columns_info  = self.builder.columns_info   # believe it is also a dict like a data dict
        columns_out   = self.builder.columns_out
        line_parts    = []
        for  ix, i_col in enumerate( columns_out ):

            i_col_info   = columns_info[i_col]
            #fmt          = i_col_info["curly_format"]  # for now do not use all left

            line_part = f"{i_col}: {str(row_object[ix] )}"

            line_parts.append( line_part )

        line    = "\n".join( line_parts )

        #rint( line, flush = True )

        self.fileout.write( line   + "\n" )

    #---------------------
    def write_footer(self, footer_info,  ):
        """
        what is says

        Args:
        Return: mutate self, output
        """
        if footer_info != "":
            self.fileout.write( footer_info   + "\n" )

        i_line    =  ":========  footer eof  ============"
        self.fileout.write( i_line   + "\n" )

        self.fileout.close( )

#====================================
class SelectMessageWriter( object ):
    """
    Message a txt file to go to the message area
    Might want to change to write directly to it
    """
    #----------- init -----------
    def __init__(self, builder ):
        """
        what is says
        """
        self.builder                = builder
        self.file_name              = builder.output_name
        self.columns                = builder.columns_out
        self.included_columns       = [ 2 ]   # later parse for these

    #----------- init -----------
    def write_header(self,  ):
        """
        what is says
        Args: Return: state change, output
        Raises: none planned
        """
        msg   = "write header for MessageWriter ...."
        #AppGlobal.print_debug( msg )

        self.fileout                = open( self.file_name, "w", encoding = "utf8", errors = 'replace' )

        columns_info  = self.builder.columns_info   # believe it is also a dict like a data dict
        columns_out   = self.builder.columns_out
        line_parts    = []
        for  ix, i_col in enumerate( columns_out ):

            i_col_info   = columns_info[i_col]
            fmt          = i_col_info["text_format"]
            col_text     = i_col_info["column_head"]

            line_parts.append( fmt.format( x =  col_text  ) )

        line    = "".join( line_parts )
        #rint( line, flush = True )

        self.fileout.write( line   + "\n" )

    #----------------------
    def write_row(self, row_object ):
        """
        what is says
        Args: Return: state change, output
        Raises: none planned
        for now just accumulate, then render in footer
        might want to output in pages... chunks
        this needs a parse in the header to get the right columns, for now hardcode
        """
        # probably could zip columns and row_object
        #self.included_columns
        columns_info  = self.builder.columns_info   # believe it is also a dict like a data dict
        columns_out   = self.builder.columns_out
        line_parts    = []
        for  ix   in self.included_columns :
            i_columns_out  = columns_out[ix]
            i_col_info     = columns_info[i_columns_out]
            fmt            = i_col_info["curly_format"]

            line_parts.append( fmt.format( x = str( row_object[ix] ) ) )

        line    = " - ".join( line_parts )    # but odd if just one cloumn
        #rint( "the line is", line )

        #rint( line, flush = True )

        self.fileout.write( ">> " +  line   + "\n\n" )

    #---------------------
    def write_footer(self, footer_info ):
        """
        what is says
        Args: Return: state change, output
        Raises: none planned
        """
        self.fileout.close( )
#        msg       = "\n".join( lines )
#        AppGlobal.logger.log( AppGlobal.force_log_level, i_line )
#====================================
class SelectZapWriter( object ):
    """
    Zap right to message area
    how different from message one or other not maintained neight works right now
    """
    #----------- init -----------
    def __init__(self, builder ):
        """
        what is says
        """
        self.builder                = builder
        self.file_name              = builder.output_name
        self.columns                = builder.columns_out
        self.included_columns       = [ 2 ]   # later parse for these

    #----------- init -----------
    def write_header(self,  ):
        """
        what is says
        Args: Return: state change, output
        Raises: none planned
        """
        msg   = "write header for MessageWriter ...."
        AppGlobal.print_debug( msg )

        #self.fileout                = open( self.file_name, "w", encoding = "utf8", errors = 'replace' )

        columns_info  = self.builder.columns_info   # believe it is also a dict like a data dict
        columns_out   = self.builder.columns_out
        line_parts    = []
        for  ix, i_col in enumerate( columns_out ):

            i_col_info   = columns_info[i_col]
            fmt          = i_col_info["curly_format"]
            col_text     = i_col_info["column_head"]

            line_parts.append( fmt.format( x =  col_text  ) )

        line    = "".join( line_parts )
        #rint( line, flush = True )

        AppGlobal.gui.display_string( line   + "\n" )

    #----------------------
    def write_row(self, row_object ):
        """
        what is says
        Args: Return: state change, output
        Raises: none planned
        for now just accumulate, then render in footer
        might want to output in pages... chunks
        this needs a parse in the header to get the right columns, for now hardcode
        """
        # probably could zip columns and row_object
        columns_info  = self.builder.columns_info   # believe it is also a dict like a data dict
        columns_out   = self.builder.columns_out
        line_parts    = []

        for  ix, i_col in enumerate( columns_out ):

            i_col_info   = columns_info[i_col]
            fmt          = i_col_info["curly_format"]
            line_parts.append( fmt.format( x = str( row_object[ix] ) ) )

        line    = " - ".join( line_parts )    # but odd if just one cloumn
        #rint( "the line is", line , flush = True)

        #self.fileout.write( ">> " +  line   + "\n\n" )
        AppGlobal.gui.display_string( ">> " +  line   + "\n\n" )

    #---------------------
    def write_footer(self, footer_info ):
        """
        what is says
        Args: Return: state change, output
        Raises: none planned
        """
        pass
        #self.fileout.close( )
#        msg       = "\n".join( lines )
#        AppGlobal.logger.log( AppGlobal.force_log_level, i_line )


#====================================
class SelectHTMLWriter( SelectWriter ):
    """
    HTML.py - a Python module to easily generate HTML tables and lists | Decalage
        *>url  https://www.decalage.info/python/html
    ?? use tuple to reduce memory use
    """
    #----------- init -----------
    def __init__(self, builder ):
        """
        what is says
        """
        super().__init__( builder )

        # self.builder                = builder
        # self.file_name              = builder.output_name
        # self.columns                = builder.columns_out

        self.current_rows           = 0
        self.max_current_table_rows = 200    # plan to output after this many !!
        self.current_table_rows     = 0

    #----------- init -----------
    def write_header(self,  ):
        """
        what is says
        Args: Return: state change, output
        Raises: none planned
        """
        #msg   = "html write header...."
        #AppGlobal.print_debug( msg )
        self.open_output_file()
        #self.fileout       = open( self.file_name, "w", encoding = "utf8", errors = 'replace' )


        columns_info  = self.builder.columns_info
        columns_out   = self.builder.columns_out
        line_parts    = []
        for  ix, i_col in enumerate( columns_out ):

            i_col_info   = columns_info[i_col]
            fmt          = i_col_info["text_format"]
            col_text     = i_col_info["column_head"]

            line_parts.append( fmt.format( x =  col_text  ) )

        self.line_parts    = line_parts   # for later use
        self.html_table    = HTML.Table( header_row = line_parts )

        msg   = f"SelectHTMLWriter write_header()  columns_out  {columns_out}"
        #AppGlobal.print_debug( msg )

        self.fileout                = open( self.file_name, "w", encoding = "utf8", errors = 'replace' )

        #<h1>Bob fell over the chicken. [H1]</h1>   # heades at different levels
        i_line    = f"<h2>SelectHTMLWriter output from {AppGlobal.controller.app_name} {AppGlobal.controller.version}</h2>"
        self.fileout.write( i_line )

        i_line    = f"<h2>Output for: {self.builder.select_name}<h2>"
        self.fileout.write( i_line  )

        i_line    = f"<h3>SQL used was = {self.builder.sql}</h3>"
        self.fileout.write( i_line  )

#        lines.append( i_line  )
#        lines.append( f" self.table_info.sql = {self.table_info.sql}"  )
#
#        msg       = "\n".join( lines )
#        AppGlobal.logger.log( AppGlobal.force_log_level, msg )

    #----------------------
    def write_row(self, row_object ):
        """
        what is says
        Args: Return: state change, output
        Raises: none planned
        for now just accumulate, then render in footer
        might want to output in pages... chunks
        """
        self.current_table_rows     += 1
        # may want to add formatting see txt write_row
        line_parts   = self.format_row( row_object )
        self.html_table.rows.append( line_parts )
        if self.current_table_rows > self.max_current_table_rows:
            # output and start a new one
            # !! put some blank space between tables, move max to parameters,
            #?? can we keep col width more consisten
            # perhaps thru headers
            htmlcode      = str( self.html_table )
#           AppGlobal.print_debug( htmlcode )
            self.fileout.write( htmlcode )
            self.current_table_rows     = 0

            self.html_table    = HTML.Table( header_row = self.line_parts )

    #---------------------
    def write_footer(self, footer_info ):
        """
        what is says
        Args: Return: state change, output
        Raises: none planned
        """
        # pass
        # return
        htmlcode      = str( self.html_table )
#        AppGlobal.print_debug( htmlcode )

        self.fileout.write( htmlcode )

        html    = f"<p>{footer_info}</p>"
        self.fileout.write( html )

#        i_line    =  ":======== eof footer ============"
#        self.fileout.write( i_line   + "\n" )

        # # try out this   !! update for new pseudo cols
        # if self.builder.ix_twr  is not None:

        #         average_word_rank   = self.builder.total_word_rank  / self.builder.row_count
        #         msg   = f"average word rank = {average_word_rank}"
        #         i_line    = f"<h2>...{msg}...</h2>"
        #         self.fileout.write( i_line )

        self.fileout.close( )
#        msg       = "\n".join( lines )
#        AppGlobal.logger.log( AppGlobal.force_log_level, i_line )




# ==============================================
if __name__ == '__main__':
    """
    run the app: here for convenience of launching
    """
    # import sys
    # sys.path.append( r"D:\Russ\0000\python00\python3\_examples"  )
    # import ex_helpers       # ex_helpers.info_about_obj()
    import tweet_app
    a_app = tweet_app.TweetApp(  )
# ======================== eof ======================


