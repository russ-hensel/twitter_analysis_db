# twitter_analysis_db

First code this is an alpha release.
Works for me, run from a development environment, I use Spyder 

```
The point:

Quickly select and view tweets ( typically for a single person based on a number of criteria ).
Display concordance and simple linguistic analysis for a body of tweets.
Provide a database of tweet and concordance data for analysis using tools external to the app.

This program hassupporting functionality:

Load a body of tweets into a database ( currently sqlite )
Break the tweets down into a concordance.
Have an accompanying db of English words ( right now sourced from Kaggle )
Provide a variety of queries against the database for possible enlightenment.
I will try to documented well enough so people can relatively easily extend and adapt the program. Or as alternative they can use other tools with the database like SQLiteStudio. It should be fairly easy to download and use even for those without a desire to dive into the code but, I assume some knowledge of Python, and a Python Environment to run it in. In Python 3.6 or so.

Status:

Mostly works.  I am at the point of no longer introducing major features and just working at cleaning up what I have.  While I have a nice concordance, I am still not doing as much with it as I think it might offer.  I am shifting my efforts to other projects so this may become more static untill I again refocus on it.  That said I will continure to upgrade for the immediate future.

So what are the features?

Free open source
Runs across OSs Linux ( inc Raspberry Pi ), Mac or Windows we hope 
Python
Multiple tables, preloaded with sample data.
Database Interface ( sqlite, could be modified for other relational databases )
Parameter file for wide range of modifications of program behavior.
Uses standard Python logging class.

```

Guide to directories and files:
```
  .... whatever --|
                    |
                    |-- twitter_analysis_db ----| -> all code required to run the application  
                                                |    some logs from my running of the code may or may not be present, these will be deleted as they creep in, when you run the program you will
                                                |    get your own log files ... all typically named xxx.py_log 
                                                |
                                                | -- input -> input files I have used to build the db -- may have sub directories 
                                                | -- output -> output files, if present from my runs, ok to delete
                                                | -- help -> help files used by the application 
                                                | -- wiki_etc -> various files documenting program, including at least some of the material from the open circuits wiki, image files
```
Some individual files:
         comming soon see the readme_rsh.txt that is in each directory ( maybe ).

More documentation starting at:  http://www.opencircuits.com/Twitter_Analysis_DB#Goal

 
