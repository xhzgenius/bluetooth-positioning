import multiprocessing
from database import DataBase
from server import serve
from algorithm import analyze, visualize
from multiprocessing import Pool
from key import database_name

# import mysql.connector.pooling

def main(name = 'lab1'):
    DataBase(database_name).clear()
    pool = Pool(3)
    pool.apply_async(serve, (name,))
    pool.apply_async(analyze, (name,))
    pool.apply_async(visualize, (name, 'log',))
    pool.close()
    pool.join()
    # server = multiprocessing.Process(target=serve, args = [name])
    # analyzer = multiprocessing.Process(target=analyze, args = [name])
    # visualizer = multiprocessing.Process(target=visualize, args = [name, 'log'])
    
    # server = threading.Thread(target=serve, args = [name])
    # analyzer = threading.Thread(target=analyze, args = [name])
    # visualizer = threading.Thread(target=visualize, args = [name, 'log'])
    
    # server.start()
    # analyzer.start()
    # visualizer.start()

     
if __name__ == '__main__':
    main()