# wikipedia-bot

## Config:

In the config file there are some configurable values for each script

## Indexer:

The indexer must be executed before being able to use the searcher script.

What does it do:

* The indexer takes the wikipedia dump as XML and slices it into smaller files of 100 wikipedia articles each.
* It also creates an index where all the titles along with the filename of the article text and the article id are stored in.
* Then the index is going to be sorted so it can be searched easily.

## Searcher:

The searcher searches the index and returns the article to a given search word. 
If the search word is not in the index but there is at least one article that starts with the search word, a list with all the optional titles is returned.

## Api:

The api script contains a REST API contains a development webserver that is running on localhost, port 5000.
The API has one endpoint ("/definition/") and accepts POST requests with an option to receive a long and a short answer.
Because the index File is loaded into memory there needs to be about 2 GiB of free Memory on the host system!

## Frontend:

Graphical client to the REST API server.

## Tests:

Some tests are implemented.
