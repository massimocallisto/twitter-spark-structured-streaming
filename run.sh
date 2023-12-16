#/bin/sh

/opt/spark/bin/spark-submit \
  --master spark://192.168.205.3:7077 \
  --packages org.mongodb.spark:mongo-spark-connector_2.13:10.2.1 \
  --conf "spark.mongodb.write.connection.uri=mongodb://192.168.205.3/sentiment.tweets" \
  sentiment_analysis.py
