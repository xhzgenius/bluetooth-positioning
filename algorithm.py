import time
from typing import Dict, Tuple
from database import global_db
# from key import database_name

# TODO: replace mac names with MAC address and hardcode the location
MACS = {
    'E0E2E69C1E6C': (0, 212.8),
    'E0E2E69C1FD0': (0, 0),
    'E0E2E570175C': (266.0, 1)
}

class Analyzer:
    _sleep_time = 1
    # standard rssi for 1 meter
    # https://iotandelectronics.wordpress.com/2016/10/07/how-to-calculate-distance-from-the-rssi-value-of-the-ble-beacon/
    _measured_power = -69 
    _N = 2
    
    def __init__(self):
        self.db = global_db
    
    def _find_location(self, data: Dict[str, float]):
        xs = []
        ys = []
        rs = []
        for mac in MACS:
            xs.append(MACS[mac][0])
            ys.append(MACS[mac][1])
            rs.append(data[mac])
        A = 2*xs[1] - 2*xs[0]
        B = 2*ys[1] - 2*ys[0]
        C = rs[0]**2 - rs[1]**2 - xs[0]**2 + xs[1]**2 - ys[0]**2 + ys[1]**2
        D = 2*xs[2] - 2*xs[1]
        E = 2*ys[2] - 2*ys[1]
        F = rs[1]**2 - rs[2]**2 - xs[1]**2 + xs[2]**2 - ys[1]**2 + ys[2]**2
        x = (C*E - F*B) / (E*A - B*D)
        y = (C*D - A*F) / (B*D - A*E)
        return x, y
    
    def _calculate_distance(self, rssi):
        return 10 ** ((-Analyzer._messured_power - rssi) / 10  * Analyzer._N)
    
    def single_run(self):
        data = {}
        failed = False
        for mac in MACS:
            results = self.db.get_signal(mac = mac)
            print("Signals from %s:"%(mac))
            for x in results: print(x)
            if len(results)==0:
                failed = True 
                break 
            mac, rssi, _ = results[0]
            rssi = int(rssi)
            data[mac] = self._calculate_distance(rssi) 
        if failed:
            print("Calculate distance failed. ")
            return
        x, y = self._find_location(data)
        self.db.insert_location(x, y)
        print("Calculate distance succeeded. Inserted location: (%f, %f). "%(x, y))

    def run(self):
        print (f'analyzer runnning...')
        while True:
            self.single_run()
            time.sleep(self._sleep_time)

import os
import matplotlib.pyplot as plt

class Visualizer: 
    _sleep_time = 5
    
    def __init__(self, logdir = '.'):
        self.db = global_db
        self.logdir = logdir 
        self.cnt = 0
        os.system(f'mkdir -p {logdir}')

    def single_run(self):
        print ('visualizer now runnning...')
        self.cnt += 1 
        # debug
        res = self.db.get_all_locations()
        for y in res: print ("location:", y)
        # get all location
        locations = self.db.get_location(last = -1)
        if not len(locations): return
        xs = [int(x) for x, _, _ in locations]
        ys = [int(y) for y, _, _ in locations]
        fig, ax = plt.subplots()
        ax.scatter([x[0] for x in MACS.values()], [x[1] for x in MACS.values()], c = 'red')
        for mac in MACS:
            ax.annotate(mac, MACS[mac])
            
        ax.scatter(xs, ys, c = 'black')
        
        for i,x,y in enumerate(zip(xs,ys)):
            ax.annotate(str(i), (x,y))
        logfile = f'log-{str(self.cnt)}.txt'
        fig.savefig(os.path.join(self.logdir, logfile))
    
    def run(self):
        print (f'visualizer runnning...')
        while True:
            self.single_run()
            time.sleep(self._sleep_time)
            
            
def analyze(name):
    Analyzer(name).run()

def visualize(name, logdir):
    Visualizer(name, logdir).run()
    

global_analyzer = Analyzer()
global_visualizer = Visualizer()