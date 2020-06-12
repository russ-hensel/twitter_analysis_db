# -*- coding: utf-8 -*-

""""
this is a template for example or template files




"""



# ----------------------------------------
def   ex_1():
    print("""
    ================ ex_1(): ===============
    """)



#ex_1()


# ----------------------------------------
def   ex_2():
    print("""
    ================ ex_2(): ===============
    """)


#ex_2()


# ----------------------------------------
def   ex_3():
    print("""
    ================ ex_3(): ===============
    """)


#ex_3()


##-------------------------- prob do not want to use --------------------------------------------
#if __name__ == "__main__":

#    print """ ================================ run main ==================================
#
#
#
#    """
#    print"""Seting some standards....
#    """
#
#    ex_4()



# -*- coding: utf-8 -*-


#import a1

import unittest


import ex_unit_test_me


class ExTests( unittest.TestCase ):
    """ Test class for function a1.stock_price_summary. """

    def test_f1( self ):
        """

        """

        actual        = ex_unit_test_me.function1(5, 6)
        expected      = 30.1
        self.assertEqual( actual, expected )    # THERE  are other assertions





class TestSwapK( unittest.TestCase ):
    """ Test class for function a1.stock_price_summary. """

#    def est_doc_test( self ):
#        """
#        same as original doc test
#        """
#        a_list        = [1, 2, 3, 4, 5, 6]
#        a_none        = a1.swap_k( a_list, 2 )
#        actual        = a_list
#        expected      = [5, 6, 3, 4, 1, 2]
#        self.assertEqual( actual, expected )
#
#
#
#
#    def est_len_0( self ):
#        """
#        same as original doc test but odd number of elements
#        """
#        a_list        = []
#        a_none        = a1.swap_k( a_list, 0 )
#        actual        = a_list
#        expected      = []
#        self.assertEqual( actual, expected )
#
#
#
#    def est_len_1_0( self ):
#        """
#        same as original doc test but odd number of elements
#        """
#        a_list        = ["a"]
#        a_none        = a1.swap_k( a_list, 0 )
#        actual        = a_list
#        expected      = ["a"]
#        self.assertEqual( actual, expected )
#
#    def est_len_1_1( self ):
#        """
#        same as original doc test but odd number of elements
#        """
#        a_list        = ["a"]
#        a_none        = a1.swap_k( a_list, 1 )
#        actual        = a_list
#        expected      = ["a"]
#        self.assertEqual( actual, expected )
#
#    def  est_len_n_0( self ):
#        """
#        same as original doc test but odd number of elements
#        """
#        a_list        = ["a","b"]
#        a_none        = a1.swap_k( a_list, 0 )
#        actual        = a_list
#        expected      = ["a","b"]
#        self.assertEqual( actual, expected )
#
#    def est_len_n_1( self ):
#        """
#        same as original doc test but odd number of elements
#        """
#        a_list        = ["a","b"]
#        a_none        = a1.swap_k( a_list, 0 )
#        actual        = a_list
#        expected      = ["a","b"]
#        self.assertEqual( actual, expected )
#
#
#    def est_doc_test_odd( self ):
#        """
#        same as original doc test but odd number of elements
#        """
#        a_list        = [1, 2, 3, 4, 5, 6, 7]
#        a_none        = a1.swap_k( a_list, 2 )
#        actual        = a_list
#        expected      = [6, 7, 3, 4, 5, 1, 2]
#        self.assertEqual( actual, expected )
#
#    def est_doc_test_odd_max( self ):
#        """
#        same as original doc test but odd number of elements and max k = 3 here
#        """
#        a_list        = [1, 2, 3, 4, 5, 6, 7]
#        a_none        = a1.swap_k( a_list, 3 )
#        actual        = a_list
#        expected      = [5, 6, 7, 4, 1, 2, 3]
#        self.assertEqual( actual, expected )
#
#    def est_doc_test_odd_odd( self ):
#        """
#        same as original doc test but odd number of elements and odd k
#        """
#        a_list        = [1, 2, 3, 4, 5, 6, 7]
#        a_none        = a1.swap_k( a_list, 3 )
#        actual        = a_list
#        expected      = [5, 6, 7, 4, 1, 2, 3]
#        self.assertEqual( actual, expected )
#
#    def est_doc_test_odd_one( self ):
#        """
#        same as original doc test but odd number of elements and k = 1
#        """
#        a_list        = [1, 2, 3, 4, 5, 6, 7]
#        a_none        = a1.swap_k( a_list, 1 )
#        actual        = a_list
#        expected      = [7, 2, 3, 4, 5, 6, 1,]
#        self.assertEqual( actual, expected )
#
#    def est_doc_test_two_one( self ):
#        """
#        mininum length list
#        """
#        a_list        = [1, 2, 3, 4, 5, 6, 7]
#        a_none        = a1.swap_k( a_list, 1 )
#        actual        = a_list
#        expected      = [7, 2, 3, 4, 5, 6, 1,]
#        self.assertEqual( actual, expected )
#


if __name__ == '__main__':
    print( "" )
    print( "" )
    print( "------------- Begin Unit Test Swap K ---------------------" )
    unittest.main(exit=False)






