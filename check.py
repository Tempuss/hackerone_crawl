import urllib3.request
import os
from datetime import datetime


log_dir = './log/'
log_name = 'debug.log'
log_file = open(log_dir+log_name, 'w')

def getDate():
    return datetime.today().strftime('%Y-%m-%d-%H:%M:%S') 
    
def logging(text):
    global log_file
    time = getDate()
    log_file.write(time+" "+str(text)+"\n")

def writeJson(num, data):
    log = open("result/check/"+str(num)+".json", 'a')
    log.write(data)
    log.close()


http = urllib3.PoolManager()

start_url = "https://hackerone.com/reports/"
end_url = ".json"

limit = 1000000
for idx,val in enumerate(range(1,limit)):
    #time.sleep(3)
    fname = './result/check/'+str(val)+".json"
    url = start_url+str(val)+end_url
    logging("Progress : "+"("+str(val)+"/"+str(limit)+")")
    logging(url)
    if not os.path.exists(fname):
        try:
            #r = http.request('GET', url, timeout=3)
            r = http.request('GET', url)
        except Exception as e:
            logging(str(traceback.print_tb(e.__traceback__)))
        logging(r.status)
        if r.status == 200:
            #logging("Success")
            writeJson(str(val), r.data.decode('utf-8'))
        else:
            logging("Fail")



log_file.close()