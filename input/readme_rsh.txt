C:\Russ\python\tweet_concordance\readme_rsh.txt



before moved was:
      D:\Russ\0000\python00\python3\_projects\covid_data\trump\readme_rsh.txt


      toc
          Status
          code and WorkFlow  ... workflow obsolete
          trump and word info
          old sql   .............. moving to some_querries.txt


          ======================= scratch

          concord joined to words

          concord_joined_select_1


=========== Status:

=========== Some ideas for work or past work !! = do it, ?? = perhaps do it, ** = done, xx = dropped at least for now

        !! select types .....

                just tweets   criteria   dates, text like, tweet_type, is_covid
                concondance/words    criteria dates
                                     join tweets for dates, words for rank this is the one i worked on



                have slect type show what columns

                concordance 1     columns:   word, word_type, word_rank, word_count
                                  select:    dates min_rank, max_count  is_covid  tweet_type    average word rank
                                  group by   concord.word
                                  order by   rank count concordance.word
                                  having

        !! Ver 10 fix up names for selects


        concordance  tweets xref to concordance   tx xref con

        ** decode for is_ascii and word_type
        ** get gui name for select into header

        ** next work  on gui to build the database tables

        ** remove stuff in parse   ? paren be careful # and @ do not remove
                                   substituee " of various kinds or remove

        ** word type .... leading number  ?? test decode

        ** add decode word type

        !! clean up gui select management

        !! delete 's       joe's   but not for it's   change to it is or treat as word what about other

        note rt is a word for retweet

        *! add test select after load -- need one for words ... do not select all just some a's

        !! csv without sql timing... just data or data and colum headers
        ** gui 80% effective, does not crash mostly run something

        ** move more stuff to gui some only avail from command line

        ** display sql prior to final run of select

        ** add calculated columns
            *! add average rank, median to some queries

        ** reset default search

        !! include sql in reports as an option .... keep in log as info ??
        ** add not ascii as an atribute to covid is_ascii

        ** add word like -- perhaps auto if wildcard in word
        ** implement some Pseudo Columns  *col_name* and prior_row ..... footer support

        !! look into
        !! add a bit of logging to reports keep track of sql -- have a config parm
        ** make a select_builder   -- still called sql_builder incorporate select_dict

        ** add html output -- ?? consider paging
        ** add yamal like txt output
        !! add pickled np array or similar
        ** add output to message area

        !! get icon for bird
            Twitter Icon - Free Download, PNG and Vector
            https://icons8.com/icon/3861/twitter
            C:\Russ\python\tweet_concordance\help\icons8-twitter-240.png

            icons8-twitter-squared-96
            C:\Russ\python\tweet_concordance\help\icons8-twitter-squared-96.png
            Twitter Squared Icon - Free Download, PNG and Vector
            https://icons8.com/icon/60469/twitter-squared

            twitter.png
            Free twitter icons & vector files in Black Twitter, (Icon Search Engine)
            https://findicons.com/icon/download/75612/twitter/128/png
            C:\Russ\python\tweet_concordance\help\twitter.png


        !! add indication of selection  in progress
        !! tweets ... if no selection on word drop join to other tables ??
           or at least reverse the order... a select on all concord.words is a bit much

        xx looks like we may want to add back a helper thread -- perhaps not

        *! time operations
        !! what happed to \n on gui ... seems ok

        *! put add rank into the gui

        ** set search to default

        !! compare word lists in an intelligent way

        ** add more to tweet table

        ** add show some current parms -- might add more parms

           >>Select Tweets by a Word (cb_select_tweet_word)

        gui
                *! gray out slider when not accurate
                xx add min max none for word rank --- two fields, perhaps dropdowns
                ** add is covid
                ** add max rank
                ** add min count

                ** add dropdown for output format -- but perhaps change back to 2 buttons

                ** add frame for Define DB -- then make work


----------------------------------

