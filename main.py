import multiprocessing
from database import global_db
from server import serve
from algorithm import analyze, visualize

def main(name = 'lab1'):
    global_db.clear()
    server = multiprocessing.Process(target=serve, args = [name])
    analyzer = multiprocessing.Process(target=analyze, args = [name])
    visualizer = multiprocessing.Process(target=visualize, args = [name, 'log'])
    
    server.start()
    analyzer.start()
    visualizer.start()
     
if __name__ == '__main__':
    main()