import os
import json
import traceback
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from datetime import datetime 

#ElasticSearch Setting
es = Elasticsearch("http://192.168.0.19:9200") 
index_name = "hackerone2"

#fix field name
int_list = ['report_id','reputation', 'rank', 'signal', 'signal_percent', 'impact', 'percent', 'bounty', 'severity_score']

#document file directory
file_directory = "C:/dev/python/hackerone/result/success/"
file_list = os.listdir(file_directory)


#Fix Specific Field Data
def fixData(json_data):
    for val in json_data:
        if val in int_list and json_data[val] is not '':

            #Remove Specific String 
            if val == 'rank' or val == 'percent' or val == 'signal_percent':
                if json_data[val] == '-':
                    json_data[val] = -1 
                else:
                    json_data[val] = json_data[val].replace("st", "")
                    json_data[val] = json_data[val].replace("nd", "")
                    json_data[val] = json_data[val].replace("rd", "")
                    json_data[val] = json_data[val].replace("th", "")

            #Remove Specific String From Score
            if val == 'severity_score':
                if json_data[val] == '(---)':
                    json_data[val] = -1
                else:
                    json_data[val] = json_data[val].replace("(", "")
                    json_data[val] = json_data[val].replace(")", "")
                
                if type(json_data[val]) is str and json_data[val].find(' ~ ') is not -1:
                    split = json_data[val].split(" ~ ")
                    first = float(split[0])
                    last = float(split[1])
                    avr = (first+last) / 2
                    json_data[val] = avr
        
            if json_data[val] == '-':
                json_data[val] = -1 
                    

            try:
                json_data[val] = int(json_data[val])
            except Exception as e:
                try:
                    json_data[val] = float(json_data[val])
                except Exception as e:
                    print(json_data['report_id'])
                    print(str(e)+"\n")
                    print(str(traceback.print_tb(e.__traceback__))+"\n")

    
    return json_data



#Inser Document To ElasticSearch
def indexData(document):
    try:
        es.index(index=index_name, doc_type='_doc', body=document)
    except Exception as e:
        print(document)
        print(str(e)+"\n")
        print(str(traceback.print_tb(e.__traceback__))+"\n")


#float and Int Check
def isNumeric(var):
    try:
        if int(var) == float(var):
            return True 
    except:
        try:
            float(var)
            return True
        except:
            return False 



#Fix Data & Index To ElasticSearch
for file_name in file_list:
    json_data=open(file_directory+file_name).read()
    json_data = json.loads(json_data)
    json_data = fixData(json_data)
    indexData(json_data)
    #print(json_data)

es.indices.refresh(index=index_name)