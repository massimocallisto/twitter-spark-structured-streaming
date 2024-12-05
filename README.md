<H1>Sentiment analysis on streaming twitter data using Spark Structured Streaming & Python </H1>

Original example: https://towardsdatascience.com/sentiment-analysis-on-streaming-twitter-data-using-spark-structured-streaming-python-fc873684bfe3

**Update: this example is no longer valid due to the Twitter X API update program. Now it is required a paid subscription to read twees.** See more on this [link](https://developer.twitter.com/en/docs/twitter-api/getting-started/about-twitter-api]). The examplen has been updated to work in combination of a remote TCP server.


## Requirements and assumption:
To run this example you need:
* A local Spark cluster (docker, wsl, native linux). *Tested on Spark 3.5.3, Java 11, Python 3.10.12*
* A local MongoDB instance listening on port  27017
*  ~~API access to Twitter to provide in   twitter_connection.py~~

In the example the master node is  `spark://master:7070`

Also those python libraries are requires to install

    pip install textblob

## How to run the example

1. Start Mongo
2. Start a local TCP server
3. Run `sentiment_analysis.py` Spark's application
4. Send strings over the TCP server

Detailed steps are reported below.

### Run Mongo
Run the `docker_compose.yaml` file in this directory.

    docker-compose up -d

This command will run a local instance of Mongo. 

### Run TCP Server
In a different terminal start the tcp socket on port 5555

    nc -lk 5555

Each line of text followed by a new line will be sent to a connected client.

### Run the Spark job
Update the master ulr in the python file as weel as the mondo address. Finally run the command:


```
spark-submit \
  --master spark://primary:7077 \
  --packages org.mongodb.spark:mongo-spark-connector_2.12:10.4.0 \
  --conf "spark.mongodb.write.connection.uri=mongodb://192.168.205.8/sentiment.tweets" \
  sentiment_analysis.py
```

You can omit the `--master` option if you want to use the local execution of Spark. Remember to change the IP address according to your configuration.

**Note 1**: the `--packages` will download the Java dependency of Mongo. You can add more `--package` options do download further dependencies. 

**Note 2**: take a look on your version of Spark and the releted Scala version (`2.13` in `org.mongodb.spark:mongo-spark-connector_2.13:10.2.1`). If you use a different version, update the connector accordingly. 

**Note 3**: if you are using a Spark cluster, remember that the code run remotly. All the dependencies must be satisfied on the worker nodes. 
