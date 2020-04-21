from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, IntegerType, StructType, StructField


spark = SparkSession.builder.appName("join_tests").getOrCreate()
schema = StructType(
    [StructField("id", IntegerType()), StructField("value", StringType())]
)


A = spark.createDataFrame(
    schema=schema, data=[
        (1, "A"),
        (2, "B"),
        (3, "C"),
        (4, "D"),
        (5, "E"),
        (None, "Z")
    ]
)

B = spark.createDataFrame(
    schema=schema, data=[
        (3, "C"),
        (4, "D"),
        (5, "E"),
        (6, "F"),
        (7, "G")
    ]
)

# INNER JOINS
# A.join(B, ["id"], "inner").show()

# CROSS JOINS (CARTESIAN PRODUCT)
# A.crossJoin(B).show()

# FULL JOINS
# A.join(B, ["id"], "outer").show()
# A.join(B, ["id"], "full").show()
# A.join(B, ["id"], "full_outer").show()

# LEFT OUTER
# A.join(B, ["id"], "left").show()
# A.join(B, ["id"], "left_outer").show()

# RIGHT OUTER
# A.join(B, ["id"], "right").show()
# A.join(B, ["id"], "right_outer").show()

# LEFT SPECIAL
# A.join(B, ["id"], "left_semi").show()
# A.join(B, ["id"], "left_anti").show()
