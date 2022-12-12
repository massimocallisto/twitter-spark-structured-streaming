from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import functions as F
from textblob import TextBlob

def preprocessing(lines):
    words = lines.select(explode(split(lines.value, "t_end")).alias("word"))
    words = words.na.replace('', None)
    words = words.na.drop()
    words = words.withColumn('word', F.regexp_replace('word', r'http\S+', ''))
    words = words.withColumn('word', F.regexp_replace('word', '@\w+', ''))
    words = words.withColumn('word', F.regexp_replace('word', '#', ''))
    words = words.withColumn('word', F.regexp_replace('word', 'RT', ''))
    words = words.withColumn('word', F.regexp_replace('word', ':', ''))
    return words

# text classification
def sentiment_detection(polarity):
    if polarity < 0:
      return 'Negative'
    elif polarity == 0:
      return 'Neutral'
    else:
      return 'Positive'
def polarity_detection(text):
    return TextBlob(text).sentiment.polarity
def subjectivity_detection(text):
    return TextBlob(text).sentiment.subjectivity
def text_classification(words):
    # polarity detection
    polarity_detection_udf = udf(polarity_detection, StringType())
    words = words.withColumn("polarity", polarity_detection_udf("word"))
    # subjectivity detection
    subjectivity_detection_udf = udf(subjectivity_detection, StringType())
    words = words.withColumn("subjectivity", subjectivity_detection_udf("word"))
    # sentiment detection
    sentiment_detection_udf = udf(sentiment_detection, StringType())
    words = words.withColumn("sentiment", sentiment_detection_udf("polarity"))
    return words

def write_mongo_row(df, epoch_id):
    mongoURL = "mongodb://localhost:27017/sentiment.sentiment2"
    df.write.format("mongo").mode("append").option("uri",mongoURL).save()
    pass


if __name__ == "__main__":
    # create Spark session
    spark = SparkSession.builder.master("spark://master:7077").appName("TwitterSentimentAnalysis").getOrCreate()

    # read the tweet data from socket
    lines = spark.readStream.format("socket").option("host", "0.0.0.0").option("port", 5555).load()
    # Preprocess the data
    words = preprocessing(lines)
    # text classification to define polarity and subjectivity
    words = text_classification(words)
    #words.printSchema();

    words = words.repartition(1)
    query = words.writeStream.queryName("all_tweets")\
        .outputMode("append").format("console")\
        .option("checkpointLocation", "./check")\
        .trigger(processingTime='10 seconds').start()
    query2=words.writeStream.foreachBatch(write_mongo_row).start()


    query.awaitTermination()
    query2.awaitTermination()
    