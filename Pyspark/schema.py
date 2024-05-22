from pyspark.sql.types import *

# Define the flattened schema
vechicle_summary_base_schema = StructType([
    StructField("createAt", StringType(), True),
    StructField("platform", StringType(), True),
    StructField("user", StringType(), True),
    StructField("vin", StringType(), False),
    StructField("loginAt", StringType(), True),
    StructField("logoutAt", StringType(), True),
    StructField("request_url", StringType(), True),
    StructField("request_page", StringType(), True),
    StructField("request_action", StringType(), True),
    StructField("request_dllCallMethod", StringType(), True),
    StructField("request_ecuName", StringType(), True),
    StructField("response_data_message", StringType(), True)
])


vechicle_summary_response_coordinates = StructType([
    StructField("vin", StringType(), False),
    StructField("response_url", StringType(), True),
    StructField("response_data_status", IntegerType(), True),
    StructField("response_data_data_id", IntegerType(), True),
    StructField("response_data_data_ecuName", StringType(), True),
    StructField("response_data_data_ecuStatus", StringType(), True),
    StructField("response_data_data_directionX", IntegerType(), True),
    StructField("response_data_data_directionY", IntegerType(), True),
    StructField("response_data_data_dtdDirectionX2D", IntegerType(), True),
    StructField("response_data_data_dtdDirectionY2D", IntegerType(), True),
    StructField("response_data_data_directionX3d", IntegerType(), True),
    StructField("response_data_data_directionY3d", IntegerType(), True),
    StructField("response_data_message", StringType(), True)
])

vechicle_summary_response_dtclist = StructType([
    StructField("vin", StringType(), False),
    StructField("ecuName", StringType(), True),
    StructField("diagnosticTroubleCode", StringType(), True),
    StructField("description", StringType(), True),
    StructField("dtcState", StringType(), True)
])



