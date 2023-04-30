# Bluetooth-positioning
北京大学计算机网络2023年春季学期课程Lab1：通过蓝牙嗅探装置进行设备定位。

## Build env
```
pip3 install msgpack msgpack_numpy mysql-connector-python 
```

## DataBase 
1. installation 
    - login to mysql 
    ```bash 
    sudo mysql -u root 
    ```
    - add an account;
    ```mysql
    mysql> CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
    mysql> GRANT ALL PRIVILEGES ON *.* TO 'user'@'localhost'
    ```
    - add a key.py with following attributes:
```python
user = 'xxx'
host = 'xxx'
password = 'xxx'
``` 

2. API
```
1: signals (mac VARCHAR(255), rssi VARCHAR(255), date VARCHAR(255))
2: locations (x VARCHAR(255), y VARCHAR(255), date VARCHAR(255))
```

## Run 
```
python ./main.py 
```