from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import when, col, lag, sum, lit, expr, monotonically_increasing_id
from pyspark.sql.types import StructType, StructField, DoubleType
from pyspark.sql import functions as F
import os
import shutil

def delete_spark_folders(path):
    # Get a list of all items in the specified path
    items = os.listdir(path)

    # Iterate through the items in the path
    for item in items:
        # Check if the item is a directory and starts with 'spark'
        if os.path.isdir(os.path.join(path, item)) and item.startswith('spark'):
            # Construct the full path to the folder
            folder_path = os.path.join(path, item)

            # Delete the folder and its contents
            try:
                shutil.rmtree(folder_path)  # Use os.rmdir to remove an empty directory
                print(f"Deleted folder: {folder_path}")
            except OSError as e:
                print(f"Error deleting folder {folder_path}: {e}")



# Start a Spark session
spark = SparkSession.builder \
    .appName("MySQL to PySpark") \
    .getOrCreate()

# Define JDBC connection properties
jdbc_url = "jdbc:mysql://127.0.0.1:3306/test"
connection_properties = {
    "user": "root",
    "password": "",
    "driver": "com.mysql.jdbc.Driver"
}
row_count=0
# Load data from MySQL
while True:
    df = spark.read \
    .jdbc(url=jdbc_url, table="pysparktable", properties=connection_properties).limit(100)
    #df = df.limit(100)
    k = df.count()
    df1 = df.collect()[row_count:k]
    df = spark.createDataFrame(df1)
    # Create an empty DataFrame
    #empty_df = spark.createDataFrame([], schema=StructType([]))

    # Create a Window specification
    windowSpec = Window.partitionBy("Weather").orderBy("timestamp")

    # Calculate the "Acceleration" column based on the previous "Speed" value
    df = df.withColumn("Acceleration", (col("Speed") - lag("Speed").over(windowSpec)) / 2).fillna(0)

    # Calculate Jerk
    df = df.withColumn("Jerk", (col("Acceleration") - lag("Acceleration").over(windowSpec))).fillna(0)

    df = df.withColumn("Speed variation", (col("Speed") - lag("Speed").over(windowSpec))).fillna(0)

    df = df.withColumn("Steering variation", (col("Steering angle") - lag("Steering angle").over(windowSpec))).fillna(0)

    # Calculate Overspeed Value
    df = df.withColumn("Overspeed Value", lit(90) - col("Speed"))
    df = df.withColumn("Yaw rate",col("gyroZ"))

    new_df = df.select("Acceleration", "Jerk","Speed variation","Steering variation","Overspeed Value","Yaw rate")


    new_df = new_df.withColumn("Hard Braking", when((col("Yaw Rate") <= 5) & (col("Jerk") >= 1) & (col("Speed Variation") <= -10), 2)
                                        .when((col('Yaw rate')<=5) & ((col('Jerk')>=0.3) & (col('Jerk')<=1)) & ((col('Speed variation')<=-7) & (col('Speed variation')>-10)), 1)
                                        .otherwise(0))

    new_df = new_df.withColumn("Hard Acceleration", when((col("Yaw Rate") <= 5) & (col("Jerk") >= 1) & (col("Speed Variation") >= 10), 2)
                                            .when((col('Yaw rate')<=5) & ((col('Jerk')>=0.3) & (col('Jerk')<=1)) & ((col('Speed variation')>=7) & (col('Speed variation')<10)), 1)
                                            .otherwise(0))

    new_df = new_df.withColumn("Overspeeding", when(col("Overspeed Value") < 0, 2)
                                    .when(col("Overspeed Value").between(0, 5), 1)
                                    .otherwise(0))
    new_df = new_df.withColumn("Aggressive Steering", when((col("Yaw Rate") >= 10) & (col("Steering Variation") >= 10), 2)
                                        .when((col('Yaw rate')>=10) & ((col('Steering variation')>=7) & (col('Steering variation')<10)), 1)
                                        .otherwise(0))

    final_df=new_df.select("Hard Braking","Hard Acceleration","Overspeeding","Aggressive Steering")

    # Replace 'your_specific_path' with the path where you want to delete folders
    row_count=k
    df.show()
    new_df.show()
    final_df.show()


#new_df = new_df.withColumn("id", monotonically_increasing_id())
#df_additional = df_additional.withColumn("id", monotonically_increasing_id())

#dd=new_df.crossJoin(new_df.select("Jerk"))
#new_df = df.select("Steering angle")
#print(df["Speed"])
# Select the "Acceleration" column
#acc_values = df.select("Acceleration").rdd.flatMap(lambda x: x).collect()   

# Reference the "Acceleration" column using col
#column_to_take = "NewAcceleration"
#result_df = empty_df.withColumn("Acceleration", df["Acceleration"])

#Show the result
#new_df.show()
#print(acc_values)
# Stop the Spark session
    delete_spark_folders('C:/Users/2201-00066/AppData/Local/Temp')
    spark.stop()
