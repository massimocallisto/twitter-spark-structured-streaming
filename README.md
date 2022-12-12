<H1>Sentiment analysis on streaming twitter data using Spark Structured Streaming & Python </H1>

Original example: https://towardsdatascience.com/sentiment-analysis-on-streaming-twitter-data-using-spark-structured-streaming-python-fc873684bfe3

## Requirements and assumption:
To run this example you need:
* A local Spark cluster (docker, wsl, native linux)
* A local MongoDB instance listening on port  27017
* API access to Twitter to provide in   twitter_connection.py

In the example the master node is  `spark://master:7070`

Also those python libraries are requires to install

    pip install tweepy==3.10.0
    pip install textblob

## How to run the example
### Run the twitter connector
Remember to ser the API keys. Change the keyword and language if ou want

    twitter_connection.py

After the run the server fill expose a local port `5555` to send to the client the tweets read from Twitter.
No data will be printed as soon as a client connects.

### Run the twitter connector
Update the master ulr in the python file as weel as the mondo address. Finally run the command:

```
/opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
  sentiment_analysis.py
```

If you are lucky, you will see a lot of output in the console and Mongo will contains the exported messages as expected.


## Original Descritpion

This project is a good starting point for those who have little or no experience with <b>Apache Spark Streaming</b>. We use Twitter data since Twitter provides an API for developers that is easy to access.
We present an end-to-end architecture on how to stream data from Twitter, clean it, and apply a simple sentiment analysis model to detect the polarity and subjectivity of each tweet.

<b> Input data:</b> Live tweets with a keyword <br>
<b>Main model:</b> Data preprocessing and apply sentiment analysis on the tweets <br>
<b>Output:</b> A parquet file with all the tweets and their sentiment analysis scores (polarity and subjectivity) <br>

<img align="center"  width="90%" src="https://github.com/stamatelou/twitter_sentiment_analysis/blob/master/architecture.png">

We use Python version 3.7.6 and Spark version 2.4.7. We should be cautious on the versions that we use because different versions of Spark require a different version of Python. 

## Main Libraries
<b> tweepy:</b> interact with the Twitter Streaming API and create a live data streaming pipeline with Twitter <br>
<b> pyspark: </b>preprocess the twitter data (Python's Spark library) <br>
<b> textblob:</b> apply sentiment analysis on the twitter text data <br>

## Instructions
First, run the <b>Part 1:</b> <i>twitter_connection.py</i> and let it continue running. <br>
Then, run the <b>Part 2:</b> <i>sentiment_analysis.py</i> from a different IDE. 

## Part 1: Send tweets from the Twitter API 
In this part, we use our developer credentials to authenticate and connect to the Twitter API. We also create a TCP socket between Twitter's API and Spark, which waits for the call of the Spark Structured Streaming and then sends the Twitter data. Here, we use Python's Tweepy library for connecting and getting the tweets from the Twitter API. 

## Part 2: Tweet preprocessing and sentiment analysis
In this part, we receive the data from the TCP socket and preprocess it with the pyspark library, which is Python's API for Spark. Then, we apply sentiment analysis using textblob, which is Python's library for processing textual data. After sentiment analysis, we save the tweet and the sentiment analysis scores in a parquet file, which is a data storage format.



