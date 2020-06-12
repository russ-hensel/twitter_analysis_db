# -*- coding: utf-8 -*-

""""
not really testing much but perhaps one


may let a new relief program run out of money.  https://t.co/2nihHg8DQw via @WSJ,04-10-2020 05:17:1

"""






import unittest


from   app_global import AppGlobal
import load_tweet_data


class ExTests( unittest.TestCase ):
    """
    not really test but may be with time
    need to look at return from a list of concord words, but order does
    not matter
    * need to generate the right answer
    * may need to sort into a defined order
    * then compare
    seems like a pain -- could construct so just tested
    the one function ?? set aside for later, for now just visual inspedt
    """

    # ------------------------------
    def parse_one( self, tweet ):
        """
        look at url processing
        """
        parsed_tweet             = load_tweet_data.ParsedTweet( tweet = tweet, tweet_id = "666" )
        parsed_tweet.who_tweets  = "dJt"

        if tweet.startswith( "RT"):  # be careful where we lower case
            parsed_tweet.tweet_type  = "retweet"

        parsed_tweet.parse_me( )

        return parsed_tweet

    # ------------------------------
    def xtest_f1( self ):
        """

        """

        tweet    = "joe to all http:aurl"
        print( f">>{tweet}<<" )
        parsed_tweet   = self.parse_one(  tweet )
        print(  f"parsed_tweet =>>>>>> {parsed_tweet}" )
        concord_list   = parsed_tweet.concordance_words
        # for i_concord_word in concord_list:
        #     i_concord_word.string, i_concord_word.string


        actual        = 30.1
        expected      = 30.1
        self.assertEqual( actual, expected )    # THERE  are other assertions

    # ------------------------------
    def xtest_f2( self ):
        """

        """
        tweet    = "joe to all https:aurl_with_https"
        print( f">>{tweet}<<" )
        parsed_tweet   = self.parse_one(  tweet )
        print(  f"parsed_tweet =>>>>>> {parsed_tweet}" )
        concord_list   = parsed_tweet.concordance_words

    # ------------------------------
    def xtest_f2( self ):
        """

        """
        tweet    = "joe to all a single secure url https:aurl_with_https"
        print( f">>{tweet}<<" )
        parsed_tweet   = self.parse_one(  tweet )
        print(  f"parsed_tweet =>>>>>> {parsed_tweet}" )
        concord_list   = parsed_tweet.concordance_words

    # ------------------------------
    def test_f2( self ):
        """

        """
        tweet    = "Two_tail both_http  http:url_1_http http:url_2_http"
        print( f">>{tweet}<<" )
        parsed_tweet   = self.parse_one(  tweet )
        print(  f"parsed_tweet =>>>>>> {parsed_tweet}" )
        concord_list   = parsed_tweet.concordance_words


    # ------------------------------
    def xtest_f2( self ):
        """
        test tweet parsing -- tweet explains test
        """
        tweet    = "joe to all a Two_tail one of_each type http:url_with_https http:url_2_http"
        print( f">>{tweet}<<" )
        parsed_tweet   = self.parse_one(  tweet )
        print(  f"parsed_tweet =>>>>>> {parsed_tweet}" )
        concord_list   = parsed_tweet.concordance_words


    # ------------------------------
    def xtest_f2( self ):
        """
        test tweet parsing -- tweet explains test
        """
        tweet    = "Two_http_one_followed by_non_url http:url_1_http then some_text http:url_2_http"
        print( f">>{tweet}<<" )
        parsed_tweet   = self.parse_one(  tweet )
        print(  f"parsed_tweet =>>>>>> {parsed_tweet}" )
        concord_list   = parsed_tweet.concordance_words


    # ------------------------------
    def xtest_f2( self ):
        """
        test tweet parsing -- tweet explains test
        """
        tweet    = "Two_https_one_followed by_non_url https:url_1_http then some_text http:url_2_http"
        print( f">>{tweet}<<" )
        parsed_tweet   = self.parse_one(  tweet )
        print(  f"parsed_tweet =>>>>>> {parsed_tweet}" )
        concord_list   = parsed_tweet.concordance_words

    # ------------------------------
    def xtest_f2( self ):
        """
        test tweet parsing -- tweet explains test
        """
        tweet    = "realdata_fail_let_a new relief program run out of money.  https://t.co/2nihHg8DQw via @WSJ"
        print( f">>{tweet}<<" )
        parsed_tweet   = self.parse_one(  tweet )
        print(  f"parsed_tweet =>>>>>> {parsed_tweet}" )
        concord_list   = parsed_tweet.concordance_words

    # ------------------------------
    def xest_f3( self ):
        """
        test tweet parsing -- tweet explains test
        """
        tweet    = "a https://t.co/gdDcamhY9M,01-12-2020"
        print( f">>{tweet}<<" )
        parsed_tweet   = self.parse_one(  tweet )
        print(  f"parsed_tweet =>>>>>> {parsed_tweet}" )
        concord_list   = parsed_tweet.concordance_words

    # ------------------------------
    def test_f4( self ):
        """
        test tweet parsing -- tweet explains test
        """
        tweet    = "lead_word   http://t.co/gdDcamhY9M trail_word"
        tweet    = "lead_word   http://url_1  http://url_2  trail_word"
        tweet    = "lead_word   https://url_1 middle_word  http://url_2  trail_word"
        print( f">>{tweet}<<" )
        parsed_tweet   = self.parse_one(  tweet )
        print(  f"parsed_tweet =>>>>>> {parsed_tweet}" )
        concord_list   = parsed_tweet.concordance_words

        # parsed_tweet   = self.parse_one(  "joe to all http:" )
        # print(  f"parsed_tweet =>>>>>> {parsed_tweet}" )

        # parsed_tweet   = self.parse_one(  "joe to all https:url_with_https" )
        # print(  f"parsed_tweet =>>>>>> {parsed_tweet}" )

        # actual        = 30.1
        # expected      = 30.1
        # self.assertEqual( actual, expected )    # THERE  are other assertions

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
    print( "------------- Begin Unit Test   ---------------------" )
    unittest.main(exit=False)






