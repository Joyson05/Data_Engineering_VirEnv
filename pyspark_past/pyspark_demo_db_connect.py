from pyspark.sql import SparkSession
from pyspark.sql.functions import lit
from pyspark.sql.window import Window
from pyspark.sql.functions import sum
from pyspark.sql.functions import when, col


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


# Load data from MySQL
#data = spark.read \
 #   .jdbc(url=jdbc_url, table="pysparktable", properties=connection_properties)

# Display the first few rows
#data.show(5)

# Stop the Spark session
#spark.stop()




df = spark.read \
    .jdbc(url=jdbc_url, table="pysparktable", properties=connection_properties)
df.show(5)
# Limit the DataFrame to the first 2000 rows
df = df.limit(2000)

# Calculate Acceleration
df = df.withColumn("Acceleration", (df["Speed"] - df["Speed"].lag()) / 2).fillna(0)

# Calculate Jerk
df = df.withColumn("Jerk", df["Acceleration"] - df["Acceleration"].lag()).fillna(0)

# Calculate Speed Variation
df = df.withColumn("Speed Variation", df["Speed"] - df["Speed"].lag()).fillna(0)

# Calculate Steering Variation
df = df.withColumn("Steering Variation", df["Steering Angle"] - df["Steering Angle"].lag()).fillna(0)

# Calculate Overspeed Value
df = df.withColumn("Overspeed Value", lit(90) - df["Overspeed Value"])

# Calculate Hard Braking
hard_braking = (df["Yaw Rate"] <= 5) & (df["Jerk"] >= 0.3) & (df["Jerk"] <= 1) & (df["Speed Variation"] <= -7) & (df["Speed Variation"] > -10)
df = df.withColumn("Hard Braking", hard_braking.cast("int"))

# Calculate Hard Acceleration
hard_acceleration = (df["Yaw Rate"] <= 5) & (df["Jerk"] >= 0.3) & (df["Jerk"] <= 1) & (df["Speed Variation"] >= 7) & (df["Speed Variation"] < 10)
df = df.withColumn("Hard Acceleration", hard_acceleration.cast("int"))

# Calculate Overspeeding
overspeeding = df["Overspeed Value"].between(0, 5).cast("int")
df = df.withColumn("Overspeeding", overspeeding)

# Calculate Aggressive Steering
aggressive_steering = (df["Yaw Rate"] >= 10) & (df["Steering Variation"] >= 7) & (df["Steering Variation"] < 10)
df = df.withColumn("Aggressive Steering", aggressive_steering.cast("int"))

# Create a sliding window to calculate score_dec_count


windowSpec = Window.orderBy()

df = df.withColumn("score_dec_count", sum(df["Hard Acceleration"]).over(windowSpec) +
                                      sum(df["Hard Braking"]).over(windowSpec) +
                                      sum(df["Overspeeding"]).over(windowSpec) +
                                      sum(df["Aggressive Steering"]).over(windowSpec))

# Calculate Score


df = df.withColumn("Hard Braking", when((df["Yaw Rate"] <= 5) & (df["Jerk"] >= 1) & (df["Speed Variation"] <= -10), 2)
                                    .when((new_df['Yaw rate']<=5) & ((new_df['Jerk']>=0.3) & (new_df['Jerk']<=1)) & ((new_df['Speed variation']<=-7) & (new_df['Speed variation']>-10)), 1)
                                    .otherwise(0))
df = df.withColumn("Hard Acceleration", when((df["Yaw Rate"] <= 5) & (df["Jerk"] >= 1) & (df["Speed Variation"] >= 10), 2)
                                        .when((df["Yaw Rate"] <= 5) & (df["Jerk"] >= 0.3) & (df["Speed Variation"] >= 7), 1)
                                        .otherwise(0))
df = df.withColumn("Overspeeding", when(col("Overspeeding") < 0, 2)
                                   .when(col("Overspeeding").between(0, 5), 1)
                                   .otherwise(0))
df = df.withColumn("Aggressive Steering", when((df["Yaw Rate"] >= 10) & (df["Steering Variation"] >= 10), 2)
                                       .when((df["Yaw Rate"] >= 10) & (df["Steering Variation"] >= 7), 1)
                                       .otherwise(0))

# Create an empty DataFrame to store the final result
final_df = spark.createDataFrame([], df.schema)

# Loop to calculate the sum for every 60 rows
for i in range(60, df.count(), 60):
    prev_sum = df.filter((col("timestamp") >= i - 59) & (col("timestamp") <= i)).select("score_dec_count").distinct().count()
    if prev_sum > 0:
        final_df = final_df.union(df.filter((col("timestamp") >= i - 59) & (col("timestamp") <= i)).limit(1))

# Assuming you have a "Score.xlsx" file available, you can read it into a DataFrame
score_df = spark.read.csv("Score.xlsx", header=True, inferSchema=True)

# Initialize variables
event_count = {"Hard Acceleration": df.filter(col("Hard Acceleration") > 0).count(),
               "Hard Braking": df.filter(col("Hard Braking") > 0).count(),
               "Aggressive Steering": df.filter(col("Aggressive Steering") > 0).count(),
               "Overspeeding": df.filter(col("Overspeeding") > 0).count()}

scores = score_df.select("Score").rdd.flatMap(lambda x: x).collect()
scores = [float(score) for score in scores]

timestamp = df.select("timestamp").rdd.flatMap(lambda x: x).collect()
acceleration = df.select("Acceleration").rdd.flatMap(lambda x: x).collect()
jerk = df.select("Jerk").rdd.flatMap(lambda x: x).collect()
speed_variation = df.select("Speed Variation").rdd.flatMap(lambda x: x).collect()
steering_variation = df.select("Steering Variation").rdd.flatMap(lambda x: x).collect()
overspeed_value = df.select("Overspeed Value").rdd.flatMap(lambda x: x).collect()
yaw_rate = df.select("Yaw Rate").rdd.flatMap(lambda x: x).collect()

input_data = {"timestamp": timestamp,
              "Acceleration": acceleration,
              "Jerk": jerk,
              "Speed_variation": speed_variation,
              "Steering_variation": steering_variation,
              "Overspeed_value": overspeed_value,
              "Yaw_rate": yaw_rate}

final_out = {"Event_count": event_count, "Score": scores, "input_data": input_data}

# Show the final result
final_df.show()

# Stop the Spark session
spark.stop()

# Print the final result
print(final_out)
