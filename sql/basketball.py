import sys
import json
from os.path import abspath
from pyspark.sql import SparkSession

if __name__ == "__main__":
    warehouse_location = abspath('spark-warehouse')
    spark = SparkSession \
        .builder \
        .appName("Twitter Trends") \
        .config("spark.sql.warehouse.dir", warehouse_location) \
        .enableHiveSupport() \
        .getOrCreate()

    playresDF = spark.read.csv('data/Players.csv', header=True)
    playresDF.registerTempTable('players')
    statsDF = spark.read.csv('data/Seasons_Stats.csv', header=True)
    statsDF.registerTempTable('stats')

    # Top 10 tallest players
    spark.sql('SELECT Name, height FROM players ORDER BY height DESC LIMIT 10').write.json('output/top_10_tallest_players')

    # Top 10 shortest players
    spark.sql('SELECT Name, height FROM players WHERE LENGTH(height) > 0 ORDER BY height LIMIT 10').write.json('output/top_10_shortest_players')

    # Top 10 colleges
    spark.sql('SELECT college, COUNT(college) as players FROM players GROUP BY college ORDER BY players DESC LIMIT 10').write.json('output/top_10_colleges')

    # Top 10 scorers
    spark.sql('SELECT Name, SUM(CAST(PTS AS DOUBLE)) AS Points FROM stats GROUP BY Name ORDER BY Points DESC LIMIT 10').write.json('output/top_10_scorers')
