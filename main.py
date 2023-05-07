import multiprocessing
from database import DataBase
from server import serve
from algorithm import analyze, visualize
from multiprocessing import Pool
from key import database_name

# import mysql.connector.pooling

def main():
    serve()
     
if __name__ == '__main__':
    main()