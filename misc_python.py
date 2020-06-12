# -*- coding: utf-8 -*-
"""
Created on Sat May 30 15:50:21 2020

misc code stuff


"""


"""
buckets for frequency graphs.... do on rank or count
count goes to about 330k




"""

import math



# ==========================================================
def ex_named_tuples_elements():
    print( """
    ----------------------- ex_named_tuples_elements()   ------------

    """ )
    ThreeParts = collections.namedtuple( 'ThereParts', 'index_1 index_2, index_3')
    an_example   = ThreeParts( index_1  = "aaa", index_2 = "bbb", index_3 = "ccc" )
    print( an_example )

    print( an_example.index_1 )
    print( an_example[ 1 ] )
    #print( an_example[ "index_1" ] )   # error


#ex_named_tuples_elements()



# ==========================================================
def ex_char_codes():
    print( """
    ----------------------- ex_char_codes()   ------------
    turkey's
    	hillary's
    """ )
    test_me    =   "'"      #   turkey's
    print( f"testing turkey's   >{test_me}<   ord >{ord(  test_me)}<"  )


    test_me    =   "'"      #
    print( f"testing hillary's   >{test_me}<   ord >{ord(  test_me)}<"  )

"""
	honest....are
    	flynn."(terrible
	cook!l
	two-thirds
	s&p

	usa!+israel2
	expected--we
	❤
	miners&coal
	beat—she

    thursday!mi




"""


ex_char_codes()






