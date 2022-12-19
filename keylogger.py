from pynput.keyboard import Key, Listener
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import time
from datetime import datetime

class main:

    def __init__(self):
        self.key_frequency = {'q': 0, 'w': 0, 'e': 0, 'r': 0,
                             'd' : 0, 'f': 0, 't': 0, 'g': 0,
                             '1': 0, '2': 0, '3': 0, '4': 0,
                             '5': 0, '6': 0, '7': 0, 'a': 0}
        
        self.csvList = {"f" : []}


        self.t1 = 0
        self.t2 = 0
        self.preKey = ""
        self.startFlag = False
        self.startTime()

    def startTime(self) :
        self.flag = 1
        self.t1 = self.getTime()
        self.t2 = 0
        
    def getTime(self) :
        today = datetime.today()
        t1 = datetime.strptime(today.strftime("%H:%M:%S.%f"), "%H:%M:%S.%f")
        timed = t1.time()
        return datetime.strptime(str(timed), "%H:%M:%S.%f")

    def clicked(self) :
        self.t2 = self.getTime()
        delta = self.t2 - self.t1
        self.t1 = self.getTime()
        self.t2 = 0
        return delta.total_seconds()

    def on_release(self, key):
        data = str(key)[1:-1].lower()
        repeat_sec= 0.00000
        if key == Key.enter :
            self.flag *= -1
        if self.flag == 1 and data in self.key_frequency.keys() :
            if self.startFlag == False :
                self.startFlag = True
            if self.preKey == data : 
                second = self.clicked()
                repeat_sec = second
                print(second)
                
            else : 
                ##
                self.preKey = data
                self.startTime()
                ##
            # self.key_frequency[data] += 1
            self.csvList['f'].append({
                'idx' : len(self.csvList['f'])+1,
                'key' : data,
                'repeat_sec' : round(repeat_sec, 4)
            })
        print(f'{key} release')
        if key == Key.f4 :
            return False
            
    
    
    def convert_df(self):
        return pd.DataFrame(self.csvList['f'])
    
    def save_df(self):
        if not os.path.exists('key_freq.csv'):
            self.convert_df().to_csv('key_freq.csv', 
                                     mode='w', index=False)
        else :
            self.convert_df().to_csv('key_freq.csv', 
                                     mode='a', index=False)
    
    def run(self):
        print('Recording start ..\n')
        with Listener(on_release = self.on_release) as listener:
            listener.join()
        self.save_df()
        
if __name__ == '__main__':
    main().run()
    