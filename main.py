import multiprocessing
from database import global_db
from server import serve
from algorithm import analyze, visualize

def main():
    serve()
     
if __name__ == '__main__':
    main()