Select:         Tweets are selected to contain a given word, and by date-hour range
Sort:           Sorted by date-hour ascending
Output Format:  txt file
User Input:
                A word in Word Search field ( or blank for not word criteria )
                Is word a covid word
                Start Date and Hour
                End Date and Hour

                    Buttons to the right of the date controls let you set the
                    date range by some alternate methods:
                        for today
                        for this week
                        for this month ( 4 weeks )
                        for as long as twitter has been around
                        slider: backward thru time for a week sample
                            for some number of weeks into the past



               .\input\english-word-frequency\unigram_freq.csv
                    sourced from:
                    English Word Frequency | Kaggle
                    https://www.kaggle.com/rtatman/english-word-frequency/

may be from kaggle
C:\Russ\python\tweet_concordance\input\english-word-frequency
C:\Russ\python\tweet_concordance\input\english-word-frequency
C:\Russ\python\tweet_concordance\input\english-word-frequency\english-word-frequency.zip

-------------------- how to speed up sql lite

use a ram disk ..... this is really easy, do not beat up your ssd

journal off ??
index off ??
execute many ??
R:\big_test.db

------------------------- open circuit links

Recent changes - OpenCircuits
http://www.opencircuits.com/Special:RecentChanges

Category:Twitter Analysis DB - OpenCircuits
http://www.opencircuits.com/Category:Twitter_Analysis_DB

Twitter Analysis DB GUI - OpenCircuits
http://www.opencircuits.com/Twitter_Analysis_DB_GUI

Twitter Analysis DB Details - OpenCircuits
http://www.opencircuits.com/Twitter_Analysis_DB_Details

Twitter Analysis DB - OpenCircuits
http://www.opencircuits.com/Twitter_Analysis_DB

Python Desk Top Applications - OpenCircuits
http://www.opencircuits.com/Python_Desk_Top_Applications

Configuration Files For Python - OpenCircuits
http://www.opencircuits.com/Configuration_Files_For_Python

Twitter Analysis DB - OpenCircuits
http://www.opencircuits.com/Twitter_Analysis_DB



--------------------- twitter analytic links -- covid models

WordSmith Tools
https://lexically.net/downloads/version5/HTML/index.html?convert_text_file_format.htm

arizona covid data model source code at DuckDuckGo
https://duckduckgo.com/?q=arizona+++covid+data+model+source+code&t=vivaldi&ia=software

GardenMyths.com - leader in debunking gardening myths
https://www.gardenmyths.com/

Semantic Tweet Analytics with ArangoDB and Rlang
https://www.arangodb.com/why-arangodb/case-studies/kode-semantic-tweet-analytics-arangodb-rlang/

Where to get Twitter data for academic research • Social Feed Manager
https://gwu-libraries.github.io/sfm-ui/posts/2017-09-14-twitter-data

SQL on Twitter: Analysis Made Easy Using N1QL - DZone Database
https://dzone.com/articles/sql-on-twitter-twitter-analysis-made-easy

ugis22/analysing_twitter: Stream Tweets and store them in a relational DB. Perform sentiment analysis and network interaction.
https://github.com/ugis22/analysing_twitter

How to Analyze Twitter Data | Sprout Social
https://sproutsocial.com/insights/twitter-data/

COVID-19 Projections
https://github.com/covid-projections

Add multiline editing to the Editor · Issue #2112 · spyder-ide/spyder
https://github.com/spyder-ide/spyder/issues/2112



-----------------------------------------------------------



==========Code and WorkFlow  -- ever changing


    ------ matain on open circuits
    ----- all moving to gui

    ----- concord
        ----- code

        concordance.py
            will take raw input file csv and output concord table and a tweet file not db
            run from command line
                output ConcordanceDictOutput(   ):  a file of the dict of concordance -- no further use of it
                TweetOutput   writes to db ( table concord )and to file -- file used for -- maybe nothing but inspection

        db_util_tweet.py

        db_util_concord.py
            will define the concord table and do some selects


        ----- Workflow-------------------------
        to build a concord table from scratch
            make table with util
            run concord.py

        to build a tweet table from scratch
            make table with db_util_tweet.py
            take file output from concord.py and use as input to
                 db_util_tweet.py    util_insert_tweets_from_file()

            can do some select test using
                  db_util_tweet.py

    ----- tweets


    ----- words



