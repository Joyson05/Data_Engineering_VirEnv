from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
# import threading
from flask import request
import pandas as pd
import numpy as np
import json 


app = Flask(__name__)
CORS(app)
api_hit_count = 0

@app.route("/", methods=['GET'])
@cross_origin()
def main():
    global api_hit_count
    # print(api_hit_count)
    df=pd.read_excel("Car_Data_DS1.xlsx")
    df['Date']=pd.to_datetime(df['Date'], format='%a, %d %b %Y %H:%M:%S %Z')
    if api_hit_count<=len(df):
    # for i in range(1,len(df)):
        j=[]
        data={}
        j=df.iloc[api_hit_count].to_list()
        data["accelX"] = float(j[1])
        data["accelY"] = float(j[2])
        data["accelZ"] = float(j[3])
        data["gyroX"] = float(j[4])
        data["gyroY"] = float(j[5])
        data["gyroZ"] = float(j[6])
        data["Trip"] = int(j[7])
        data["timestamp"] = int(j[8])
        data["Steering angle"] = int(j[9])
        data["Speed"] = int(j[10])
        data["Weather"] = j[11]
        # print(len(df))
        api_hit_count += 1
        f_out=jsonify(data)
    print(api_hit_count)
    
    if api_hit_count==len(df):
        api_hit_count=0
    
    
    # print(j[1])
    
    return f_out



