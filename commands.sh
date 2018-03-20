# starting zookeeper
/usr/local/kafka/bin/zookeeper-server-start.sh /usr/local/kafka/config/zookeeper.properties

# starting kafka server
/usr/local/kafka/bin/kafka-server-start.sh /usr/local/kafka/config/server.properties

# starting hadoop dfs
/usr/local/hadoop/sbin/start-dfs.sh

# list kafka topics
/usr/local/kafka/bin/kafka-topics.sh --list --zookeeper localhost:2181

# kafka console consumer
/usr/local/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic twitter --from-beginning

# run spark streaming
/usr/local/spark/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.2.1 spark/sparkStream.py 5

# run kafka stream
python kafka/twitter.py
