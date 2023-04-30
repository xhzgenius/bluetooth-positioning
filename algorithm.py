import time
from typing import Dict, Tuple
from database import DataBase

def locate(positions: Tuple[float], values: Tuple[float]) -> Tuple[float]:
    '''
    ### 描述

    给定三个蓝牙接收装置的坐标和它们接收到的值（信号强度），计算出设备的坐标。
    
    ### Params:
    
    positions: 三个装置的坐标，包装成(x1, y1, x2, y2, x3, y3)的形式。
    
    values: 三个装置接收到的信号强度，包装成(value1, value2, value3)的形式。
    
    ### Returns:
     
    返回设备的坐标，包装成(x, y)的形式。
    '''
    # TODO: @xhz
    return (0, 0)

macs = {
    'mac1': (0, 0),
    'mac2': (0, 0),
    'mac3': (0, 0)
}

class Analyzer:
    _sleep_time = 1
    
    def __init__(self, name):
        self.db = DataBase(name) 
    
    def _find_location(self, data: Dict[str, int]):
        # TODO: trielocation: _mac_map X rssi -> location x,y
        return (0,0)
    
    def run(self):
        print (f'analyzer runnning...')
        while True:
            time.sleep(Analyzer._sleep_time)
            data = {}
            failed = False
            for mac in macs:
                results = self.db.get_signal(mac = mac)
                if not len(results):
                    failed = True 
                    break 
                mac, rssi, _ = results[0]
                rssi = int(rssi)
                data[mac] = rssi 
            if failed: continue 
            x,y = self._find_location(data)
            self.db.insert_location(x,y)

import os
import matplotlib.pyplot as plt

class Visualizer: 
    _sleep_time = 5
    
    def __init__(self, name, logdir = '.'):
        self.db = DataBase(name)
        self.logdir = logdir 
        self.cnt = 0
        os.system(f'mkdir -p {logdir}')
    
    def run(self):
        print (f'visualizer runnning...')
        while True:
            time.sleep(self._sleep_time)
            self.cnt += 1 
            # get all location
            locations = self.db.get_location(last = -1)
            if not len(locations): continue 
            xs = [int(x) for x, _, _ in locations]
            ys = [int(y) for y, _, _ in locations]
            fig, ax = plt.subplots()
            ax.scatter(xs, ys)
            
            for i,x,y in enumerate(zip(xs,ys)):
                ax.annotate(str(i), (x,y))
            logfile = f'log-{str(self.cnt)}.txt'
            fig.savefig(os.path.join(self.logdir, logfile))
            
def analyze(name):
    Analyzer(name).run()

def visualize(name, logdir):
    Visualizer(name, logdir).run()
    