#/bin/sh

/opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
  --packages org.elasticsearch:elasticsearch-spark-30_2.12:7.16.0 \
  sentiment_analysis.py