----------------------------  trump data


precision for covid . org


(Better) - Donald Trump Tweets! | Kaggle
https://www.kaggle.com/kingburrito666/better-donald-trump-tweets



All the President’s tweets - CNN.com
https://www.cnn.com/interactive/2017/politics/trump-tweets/

Donald Trump Complete - Search Tweets, Speeches, Policies | Factbase
https://factba.se/search



Donald Trump Deleted Tweets Twitter | Factbase
https://factba.se/topic/deleted-tweets



Donald Trump Tweet's 100% Realtime | US News.com
https://u-s-news.com/donald-trump-tweets-100-realtime/



shut down but twitter
Every Donald Trump Tweet - dataset by datacrunch | data.world
https://data.world/datacrunch/every-donald-trump-tweet



Trump Tweets | US News.com
https://www.u-s-news.com/category/donald-j-trump-tweets/



this may be it !!!!!!!!!!!!!!!!!! try again may 20 seem to have to copy and paste from upper window ... slow
Trump Twitter Archive
http://www.trumptwitterarchive.com/


USA President Donald Trump on Twitter - 2009 / 2020 analysis
https://www.tweetbinder.com/blog/trump-twitter/

download trump tweets - Google Search
https://www.google.com/search?q=download%20trump%20tweets


old data and code in r
mkearney/trumptweets: Download data on all of Donald Trump's (@realDonaldTrump) tweets
https://github.com/mkearney/trumptweets



Obama White House Twitter Archive : Free Data : Free Download, Borrow and Streaming : Internet Archive
https://archive.org/details/ObamaWhiteHouseTwitterArchive

------------------ common words


English frequency word list for download | Sketch Engine
*>url   https://www.sketchengine.eu/english-word-list/




*>url  https://www.wordfrequency.info/free.asp?s=y







---------------------- scratch

Natural Language Processing With spaCy in Python – Real Python
*>url https://realpython.com/natural-language-processing-spacy-python/#what-are-nlp-and-spacy



import spacy
nlp = spacy.load('en')

doc = nlp(u"Apples and oranges are similar. Boots and hippos aren't.")

for token in doc:
    print(token, token.lemma, token.lemma_)


spacy   from navigator but then ng so tried
python -m spacy download en_core_web_sm

then worked with 'en_core_web_sm' in the code some simlink problem


====================== more possible word sources some downloaded


4000 Essential English words PDF Download | 6 Books Set
https://www.ilmcorner.com/4000-english-vocabulary-words-pdf

Current Version | WordNet
https://wordnet.princeton.edu/download/current-version

Downloading WordNet and associated packages and tools | WordNet
https://wordnet.princeton.edu/download

English Words - PDF Free Download
https://epdf.pub/english-words.html

English frequency word list for download | Sketch Engine
https://www.sketchengine.eu/english-word-list/

Frequently Asked Questions | WordNet
https://wordnet.princeton.edu/frequently-asked-questions

How to get english language word database? - Stack Overflow
https://stackoverflow.com/questions/2213607/how-to-get-english-language-word-database

List Of All English Words Database Free Download
https://list-of-all-english-words-database-software.soft112.com/

Microsoft Word - 119231_84669-vocabulary-list
https://www.cambridgeenglish.org/images/84669-pet-vocabulary-list.pdf

MySQL English Dictionary - Browse Files at SourceForge.net
https://sourceforge.net/projects/mysqlenglishdictionary/files/

Natural Language Processing With spaCy in Python – Real Python
https://realpython.com/natural-language-processing-spacy-python/#what-are-nlp-and-spacy

SCOWL (And Friends)
http://wordlist.aspell.net/

