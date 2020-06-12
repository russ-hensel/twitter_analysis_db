# -*- coding: utf-8 -*-



"""

What:
Notes:



Search on:
        npl
        spacy
        how

"""


import sys
sys.path.append( r"D:\Russ\0000\python00\python3\_examples"  )
import ex_helpers

import spacy          # linguistic module words to lemmas ( might not be correct explain )


#from   app_global import AppGlobal
#import app_global

nlp             = spacy.load( 'en_core_web_sm'   )    # object to do spacy processing
                                                      # example used 'en' but throws error


"""

if use_spacy:   # if using npl spacy....
            "rebuild line, then convert to list again "
            spacy_line  = " ".join( clean_words )
            doc         = nlp( spacy_line )

            #what is doc?

            # clean_words = doc    # this is not array of words, may need to convert

            npl_words = []
            for token in doc:
                #print( token, token.lemma, token.lemma_)  # debug
                npl_words.append( (token.lemma_) )  # token   just messing with this
            #print( f"npl_words {npl_words}" )  # debug
            clean_words   = npl_words

        return clean_words


"""

"""
may get a word out that is spaces
plural to singular
contractions to ...  some seem to be converted, do we ever get 2 words instead of one, like a contraction expanded?
                     as tokenized some 1 to two

"""


# --------- Helper Function  -----
#-----divider 3
#-----divider 4 -------
def eval_it( eval_string ):
    print( f"Next eval the string {eval_string}" )
    eval( eval_string )
    # next is not really useful, eval returns None ( at least in some cases )
    # this next does run the code again in eval_string
    print(( eval_string, " => ", str( eval( eval_string )) ))

# ---------------------------------------- what
def ex_eval():
    print( """\n
    ================ ex_eval(): evaluation of a string as py code ===============
    """ )
    a_string = "print('hi there')"
    eval_it( a_string )

# ex_eval()


# --------- Helper Function  -----
# ----------------------------------------
def try_spacy( msg, spacy_line, print_it = True ):
    """
    input a line, return a list
    list is normalized words
    """

    print( f">>> {msg} \n   for spacy_line{spacy_line}" )
    doc         = nlp( spacy_line )
    npl_words = []
    for token in doc:
        print( f"        >{token}< >>{token.lemma}< >>>{token.lemma_}<" )     # debug
        npl_words.append( (token.lemma_) )
    print( f"  spacy_line: {spacy_line}" )
    print( f"  npl_words:  {npl_words}" )                # debug

    return npl_words

# ----------------------------------------
def ex_spacy_0():
    print( """
    ================ ex_spacy_0(): run spacy on a line ===============
    """)

    msg         = "try some random stuff -- case is shifted down, go to singulars"
    spacy_line  = "the quick Brown Fox Jumped OVER a fence, may fences choice choices eats the dog's face, is'nt is to be"
    npl_words   = try_spacy( msg = msg, spacy_line = spacy_line )


    spacy_line  = " witch-hunts women's      won't  wonerful  world's   worsts    wouldn't"
    npl_words   = try_spacy( msg = msg, spacy_line = spacy_line )

    # spacy_line  = " WITCH-HUNTS WOMEN'S      WON'T  WONERFUL  WORLD'S   WORSTS    WOULDN'T"
    # npl_words   = try_spacy( msg = msg, spacy_line = spacy_line )

    spacy_line  = ""
    npl_words   = try_spacy( msg = msg, spacy_line = spacy_line )


ex_spacy_0()


















