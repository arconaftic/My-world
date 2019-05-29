import csv
import json
import logging
import requests
import datetime
import threading
from os import path
import time

from  logging.handlers import TimedRotatingFileHandler
from os import environ

class PhoneChecker:
    
#    def log_setup(filename):
 #       formatter = print.Formatter('[%(asctime)s] [%(levelname)s] %(filename)s [LINE: %(lineno)d]: %(message)s')
  #      formatter.converter = time.gmtime
   #     log_handler = TimedRotatingFileHandler(filename='logs/{filename}'.format(filename=filename),when='d',interval=1,backupCount=10)
    #    log_handler.setFormatter(formatter)

   # print = logging.getLogger()
   # print.addHandler(log_handler)
    #print.setLevel(print.getLevelName(environ.get('LOG_LEVEL')))
    
    def __init__(self):
        self.token = '627db79feac72'
        self.url = 'https://ekapusta.com/partner/checkPhones/'
        self.chunksize = 9000
        self.incorrect = csv.writer(open('result/incorrect'+ str(datetime.date.today()) +'.csv', 'w'), delimiter=';')
        self.exists = csv.writer(open('result/exists'+ str(datetime.date.today()) +'.csv', 'w'),delimiter=';')
        self.unexists = csv.writer(open('result/unexists'+ str(datetime.date.today()) +'.csv', 'w'), delimiter=';')
        self.failed = csv.writer(open('result/failed'+ str(datetime.date.today()) +'.csv', 'w'), delimiter=';')

    def gen_chunks(self, reader):
        chunk = []
        for i, line in enumerate(reader):
            if (i % self.chunksize == 0 and i > 0):
                yield chunk
                del chunk[:]
            chunk.append(line)
        yield chunk

    def check_phones(self, phones):
        params = {
            'token': self.token,
            'phones': ', '.join(phones)
        }

        try:
            request = requests.post(url=self.url, data=params)
            response = request.json()
            print(response)
            data = response['phones']
            
            for d in data:
                if d['result'] == 'exists':
                    self.exists.writerow(['7' + d['phone']])

                if d['result'] == 'unexists':
                    self.unexists.writerow(['7' + d['phone']])

                if d['result'] == 'incorrect':
                    self.incorrect.writerow(['7' + d['phone']])
        except Exception as e:
            #logging.info('Failed to parse chunk: {error}'.format(error=e))
            for phone in phones:
                self.failed.writerow([phone])


if __name__ == '__main__':
    file_path = "C:\\Users\\USER\Desktop\\python_files\\12.csv"
    #log_setup(filename=path.basename(__file__).split('.')[0] + '.log')
    checker = PhoneChecker()
    thread_list = []
    print('Start checker')

    with open(file_path, encoding='windows-1251', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        values = []
        for row in reader:
            try:
                values.append(row[0])
                
            except:
                pass
        #print(values)
        
    for chunk in checker.gen_chunks(values):
        if len(thread_list) == 10:
            for running_thread in thread_list:
                running_thread.join()
            thread_list = []

        thread = threading.Thread(target=checker.check_phones, args=(chunk,))
        logging.info('Send data to server..')

        thread.daemon = True
        thread.start()
        thread_list.append(thread)

    for running_thread in thread_list:
        running_thread.join()
