from pyspark.sql import SparkSession

print("hello world from a sub-package")
spark = SparkSession.builder.getOrCreate()
