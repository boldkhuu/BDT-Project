import sys
import json
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pykafka import KafkaClient
from collections import OrderedDict


def pushTrendsInKafka(trends):
    client = KafkaClient(hosts="localhost:9092")
    topic = client.topics['twitter-trends']
    obj = OrderedDict()
    for trend in trends:
        obj[trend[1]] = trend[0]
    with topic.get_producer() as producer:
        producer.produce(json.dumps(obj))


def getHashtags(data):
    parsed = json.loads(data[1])
    if not 'entities' in parsed or not 'hashtags' in parsed['entities']:
        return []
    return parsed['entities']['hashtags']


if __name__ == "__main__":
    zkQuorum = "localhost:2181"
    topic = "twitter"

    if len(sys.argv) != 2:
        print("Usage: sparkStream.py <seconds_to_run>")
        exit(-1)
    seconds_to_run = int(sys.argv[1])

    sc = SparkContext("local[2]", "TwitterStreamKafka")
    ssc = StreamingContext(sc, seconds_to_run)
    ssc.checkpoint('checkpoint')

    stream = KafkaUtils.createStream(
        ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})

    # Tweet processing
    trends = stream \
        .flatMap(getHashtags) \
        .map(lambda x: (x['text'], 1)) \
        .reduceByKeyAndWindow(lambda x, y: x + y, lambda x, y: x - y, seconds_to_run * 20, seconds_to_run) \
        .map(lambda (k, v): (v, k)) \
        .transform(lambda rdd: rdd.sortByKey(False))

    # trends.foreachRDD(lambda rdd: rdd.foreachPartition(pushTrendsInKafka))
    trends.foreachRDD(lambda rdd: pushTrendsInKafka(rdd.take(10)))

    ssc.start()
    ssc.awaitTermination()
