# Project - Big Data Technology
Built with: Spark Streaming, Kafka, Spark SQL, Javascript

#### Start Hadoop DFS
```sh
/usr/local/hadoop/sbin/start-dfs.sh
```

#### Start zookeeper
```sh
/usr/local/kafka/bin/zookeeper-server-start.sh /usr/local/kafka/config/zookeeper.properties
```

#### Start Kafka server
```sh
/usr/local/kafka/bin/kafka-server-start.sh /usr/local/kafka/config/server.properties
```

## Project 1 - Twitter Trending hashtag /Realtime/

#### Run Spark stream
```sh
/usr/local/spark/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.2.1 spark/sparkStream.py 5
```

#### Run Kafka stream
```sh
python kafka/twitter.py
```

## Project 2 - Basketball players dataset querying

#### Run Spark SQL
```sh
cd sql
/usr/local/spark/bin/spark-submit reader.py
```