SCOWL Custom List/Dictionary Creator
http://app.aspell.net/create

User Login | WordNet
https://wordnet.princeton.edu/user/login?destination=node/31

Word frequency: based on 450 million word COCA corpus
https://www.wordfrequency.info/top5000.asp

Word frequency: based on 450 million word COCA corpus
https://www.wordfrequency.info/5k_lemmas_download.asp

Word frequency: based on 450 million word COCA corpus
https://www.wordfrequency.info/

WordWeb: Free English dictionary and thesaurus download
https://wordweb.info/free/

Wordlists - word frequency lists | Sketch Engine
https://www.sketchengine.eu/guide/wordlist-frequency-lists/#toggle-id-3

dwyl/english-words: A text file containing 479k English words for all your dictionary/word-based projects e.g: auto-completion / autosuggestion
https://github.com/dwyl/english-words

entries.pdf
https://www.wordfrequency.info/files/entries.pdf

https://wordnetcode.princeton.edu/3.0/README
https://wordnetcode.princeton.edu/3.0/README

wordnet-mysql-20
http://androidtech.com/html/wordnet-mysql-20.php

download english lemma dataset at DuckDuckGo
https://duckduckgo.com/?q=download+english+lemma+dataset&t=vivaldi&ia=software

download english lemma dataset at DuckDuckGo
https://duckduckgo.com/?q=download+english+lemma+dataset&t=vivaldi&ia=software

Page not found (error) | The MIT Press
https://mitpress.mit.edu/book-home.tcl?isbn=026206197X

Text Analysis in R made easy with Udpipe - Towards Data Science
https://towardsdatascience.com/easy-text-analysis-on-abc-news-headlines-b434e6e3b5b8

Search | Kaggle
https://www.kaggle.com/search

Search | Kaggle
https://www.kaggle.com/search

Sign in - Google Accounts
https://accounts.google.com/signin/oauth/oauthchooseaccount?response_type=code&client_id=378513217926-6q3lp8ojftf1i14dlrj0udqh4ou2jjok.apps.googleusercontent.com&redirect_uri=https%3A%2F%2Fwww.kaggle.com%2Fsignin-google&scope=openid%20profile%20email&state=CfDJ8LdUzqlsSWBPr4Ce3rb9VL_Kefga5JdYBpntkRHAA0AelKKFfmwOQTZnwPdN3KU7y0gSlVSC51CxC70SRBPurNnDFXW_eIT5PAX2PmHwXCEp917rAcscadH2eOB5LzLCw3h28P1qMeqc21l-HKoC0iEmd1IaDpPWG5BqISgwl94RIvYnD7dm2ZdYQly9ftWxgXp3jntFXao3P7QhFgU8n2hC609N_1ZuQHTSkji_qgChtJNyXLs96CjzY_UFpBRsCq7h7tDIxhLg0jv8uUmohEtXxnsiQ9YZSaInMtNxeaHwy9H-ou1iMbMe6BfrUX26sHznJ7UfAqeQu0W4TKFW8wo&o2v=2&as=iuRun39m7trsuUb5-chAiw&flowName=GeneralOAuthFlow

https://raw.githubusercontent.com/michmech/lemmatization-lists/master/lemmatization-en.txt
https://raw.githubusercontent.com/michmech/lemmatization-lists/master/lemmatization-en.txt

dwyl/english-words: A text file containing 479k English words for all your dictionary/word-based projects e.g: auto-completion / autosuggestion
https://github.com/dwyl/english-words/


Find Open Datasets and Machine Learning Projects | Kaggle
https://www.kaggle.com/datasets

michmech/lemmatization-lists: Machine-readable lists of lemma-token pairs in 23 languages.
https://github.com/michmech/lemmatization-lists/

dwyl/english-words: A text file containing 479k English words for all your dictionary/word-based projects e.g: auto-completion / autosuggestion
https://github.com/dwyl/english-words/





